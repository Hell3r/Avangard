from fastapi import APIRouter
from src.api.v1.health import router as health_router
from src.api.v1.users import router as user_router
from src.api.v1.addresses import router as address_router
from src.api.v1.storage import router as storage_router
from src.api.v1.tasks import router as task_router
from src.api.v1.cache import router as cache_router


main_router = APIRouter()
main_router.include_router(health_router)
main_router.include_router(user_router)
main_router.include_router(address_router)
main_router.include_router(storage_router)
main_router.include_router(task_router)
main_router.include_router(cache_router)
