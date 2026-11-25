from fastapi import APIRouter
from pydantic import BaseModel
from app.core.config import settings
from app.evaluation.judge import GeminiJudge, MockJudge, OpenAICompatibleJudge
from app.evaluation.rubrics import RUBRICS
from app.evaluation.scoring import calculate_weighted_score
from app.evaluation.deterministic import exact_match, word_overlap
from app.evaluation.hallucination import analyze_context_groundedness
from app.evaluation.safety import assess_safety

router = APIRouter(prefix="/evaluation", tags=["evaluation"])


class SingleRequest(BaseModel):
    prompt: str
    response: str
    reference: str | None = None
    context: str | None = None


class PairRequest(BaseModel):
    prompt: str
    response_a: str
    response_b: str
    reference: str | None = None


def judge():
    provider = settings.llm_provider.lower()
    if provider == "gemini":
        if not settings.gemini_api_key:
            from fastapi import HTTPException
            raise HTTPException(status_code=503, detail="GEMINI_API_KEY is required to use the Gemini judge")
        return GeminiJudge(settings.gemini_api_key, settings.gemini_model)
    if provider == "openai":
        if not settings.openai_api_key:
            from fastapi import HTTPException
            raise HTTPException(status_code=503, detail="OPENAI_API_KEY is required to use the OpenAI-compatible judge")
        return OpenAICompatibleJudge(settings.openai_base_url, settings.openai_api_key, settings.openai_model)
    if provider == "mock":
        return MockJudge()
    from fastapi import HTTPException
    raise HTTPException(status_code=500, detail=f"Unsupported LLM_PROVIDER: {settings.llm_provider}")


@router.post("/single")
async def evaluate_single(payload: SingleRequest):
    result = await judge().evaluate(payload.prompt, payload.response, payload.reference)
    result["deterministic"] = {
        "exact_match": exact_match(payload.response, payload.reference),
        "word_overlap": word_overlap(payload.response, payload.reference),
    }
    result["safety"] = assess_safety(payload.response)
    if payload.context:
        result["groundedness"] = analyze_context_groundedness(payload.response, payload.context)
    return result


@router.post("/pairwise")
async def evaluate_pairwise(payload: PairRequest):
    score_a = await judge().evaluate(payload.prompt, payload.response_a, payload.reference)
    score_b = await judge().evaluate(payload.prompt, payload.response_b, payload.reference)
    overall_a = score_a.get("overall_score") or calculate_weighted_score(score_a, RUBRICS["general"])
    overall_b = score_b.get("overall_score") or calculate_weighted_score(score_b, RUBRICS["general"])
    preference = "A" if overall_a > overall_b else "B" if overall_b > overall_a else "Tie"
    return {"preference": preference, "response_a": score_a, "response_b": score_b}


@router.post("/batch")
async def evaluate_batch(items: list[SingleRequest]):
    return [await evaluate_single(item) for item in items]
