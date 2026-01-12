from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Second Brain API"
    api_prefix: str = "/api"
    base_dir: Path = Path(__file__).resolve().parents[2]
    data_dir: Path = base_dir / "data"
    upload_dir: Path = base_dir / "uploads" / "originals"
    extracted_dir: Path = base_dir / "uploads" / "extracted"
    registry_path: Path = data_dir / "documents.json"
    allowed_extensions: set[str] = {".md", ".txt", ".csv", ".xls", ".xlsx", ".pdf"}
    max_upload_mb: int = 100
    text_excerpt_chars: int = 900


settings = Settings()
settings.data_dir.mkdir(parents=True, exist_ok=True)
settings.upload_dir.mkdir(parents=True, exist_ok=True)
settings.extracted_dir.mkdir(parents=True, exist_ok=True)
