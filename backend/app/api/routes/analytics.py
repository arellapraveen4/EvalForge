from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.annotation import Annotation
from app.models.evaluation_task import EvaluationTask
from app.models.review import Review
from app.models.dataset import Dataset
from app.analytics.agreement import percentage_agreement
from app.analytics.bias import position_bias
from app.analytics.reliability import bootstrap_metric

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    tasks = db.query(EvaluationTask).all()
    annotations = db.query(Annotation).all()
    return {
        "datasets": db.query(Dataset).count(),
        "tasks": len(tasks),
        "completed_tasks": sum(t.status in ("submitted", "approved") for t in tasks),
        "pending_tasks": sum(t.status in ("pending", "assigned") for t in tasks),
        "annotations": len(annotations),
        "reviewed_tasks": db.query(Review).count(),
    }


@router.get("/agreement")
def agreement(db: Session = Depends(get_db)):
    grouped = {}
    for annotation in db.query(Annotation).all():
        grouped.setdefault(annotation.task_id, []).append(annotation.preference)
    values = [percentage_agreement(labels) for labels in grouped.values() if labels]
    bootstrap = bootstrap_metric(values, lambda sample: sum(sample) / len(sample) if sample else None)
    return {"task_agreement": bootstrap, "task_count": len(values)}


@router.get("/judge-reliability")
def judge_reliability():
    return {"accuracy": None, "kappa": None, "confusion_matrix": None, "message": "Requires human and judge labels"}


@router.get("/error-distribution")
def error_distribution(db: Session = Depends(get_db)):
    from app.models.annotation import AnnotationError
    counts = {}
    for error in db.query(AnnotationError).all():
        counts[error.category] = counts.get(error.category, 0) + 1
    return {"categories": counts}


@router.get("/benchmark")
def benchmark(db: Session = Depends(get_db)):
    annotations = db.query(Annotation).all()
    preferences = {"A": 0, "B": 0, "Tie": 0, "BothPoor": 0}
    for annotation in annotations:
        if annotation.preference in preferences:
            preferences[annotation.preference] += 1
    return {"preference_distribution": preferences}


@router.post("/position-bias")
def position_bias_endpoint(original: list[str], reversed: list[str]):
    return position_bias(original, reversed)
