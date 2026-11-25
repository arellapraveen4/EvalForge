import csv
import json
from io import StringIO
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.dataset import Dataset, DatasetItem
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    content = (await file.read()).decode("utf-8-sig")
    suffix = (file.filename or "").lower().rsplit(".", 1)[-1]
    if suffix == "csv":
        rows = list(csv.DictReader(StringIO(content)))
    elif suffix in ("json", "jsonl"):
        rows = [json.loads(line) for line in content.splitlines() if line.strip()] if suffix == "jsonl" else json.loads(content)
        if isinstance(rows, dict):
            rows = rows.get("tasks", rows.get("items", [rows]))
    else:
        raise HTTPException(status_code=400, detail="Only CSV, JSON, and JSONL files are supported")
    if not isinstance(rows, list) or not rows:
        raise HTTPException(status_code=400, detail="The dataset is empty")

    dataset = Dataset(name=file.filename or "Uploaded dataset", format=suffix, created_by=user.id)
    db.add(dataset)
    db.flush()
    duplicates = set()
    missing_prompt = 0
    inserted = 0
    for row in rows:
        prompt = row.get("prompt")
        external_id = str(row.get("id") or row.get("task_id") or "")
        if not prompt:
            missing_prompt += 1
            continue
        if external_id and external_id in duplicates:
            continue
        if external_id:
            duplicates.add(external_id)
        db.add(DatasetItem(
            dataset_id=dataset.id, external_id=external_id or None,
            category=row.get("category"), task_type=row.get("task_type") or "pairwise",
            difficulty=row.get("difficulty"), prompt=prompt, context=row.get("context"),
            response_a=row.get("response_a"), response_b=row.get("response_b"),
            reference_answer=row.get("reference_answer"), expected_constraints=row.get("expected_constraints"),
            source=row.get("source"), license=row.get("license"), extra=row,
        ))
        inserted += 1
    db.commit()
    db.refresh(dataset)
    return {"id": dataset.id, "name": dataset.name, "items": inserted, "missing_prompt": missing_prompt}


@router.get("")
def list_datasets(db: Session = Depends(get_db)):
    datasets = db.query(Dataset).order_by(Dataset.created_at.desc()).all()
    return [{"id": d.id, "name": d.name, "format": d.format, "created_at": d.created_at.isoformat()} for d in datasets]


@router.get("/{dataset_id}")
def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    dataset = db.get(Dataset, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    items = [{"id": i.id, "external_id": i.external_id, "category": i.category, "prompt": i.prompt,
              "response_a": i.response_a, "response_b": i.response_b, "reference_answer": i.reference_answer,
              "difficulty": i.difficulty} for i in dataset.items]
    return {"id": dataset.id, "name": dataset.name, "items": items}


@router.delete("/{dataset_id}")
def delete_dataset(dataset_id: int, db: Session = Depends(get_db)):
    dataset = db.get(Dataset, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    db.delete(dataset)
    db.commit()
    return {"deleted": dataset_id}
