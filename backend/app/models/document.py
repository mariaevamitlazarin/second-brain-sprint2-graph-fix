from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class DocumentStatus(str, Enum):
    uploaded = "uploaded"
    duplicate = "duplicate"
    processing = "processing"
    processed = "processed"
    failed = "failed"


class ExtractionMetadata(BaseModel):
    text_length: int = 0
    word_count: int = 0
    page_count: Optional[int] = None
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    sheet_names: List[str] = Field(default_factory=list)
    extraction_engine: Optional[str] = None


class DocumentRecord(BaseModel):
    id: str
    original_filename: str
    stored_filename: Optional[str] = None
    file_extension: str
    mime_type: Optional[str] = None
    size_bytes: int
    sha256: str
    area: Optional[str] = None
    subject: Optional[str] = None
    source: Optional[str] = None
    status: DocumentStatus = DocumentStatus.uploaded
    duplicate_of: Optional[str] = None
    extracted_text_path: Optional[str] = None
    text_excerpt: Optional[str] = None
    summary: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    extraction_metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)
    extraction_error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UploadResponse(BaseModel):
    document: DocumentRecord
    is_duplicate: bool
    message: str


class DocumentListResponse(BaseModel):
    total: int
    documents: List[DocumentRecord]


class ReprocessResponse(BaseModel):
    document_id: str
    status: str
    message: str


class DocumentTextResponse(BaseModel):
    document_id: str
    original_filename: str
    text: str
    metadata: ExtractionMetadata


class GraphNode(BaseModel):
    id: str
    type: str
    label: str
    color: str
    size: int = 18
    metadata: Dict = Field(default_factory=dict)


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    relationship_type: str
    weight: float = 1.0


class GraphResponse(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]
