import json
from abc import ABC, abstractmethod

from pydantic import ValidationError

from app.evaluation.rubrics import RUBRICS
from app.evaluation.scoring import calculate_weighted_score
from app.schemas.evaluation import EvaluationResult


class BaseJudge(ABC):
    @abstractmethod
    async def evaluate(self, prompt: str, response: str, reference=None):
        pass


class MockJudge(BaseJudge):
    async def evaluate(self, prompt: str, response: str, reference=None):
        dimensions = {}
        for name in RUBRICS["general"]:
            dimensions[name] = {"score": 4, "explanation": "Illustrative deterministic mock score."}
        dimensions["error_tags"] = []
        dimensions["rationale"] = "Mock evaluation only; configure an external provider for real judgments."
        dimensions["confidence"] = 0.5
        dimensions["overall_score"] = calculate_weighted_score(dimensions, RUBRICS["general"])
        dimensions["verdict"] = "good"
        return dimensions


class OpenAICompatibleJudge(BaseJudge):
    def __init__(self, base_url: str, api_key: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model

    async def evaluate(self, prompt: str, response: str, reference=None):
        import httpx

        rubric_text = json.dumps(RUBRICS["general"])
        system = "You are an independent AI response evaluator. Return only valid JSON."
        user = f"""Evaluate the response using this rubric:
{rubric_text}

Prompt:
{prompt}

Reference:
{reference or "Not provided"}

Response:
{response}

Return JSON with correctness, instruction_following, relevance, completeness, clarity,
each containing score (1-5) and explanation, plus error_tags, rationale, confidence (0-1),
overall_score (0-5), and verdict."""
        async with httpx.AsyncClient(timeout=60) as client:
            result = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={"model": self.model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}], "temperature": 0},
            )
            result.raise_for_status()
            content = result.json()["choices"][0]["message"]["content"]
            return json.loads(content)


class GeminiJudge(BaseJudge):
    def __init__(self, api_key: str, model: str):
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required when LLM_PROVIDER=gemini")
        self.api_key = api_key
        self.model = model

    async def evaluate(self, prompt: str, response: str, reference=None):
        import httpx

        rubric_text = json.dumps(RUBRICS["general"])
        system = (
            "You are an independent AI response evaluator. Evaluate only the supplied "
            "information. Do not invent evidence. Return a JSON object matching the requested fields."
        )
        user = f"""Evaluate the response using this rubric:
{rubric_text}

Prompt:
{prompt}

Reference:
{reference or "Not provided"}

Response:
{response}

Return JSON with correctness, instruction_following, relevance, completeness, and clarity,
each containing an integer score from 1 to 5 and an explanation. Also include error_tags
(array of strings), rationale (string), confidence (number from 0 to 1), overall_score
(number from 0 to 5), and verdict (string)."""
        endpoint = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent"
        )
        async with httpx.AsyncClient(timeout=60) as client:
            result = await client.post(
                endpoint,
                headers={"x-goog-api-key": self.api_key},
                json={
                    "systemInstruction": {"parts": [{"text": system}]},
                    "contents": [{"role": "user", "parts": [{"text": user}]}],
                    "generationConfig": {
                        "temperature": 0,
                        "responseMimeType": "application/json",
                    },
                },
            )
            result.raise_for_status()
            payload = result.json()

        try:
            content = payload["candidates"][0]["content"]["parts"][0]["text"]
            parsed = json.loads(content)
            validated = EvaluationResult.parse_obj(parsed)
        except (KeyError, IndexError, TypeError, json.JSONDecodeError, ValidationError) as exc:
            raise ValueError("Gemini returned an invalid evaluation JSON response") from exc

        result_data = validated.dict()
        result_data["overall_score"] = calculate_weighted_score(
            result_data, RUBRICS["general"]
        )
        return result_data
