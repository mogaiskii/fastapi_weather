from datetime import datetime

import pytz

from services.weather import _calculate_forecast  # noqa


def test_calculate_forecast(load_test_json_data):
    cet = pytz.timezone("Europe/Belgrade")
    cet_dt = cet.localize(datetime(2025, 5, 6, 14, 0))

    timeseries = load_test_json_data("test_weather_data.json")
    forecast = _calculate_forecast(cet_dt, timeseries)
    assert forecast
    assert forecast == [
        {'date': '2025-05-06 17:00:00+02:00', 'value': 99.9},  # it is already 5pm on the clock, earliest we can get
        {'date': '2025-05-07 14:00:00+02:00', 'value': 99.8},  # just normal situation
        {'date': '2025-05-08 14:00:00+02:00', 'value': 30.0},  # interpolation
        # last day forecast ends too early, no forecast for 2pm for this one
    ]

