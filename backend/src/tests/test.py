import pytest
from httpx import AsyncClient
from fastapi import status

from app.main import app


@pytest.mark.asyncio
async def test_create_task_success(
    async_client: AsyncClient,
    admin_token_headers: dict
):
    task_payload = {
        "title": "Тестовая задача",
        "description": "Описание тестовой задачи",
        "status": "В работе",
        "due_at": "2026-05-20T12:00:00"
    }

    response = await async_client.post(
        "/tasks/",
        json=task_payload,
        headers=admin_token_headers
    )

    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data["title"] == task_payload["title"]
    assert response_data["description"] == task_payload["description"]
    assert "id" in response_data
    assert response_data["id"] is not None