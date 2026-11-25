# EvalForge

<div align="center">

**Human and AI Response Evaluation Laboratory**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=111827)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

Production-oriented platform for dataset management, LLM response evaluation, human preference annotation, reviewer adjudication, evaluator reliability analysis, benchmarking, and reproducible AI quality experiments.

</div>

---

## Table of Contents

- [Overview](#overview)
- [Why EvalForge](#why-evalforge)
- [Key Capabilities](#key-capabilities)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Repository Structure](#repository-structure)
- [Data Model](#data-model)
- [Evaluation Framework](#evaluation-framework)
- [Annotation Workflow](#annotation-workflow)
- [Reliability and Analytics](#reliability-and-analytics)
- [Frontend Pages](#frontend-pages)
- [API Reference](#api-reference)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Docker Deployment](#docker-deployment)
- [Sample Workflow](#sample-workflow)
- [Testing](#testing)
- [Experiment and Benchmark Design](#experiment-and-benchmark-design)
- [Security and Responsible Use](#security-and-responsible-use)
- [Current Implementation Status](#current-implementation-status)
- [Roadmap](#roadmap)
- [Documentation](#documentation)
- [License](#license)

---

## Overview

EvalForge is a full-stack research and operations platform for evaluating AI-generated responses.

It combines:

- Human data annotation
- Side-by-side response ranking
- Rubric-based 1–5 scoring
- Error taxonomy annotation
- Independent AI-as-a-Judge evaluation
- Hallucination and groundedness analysis
- Safety screening
- Inter-annotator agreement analysis
- Human-versus-AI reliability measurement
- Position-bias experiments
- Benchmark reporting
- Dataset and annotation exports

EvalForge is designed for AI quality analyst, AI trainer, red-team, human-feedback, evaluation research, and LLM benchmark workflows.

> EvalForge does not treat majority vote or a judge score as automatically correct. Human consensus, adjudication, available ground truth, and AI judgments are modeled as separate evidence sources.

---

## Why EvalForge

Generic dashboards and static spreadsheets cannot provide a controlled, traceable evaluation process.

EvalForge provides:

| Concern | EvalForge approach |
|---|---|
| Reproducibility | Task IDs, model versions, prompt versions, experiment configuration, and timestamps |
| Blindness | Independent submissions remain isolated until review |
| Auditability | Annotation revisions, review decisions, and adjudication records |
| Human diversity | Separate user records and independent annotator judgments |
| Judge validation | Agreement, accuracy, Kappa, confusion matrices, and bootstrap confidence intervals |
| Bias testing | Controlled pair order reversal for position-bias measurement |
| Evidence | Rationale, error spans, evidence context, and claim-level groundedness |
| Portability | SQLite locally and PostgreSQL in Docker |
| Provider independence | Gemini, OpenAI-compatible, and mock providers |
| Data export | CSV and JSON annotation and benchmark exports |

---

## Key Capabilities

### Dataset Operations

- CSV, JSON, and JSONL ingestion
- Prompt, response, reference, context, and metadata support
- Dataset preview and item retrieval
- Missing prompt and duplicate ID detection
- Category, difficulty, task type, source, and license metadata
- Dataset deletion with related item cleanup

### Human Annotation

- Pairwise A/B comparison
- A, B, Tie, and Both Poor preferences
- Multi-dimensional rubric scoring
- Multiple error labels per response
- Evidence and rationale capture
- Confidence reporting
- Time spent and submission timestamp
- Revision history for submitted annotations
- Blind annotation mode

### Review and Adjudication

- Reviewer pending queue
- Approve, reject, and return workflows
- Independent annotation visibility after blind submissions
- Final preference and rationale capture
- Conflict resolution through adjudication
- Audit trail for review decisions

### Evaluation Engine

- Normalized exact-match comparison
- Word-overlap metric
- Weighted rubric calculation
- Deterministic mock judge for dependency-free development
- Google Gemini API, OpenAI-compatible, and deterministic mock providers
- Structured judge JSON output
- Pairwise score comparison
- Claim-level context-groundedness analysis
- Rule-based safety warning checks

### Reliability and Research

- Percentage agreement
- Mean task-level agreement
- Bootstrap confidence intervals
- Cohen's Kappa for paired judgments
- Human-versus-AI accuracy and Kappa
- Confusion matrices
- Spearman correlation
- Position-bias measurement
- Error distribution
- Preference distribution

### Benchmark and Export

- Dashboard statistics
- Task and annotation progress
- Model preference summaries
- JSON and CSV annotation export
- JSON benchmark export

---

## System Architecture

```mermaid
flowchart LR
    A[React + TypeScript] -->|REST / JSON| B[FastAPI]
    B --> C[Authentication]
    B --> D[Dataset Service]
    B --> E[Task Service]
    B --> F[Annotation Service]
    B --> G[Review Service]
    B --> H[Evaluation Engine]
    B --> I[Quality Analytics]
    H --> J[Deterministic Metrics]
    H --> K[Rubric Engine]
    H --> L[Mock or LLM Judge]
    H --> M[Groundedness and Safety]
    I --> N[Agreement and Reliability]
    I --> O[Bias and Correlation]
    B --> P[(SQLite or PostgreSQL)]
```

### Request Flow

1. The frontend submits an authenticated API request.
2. FastAPI validates role and request data.
3. SQLAlchemy reads or writes relational state.
4. Evaluation services calculate deterministic or AI-assisted results.
5. Analytics endpoints aggregate human, AI, and benchmark data.
6. Export endpoints serialize annotations or benchmark reports.

### Component Design

| Component | Responsibility |
|---|---|
| `app/core` | Settings and JWT/password security |
| `app/database` | SQLAlchemy engine and declarative base |
| `app/models` | Persistent entities and relationships |
| `app/schemas` | Pydantic request and response contracts |
| `app/api/routes` | REST endpoints |
| `app/evaluation` | Rubrics, metrics, judges, and safety |
| `app/analytics` | Agreement, reliability, correlation, and bias |
| `frontend/src/pages` | Product workflows |
| `frontend/src/services` | Axios API integration |
| `frontend/src/types` | Shared TypeScript types |

---

## Technology Stack

| Area | Technology |
|---|---|
| Frontend | React 18, TypeScript 5, Vite |
| Styling | Tailwind CSS v4 |
| Charts | Recharts |
| Icons | Lucide React |
| API client | Axios |
| Backend | Python 3.11, FastAPI |
| Database ORM | SQLAlchemy |
| Validation | Pydantic |
| Authentication | JWT, bcrypt |
| Database | SQLite for local use, PostgreSQL 16 for Docker |
| Statistics | scikit-learn, SciPy |
| Data | pandas, NumPy |
| LLM integration | HTTPX, Google Gemini API, OpenAI-compatible API |
| Testing | pytest, Vitest |
| Deployment | Docker Compose, Nginx |

---

## Repository Structure

```text
EvalForge/
├── backend/
│   ├── app/
│   │   ├── analytics/          Agreement and reliability analysis
│   │   ├── api/routes/         Authentication and REST endpoints
│   │   ├── core/               Settings and security
│   │   ├── database/           SQLAlchemy setup
│   │   ├── evaluation/         Rubrics, metrics, judges, safety
│   │   ├── models/             Database entities
│   │   ├── schemas/            Pydantic contracts
│   │   └── main.py             FastAPI application
│   ├── app/tests/              Backend tests
│   ├── .env.example
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/              Product screens
│   │   ├── services/           API client
│   │   ├── types/              Shared frontend types
│   │   ├── App.tsx
│   │   └── styles.css
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   └── vite.config.ts
├── datasets/
│   ├── raw/
│   ├── processed/
│   └── sample/
├── experiments/
│   ├── judge_reliability/
│   ├── position_bias/
│   └── human_agreement/
├── docs/
│   ├── architecture.md
│   ├── annotation_guidelines.md
│   ├── evaluation_protocol.md
│   └── research_report.md
├── docker-compose.yml
├── .gitignore
├── LICENSE
└── README.md
```

---

## Data Model

Core persisted entities:

| Entity | Purpose |
|---|---|
| `User` | Account, role, credentials |
| `Dataset` | Dataset metadata |
| `DatasetItem` | Prompt, response, context, reference, and source |
| `EvaluationTask` | Assignment and task status |
| `Rubric` | Named rubric |
| `RubricDimension` | Weighted rubric criterion |
| `Annotation` | Independent human judgment |
| `AnnotationScore` | Dimension-level score |
| `AnnotationError` | Category, severity, span, and explanation |
| `Review` | Reviewer decision |
| `Adjudication` | Final conflict resolution |
| `ModelRun` | Raw and parsed AI model response |
| `JudgeResult` | AI judge result and metadata |
| `Experiment` | Experiment configuration |
| `ExperimentResult` | Experiment metric and details |

Human annotations remain separate from AI judgments. Revisions preserve prior values rather than silently overwriting submitted work.

---

## Evaluation Framework

### Default General Rubric

| Dimension | Weight | Description |
|---|---:|---|
| Correctness | 30% | Factual and logical accuracy |
| Instruction following | 20% | Adherence to explicit requirements |
| Relevance | 20% | Focus on the user's request |
| Completeness | 15% | Coverage of important information |
| Clarity | 15% | Understandability and structure |

The weighted rubric formula is:

```text
weighted score = sum(dimension score × dimension weight) / sum(applied weights)
```

A task-specific rubric should be used instead of forcing one generic rubric onto every domain.

### Error Taxonomy

- Factual error
- Hallucination
- Logical error
- Instruction violation
- Omission
- Relevance failure
- Code failure
- Formatting failure
- Safety violation
- Excessive verbosity
- Contradiction

Error tags may be accompanied by severity, evidence span, and explanation.

### Pairwise Preference

Supported preferences:

| Preference | Meaning |
|---|---|
| `A` | Response A is better |
| `B` | Response B is better |
| `Tie` | Neither response is clearly better |
| `BothPoor` | Both responses are inadequate |

The final preference should consider severe errors and safety—not merely a higher weighted numerical score.

### Judge Behavior

Gemini is the configured default judge. It uses Google's `generateContent` REST API, requests JSON output, validates the result against the evaluation schema, and calculates the final weighted score in the backend. The API key is sent in the `x-goog-api-key` header.

The mock judge is intentionally deterministic and is only suitable for architecture, UI, API, and workflow testing. It is not a real AI evaluation.

The Gemini and OpenAI-compatible judges send a structured evaluation prompt and return JSON containing:

- Correctness
- Instruction following
- Relevance
- Completeness
- Clarity
- Overall score
- Verdict
- Error tags
- Rationale
- Confidence

Configure a real provider only for controlled experiments or production evaluation.

---

## Annotation Workflow

```mermaid
sequenceDiagram
    participant Admin
    participant Dataset
    participant Task
    participant Annotator
    participant Reviewer

    Admin->>Dataset: Upload data
    Admin->>Task: Create and configure tasks
    Admin->>Task: Assign annotators
    Annotator->>Task: Submit blind judgment
    Task->>Reviewer: Send completed annotation
    Reviewer->>Task: Approve, reject, or request adjudication
    Reviewer->>Task: Store final preference and rationale
```

Recommended quality settings:

1. Assign independent annotators.
2. Prevent peer judgments from appearing before submission.
3. Collect rationale and confidence.
4. Preserve revision history.
5. Use a reviewer for disputes or low-confidence labels.
6. Keep adjudicated labels separate from individual and majority labels.
7. Record model, prompt, rubric, and task versions.

---

## Reliability and Analytics

EvalForge supports the following concepts:

| Metric | Use |
|---|---|
| Percentage agreement | Agreement with the most frequent label for one item |
| Cohen's Kappa | Agreement between two annotators or judge/human labels |
| Fleiss' Kappa | Multi-annotator categorical agreement, where assumptions are appropriate |
| Spearman correlation | Ranked relationship between scores or systems |
| Accuracy | Human-versus-AI preference match |
| Confusion matrix | Human/AI disagreement patterns |
| Bootstrap CI | Sampling uncertainty for benchmark metrics |
| Position-bias rate | Preference change after swapping response positions |

Example bootstrap reporting format:

```text
Judge agreement: 82.4%
95% bootstrap CI: 78.1–86.2%
```

Bootstrap values are only valid for the tested sample and must include the sample size and resampling configuration.

### Interpretation Rules

- Majority vote is not automatically truth.
- Agreement does not alone measure annotator competence.
- A small dataset should not support strong superiority claims.
- Separate AI judge agreement from adjudicated ground truth.
- Report category-level results and limitations.
- Consider bias, annotation uncertainty, safety, and task ambiguity.

---

## Frontend Pages

| Page | Main Functions |
|---|---|
| Login | Register, login, and role setup |
| Dashboard | Task and annotation overview |
| Datasets | Upload, preview, validation, and dataset management |
| Annotation Tasks | Prompt and A/B response evaluation |
| Reviews | Approve, reject, and adjudicate judgments |
| Benchmarks | Preference and model experiment summaries |
| Analytics | Agreement, judge reliability, and error analysis |
| Settings | Reserved for provider and workspace configuration |

---

## API Reference

Interactive API documentation is available at:

- Swagger UI: `http://localhost:8000/docs`
- OpenAPI schema: `http://localhost:8000/openapi.json`
- Health: `http://localhost:8000/health`

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/register` | Register a user |
| `POST` | `/api/auth/login` | Obtain a JWT |
| `GET` | `/api/auth/me` | Return the current user |

Supported roles:

- `admin`
- `annotator`
- `reviewer`

### Datasets

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/datasets/upload` | Upload CSV, JSON, or JSONL |
| `GET` | `/api/datasets` | List datasets |
| `GET` | `/api/datasets/{id}` | Get dataset items |
| `DELETE` | `/api/datasets/{id}` | Delete a dataset |

### Tasks

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/tasks/create` | Generate tasks from a dataset |
| `GET` | `/api/tasks` | List tasks |
| `GET` | `/api/tasks/{id}` | Get task and responses |
| `POST` | `/api/tasks/{id}/assign` | Assign an annotator |
| `GET` | `/api/tasks/my-tasks` | Get assigned tasks |

### Annotations

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/annotations/submit` | Submit an annotation |
| `GET` | `/api/annotations/{id}` | Get annotation details |
| `GET` | `/api/annotations/task/{task_id}` | List task annotations |
| `PUT` | `/api/annotations/{id}` | Revise an annotation |

### Reviews

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/reviews/pending` | List pending annotations |
| `POST` | `/api/reviews/approve` | Approve an annotation |
| `POST` | `/api/reviews/reject` | Reject an annotation |
| `POST` | `/api/reviews/adjudicate` | Create a final adjudication |

### Evaluation

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/evaluation/single` | Evaluate one response |
| `POST` | `/api/evaluation/pairwise` | Compare two responses |
| `POST` | `/api/evaluation/batch` | Evaluate multiple responses |

### Analytics and Export

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/analytics/dashboard` | Dashboard statistics |
| `GET` | `/api/analytics/agreement` | Annotation agreement |
| `GET` | `/api/analytics/judge-reliability` | Human/AI reliability placeholder |
| `GET` | `/api/analytics/error-distribution` | Error category counts |
| `GET` | `/api/analytics/benchmark` | Preference benchmark summary |
| `POST` | `/api/analytics/position-bias` | Compare original and reversed preferences |
| `GET` | `/api/export/annotations/csv` | Download annotation CSV |
| `GET` | `/api/export/annotations/json` | Download annotation JSON |
| `GET` | `/api/export/benchmark/json` | Download benchmark JSON |

---

## Quick Start

### Prerequisites

- Windows PowerShell or a compatible shell
- Python 3.11
- Node.js 20 or later
- Docker Desktop, for the full container stack

### 1. Create the Backend Environment

Before starting the backend, set `GEMINI_API_KEY` in `backend/.env` as described in [Configuration](#configuration). The default judge is Gemini; evaluation requests return a configuration error until a key is supplied. Choose `LLM_PROVIDER=mock` if you want to explore the UI without calling an external model.

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

The backend will be available at `http://localhost:8000`.

### 2. Start the Frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

The Vite development server proxies `/api` requests to `http://localhost:8000`.

### 3. Register a User

Open Swagger UI at `http://localhost:8000/docs` and register through:

```text
POST /api/auth/register
```

Example:

```json
{
  "email": "admin@example.com",
  "name": "Admin",
  "password": "replace-with-a-strong-password",
  "role": "admin"
}
```

Use the returned JWT as a bearer token in protected requests.

---

## Configuration

Copy `backend/.env.example` to `backend/.env`.

```env
DATABASE_URL=sqlite:///./evalforge.db
JWT_SECRET=replace-this-with-a-random-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_MINUTES=720

LLM_PROVIDER=gemini
GEMINI_API_KEY=your-google-ai-studio-api-key
GEMINI_MODEL=gemini-2.5-flash

OPENAI_API_KEY=
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

### Local SQLite

```env
DATABASE_URL=sqlite:///./evalforge.db
```

SQLAlchemy creates required tables on backend startup.

### PostgreSQL

```env
DATABASE_URL=postgresql+psycopg://evalforge:evalforge@localhost:5432/evalforge
```

### Gemini Judge (Default)

Create a Gemini API key in Google AI Studio, then configure:

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-google-ai-studio-api-key
GEMINI_MODEL=gemini-2.5-flash
```

The evaluation endpoints return HTTP 503 with a configuration message if Gemini is selected but `GEMINI_API_KEY` is missing. Provider errors are not silently replaced with mock scores.

### Deterministic Mock Judge

Use the mock only for local UI and workflow testing without an API key:

```env
LLM_PROVIDER=mock
```

Mock scores are illustrative and must not be used as experimental results.

### OpenAI-Compatible Judge

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

Never commit API keys, credentials, private datasets, or confidential annotations.

---

## Docker Deployment

Start PostgreSQL, the FastAPI backend, and the React frontend:

```powershell
docker compose up --build
```

Docker Compose reads interpolation variables from a root `.env` file next to `docker-compose.yml`. Create it with the Gemini settings below to use Gemini:

```env
GEMINI_API_KEY=your-google-ai-studio-api-key
GEMINI_MODEL=gemini-2.5-flash
LLM_PROVIDER=gemini
JWT_SECRET=replace-this-with-a-long-random-secret
```

Set `LLM_PROVIDER=mock` in that file to run without an external judge. The backend's `backend/.env` is used for direct local runs, not automatically loaded by Compose.

Services:

| Service | Address |
|---|---|
| Frontend | `http://localhost:5173` |
| Backend | `http://localhost:8000` |
| API docs | `http://localhost:8000/docs` |
| PostgreSQL | `localhost:5432` |

Stop the stack:

```powershell
docker compose down
```

Remove PostgreSQL data:

```powershell
docker compose down -v
```

> `down -v` deletes the named database volume. Do not use it with production data.

Before public deployment, replace default database credentials and JWT secrets, restrict CORS, enable TLS, and add appropriate rate limiting and monitoring.

---

## Sample Workflow

### 1. Upload a Dataset

Upload [`datasets/sample/sample_tasks.json`](/c:/Users/arell/OneDrive/Desktop/EvalForge/datasets/sample/sample_tasks.json).

```text
POST /api/datasets/upload
```

### 2. Create Tasks

```text
POST /api/tasks/create?dataset_id=1&annotators_per_task=3
```

### 3. Assign an Annotator

```text
POST /api/tasks/1/assign?annotator_id=2
```

### 4. Submit an Annotation

```json
{
  "task_id": 1,
  "preference": "A",
  "scores": [
    {
      "dimension": "correctness",
      "response_side": "A",
      "score": 5,
      "explanation": "The response is factually correct."
    }
  ],
  "errors": [
    {
      "category": "factual_error",
      "severity": "major",
      "explanation": "The response contradicts the reference."
    }
  ],
  "rationale": "Response A answers the prompt accurately and follows the required format.",
  "confidence": 0.91,
  "time_taken_seconds": 42
}
```

### 5. Review and Export

- Approve or reject through the review API.
- Adjudicate disagreements through `/api/reviews/adjudicate`.
- Export annotations as CSV or JSON.
- Compare human and AI judgments in analytics.

---

## Testing

### Backend

```powershell
cd backend
pytest
```

Backend tests should cover:

- Authentication and role restrictions
- Dataset ingestion and validation
- Duplicate and missing-field detection
- Task creation and assignment
- Annotation submission and revision history
- Reviewer decisions
- Adjudication
- Rubric calculations
- Pairwise comparison
- Deterministic metrics
- Judge parsing
- Groundedness and safety helpers

### Frontend

```powershell
cd frontend
npm run build
npm test
```

Frontend tests should cover:

- Annotation submission
- Rubric selection
- Error tagging
- Task navigation
- Dataset upload
- Reviewer controls
- Dashboard and analytics rendering

### Evaluation Quality

Use controlled test cases:

| Test | Expected behavior |
|---|---|
| Correct answer | High correctness score |
| Factual error | Low correctness score |
| Missing list items | Instruction-following failure |
| Irrelevant answer | Low relevance score |
| Unsupported claim | Groundedness warning |
| Contradictory answer | Contradiction tag |
| Unsafe answer | Safety warning where appropriate |
| Reversed pair order | Agreement/position-bias measurement |
| Repeated judging | Repeatability assessment |
| Rubric version change | Rubric sensitivity assessment |

LLM judge output must be validated rather than assumed correct.

---

## Experiment and Benchmark Design

### Position-Bias Experiment

1. Evaluate a pair with the original response order.
2. Repeat with the responses swapped.
3. Use identical task IDs and judge configuration.
4. Measure preference changes.
5. Report tie rates and confidence changes.

### Human Agreement Experiment

1. Collect independent human labels.
2. Preserve individual judgments.
3. Calculate majority and agreement labels.
4. Adjudicate unresolved conflicts.
5. Do not relabel the majority as ground truth automatically.

### Judge Reliability Experiment

1. Generate or collect response pairs.
2. Obtain independent human labels.
3. Run the AI judge under a fixed prompt and rubric version.
4. Compare individual and consensus human labels separately.
5. Report accuracy, Kappa, confusion matrices, category results, and confidence intervals.

### Rubric Sensitivity Experiment

Compare:

- Rubric versions
- Weighted versus unweighted scores
- Task-specific versus generic dimensions
- Judge models
- Prompt templates
- Response order

### Bias Experiment

Matched controlled prompts may vary a single attribute. Use adequately sized samples and appropriate safeguards. Do not infer bias from isolated prompt pairs or demographic names alone.

### Reproducibility Record

For every benchmark run, retain:

- Dataset version
- Dataset license and source
- Task IDs
- Response model and version
- Prompt template version
- Rubric version
- Judge model and settings
- Random seed
- Temperature
- Sample size
- Timestamp
- Raw model output
- Parsed output
- Human adjudication status

---

## Security and Responsible Use

- Store passwords only as bcrypt hashes.
- Use short-lived JWTs and strong production secrets.
- Add role-based authorization before exposing admin operations.
- Restrict CORS to known frontend origins.
- Never log API keys or private annotation payloads.
- Encrypt credentials and sensitive data at rest where required.
- Encrypt API traffic with HTTPS in production.
- Review the licenses of public datasets before redistribution.
- Separate public benchmark data from judge-tuning data.
- Use content safeguards for safety datasets.
- Add rate limiting, audit logs, monitoring, and backups.
- Use access controls for reviewer and adjudication operations.
- Do not use annotator agreement metrics for punitive or competency decisions without validated procedures and contextual review.

---

## Current Implementation Status

The repository provides working local and Docker project scaffolding.

Implemented:

- FastAPI data models and REST routes
- Gemini, OpenAI-compatible, and mock judge paths
- SQLite/PostgreSQL database configuration
- Human annotation and revision structures
- Review and adjudication endpoints
- Dataset upload for CSV, JSON, and JSONL
- Agreement and analytics endpoints
- React workflow screens
- Docker Compose deployment
- Sample dataset
- Backend evaluation tests

Production work still needed:

- Alembic migrations
- Fine-grained role authorization on every route
- Database migration-managed PostgreSQL startup
- Judge JSON-schema enforcement
- Full Fleiss' Kappa integration
- Production worker or queue for batch evaluation
- Redis/caching if required
- Persistent raw audit logs
- Complete frontend API authentication workflow
- End-to-end and frontend test suites
- Secret and key management
- Monitoring, tracing, and error reporting

---

## Roadmap

### Near Term

- Alembic schema migrations
- Admin rubric editor
- Strong per-route role checks
- Annotator assignment queue
- Real-time task status
- Structured judge-output validation
- Annotation revisions in the frontend
- Reviewer disagreement comparison

### Evaluation Advanced

- Claim extraction models
- Sentence-transformer evidence retrieval
- NLI claim classification
- Coding executor and test verification
- Multi-turn task evaluation
- LLM cost and latency tracking
- Model leaderboard with confidence intervals
- Rubric version comparisons

### Reliability Advanced

- Fleiss' Kappa
- Intraclass correlation
- Krippendorff's Alpha
- Confidence calibration
- Annotator drift tracking
- Bias audit workflows
- Per-category reliability reports

### Platform Advanced

- Background task workers
- Redis job queue
- Object storage for large datasets
- Optional Qdrant evidence index
- SSO and organization-level RBAC
- Managed secrets
- Production audit logging
- Kubernetes deployment options

---

## Documentation

- [Architecture](/c:/Users/arell/OneDrive/Desktop/EvalForge/docs/architecture.md)
- [Annotation Guidelines](/c:/Users/arell/OneDrive/Desktop/EvalForge/docs/annotation_guidelines.md)
- [Evaluation Protocol](/c:/Users/arell/OneDrive/Desktop/EvalForge/docs/evaluation_protocol.md)
- [Research Report](/c:/Users/arell/OneDrive/Desktop/EvalForge/docs/research_report.md)

---

## License

EvalForge is distributed under the [MIT License](/c:/Users/arell/OneDrive/Desktop/EvalForge/LICENSE).
#   E v a l F o r g e  
 