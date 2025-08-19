from slowapi import Limiter
from slowapi.util import get_remote_address
from app.config import settings

# Initialize the Limiter and connect it to Redis using your settings.
# This single instance will be imported by both main.py and your routers.
limiter = Limiter(key_func=get_remote_address, storage_uri=settings.redis_url)