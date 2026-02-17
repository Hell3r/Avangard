from fastapi import APIRouter, HTTPException, status, Depends
from src.database.deps import SessionDep
from src.schemas.addresses import Address, AddressCreate
from src.dependencies.services import AddressServiceDep
from typing import List


router = APIRouter(prefix="/v1/addresses", tags=["Адреса"])


@router.post("", response_model=Address, status_code=status.HTTP_201_CREATED, summary="Создание адреса")
async def create_address(
    service: AddressServiceDep,
    address_data: AddressCreate
):
    return await service.create(address_data)


@router.get("/{address_id}", response_model=Address, summary="Получить адрес по ID")
async def get_address(
    service: AddressServiceDep,
    address_id: int
):
    address = await service.get_by_id(address_id)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Адрес не найден"
        )
    return address


@router.get("", response_model=List[Address], summary="Получить все адреса")
async def get_addresses(
    service: AddressServiceDep,
    skip: int = 0,
    limit: int = 100
):
    return await service.get_all(skip=skip, limit=limit)


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить адрес")
async def delete_address(
    service: AddressServiceDep,
    address_id: int
):
    deleted = await service.delete(address_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Адрес не найден"
        )

