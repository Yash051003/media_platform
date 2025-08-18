import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.database import Base, get_db

# --- DATABASE SETUP FOR TESTING ---
SQLALCHEMY_DATABASE_URL = "postgresql://dev_user:dev_password123@localhost:5432/media_platform_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the 'get_db' dependency for the tests
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# --- PYTEST FIXTURE FOR THE TEST CLIENT ---
@pytest.fixture(scope="session")
def client():
    """
    A fixture that sets up the database before any tests run,
    and tears it down after all tests are done.
    """
    # Create all tables in the test database
    Base.metadata.create_all(bind=engine)
    
    # Yield a TestClient instance
    with TestClient(app) as c:
        yield c
        
    # Drop all tables after the tests are finished
    Base.metadata.drop_all(bind=engine)