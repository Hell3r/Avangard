from fastapi import APIRouter, HTTPException, status, Depends, Response, Request, BackgroundTasks
import logging



logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/health")

@router.get('', tags = ["Проверка Бэкенда"], 
            summary= "Проверить работу API",
            status_code= status.HTTP_200_OK)
async def get_health():
    return {"message": "OK"}




