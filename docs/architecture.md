# EvalForge Architecture

The React frontend communicates with FastAPI through REST and JSON. FastAPI exposes authentication, dataset ingestion, task assignment, annotation, review, evaluation, analytics, and export workflows.

SQLAlchemy models persist users, datasets, dataset items, tasks, rubrics, annotations, scores, errors, reviews, adjudications, model runs, judge results, and experiments. The default database is SQLite; Docker uses PostgreSQL.

The evaluation package separates deterministic metrics, rubric scoring, pairwise comparison, mock or external LLM judging, factual claim extraction, groundedness analysis, safety checks, and statistical metrics.

Raw model output and parsed structured output should be retained separately. Keep human judgments separate from AI judgments and from adjudicated ground truth.
