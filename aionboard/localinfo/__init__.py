"""Free local-intelligence services for sole traders, via MCP.

Everything here is free, no API key, stdlib only. Each lookup is a
read tool (no approval needed) that answers a question a trade business
actually asks: where is this job, is that day a holiday, will it rain,
how much daylight do I have, which jobs cluster together.

Sources: postcodes.io, gov.uk bank-holidays.json, Open-Meteo,
sunrise-sunset.org, plus local haversine math (no network).
Respect rate limits: postcodes.io and sunrise-sunset are shared free
services — cache aggressively, never hammer.
"""

from .daylight import daylight_hours
from .distance import cluster_by_proximity, haversine_km, travel_estimate
from .holidays import bank_holidays, is_bank_holiday, next_holiday
from .postcodes import outward_code, postcode_lookup
from .weather import rain_risk_days, weather_forecast

__all__ = [
    "daylight_hours",
    "cluster_by_proximity",
    "haversine_km",
    "travel_estimate",
    "bank_holidays",
    "is_bank_holiday",
    "next_holiday",
    "outward_code",
    "postcode_lookup",
    "rain_risk_days",
    "weather_forecast",
]
