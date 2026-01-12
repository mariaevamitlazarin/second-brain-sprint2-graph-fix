import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from app.core.config import settings
from app.models.document import DocumentRecord


class DocumentRegistry:
    def __init__(self, path: Path = settings.registry_path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write([])

    def _read(self) -> List[Dict]:
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []

    def _write(self, records: List[Dict]) -> None:
        self.path.write_text(
            json.dumps(records, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )

    def all(self) -> List[DocumentRecord]:
        return [DocumentRecord.model_validate(item) for item in self._read()]

    def get(self, document_id: str) -> Optional[DocumentRecord]:
        for record in self.all():
            if record.id == document_id:
                return record
        return None

    def find_by_hash(self, sha256: str) -> Optional[DocumentRecord]:
        for record in self.all():
            if record.sha256 == sha256 and record.duplicate_of is None:
                return record
        return None

    def add(self, document: DocumentRecord) -> DocumentRecord:
        records = self._read()
        records.append(document.model_dump(mode="json"))
        self._write(records)
        return document

    def update(self, document: DocumentRecord) -> DocumentRecord:
        records = self._read()
        updated = False
        document.updated_at = datetime.utcnow()

        for index, item in enumerate(records):
            if item.get("id") == document.id:
                records[index] = document.model_dump(mode="json")
                updated = True
                break

        if not updated:
            records.append(document.model_dump(mode="json"))

        self._write(records)
        return document


registry = DocumentRegistry()
