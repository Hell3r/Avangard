from fastapi import FastAPI
from src.api import main_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import logging
from src.services.RedisService import redis_service
from dotenv import load_dotenv
import os, asyncio

# Import models to register them with SQLAlchemy Base
from src.models import UserModel, AddressModel, TaskModel, StorageModel

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


logging.getLogger('httpx').setLevel(logging.WARNING)
app = FastAPI()
app.include_router(main_router)

PUBLIC_ENDPOINTS = {
    "/v1/users/login",
    "/v1/users/user",
    "/v1/addresses",
    "/v1/addresses/{address_id}",
    "/v1/health",
    "/v1/health/db_check",
    "/v1/health/setup_db",
    "/docs",
    "/openapi.json",
    "/redoc",
}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Avangard API",
        version="1.0.0",
        description="API for Avangard project",
        routes=app.routes,
    )
    
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "v1/users/login",
                    "scopes": {}
                }
            }
        }
    }
    
    
    for path in openapi_schema["paths"]:

        is_public = path in PUBLIC_ENDPOINTS or any(path.startswith(p.rstrip('/')) for p in PUBLIC_ENDPOINTS if p.endswith('/'))
        
        if path.rstrip('/') in {p.rstrip('/') for p in PUBLIC_ENDPOINTS}:
            is_public = True
            
        for method in openapi_schema["paths"][path]:
            if is_public:
               
                openapi_schema["paths"][path][method].pop("security", None)
            else:
     
                openapi_schema["paths"][path][method]["security"] = [{"OAuth2PasswordBearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



async def initialize_redis():
    try:
        success = await redis_service.connect()
        if success:
            logger.info("✅ Redis successfully connected and cache enabled")
            
            test_result = await redis_service.set("health_check", {"status": "ok", "app": "Beatok"}, 60)
            if test_result:
                logger.info("✅ Redis cache test passed")
            else:
                logger.warning("⚠️ Redis cache test failed")
        else:
            logger.warning("⚠️ Redis connection failed - running without cache")
    except Exception as e:
        logger.warning(f"⚠️ Redis initialization error: {e} - running without cache")




@app.on_event("startup")
async def startup_event():
    await initialize_redis()
    logger.info(" Application started with background tasks")
    
    
    
    
@app.on_event("shutdown") 
async def shutdown_event():
    await redis_service.disconnect()
    logger.info(" Application shutdown")