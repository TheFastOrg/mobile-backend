import pytest


@pytest.mark.anyio
async def test_api_health_check_status(client):
    response = await client.get("/status")
    assert response.status_code == 200
