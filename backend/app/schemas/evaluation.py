from pydantic import BaseModel, Field
from typing import Optional


class DimensionScore(BaseModel):
    score: int = Field(ge=1, le=5)
    explanation: str


class EvaluationResult(BaseModel):
    correctness: DimensionScore
    instruction_following: DimensionScore
    relevance: DimensionScore
    completeness: DimensionScore
    clarity: DimensionScore
    overall_score: float
    verdict: str
    error_tags: list[str] = []
    rationale: str
    confidence: Optional[float] = Field(default=None, ge=0, le=1)
