from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.dataset import Dataset, DatasetItem
from app.models.evaluation_task import EvaluationTask
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/create")
def create_tasks(dataset_id: int, annotators_per_task: int = 1, db: Session = Depends(get_db),
                 user: User = Depends(get_current_user)):
    dataset = db.get(Dataset, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    created = []
    for item in dataset.items:
        for _ in range(max(1, annotators_per_task)):
            task = EvaluationTask(dataset_item_id=item.id, task_type=item.task_type or "pairwise")
            db.add(task)
            db.flush()
            created.append(task.id)
    db.commit()
    return {"created": len(created), "task_ids": created}


@router.get("")
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(EvaluationTask).order_by(EvaluationTask.id).all()
    return [{"id": t.id, "status": t.status, "task_type": t.task_type} for t in tasks]


@router.get("/my-tasks")
def my_tasks(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = db.query(EvaluationTask).filter(EvaluationTask.assignee_id == user.id).all()
    return [{"id": t.id, "status": t.status, "task_type": t.task_type} for t in tasks]


@router.get("/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(EvaluationTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    item = db.get(DatasetItem, task.dataset_item_id)
    return {"id": task.id, "status": task.status, "task_type": task.task_type,
            "item": {"prompt": item.prompt, "context": item.context, "response_a": item.response_a,
                     "response_b": item.response_b, "category": item.category}}


@router.post("/{task_id}/assign")
def assign_task(task_id: int, annotator_id: int, db: Session = Depends(get_db)):
    task = db.get(EvaluationTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.assignee_id = annotator_id
    task.status = "assigned"
    db.commit()
    return {"id": task_id, "assignee_id": annotator_id}
