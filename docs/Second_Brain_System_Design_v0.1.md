# Second Brain — System Design v0.1

## 1. Product Vision

Second Brain is a Python-based web knowledge system that transforms documents, notes, spreadsheets, PDFs, and structured data into an organized, searchable, visual knowledge graph.

The system is not only a file repository. It is a private intelligence layer where uploaded content becomes structured knowledge: areas, subjects, concepts, entities, relationships, insights, and updates.

Core idea:

```text
Files become knowledge.
Knowledge becomes nodes.
Nodes become a living brain graph.
Updates become versioned intelligence.
```

## 2. Prototype Package Review

The uploaded package contains:

```text
second-brain-prototipe/
├── brand-guide/
│   └── SB - Color and Style.pdf
├── notes/
│   └── what-I-want.md
├── prototype-code/
│   └── empty
├── screeshots/
│   └── empty
└── sample-files/
    ├── PDFs about AI, smart cities, governance, healthcare, finance, and technology
    └── Pasta1.csv
```

Important findings:

- There is no current codebase, so this should be treated as a from-zero MVP.
- The brand guide defines a dark neural-graph visual identity.
- The main background color is `#171927`.
- The neural graph color family includes `#F8E26C`, `#885BD6`, `#2EBCB6`, `#467CD9`, `#D463E6`, `#BFE081`, `#51E697`, and `#F89570`.
- The sample files are strong enough to test long PDF ingestion, duplicate detection, classification, and graph generation.
- Two Smart Cities PDFs are exact duplicates by file hash, which is useful for testing duplicate detection.
- `Pasta1.csv` contains simple area-performance data and can be used to test structured-data ingestion.

## 3. Initial Knowledge Areas

The first taxonomy should begin with the areas defined in the package:

```text
- AI
- Business
- Research
- Smart Cities
- Finance
```

Recommended additional areas based on the sample files:

```text
- Healthcare
- Government / Public Policy
- Digital Transformation
- Risk / Security
- Urban Intelligence
```

The taxonomy should be editable by the user. The AI can suggest classifications, but the user should be able to correct them.

## 4. Product Scope

### MVP 1 — Functional Second Brain

The first MVP should include:

1. Web interface with dark strategic visual style.
2. File upload for `.pdf`, `.md`, `.txt`, `.csv`, `.xls`, and `.xlsx`.
3. File hashing for duplicate detection.
4. Text extraction from uploaded files.
5. Automatic summary generation.
6. Automatic area and subject classification.
7. Concept and entity extraction.
8. Basic graph visualization.
9. Document explorer.
10. Update and version-control logic.
11. Ask/search over uploaded content.

### MVP 2 — Intelligent Brain

After MVP 1:

1. Semantic search using embeddings.
2. Related idea suggestions.
3. Similar document detection.
4. Contradiction and update alerts.
5. Timeline of knowledge evolution.
6. Manual and AI-assisted taxonomy refinement.

### MVP 3 — Knowledge Operating System

Later expansion:

1. Obsidian import/export.
2. Multi-user workspace.
3. Area-specific agents.
4. Research assistant.
5. Strategic reports generated from the graph.
6. API integrations.
7. Enterprise governance, audit trail, and permissions.

## 5. Recommended Architecture

Recommended stack:

| Layer | Technology |
|---|---|
| Frontend | Next.js + React + TypeScript |
| Backend | Python FastAPI |
| Processing | Python ingestion workers |
| Database | PostgreSQL |
| Vector search | pgvector |
| Graph visualization | Cytoscape.js or Sigma.js |
| File storage | Local storage first; Azure Blob/S3 later |
| AI layer | LLM for summarization, classification, extraction, Q&A |
| Deployment | Local-first, cloud-ready |

High-level architecture:

```text
Web Frontend
    ↓
FastAPI Backend
    ↓
Upload Service
    ↓
Ingestion Pipeline
    ↓
Text Extraction
    ↓
Chunking + Metadata Extraction
    ↓
LLM Classification + Embeddings
    ↓
PostgreSQL + pgvector
    ↓
Graph API
    ↓
Neural Brain UI
```

## 6. Frontend Design

### Main Screens

```text
Dashboard
├── Brain Graph
├── Upload Center
├── Knowledge Areas
├── Document Explorer
├── Processing Jobs
├── Duplicate / Update Alerts
└── Ask My Brain
```

### Visual Direction

The UI should follow the provided brand guide:

- Dark background: `#171927`
- Neural graph with glowing but elegant node colors
- Clean dashboard inspired by enterprise technology interfaces
- Cisco-like clarity, but with a more intelligent/neural visual identity
- Strategic, not playful
- Visual brain graph as the hero interaction

### Suggested Color Mapping

| Area | Color |
|---|---|
| AI | `#885BD6` |
| Business | `#F8E26C` |
| Research | `#2EBCB6` |
| Smart Cities | `#467CD9` |
| Finance | `#51E697` |
| Healthcare | `#BFE081` |
| Alert / Update / Conflict | `#F89570` |
| Special Insight | `#D463E6` |
| Background | `#171927` |

## 7. Backend Design

The backend should be a Python FastAPI application with modular services.

Recommended structure:

```text
backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── upload_routes.py
│   │   ├── document_routes.py
│   │   ├── graph_routes.py
│   │   ├── search_routes.py
│   │   └── taxonomy_routes.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── logging.py
│   ├── db/
│   │   ├── models.py
│   │   ├── session.py
│   │   └── migrations/
│   ├── services/
│   │   ├── file_service.py
│   │   ├── ingestion_service.py
│   │   ├── extraction_service.py
│   │   ├── classification_service.py
│   │   ├── embedding_service.py
│   │   ├── graph_service.py
│   │   └── version_service.py
│   └── workers/
│       └── ingestion_worker.py
└── tests/
```

## 8. File Ingestion Pipeline

Every uploaded file should pass through this flow:

```text
1. Receive file
2. Store original file
3. Calculate SHA-256 file hash
4. Check exact duplicate
5. Detect file type
6. Extract raw text or structured rows
7. Extract metadata
8. Split content into chunks
9. Generate summary
10. Extract concepts, entities, and keywords
11. Classify into area and subject
12. Generate embeddings
13. Create graph nodes
14. Create graph edges
15. Store processing result
16. Display result in dashboard
```

Supported extraction tools:

| File type | Suggested tool |
|---|---|
| PDF | PyMuPDF or pdfplumber |
| TXT | Python native read |
| MD | markdown/plain text parser |
| CSV | pandas |
| XLS/XLSX | pandas + openpyxl |

## 9. Knowledge Graph Model

The graph should be semantic and useful, not only visual.

### Node Types

```text
- Area
- Subject
- Document
- Document Version
- Chunk
- Concept
- Entity
- Person
- Organization
- Project
- Insight
- Alert
```

### Edge Types

```text
- BELONGS_TO
- CONTAINS
- MENTIONS
- SIMILAR_TO
- UPDATES
- DUPLICATES
- CONTRADICTS
- SUPPORTS
- DERIVED_FROM
- RELATED_TO
```

### Example

```text
Document: AI in Smart Cities PDF
    BELONGS_TO → Area: Smart Cities
    MENTIONS → Concept: AI governance
    MENTIONS → Concept: urban intelligence
    SIMILAR_TO → Document: AI urbanism paper
    DUPLICATES → Duplicate Smart Cities PDF
```

## 10. Database Schema v0.1

Recommended starting tables:

```text
users
knowledge_areas
subjects
documents
document_versions
chunks
concepts
entities
graph_nodes
graph_edges
ingestion_jobs
file_duplicates
```

### Core Tables

#### documents

```text
id
user_id
title
file_name
file_type
file_hash
storage_path
area_id
subject_id
status
created_at
updated_at
```

#### document_versions

```text
id
document_id
version_number
file_hash
summary
extracted_text_path
created_at
```

#### chunks

```text
id
document_version_id
chunk_index
content
embedding
metadata
created_at
```

#### graph_nodes

```text
id
node_type
label
color
size
metadata
created_at
```

#### graph_edges

```text
id
source_node_id
target_node_id
relationship_type
weight
metadata
created_at
```

#### ingestion_jobs

```text
id
document_id
status
current_step
error_message
started_at
finished_at
```

## 11. API Routes v0.1

Recommended API routes:

```text
POST   /api/files/upload
GET    /api/files
GET    /api/files/{document_id}
DELETE /api/files/{document_id}

GET    /api/documents/{document_id}/summary
GET    /api/documents/{document_id}/chunks
GET    /api/documents/{document_id}/versions

GET    /api/areas
POST   /api/areas
PATCH  /api/areas/{area_id}

GET    /api/subjects
POST   /api/subjects
PATCH  /api/subjects/{subject_id}

GET    /api/graph
GET    /api/graph/node/{node_id}
GET    /api/graph/document/{document_id}

POST   /api/search
POST   /api/ask

GET    /api/jobs
GET    /api/jobs/{job_id}
```

## 12. Update and Version Control Logic

The system should treat updates as a core feature.

### Exact Duplicate

If two files have the same SHA-256 hash:

```text
Status: exact_duplicate
Action: do not create new knowledge; link as duplicate evidence
```

### Possible Duplicate

If titles, filenames, or embeddings are highly similar:

```text
Status: possible_duplicate
Action: ask user whether it is a new version, duplicate, or separate document
```

### New Version

If a file is similar to an existing document but has a different hash:

```text
Status: possible_new_version
Action: create new document version after confirmation
```

### Knowledge Update

If a new document introduces concepts related to old content:

```text
Status: knowledge_update
Action: create graph edges between old and new concepts
```

## 13. AI Responsibilities

The AI layer should perform:

```text
- Summarization
- Area classification
- Subject classification
- Concept extraction
- Entity extraction
- Keyword generation
- Similarity explanation
- Duplicate/new-version recommendation
- Question answering over the knowledge base
```

The AI should not silently overwrite the user's taxonomy. It should suggest, and the user should be able to approve or correct.

## 14. Security and Privacy

Initial recommendation:

```text
- Local-first MVP
- Store original files locally
- Use environment variables for API keys
- Avoid exposing documents publicly
- Add authentication from the beginning
- Keep audit logs for uploads and reprocessing
```

Later enterprise version:

```text
- Workspace permissions
- Encrypted file storage
- Role-based access control
- Audit trail
- Cloud storage
- Organization-level taxonomy
```

## 15. First Coding Sprint

### Sprint Goal

Create the technical foundation: web app, backend API, upload pipeline, duplicate detection, and basic document registry.

### Sprint 1 Tasks

```text
1. Create monorepo structure
2. Create FastAPI backend
3. Create Next.js frontend
4. Create PostgreSQL connection
5. Create document database models
6. Build file upload endpoint
7. Store uploaded files locally
8. Calculate SHA-256 file hash
9. Detect exact duplicates
10. Create document list UI
11. Create basic dashboard layout
12. Apply brand colors
```

### Sprint 1 Acceptance Criteria

```text
- User can upload a PDF or CSV
- Backend stores the file
- Backend calculates file hash
- Backend detects exact duplicate files
- UI lists uploaded documents
- UI shows processing status
- UI uses Second Brain visual identity
```

## 16. Recommended First Repository Structure

```text
second-brain/
├── README.md
├── docker-compose.yml
├── .env.example
├── backend/
│   ├── app/
│   ├── tests/
│   ├── pyproject.toml
│   └── requirements.txt
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── package.json
│   └── tailwind.config.ts
├── storage/
│   ├── originals/
│   └── extracted/
└── docs/
    ├── system-design.md
    ├── graph-model.md
    └── ingestion-pipeline.md
```

## 17. Build Recommendation

Start with a local-first MVP using:

```text
FastAPI + PostgreSQL + pgvector + Next.js + Cytoscape.js
```

Avoid overengineering with Neo4j in the first build. PostgreSQL plus graph tables and pgvector is enough for the first prototype. Neo4j can be added later if the graph becomes too complex.

## 18. Immediate Next Step

The next step is to create the repository skeleton and implement Sprint 1.

Recommended first implementation order:

```text
1. Backend project foundation
2. Database models
3. Upload endpoint
4. Hash-based duplicate detection
5. Frontend dashboard shell
6. Document list UI
7. Basic graph placeholder
```
