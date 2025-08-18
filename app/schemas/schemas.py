from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# A new, simple schema for the owner details
class MediaOwnerResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

# Auth Schemas
class AdminUserCreate(BaseModel):
    email: EmailStr
    password: str

class AdminUserLogin(BaseModel):
    email: EmailStr
    password: str

class AdminUserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Media Schemas
class MediaAssetCreate(BaseModel):
    title: str
    type: str

class MediaAssetResponse(BaseModel):
    id: int
    title: str
    type: str
    file_url: str
    created_at: datetime
    # --- THIS IS THE KEY CHANGE ---
    # Include the owner's details in the response
    owner: MediaOwnerResponse
    
    class Config:
        from_attributes = True

class StreamUrlResponse(BaseModel):
    stream_url: str
    expires_at: datetime