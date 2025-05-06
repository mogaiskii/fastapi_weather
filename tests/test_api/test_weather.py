import pytest


@pytest.mark.asyncio
async def test_weather_smoke(test_app):
    response = test_app.get("/rest/weather")
    assert response.status_code == 200
