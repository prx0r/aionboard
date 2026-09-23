"""Shared HTTP helper for free JSON APIs. Timeouts, UA, no keys."""

from __future__ import annotations

import json
import urllib.request


def get_json(url: str, timeout: int = 15) -> dict | list:
    """GET a JSON endpoint. Raises RuntimeError with a short message."""
    req = urllib.request.Request(
        url, method="GET",
        headers={"User-Agent": "aionboard-localinfo/1.0",
                 "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"GET {url}: HTTP {e.code}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"GET {url}: {e.reason}") from e
