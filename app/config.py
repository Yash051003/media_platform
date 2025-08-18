from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    media_upload_path: str = "./uploads"
    max_file_size: int = 100000000  # 100MB
    allowed_extensions: List[str] = ["mp4", "avi", "mov", "mp3", "wav", "flac"]
    stream_url_expire_minutes: int = 10
    
    class Config:
        env_file = ".env"

settings = Settings()