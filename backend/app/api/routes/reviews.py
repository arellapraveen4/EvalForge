from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.annotation import Annotation
from app.models.review import Review, Adjudication
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/reviews", tags=["reviews"])


class ReviewInput(BaseModel):
    annotation_id: int
    decision: str
    comments: str = ""


class AdjudicationInput(BaseModel):
    task_id: int
    final_preference: str
    final_rationale: str
    resolved_errors: str = ""


@router.get("/pending")
def pending(db: Session = Depends(get_db)):
    annotations = db.query(Annotation).filter(Annotation.status.in_(["submitted", "flagged"])).all()
    return [{"id": a.id, "task_id": a.task_id, "preference": a.preference, "status": a.status} for a in annotations]


@router.post("/approve")
def approve(payload: ReviewInput, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    annotation = db.get(Annotation, payload.annotation_id)
    if not annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")
    annotation.status = "approved"
    db.add(Review(annotation_id=payload.annotation_id, reviewer_id=user.id, decision="approve", comments=payload.comments))
    db.commit()
    return {"approved": payload.annotation_id}


@router.post("/reject")
def reject(payload: ReviewInput, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    annotation = db.get(Annotation, payload.annotation_id)
    if not annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")
    annotation.status = "rejected"
    db.add(Review(annotation_id=payload.annotation_id, reviewer_id=user.id, decision="reject", comments=payload.comments))
    db.commit()
    return {"rejected": payload.annotation_id}


@router.post("/adjudicate")
def adjudicate(payload: AdjudicationInput, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    result = Adjudication(task_id=payload.task_id, adjudicator_id=user.id,
                          final_preference=payload.final_preference, final_rationale=payload.final_rationale,
                          resolved_errors=payload.resolved_errors)
    db.add(result)
    db.commit()
    return {"id": result.id, "final_preference": result.final_preference}
