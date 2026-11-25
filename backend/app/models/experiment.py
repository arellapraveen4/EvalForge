from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String, Text, ForeignKey, JSON
from app.database.database import Base


class Experiment(Base):
    __tablename__ = "experiments"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    experiment_type = Column(String)
    config = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class ExperimentResult(Base):
    __tablename__ = "experiment_results"
    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("evaluation_tasks.id"))
    metric = Column(String, nullable=False)
    value = Column(Float)
    details = Column(JSON)


class JudgeResult(Base):
    __tablename__ = "judge_results"
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("evaluation_tasks.id"))
    model_name = Column(String)
    model_version = Column(String)
    prompt_version = Column(String)
    raw_output = Column(Text)
    parsed_output = Column(JSON)
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
