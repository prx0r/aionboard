"""powuk signal bridge — file-level import, no DB coupling.

Reads powuk's normalized JSONL output (data/normalized/<source>/...)
and shapes records for aionboard's opportunity matcher
(opportunities.score_opportunity / match_for_business).

powuk owns collection. aionboard owns matching. This file only translates.
If powuk changes layout, only this module changes.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

POWUK_BASE = Path(os.environ.get("POWUK_BASE", "/home/ubuntu/powuk"))

# powuk source -> how to extract matchable text from its records
TEXT_FIELDS: dict[str, tuple[str, ...]] = {
    "planning_apps": ("description", "summary", "title", "proposal"),
    "contracts_finder": ("title", "description", "summary"),
    "find_tender": ("title", "description", "summary"),
    "ons_labour": ("title", "summary", "description"),
    "ch_capacity": ("company_name", "sic_description", "summary"),
}


def _latest_jsonl(source: str, base: Path = POWUK_BASE) -> Path | None:
    """Newest .jsonl file for a source, or None when absent."""
    root = base / "data" / "normalized" / source
    if not root.exists():
        return None
    files = sorted(root.rglob("*.jsonl"))
    return files[-1] if files else None


def load_powuk_signals(
    sources: tuple[str, ...] = ("planning_apps", "contracts_finder"),
    limit_per_source: int = 500,
    base: Path | None = None,
) -> list[dict]:
    """Load recent records from powuk sources as opportunity dicts.

    Each dict carries title/description/summary plus provenance
    (_source, _observed_file). Empty list when powuk has no data —
    callers must handle absence, never invent signals.

    NOTE: base defaults to None (resolved to POWUK_BASE at call time),
    never to POWUK_BASE directly — a def-time default would freeze the
    path and silently ignore test fixtures and env overrides.
    """
    base = base or POWUK_BASE
    out: list[dict] = []
    for source in sources:
        path = _latest_jsonl(source, base)
        if path is None:
            continue
        fields = TEXT_FIELDS.get(source, ("title", "description", "summary"))
        with open(path) as f:
            for i, line in enumerate(f):
                if i >= limit_per_source:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                text = " ".join(str(rec.get(k, "")) for k in fields)
                out.append({
                    "title": str(rec.get("title", rec.get("description", "")))[:200],
                    "description": text[:2000],
                    "summary": str(rec.get("summary", ""))[:500],
                    "_source": f"powuk/{source}",
                    "_observed_file": str(path),
                })
    return out


def opportunities_for_target(
    profile,
    limit_per_source: int = 500,
    top_n: int = 5,
    base: Path | None = None,
) -> list[dict]:
    """Score powuk signals for a target profile. Highest first."""
    from ..opportunities import match_for_business

    signals = load_powuk_signals(limit_per_source=limit_per_source, base=base)
    if not signals or not profile.vertical or not profile.postcode:
        return []
    matched = match_for_business(
        business_postcode=profile.postcode,
        vertical=profile.vertical,
        opportunities=signals,
    )
    return matched[:top_n]
