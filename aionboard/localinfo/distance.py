"""Local distance math — no network, no keys, no rate limits.

Straight-line haversine KM between jobs for clustering a day's route.
Estimates, not navigation: drive time assumes urban ~30 km/h average.
For turn-by-turn routing the customer uses their own maps app.
"""

from __future__ import annotations

import math

_EARTH_KM = 6371.0
_URBAN_KMH = 30.0


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in KM, rounded to 1 decimal."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (math.sin(dphi / 2) ** 2
         + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2)
    return round(2 * _EARTH_KM * math.asin(math.sqrt(a)), 1)


def travel_estimate(km: float) -> dict:
    """Rough drive minutes + fuel note for a straight-line distance."""
    minutes = int(round(km / _URBAN_KMH * 60))
    return {"km": km, "drive_minutes": minutes,
            "note": "Estimate from straight-line distance at urban speeds. "
                    "Confirm with maps before promising arrival times."}


def cluster_by_proximity(jobs: list[dict], max_km: float = 8.0) -> list[list[dict]]:
    """Greedy single-link clustering of jobs by lat/lon.

    Each job: {"id": str, "latitude": float, "longitude": float}.
    Returns clusters (lists) — each cluster is roughly one van round.
    """
    remaining = list(jobs)
    clusters: list[list[dict]] = []
    while remaining:
        seed = remaining.pop(0)
        cluster = [seed]
        changed = True
        while changed:
            changed = False
            for job in list(remaining):
                if any(haversine_km(job["latitude"], job["longitude"],
                                    m["latitude"], m["longitude"]) <= max_km
                       for m in cluster):
                    cluster.append(job)
                    remaining.remove(job)
                    changed = True
        clusters.append(cluster)
    return clusters
