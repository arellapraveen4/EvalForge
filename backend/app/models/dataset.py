from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.database import Base


class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    format = Column(String, nullable=False)
    source = Column(String)
    license = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    items = relationship("DatasetItem", back_populates="dataset", cascade="all, delete-orphan")


class DatasetItem(Base):
    __tablename__ = "dataset_items"
    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    external_id = Column(String)
    category = Column(String)
    task_type = Column(String)
    difficulty = Column(String)
    prompt = Column(Text, nullable=False)
    context = Column(Text)
    response_a = Column(Text)
    response_b = Column(Text)
    reference_answer = Column(Text)
    expected_constraints = Column(JSON)
    source = Column(String)
    license = Column(String)
    extra = Column(JSON)
    dataset = relationship("Dataset", back_populates="items")
