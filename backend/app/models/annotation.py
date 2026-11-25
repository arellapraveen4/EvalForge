from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String, Text, ForeignKey, JSON
from app.database.database import Base


class Annotation(Base):
    __tablename__ = "annotations"
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("evaluation_tasks.id"), nullable=False)
    annotator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    preference = Column(String)
    rationale = Column(Text)
    confidence = Column(Float)
    time_taken_seconds = Column(Integer)
    status = Column(String, default="submitted")
    revision = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    revision_history = Column(JSON, default=list)


class AnnotationScore(Base):
    __tablename__ = "annotation_scores"
    id = Column(Integer, primary_key=True)
    annotation_id = Column(Integer, ForeignKey("annotations.id"), nullable=False)
    dimension = Column(String, nullable=False)
    response_side = Column(String)
    score = Column(Integer, nullable=False)
    explanation = Column(Text)


class AnnotationError(Base):
    __tablename__ = "annotation_errors"
    id = Column(Integer, primary_key=True)
    annotation_id = Column(Integer, ForeignKey("annotations.id"), nullable=False)
    category = Column(String, nullable=False)
    severity = Column(String)
    evidence_span = Column(Text)
    explanation = Column(Text)
