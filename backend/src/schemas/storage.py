from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class StorageBase(BaseModel):
    material_name: str = Field(..., min_length=1, max_length=200, description="Название материала")
    description: Optional[str] = Field(None, max_length=500, description="Описание")
    remainder: int = Field(..., ge=0, description="Остаток на складе")


class StorageCreate(StorageBase):
    pass


class StorageUpdate(BaseModel):
    material_name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=500)
    remainder: Optional[int] = Field(None, ge=0)


class StorageWithdraw(BaseModel):
    storage_id: int
    quantity: int = Field(..., gt=0, description="Количество к списанию со склада")
    note: Optional[str] = Field(None, max_length=500)


class Storage(StorageBase):
    id: int

    class Config:
        from_attributes = True

