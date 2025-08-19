from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.models import models
from app.routers import auth, media
from app.utils.security import verify_token
from app.config import settings
import os
import mimetypes # Import the mimetypes library

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Media Platform API",
    description="A secure media platform backend with JWT authentication and streaming capabilities",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router)
app.include_router(media.router)

# --- Frontend Serving Endpoints ---
@app.get("/", response_class=FileResponse)
def serve_signup_page():
    return "signup.html"

@app.get("/login", response_class=FileResponse)
def serve_login_page():
    return "index.html"

@app.get("/dashboard", response_class=FileResponse)
def serve_dashboard_page():
    return "dashboard.html"

# --- API Endpoints ---
@app.get("/stream/{media_id}")
def stream_media(
    media_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    """
    Stream media file with token-based access control and the correct media type.
    """
    payload = verify_token(token)
    if (
        payload is None or
        payload.get("type") != "stream" or
        payload.get("media_id") != media_id
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired stream token"
        )
    
    media = db.query(models.MediaAsset).filter(models.MediaAsset.id == media_id).first()
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")
    
    if not os.path.exists(media.file_url):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media file not found on server")
    
    # --- THIS IS THE FIX ---
    # Guess the correct MIME type from the file's path
    media_type, _ = mimetypes.guess_type(media.file_url)
    if media_type is None:
        # Default to a generic stream if the type can't be determined
        media_type = "application/octet-stream"
    
    return FileResponse(
        path=media.file_url,
        media_type=media_type # Use the guessed media type for proper streaming
    )

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.models import models
from app.routers import auth, media
from app.utils.security import verify_token
from app.config import settings
import os
import mimetypes

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Media Platform API",
    description="A secure media platform backend with JWT authentication and streaming capabilities",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router)
app.include_router(media.router)

# --- Frontend Serving Endpoints ---

@app.get("/", response_class=FileResponse)
def serve_signup_page():
    """Serves the main signup.html page for users."""
    return "signup.html"

@app.get("/login", response_class=FileResponse)
def serve_login_page():
    """Serves the index.html page for user login."""
    return "index.html"

@app.get("/dashboard", response_class=FileResponse)
def serve_dashboard_page():
    """Serves the main dashboard.html page for authenticated users."""
    return "dashboard.html"

# --- NEW ADMIN ROUTES ---

@app.get("/admin/login", response_class=FileResponse)
def serve_admin_login_page():
    """Serves the admin_login.html page."""
    return "admin_login.html"

@app.get("/admin/dashboard", response_class=FileResponse)
def serve_admin_dashboard_page():
    """Serves the admin_dashboard.html page."""
    return "admin_dashboard.html"


# --- API Endpoints ---

@app.get("/stream/{media_id}")
def stream_media(
    media_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    """
    Stream media file with token-based access control and the correct media type.
    """
    payload = verify_token(token)
    if (
        payload is None or
        payload.get("type") != "stream" or
        payload.get("media_id") != media_id
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired stream token"
        )
    
    media = db.query(models.MediaAsset).filter(models.MediaAsset.id == media_id).first()
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")
    
    if not os.path.exists(media.file_url):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media file not found on server")
    
    media_type, _ = mimetypes.guess_type(media.file_url)
    if media_type is None:
        media_type = "application/octet-stream"
    
    return FileResponse(
        path=media.file_url,
        media_type=media_type
    )

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)