import redis
import json
import logging
from typing import Optional, Any
from datetime import timedelta  # Import timedelta
from app.config import settings

logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self):
        self.redis_client = None
        self._connect()
    
    def _connect(self):
        """Initialize Redis connection with fallback for development"""
        try:
            self.redis_client = redis.from_url(
                settings.redis_url,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            self.redis_client.ping()
            logger.info("Redis connection established")
        except redis.RedisError as e:
            logger.warning(f"Redis connection failed: {e}. Caching disabled.")
            self.redis_client = None
        except Exception as e:
            logger.warning(f"Unexpected Redis error: {e}. Caching disabled.")
            self.redis_client = None
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from Redis cache"""
        if not self.redis_client:
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
        except (redis.RedisError, json.JSONDecodeError) as e:
            logger.error(f"Error getting cache key {key}: {e}")
        
        return None
    
    def set(self, key: str, value: Any, expire_minutes: Optional[int] = None) -> bool:
        """Set value in Redis cache"""
        if not self.redis_client:
            return False
        
        try:
            expire_time_minutes = expire_minutes or settings.cache_expire_minutes
            serialized_value = json.dumps(value, default=str)
            
            # --- THIS IS THE FIX ---
            # setex expects a timedelta object or an integer in seconds.
            # We'll use timedelta for clarity.
            self.redis_client.setex(
                key, 
                timedelta(minutes=expire_time_minutes),
                serialized_value
            )
            return True
        except (redis.RedisError, TypeError) as e: # Use TypeError for JSON encoding errors
            logger.error(f"Error setting cache key {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from Redis cache"""
        if not self.redis_client:
            return False
        
        try:
            self.redis_client.delete(key)
            return True
        except redis.RedisError as e:
            logger.error(f"Error deleting cache key {key}: {e}")
            return False
    
    def is_connected(self) -> bool:
        """Check if Redis is connected"""
        return self.redis_client is not None

# Global Redis client instance
redis_client = RedisClient()
