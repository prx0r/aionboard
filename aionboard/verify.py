"""Booking-link verification.

A configuration screenshot never proves a customer can book. This checker
fetches the approved booking link and confirms it resolves, returns HTTP
200, and presents the expected services. The fetcher is injectable so
tests never touch the network.
"""

from __future__ import annotations

import urllib.request
from datetime import datetime, timezone
from typing import Callable
from urllib.parse import urlparse


def _default_fetch(url: str, timeout_seconds: int = 15) -> tuple[int, str]:
    request = urllib.request.Request(
        url, headers={"User-Agent": "AIOnboardLinkCheck/1.0"}
    )
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        body = response.read().decode("utf-8", errors="replace")
        return int(response.status), body


def verify_booking_link(
    url: str,
    expected_services: list[str],
    *,
    fetcher: Callable[[str, int], tuple[int, str]] | None = None,
    timeout_seconds: int = 15,
) -> dict:
    """Verify a booking link resolves and shows the expected services.

    Returns an evidence record, never a bare boolean. Failures name the
    exact cause so the installer knows what to fix.
    """
    cleaned = (url or "").strip()
    if not cleaned:
        return _failure(url, "empty URL")
    parsed = urlparse(cleaned)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return _failure(url, "not an absolute http(s) URL")

    fetch = fetcher or _default_fetch
    try:
        status, body = fetch(cleaned, timeout_seconds)
    except Exception as exc:
        return _failure(url, f"fetch failed: {type(exc).__name__}: {exc}")

    if status != 200:
        return _failure(url, f"HTTP {status}, expected 200")

    lowered = body.lower()
    missing = [s for s in expected_services if s.lower() not in lowered]
    if missing:
        return _failure(url, f"services not found on page: {', '.join(missing)}")

    return {
        "url": cleaned,
        "verified": True,
        "status": 200,
        "services_found": list(expected_services),
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }


def _failure(url: str, reason: str) -> dict:
    return {
        "url": url,
        "verified": False,
        "reason": reason,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
