from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request, Form
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta
from typing import List
import os
import uuid
from app.database import get_db
from app.schemas.schemas import MediaAssetResponse, StreamUrlResponse
from app.models.models import MediaAsset, AdminUser
from app.utils.auth import get_current_user
from app.utils.security import create_access_token
from app.config import settings

router = APIRouter(prefix="/media", tags=["media"])

# Helper functions remain the same
def is_allowed_file_type(filename: str) -> bool:
    if '.' not in filename: return False
    return filename.rsplit('.', 1)[1].lower() in settings.allowed_extensions

def get_media_type(filename: str) -> str:
    if '.' not in filename: return "unknown"
    ext = filename.rsplit('.', 1)[1].lower()
    if ext in ['mp4', 'avi', 'mov', 'mkv', 'wmv']: return "video"
    if ext in ['mp3', 'wav', 'flac', 'aac', 'm4a']: return "audio"
    return "unknown"

@router.post("/", response_model=MediaAssetResponse, status_code=status.HTTP_201_CREATED)
async def upload_media(
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    # File validation logic...
    if not is_allowed_file_type(file.filename):
        raise HTTPException(status_code=400, detail="File type not allowed.")
    
    # File saving logic...
    os.makedirs(settings.media_upload_path, exist_ok=True)
    file_extension = file.filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(settings.media_upload_path, unique_filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # --- THIS IS THE KEY CHANGE ---
    # Create the MediaAsset and link it to the current user
    media_asset = MediaAsset(
        title=title,
        type=get_media_type(file.filename),
        file_url=file_path,
        owner_id=current_user.id  # Associate the file with the logged-in user
    )
    
    db.add(media_asset)
    db.commit()
    db.refresh(media_asset)
    
    return media_asset

@router.get("/", response_model=List[MediaAssetResponse])
def list_media(db: Session = Depends(get_db), current_user: AdminUser = Depends(get_current_user)):
    """
    List all media assets, eagerly loading the owner's information.
    """
    # Use joinedload to efficiently fetch the owner along with the media asset
    media_assets = db.query(MediaAsset).options(joinedload(MediaAsset.owner)).all()
    return media_assets

# get_stream_url endpoint remains the same
@router.get("/{media_id}/stream-url", response_model=StreamUrlResponse)
def get_stream_url(media_id: int, request: Request, db: Session = Depends(get_db)):
    media = db.query(MediaAsset).filter(MediaAsset.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    
    expires_delta = timedelta(minutes=settings.stream_url_expire_minutes)
    stream_token = create_access_token(
        data={"media_id": media.id, "type": "stream"}, expires_delta=expires_delta
    )
    base_url = str(request.base_url).rstrip('/')
    stream_url = f"{base_url}/stream/{media.id}?token={stream_token}"
    
    return {"stream_url": stream_url, "expires_at": datetime.utcnow() + expires_delta}