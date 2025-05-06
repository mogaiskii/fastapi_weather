from datetime import datetime, time, timedelta

import aiohttp
import pytz

from services.exceptions import ServiceException
from settings import settings


async def get_default_forecast():
    return await get_forecast(settings.DEFAULT_LAT, settings.DEFAULT_LON)


async def get_forecast(lat: float, lon: float):
    timeseries = await _get_forecast_timeseries(lat, lon)
    requested_datetime = _get_default_local_time()
    result = _calculate_forecast(requested_datetime, timeseries)

    return result


def _get_default_local_time():
    local_tz = pytz.timezone(settings.DEFAULT_TZ)
    today = datetime.now(local_tz).date()
    return local_tz.localize(datetime.combine(today, time(14, 0)))


def _convert_iso_to_default_local(iso_time_str: str):
    dt_utc = datetime.strptime(iso_time_str, "%Y-%m-%dT%H:%M:%SZ")  # we(I) expect api to always be in UTC
    dt_utc = pytz.utc.localize(dt_utc)

    cet = pytz.timezone(settings.DEFAULT_TZ)
    return dt_utc.astimezone(cet)


async def _get_forecast_timeseries(lat, lon):
    # it belongs here in case they will change api slightly,
    # like adding headers, adding more query params, or just bumping the version
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/complete?lat={lat}&lon={lon}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise ServiceException()

            data = await response.json()
            timeseries = data["properties"]["timeseries"]
            return timeseries


def _get_entry_temperature(entry: dict):
    return entry["data"]["instant"]["details"]["air_temperature"]


def _linear_prediction(last_datetime, last_temperature, current_datetime, current_temperature, requested_datetime):
    total_seconds = (current_datetime - last_datetime).total_seconds()
    elapsed_seconds = (requested_datetime - last_datetime).total_seconds()

    interpolated = last_temperature + (current_temperature - last_temperature) * (elapsed_seconds / total_seconds)
    return round(interpolated, 2)


# modularity makes it more testable
def _calculate_forecast(requested_datetime, timeseries: list[dict]):
    last_entry = None
    result = []  # expected to be [{"time": iso_datetime, "temperature": float max 2 digits after the point}]
    for entry in timeseries:
        entry_datetime = _convert_iso_to_default_local(entry["time"])

        if entry_datetime == requested_datetime:
            result.append({"date": str(requested_datetime), "value": _get_entry_temperature(entry)})
            requested_datetime += timedelta(days=1)

        elif entry_datetime > requested_datetime and last_entry is not None:
            entry_temperature = _get_entry_temperature(entry)
            last_temperature = _get_entry_temperature(last_entry)
            last_datetime = _convert_iso_to_default_local(last_entry["time"])
            predicted_temperature = _linear_prediction(
                last_datetime, last_temperature, entry_datetime, entry_temperature, requested_datetime
            )

            result.append({"date": str(requested_datetime), "value": predicted_temperature})
            requested_datetime += timedelta(days=1)

        # requested datetime has already passed today
        elif entry_datetime > requested_datetime and (entry_datetime - requested_datetime) <= timedelta(hours=6):
            result.append({"date": str(entry_datetime), "value": _get_entry_temperature(entry)})
            requested_datetime += timedelta(days=1)

        elif entry_datetime > requested_datetime:
            requested_datetime += timedelta(days=1)

        last_entry = entry

    # could be the case for discussion. I personally would just omit that
    # If there is no forecast from vendor, there is no forecast from us
    # last_dt = _convert_iso_to_default_local(last_entry["time"])
    # if last_dt < requested_datetime:
    #     result.append({"date": str(requested_datetime), "value": None})

    return result
