from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey, JSON
from app.database.database import Base


class EvaluationTask(Base):
    __tablename__ = "evaluation_tasks"
    id = Column(Integer, primary_key=True)
    dataset_item_id = Column(Integer, ForeignKey("dataset_items.id"), nullable=False)
    task_type = Column(String, nullable=False, default="pairwise")
    rubric_id = Column(Integer, ForeignKey("rubrics.id"))
    assignee_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, nullable=False, default="pending")
    blind_mode = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ModelRun(Base):
    __tablename__ = "model_runs"
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("evaluation_tasks.id"))
    model_name = Column(String, nullable=False)
    model_version = Column(String)
    prompt_version = Column(String)
    raw_output = Column(Text)
    parsed_output = Column(JSON)
    latency_ms = Column(Integer)
    cost = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
