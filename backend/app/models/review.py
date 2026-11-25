from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey
from app.database.database import Base


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    annotation_id = Column(Integer, ForeignKey("annotations.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    decision = Column(String, nullable=False)
    comments = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class Adjudication(Base):
    __tablename__ = "adjudications"
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("evaluation_tasks.id"), nullable=False)
    adjudicator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    final_preference = Column(String)
    final_rationale = Column(Text)
    resolved_errors = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
