"""Onboard buddy: a free per-business assistant.

Each onboarded business gets its own graph — vertical knowledge plus their
configured workflows, stack, and install state. The buddy answers from that
graph only, with citations. It is scoped to one business: it can never see
another customer's data.

Positioning: the buddy is not a Muse competitor. Muse is Meta's general
agent for everything. The buddy knows one business deeply — its services,
prices, workflows, and rules — and nothing else. Free with setup, because
every conversation teaches us what to improve.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from .graph import _tokens

REPO_ROOT = Path(__file__).resolve().parents[1]
VERTICALS_ROOT = REPO_ROOT / "verticals"

STOPWORDS = {
    "what", "how", "does", "do", "is", "are", "the", "a", "an",
    "to", "for", "my", "i", "it", "of", "in", "on", "me",
}


def build_business_graph(
    connection: sqlite3.Connection, business_id: str, vertical: str
) -> dict:
    """Compose one business's graph: vertical knowledge + their state.

    Reads (never writes): business record, install/onboarding state,
    stack inventory, and the vertical pack. Everything returned is
    scoped to this business_id.
    """
    business_id = business_id.strip()
    if not business_id:
        raise ValueError("business_id is required")

    try:
        business = connection.execute(
            "SELECT * FROM businesses WHERE business_id = ?", (business_id,)
        ).fetchone()
    except sqlite3.OperationalError:
        business = None
    if business is None:
        # Installs created before businesses existed still get a graph;
        # the business record is looked up best-effort.
        business_record: dict = {"business_id": business_id, "display_name": business_id}
    else:
        business_record = dict(business)

    with open(VERTICALS_ROOT / vertical / "profile.json", encoding="utf-8") as handle:
        profile = json.load(handle)

    stack: list[dict] = []
    company_number = (business_record.get("company_number") or "").strip()
    if company_number:
        try:
            rows = connection.execute(
                "SELECT tool, category, verdict, access, verified FROM stack_items "
                "WHERE company_number = ?",
                (company_number,),
            ).fetchall()
            stack = [dict(row) for row in rows]
        except sqlite3.OperationalError:
            stack = []

    installs: list[dict] = []
    try:
        rows = connection.execute(
            "SELECT task, status, verification FROM onboarding_tasks "
            "WHERE onboarding_id IN (SELECT id FROM onboardings WHERE business_id = ?)",
            (business_id,),
        ).fetchall()
        installs = [dict(row) for row in rows]
    except sqlite3.OperationalError:
        installs = []

    return {
        "business_id": business_id,
        "business": business_record,
        "vertical": vertical,
        "profile": profile,
        "stack": stack,
        "installs": installs,
    }


def buddy_ask(business_graph: dict, question: str, limit: int = 5) -> list[dict]:
    """Scoped retrieval over one business's graph. Never crosses tenants.

    Searches the vertical's pains, stack, workflows, and the business's
    own configured state. Returns cited nodes or nothing.
    """
    query = _tokens(question or "") - STOPWORDS
    if not query:
        return []
    candidates = []
    profile = business_graph["profile"]
    for mapping in profile.get("pain_mappings", []):
        text = f"{mapping['pain_id']} {mapping['pain_name']} {mapping['category']} {' '.join(mapping['service'].split())}"
        candidates.append(
            {
                "kind": "pain",
                "id": mapping["pain_id"],
                "text": f"{mapping['pain_name']} ({mapping['category']}).",
                "source": f"verticals/{business_graph['vertical']}/profile.json",
                "_tokens": _tokens(text),
            }
        )
    for tool in profile.get("current_stack", []):
        text = f"{tool['tool']} {tool['category']} {tool['use']}"
        candidates.append(
            {
                "kind": "tool",
                "id": tool["tool"],
                "text": f"{tool['tool']} ({tool['category']}): {tool['use']}.",
                "source": f"verticals/{business_graph['vertical']}/profile.json",
                "_tokens": _tokens(text),
            }
        )
    for item in business_graph.get("stack", []):
        text = f"{item['tool']} {item.get('category', '')} {item.get('verdict', '')}"
        candidates.append(
            {
                "kind": "configured-tool",
                "id": item["tool"],
                "text": f"Your {item['tool']} is recorded as {item.get('verdict', 'tracked')}.",
                "source": "your installation record",
                "_tokens": _tokens(text),
            }
        )
    for task in business_graph.get("installs", []):
        text = f"{task['task']} {task['status']}"
        candidates.append(
            {
                "kind": "install-state",
                "id": task["task"],
                "text": f"Your {task['task']} is {task['status']}.",
                "source": "your installation record",
                "_tokens": _tokens(text),
            }
        )

    scored = []
    for candidate in candidates:
        overlap = query & candidate.pop("_tokens")
        if overlap:
            scored.append((len(overlap), candidate["id"], candidate))
    scored.sort(key=lambda item: (-item[0], item[1]))
    seen: set[str] = set()
    results = []
    for _, _, candidate in scored[:limit]:
        key = (candidate["kind"], candidate["id"])
        if key not in seen:
            seen.add(key)
            results.append(candidate)
    return results


def buddy_answer(results: list[dict], business_name: str) -> str:
    """Render scoped results. Admits ignorance; never invents."""
    if not results:
        return (
            f"I don't have verified information on that for {business_name} yet. "
            "Ask about your services, bookings, deposits, reminders, or reviews — "
            "or ask your installer to add it."
        )
    lines = [f"For {business_name}, here's what I know:"]
    for result in results:
        lines.append(f"- [{result['kind']}] {result['text']} (source: {result['source']})")
    lines.append("I can't send messages, move money, or change bookings — your owner approves those.")
    return "\n".join(lines)
