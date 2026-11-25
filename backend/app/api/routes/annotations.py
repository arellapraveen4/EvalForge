from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.annotation import Annotation, AnnotationScore, AnnotationError
from app.models.evaluation_task import EvaluationTask
from app.schemas.annotation import AnnotationInput
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/annotations", tags=["annotations"])


@router.post("/submit")
def submit(payload: AnnotationInput, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    task = db.get(EvaluationTask, payload.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    annotation = Annotation(task_id=payload.task_id, annotator_id=user.id, preference=payload.preference,
                            rationale=payload.rationale, confidence=payload.confidence,
                            time_taken_seconds=payload.time_taken_seconds)
    db.add(annotation)
    db.flush()
    for score in payload.scores:
        db.add(AnnotationScore(annotation_id=annotation.id, dimension=score.dimension,
                               response_side=score.response_side, score=score.score, explanation=score.explanation))
    for error in payload.errors:
        db.add(AnnotationError(annotation_id=annotation.id, category=error.category, severity=error.severity,
                               evidence_span=error.evidence_span, explanation=error.explanation))
    task.status = "submitted"
    db.commit()
    db.refresh(annotation)
    return {"id": annotation.id, "status": annotation.status}


@router.get("/{annotation_id}")
def get_annotation(annotation_id: int, db: Session = Depends(get_db)):
    annotation = db.get(Annotation, annotation_id)
    if not annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")
    scores = db.query(AnnotationScore).filter(AnnotationScore.annotation_id == annotation_id).all()
    errors = db.query(AnnotationError).filter(AnnotationError.annotation_id == annotation_id).all()
    return {"id": annotation.id, "task_id": annotation.task_id, "preference": annotation.preference,
            "rationale": annotation.rationale, "confidence": annotation.confidence,
            "scores": [{"dimension": s.dimension, "response_side": s.response_side, "score": s.score} for s in scores],
            "errors": [{"category": e.category, "severity": e.severity} for e in errors],
            "status": annotation.status, "revision": annotation.revision}


@router.get("/task/{task_id}")
def task_annotations(task_id: int, db: Session = Depends(get_db)):
    annotations = db.query(Annotation).filter(Annotation.task_id == task_id).all()
    return [{"id": a.id, "annotator_id": a.annotator_id, "preference": a.preference,
             "rationale": a.rationale, "status": a.status} for a in annotations]


@router.put("/{annotation_id}")
def update_annotation(annotation_id: int, payload: AnnotationInput, db: Session = Depends(get_db),
                      user: User = Depends(get_current_user)):
    annotation = db.get(Annotation, annotation_id)
    if not annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")
    if annotation.annotator_id != user.id:
        raise HTTPException(status_code=403, detail="Not your annotation")
    history = list(annotation.revision_history or [])
    history.append({"revision": annotation.revision, "preference": annotation.preference,
                    "rationale": annotation.rationale})
    annotation.revision_history = history
    annotation.preference = payload.preference
    annotation.rationale = payload.rationale
    annotation.confidence = payload.confidence
    annotation.revision += 1
    db.query(AnnotationScore).filter(AnnotationScore.annotation_id == annotation_id).delete()
    db.query(AnnotationError).filter(AnnotationError.annotation_id == annotation_id).delete()
    for score in payload.scores:
        db.add(AnnotationScore(annotation_id=annotation_id, dimension=score.dimension,
                               response_side=score.response_side, score=score.score, explanation=score.explanation))
    for error in payload.errors:
        db.add(AnnotationError(annotation_id=annotation_id, category=error.category, severity=error.severity,
                               evidence_span=error.evidence_span, explanation=error.explanation))
    db.commit()
    return {"id": annotation_id, "revision": annotation.revision}
