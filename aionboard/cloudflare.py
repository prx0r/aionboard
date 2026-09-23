"""Cloudflare onboarding tracker — per-business runbook state.

We manage customer domains from Cloudflare: DNS, bot protection
(Turnstile), and access rules. The customer keeps domain ownership
always — we operate as a delegated manager, revocable any time.

This module tracks onboarding state only. Live Cloudflare API calls
happen with a per-customer token the customer provides (or our partner
token with their written consent). No calls fire from state transitions
alone — each step records who did what, when.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

STEPS = ("dns", "turnstile", "access_rules", "analytics")


def init_cloudflare_tables(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS cloudflare_onboarding (
            business_id TEXT NOT NULL,
            step TEXT NOT NULL,
            state TEXT NOT NULL DEFAULT 'pending',
            detail TEXT NOT NULL DEFAULT '',
            updated_at TEXT NOT NULL,
            PRIMARY KEY (business_id, step)
        );
        """
    )
    connection.commit()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def set_step(connection: sqlite3.Connection, business_id: str,
             step: str, state: str, detail: str = "") -> dict:
    """Record a step transition. States: pending, in_progress, done, blocked."""
    if step not in STEPS:
        return {"error": f"unknown step: {step}. Known: {list(STEPS)}"}
    if state not in ("pending", "in_progress", "done", "blocked"):
        return {"error": f"unknown state: {state}"}
    connection.execute(
        "INSERT INTO cloudflare_onboarding (business_id, step, state, "
        "detail, updated_at) VALUES (?, ?, ?, ?, ?) "
        "ON CONFLICT(business_id, step) DO UPDATE SET state=excluded.state, "
        "detail=excluded.detail, updated_at=excluded.updated_at",
        (business_id, step, state, detail, _now()))
    connection.commit()
    return {"business_id": business_id, "step": step, "state": state}


def status(connection: sqlite3.Connection, business_id: str) -> dict:
    """Full onboarding state for a business."""
    rows = connection.execute(
        "SELECT step, state, detail, updated_at FROM cloudflare_onboarding "
        "WHERE business_id=?", (business_id,)).fetchall()
    have = {r[0]: {"state": r[1], "detail": r[2], "updated_at": r[3]}
            for r in rows}
    steps = {s: have.get(s, {"state": "pending", "detail": "",
                             "updated_at": ""}) for s in STEPS}
    done = sum(1 for s in steps.values() if s["state"] == "done")
    return {"business_id": business_id, "steps": steps,
            "complete": done == len(STEPS),
            "ownership_note": "Domain ownership stays with the customer. "
                              "Revoke our access any time."}
