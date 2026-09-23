"""UK postcode lookup via postcodes.io (free, no key)."""

from __future__ import annotations

from ._http import get_json


def postcode_lookup(postcode: str, timeout: int = 15) -> dict:
    """Validate a postcode; return area, coords, region, admin areas.

    Raises RuntimeError when invalid or unreachable.
    """
    code = postcode.strip().replace(" ", "")
    data = get_json(
        f"https://api.postcodes.io/postcodes/{code}", timeout)
    if not isinstance(data, dict) or data.get("status") != 200:
        raise RuntimeError(f"postcode not found: {postcode}")
    r = data["result"]
    return {
        "postcode": r.get("postcode", ""),
        "outward_code": outward_code(postcode),
        "latitude": r.get("latitude"),
        "longitude": r.get("longitude"),
        "region": r.get("region", ""),
        "admin_district": r.get("admin_district", ""),
        "parliamentary_constituency": r.get("parliamentary_constituency", ""),
        "country": r.get("country", ""),
    }


def outward_code(postcode: str) -> str:
    """Outward code (M14 from M14 5TQ). Local, no network."""
    return postcode.strip().upper().split()[0] if postcode.strip() else ""
