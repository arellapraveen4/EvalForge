from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine
from app.database import base as _base
from app.database.database import Base
from app.api.routes import auth, datasets, tasks, annotations, reviews, evaluation, analytics, export

Base.metadata.create_all(bind=engine)

app = FastAPI(title="EvalForge", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(datasets.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")
app.include_router(annotations.router, prefix="/api")
app.include_router(reviews.router, prefix="/api")
app.include_router(evaluation.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(export.router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "healthy", "service": "EvalForge"}
