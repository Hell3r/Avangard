from pydantic import BaseModel, Field
from typing import Optional


class AddressBase(BaseModel):
    name: str = Field(..., description="Название адреса")


class AddressCreate(AddressBase):
    pass


class Address(AddressBase):
    id: int

    class Config:
        from_attributes = True

