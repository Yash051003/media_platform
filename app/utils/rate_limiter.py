from fastapi import Request
from fastapi.responses import JSONResponse

class RateLimitExceeded(Exception):
    """Custom exception for when a rate limit is exceeded."""
    def __init__(self, message: str = "Rate limit exceeded"):
        self.message = message
        super().__init__(self.message)

async def _rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """
    Handles the RateLimitExceeded exception and returns a 429 response.
    """
    return JSONResponse(
        status_code=429,
        content={"detail": exc.message},
    )