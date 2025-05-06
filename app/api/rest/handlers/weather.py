import logging

from fastapi import HTTPException

from api.rest import rest_app
from services.exceptions import ServiceException
from services.weather import get_default_forecast


logger = logging.getLogger(__name__)


@rest_app.get("/weather")
async def weather():
    try:
        weather_data = await get_default_forecast()
    except ServiceException:
        logger.error("Weather service failed", exc_info=True, stack_info=True)
        raise HTTPException(500)
    except Exception:
        logger.error("Internal weather calculation exception", exc_info=True, stack_info=True)
        raise
    else:
        return weather_data
