from uuid import UUID
from pathlib import Path

UPLOAD_DIR = Path("backend/user_uploads")  # or wherever you want, configurable

def save_user_upload(file_bytes: bytes, original_filename: str) -> Path:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    ext = Path(original_filename).suffix
    unique_name = f"{UUID().hex}{ext}"
    save_path = UPLOAD_DIR / unique_name
    with open(save_path, "wb") as f:
        f.write(file_bytes)
    return save_path 