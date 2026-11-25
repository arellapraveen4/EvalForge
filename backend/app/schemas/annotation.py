from pydantic import BaseModel, Field
from typing import Optional


class ScoreInput(BaseModel):
    dimension: str
    response_side: Optional[str] = None
    score: int = Field(ge=1, le=5)
    explanation: Optional[str] = None


class ErrorInput(BaseModel):
    category: str
    severity: Optional[str] = None
    evidence_span: Optional[str] = None
    explanation: Optional[str] = None


class AnnotationInput(BaseModel):
    task_id: int
    preference: str
    scores: list[ScoreInput] = []
    errors: list[ErrorInput] = []
    rationale: str
    confidence: float = Field(ge=0, le=1)
    time_taken_seconds: Optional[int] = None
