"""Daylight via sunrise-sunset.org (free, no key). How many jobs fit today."""

from __future__ import annotations

import urllib.parse

from ._http import get_json


def daylight_hours(latitude: float, longitude: float, day: str = "",
                   timeout: int = 15) -> dict:
    """Sunrise, sunset, day length for a date (default today).

    Outdoor trades use this to size the working day; schedulers use it
    to stop booking evening jobs in December.
    """
    qs = urllib.parse.urlencode(
        {"lat": latitude, "lng": longitude, "formatted": 0, **({"date": day} if day else {})})
    data = get_json(f"https://api.sunrise-sunset.org/json?{qs}", timeout)
    r = data.get("results", {})
    seconds = r.get("day_length") or 0
    return {
        "date": day or "today",
        "sunrise": r.get("sunrise", ""),
        "sunset": r.get("sunset", ""),
        "daylight_hours": round(seconds / 3600, 1),
    }
