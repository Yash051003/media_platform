from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.responses import FileResponse # Import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.models import models
from app.routers import auth, media
from app.utils.security import verify_token
from app.config import settings
import os

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
    allow_origins=["*"],  # Configure appropriately for production
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
    """
    Serves the main signup.html page.
    """
    return "signup.html"

@app.get("/login", response_class=FileResponse)
def serve_login_page():
    """
    Serves the index.html page for logging in.
    """
    return "index.html"

@app.get("/dashboard", response_class=FileResponse)
def serve_dashboard_page():
    """
    Serves the main dashboard.html page for authenticated users.
    """
    return "dashboard.html"

# --- API Endpoints ---

@app.get("/stream/{media_id}")
def stream_media(
    media_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    """
    Stream media file with token-based access control.
    """
    try:
        payload = verify_token(token)
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    media = db.query(models.MediaAsset).filter(models.MediaAsset.id == media_id).first()
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")
    
    if not os.path.exists(media.file_url):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media file not found on server")
    
    return FileResponse(
        path=media.file_url,
        filename=f"{media.title}.{media.file_url.split('.')[-1]}",
        media_type="application/octet-stream"
    )

@app.get("/health")
def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)