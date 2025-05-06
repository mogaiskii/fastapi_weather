import pytest


@pytest.mark.asyncio
async def test_healthcheck(test_app):
    response = test_app.get(f"/rest/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OK"
