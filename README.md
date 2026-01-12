# Second Brain Prototype — Sprint 2

Python + web prototype for a private Second Brain with file ingestion, duplicate detection, text extraction, metadata, and first knowledge graph API.

## Sprint 2 adds

- Text extraction for `.pdf`, `.md`, `.txt`, `.csv`, `.xlsx`, and `.xls`
- Extracted text storage in `backend/uploads/extracted/`
- Basic metadata: word count, text length, pages, rows, columns, sheets, extraction engine
- Basic summary placeholder without external LLM dependency
- Basic keyword extraction placeholder
- Graph API: central brain, areas, subjects, documents, file types, keywords, duplicate edges
- Frontend graph panel
- Reprocess endpoint
- Extracted text endpoint

## Repository structure

```text
second-brain-sprint2/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── documents.py
│   │   │   └── graph.py
│   │   ├── core/
│   │   ├── models/
│   │   └── services/
│   │       ├── extraction.py
│   │       ├── file_service.py
│   │       ├── graph.py
│   │       └── registry.py
│   ├── data/documents.json
│   ├── uploads/originals/
│   ├── uploads/extracted/
│   └── requirements.txt
├── frontend/
│   ├── app/
│   └── components/
└── docs/
```

## Run backend

```bash
cd second-brain-sprint2/backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
GET /health
```

Expected:

```json
{
  "status": "ok",
  "app": "Second Brain API"
}
```

## Run frontend

In another terminal:

```bash
cd second-brain-sprint2/frontend
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

## Main API routes

```text
GET  /health
GET  /api/documents
GET  /api/documents/{document_id}
GET  /api/documents/{document_id}/text
POST /api/documents/upload
POST /api/documents/{document_id}/reprocess
GET  /api/graph
```

## Sprint 2 test flow

1. Start backend.
2. Start frontend.
3. Upload one `.txt`, `.md`, `.csv`, `.xlsx`, or `.pdf` file.
4. Confirm document status becomes `processed`.
5. Confirm summary, keywords, and metadata appear.
6. Upload the same file again.
7. Confirm status becomes `duplicate`.
8. Open `GET /api/graph` in Swagger.
9. Confirm graph nodes and edges were generated.

## Notes

- The summary and keywords are simple deterministic placeholders for now.
- Sprint 3 should replace or complement them with an LLM-based extraction layer.
- The graph frontend is intentionally lightweight and does not yet use Cytoscape/Sigma.
- The backend still uses JSON storage for MVP simplicity. A later sprint should migrate to PostgreSQL + pgvector.


## Graph display fix

This package includes a Sprint 2.1 visual fix for the Brain Graph. The graph rings now stay inside the canvas, node positions are clamped, bottom labels are placed above nodes, and the canvas is taller. This resolves the cut-off graph issue from Sprint 2.
