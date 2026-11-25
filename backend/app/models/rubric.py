from sqlalchemy import Column, Float, Integer, String, Text, ForeignKey
from app.database.database import Base


class Rubric(Base):
    __tablename__ = "rubrics"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)


class RubricDimension(Base):
    __tablename__ = "rubric_dimensions"
    id = Column(Integer, primary_key=True)
    rubric_id = Column(Integer, ForeignKey("rubrics.id"), nullable=False)
    name = Column(String, nullable=False)
    weight = Column(Float, nullable=False)
    description = Column(Text)
