import hashlib
import re
from pathlib import Path
from typing import BinaryIO

from fastapi import HTTPException, UploadFile

from app.core.config import settings


_SAFE_NAME_PATTERN = re.compile(r"[^a-zA-Z0-9._-]+")


def sanitize_filename(filename: str) -> str:
    clean = _SAFE_NAME_PATTERN.sub("_", filename.strip())
    return clean[:180] or "uploaded_file"


def validate_extension(filename: str) -> str:
    extension = Path(filename).suffix.lower()
    if extension not in settings.allowed_extensions:
        allowed = ", ".join(sorted(settings.allowed_extensions))
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{extension}'. Allowed types: {allowed}.",
        )
    return extension


def calculate_sha256(file_obj: BinaryIO) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0

    while chunk := file_obj.read(1024 * 1024):
        size += len(chunk)
        digest.update(chunk)

    file_obj.seek(0)
    return digest.hexdigest(), size


async def save_upload_file(upload_file: UploadFile, sha256: str) -> tuple[str, int]:
    validate_extension(upload_file.filename or "")

    safe_name = sanitize_filename(upload_file.filename or "uploaded_file")
    stored_filename = f"{sha256[:16]}_{safe_name}"
    destination = settings.upload_dir / stored_filename

    size = 0
    max_bytes = settings.max_upload_mb * 1024 * 1024

    with destination.open("wb") as output:
        while chunk := await upload_file.read(1024 * 1024):
            size += len(chunk)
            if size > max_bytes:
                destination.unlink(missing_ok=True)
                raise HTTPException(
                    status_code=413,
                    detail=f"File exceeds max upload size of {settings.max_upload_mb} MB.",
                )
            output.write(chunk)

    await upload_file.seek(0)
    return stored_filename, size
