import os
from typing import Optional

class Settings():
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://185.55.59.6:6379")
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD")
    REDIS_DB: int = int(os.getenv("REDIS_DB", 0))
    REDIS_MAX_CONNECTIONS: int = int(os.getenv("REDIS_MAX_CONNECTIONS", 10))
    
    
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_STRICT: bool = False 
    

    ENCRYPTION_KEY: Optional[str] = os.getenv("ENCRYPTION_KEY")
    CACHE_TTL: int = 3600 
    CACHE_ENABLED: bool = True
    CACHE_PREFIX: str = "avangard"
    
    
    class Config:
        env_file = ".env"

settings = Settings()