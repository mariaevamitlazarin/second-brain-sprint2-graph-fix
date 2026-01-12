import uuid
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.models.document import (
    DocumentListResponse,
    DocumentRecord,
    DocumentStatus,
    DocumentTextResponse,
    ReprocessResponse,
    UploadResponse,
)
from app.services.extraction import process_document, read_extracted_text
from app.services.file_service import calculate_sha256, save_upload_file, validate_extension
from app.services.registry import registry

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("", response_model=DocumentListResponse)
def list_documents() -> DocumentListResponse:
    documents = sorted(registry.all(), key=lambda item: item.created_at, reverse=True)
    return DocumentListResponse(total=len(documents), documents=documents)


@router.get("/{document_id}", response_model=DocumentRecord)
def get_document(document_id: str) -> DocumentRecord:
    document = registry.get(document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found.")
    return document


@router.get("/{document_id}/text", response_model=DocumentTextResponse)
def get_document_text(document_id: str) -> DocumentTextResponse:
    document = registry.get(document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found.")

    text = read_extracted_text(document)
    if not text:
        raise HTTPException(
            status_code=404,
            detail="No extracted text found. Process or reprocess the document first.",
        )

    return DocumentTextResponse(
        document_id=document.id,
        original_filename=document.original_filename,
        text=text,
        metadata=document.extraction_metadata,
    )


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    area: Optional[str] = Form(default=None),
    subject: Optional[str] = Form(default=None),
    source: Optional[str] = Form(default=None),
) -> UploadResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename.")

    extension = validate_extension(file.filename)
    sha256, size_bytes = calculate_sha256(file.file)
    existing = registry.find_by_hash(sha256)

    if existing:
        duplicate_record = DocumentRecord(
            id=str(uuid.uuid4()),
            original_filename=file.filename,
            stored_filename=None,
            file_extension=extension,
            mime_type=file.content_type,
            size_bytes=size_bytes,
            sha256=sha256,
            area=area or existing.area,
            subject=subject or existing.subject,
            source=source,
            status=DocumentStatus.duplicate,
            duplicate_of=existing.id,
            summary=f"Exact duplicate of {existing.original_filename}",
        )
        registry.add(duplicate_record)
        return UploadResponse(
            document=duplicate_record,
            is_duplicate=True,
            message=f"Exact duplicate detected. Original document: {existing.original_filename}",
        )

    stored_filename, stored_size = await save_upload_file(file, sha256)
    document = DocumentRecord(
        id=str(uuid.uuid4()),
        original_filename=file.filename,
        stored_filename=stored_filename,
        file_extension=extension,
        mime_type=file.content_type,
        size_bytes=stored_size,
        sha256=sha256,
        area=area,
        subject=subject,
        source=source,
        status=DocumentStatus.uploaded,
    )
    registry.add(document)

    processed_document = process_document(document)
    message = "File uploaded, registered, and processed successfully."
    if processed_document.status == DocumentStatus.failed:
        message = "File uploaded and registered, but text extraction failed."

    return UploadResponse(
        document=processed_document,
        is_duplicate=False,
        message=message,
    )


@router.post("/{document_id}/reprocess", response_model=ReprocessResponse)
def reprocess_document(document_id: str) -> ReprocessResponse:
    document = registry.get(document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found.")

    processed_document = process_document(document)

    if processed_document.status == DocumentStatus.failed:
        return ReprocessResponse(
            document_id=document_id,
            status="failed",
            message=processed_document.extraction_error or "Document processing failed.",
        )

    return ReprocessResponse(
        document_id=document_id,
        status=processed_document.status,
        message="Document processed. Extracted text, metadata, summary, keywords, and graph-ready data are available.",
    )
