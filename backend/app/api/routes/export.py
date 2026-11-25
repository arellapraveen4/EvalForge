import csv
from io import StringIO
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.annotation import Annotation, AnnotationScore, AnnotationError

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/annotations/csv")
def export_csv(db: Session = Depends(get_db)):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["annotation_id", "task_id", "annotator_id", "preference", "rationale", "confidence", "revision"])
    for annotation in db.query(Annotation).all():
        writer.writerow([annotation.id, annotation.task_id, annotation.annotator_id, annotation.preference,
                         annotation.rationale, annotation.confidence, annotation.revision])
    output.seek(0)
    return StreamingResponse(iter([output.read()]), media_type="text/csv",
                             headers={"Content-Disposition": "attachment; filename=annotations.csv"})


@router.get("/annotations/json")
def export_json(db: Session = Depends(get_db)):
    output = []
    for annotation in db.query(Annotation).all():
        scores = db.query(AnnotationScore).filter(AnnotationScore.annotation_id == annotation.id).all()
        errors = db.query(AnnotationError).filter(AnnotationError.annotation_id == annotation.id).all()
        output.append({
            "id": annotation.id, "task_id": annotation.task_id, "annotator_id": annotation.annotator_id,
            "preference": annotation.preference, "rationale": annotation.rationale,
            "confidence": annotation.confidence, "revision": annotation.revision,
            "scores": [{"dimension": s.dimension, "score": s.score} for s in scores],
            "errors": [{"category": e.category, "severity": e.severity} for e in errors],
        })
    return output


@router.get("/benchmark/json")
def export_benchmark(db: Session = Depends(get_db)):
    return {"annotations": export_json(db), "format": "EvalForge benchmark export"}
