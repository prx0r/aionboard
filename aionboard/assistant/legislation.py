"""Legislation lookup for targets.

Reads regulations/registry.json. Rules carry review_date — entries past
their review date are stale and must be re-verified before use, never
silently trusted (registry's own review policy).
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

REGISTRY = Path(__file__).parent.parent.parent / "regulations" / "registry.json"


def _load_rules(registry_path: Path | str = REGISTRY) -> list[dict]:
    with open(registry_path) as f:
        return json.load(f).get("rules", [])


def is_stale(rule: dict, today: str | None = None) -> bool:
    """True when the rule is past its review_date."""
    review = rule.get("review_date", "")
    if not review:
        return True
    today = today or date.today().isoformat()
    return review < today


def rules_for_target(
    vertical: str,
    topic: str = "",
    registry_path: Path | str = REGISTRY,
    include_stale: bool = False,
) -> list[dict]:
    """Rules applying to a vertical, optionally filtered by topic.

    Matches when the vertical appears in the rule's industries, or when
    the topic appears in the law/detail text. Stale rules are excluded
    unless explicitly requested (and flagged when returned).
    """
    topic = topic.lower()
    out = []
    for rule in _load_rules(registry_path):
        industries = [i.lower() for i in rule.get("industries", [])]
        if vertical.lower() not in industries:
            continue
        if topic:
            hay = f"{rule.get('law', '')} {rule.get('detail', '')}".lower()
            if topic not in hay:
                continue
        stale = is_stale(rule)
        if stale and not include_stale:
            continue
        out.append({**rule, "stale": stale})
    return out


def cite(rule: dict) -> str:
    """One-line citation for agent/user display."""
    return f"{rule.get('id', '?')}: {rule.get('law', '')} — {rule.get('citation', '')}".strip(" —")
