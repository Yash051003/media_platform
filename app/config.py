from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    database_url: str
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Media settings
    media_upload_path: str = "./uploads"
    max_file_size: int = 100000000  # 100MB
    allowed_extensions: List[str] = ["mp4", "avi", "mov", "mp3", "wav", "flac"]
    stream_url_expire_minutes: int = 10
    
    # Redis settings
    redis_url: str = "redis://localhost:6379"
    cache_expire_minutes: int = 30
    
    # Rate limiting settings
    rate_limit_per_minute: int = 10
    rate_limit_burst: int = 20
    
    # Environment
    environment: str = "development"
    
    class Config:
        env_file = ".env"

settings = Settings()