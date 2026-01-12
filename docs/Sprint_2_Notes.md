# Sprint 2 Notes — Text Extraction and First Graph API

## Objective

Add the first intelligence layer after upload and duplicate detection.

## Implemented modules

1. File text extraction
2. Metadata extraction
3. Basic summary generation
4. Basic keyword extraction
5. Extracted text storage
6. Graph API generation
7. Frontend graph visualization placeholder

## Extraction engines

| File type | Engine |
|---|---|
| PDF | pypdf |
| TXT / MD | Python text reader |
| CSV | Python csv |
| XLSX | openpyxl |
| XLS | xlrd |

## Graph model

Nodes:

- Second Brain
- Area
- Subject
- Document
- File type
- Keyword

Edges:

- HAS_AREA
- HAS_SUBJECT
- CONTAINS_DOCUMENT
- HAS_FILE_TYPE
- MENTIONS_KEYWORD
- DUPLICATE_OF

## Next sprint recommendation

Sprint 3 should add:

1. Chunking
2. Embeddings
3. Vector search
4. LLM summary/classification
5. Ask My Brain endpoint
6. PostgreSQL/pgvector preparation
