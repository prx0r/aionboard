"""Bank holidays via gov.uk (free, no key). Surcharge days + availability."""

from __future__ import annotations

from datetime import date

from ._http import get_json

DIVISIONS = ("england-and-wales", "scotland", "northern-ireland")


def bank_holidays(division: str = "england-and-wales",
                  timeout: int = 15) -> list[dict]:
    """All bank holiday events for a division: [{title, date}]."""
    if division not in DIVISIONS:
        raise ValueError(f"unknown division: {division}. Known: {DIVISIONS}")
    data = get_json("https://www.gov.uk/bank-holidays.json", timeout)
    events = data.get(division, {}).get("events", [])
    return [{"title": e.get("title", ""), "date": e.get("date", "")}
            for e in events if e.get("date")]


def is_bank_holiday(day: str, division: str = "england-and-wales",
                    timeout: int = 15) -> dict:
    """Is YYYY-MM-DD a bank holiday? For surcharge/availability logic."""
    for e in bank_holidays(division, timeout):
        if e["date"] == day:
            return {"is_holiday": True, "title": e["title"], "date": day}
    return {"is_holiday": False, "title": "", "date": day}


def next_holiday(from_day: str | None = None,
                 division: str = "england-and-wales",
                 timeout: int = 15) -> dict:
    """Next bank holiday on or after a date (default today)."""
    from_day = from_day or date.today().isoformat()
    upcoming = [e for e in bank_holidays(division, timeout)
                if e["date"] >= from_day]
    if not upcoming:
        return {"title": "", "date": ""}
    return min(upcoming, key=lambda e: e["date"])
