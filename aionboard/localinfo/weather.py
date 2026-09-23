"""Weather via Open-Meteo (free, no key). Outdoor-work planning."""

from __future__ import annotations

import urllib.parse

from ._http import get_json


def weather_forecast(latitude: float, longitude: float, days: int = 7,
                     timeout: int = 15) -> list[dict]:
    """Daily max temp + rain probability. For go/no-go outdoor decisions."""
    days = max(1, min(16, int(days)))
    qs = urllib.parse.urlencode({
        "latitude": latitude, "longitude": longitude,
        "daily": "temperature_2m_max,precipitation_probability_max",
        "timezone": "Europe/London", "forecast_days": days,
    })
    data = get_json(f"https://api.open-meteo.com/v1/forecast?{qs}", timeout)
    daily = data.get("daily", {})
    out = []
    for day, temp, rain in zip(daily.get("time", []),
                               daily.get("temperature_2m_max", []),
                               daily.get("precipitation_probability_max", [])):
        out.append({"date": day, "temp_max_c": temp, "rain_prob_pct": rain})
    return out


def rain_risk_days(latitude: float, longitude: float,
                   threshold_pct: int = 50, days: int = 7,
                   timeout: int = 15) -> list[dict]:
    """Days where rain probability meets/exceeds threshold. Reschedule these."""
    return [d for d in weather_forecast(latitude, longitude, days, timeout)
            if (d["rain_prob_pct"] or 0) >= threshold_pct]
