"""Add-on catalog — services beyond the £20/£499 setups.

Each add-on is separately consented and separately priced. State machine
per customer: offered -> consented -> active. Nothing activates without
explicit consent recorded. Prices are proposed, not promises — confirm
at sale time.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

ADDONS: dict[str, dict] = {
    "lead_alerts": {
        "name": "Lead alerts",
        "price": "£29/mo",
        "description": "Weekly scored opportunity digest from planning, "
                       "procurement, and labour signals. Approval before "
                       "any contact.",
        "consent": "opportunity_alerts",
    },
    "security_check": {
        "name": "Security check (free)",
        "price": "£0 one-off",
        "description": "HTTPS, TLS expiry, and header check of your domain. "
                       "Free, no obligation.",
        "consent": "domain_check",
    },
    "security_report": {
        "name": "Security report",
        "price": "£49 one-off",
        "description": "Digest-pinned report with findings, fixes, and "
                       "assistant red-team results for your setup.",
        "consent": "domain_check",
    },
    "books_setup": {
        "name": "Books setup",
        "price": "£99 one-off",
        "description": "FreeAgent via your bank (free with NatWest/Mettle), "
                       "bank feed connected, turnover tracking on. Filing "
                       "stays with you.",
        "consent": "software_setup",
    },
    "custom_site": {
        "name": "Custom AI site",
        "price": "from £199 one-off",
        "description": "Personalised site: your services, areas, hours, "
                       "contact, plus your AI assistant with its own "
                       "identity. You own the domain.",
        "consent": "website_build",
    },
    "agent_identity": {
        "name": "Agent identity",
        "price": "£49 one-off",
        "description": "Name, personality, greeting, and appearance rules "
                       "for your assistant, everywhere it appears.",
        "consent": "branding",
    },
    "cloudflare_care": {
        "name": "Cloudflare care",
        "price": "£19/mo",
        "description": "We manage your DNS, bot protection, and access "
                       "rules. You keep domain ownership always.",
        "consent": "dns_management",
    },
    "muse_setup": {
        "name": "Muse setup",
        "price": "£79 one-off",
        "description": "Configure eligible Muse integrations when UK "
                       "access lands. Read-only first; gated writes only "
                       "with your approval.",
        "consent": "muse_integration",
    },
}

VALID_STATES = ("offered", "consented", "active", "cancelled")


def init_addon_tables(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS customer_addons (
            business_id TEXT NOT NULL,
            addon_id TEXT NOT NULL,
            state TEXT NOT NULL DEFAULT 'offered',
            consented_at TEXT,
            activated_at TEXT,
            PRIMARY KEY (business_id, addon_id)
        );
        """
    )
    connection.commit()


def offer_addon(connection: sqlite3.Connection, business_id: str,
                addon_id: str) -> dict:
    """Mark an add-on offered. Unknown IDs rejected."""
    if addon_id not in ADDONS:
        return {"error": f"unknown addon: {addon_id}"}
    connection.execute(
        "INSERT OR IGNORE INTO customer_addons (business_id, addon_id) "
        "VALUES (?, ?)", (business_id, addon_id))
    connection.commit()
    return {"business_id": business_id, "addon_id": addon_id,
            "state": "offered"}


def consent_addon(connection: sqlite3.Connection, business_id: str,
                  addon_id: str) -> dict:
    """Record explicit consent. Required before activation."""
    if addon_id not in ADDONS:
        return {"error": f"unknown addon: {addon_id}"}
    now = datetime.now(timezone.utc).isoformat()
    connection.execute(
        "INSERT INTO customer_addons (business_id, addon_id, state, "
        "consented_at) VALUES (?, ?, 'consented', ?) "
        "ON CONFLICT(business_id, addon_id) DO UPDATE SET "
        "state='consented', consented_at=excluded.consented_at",
        (business_id, addon_id, now))
    connection.commit()
    return {"business_id": business_id, "addon_id": addon_id,
            "state": "consented",
            "consent": ADDONS[addon_id]["consent"]}


def activate_addon(connection: sqlite3.Connection, business_id: str,
                   addon_id: str) -> dict:
    """Activate. Refuses without recorded consent."""
    row = connection.execute(
        "SELECT state FROM customer_addons WHERE business_id=? AND addon_id=?",
        (business_id, addon_id)).fetchone()
    if row is None or row[0] != "consented":
        return {"error": "consent required before activation",
                "business_id": business_id, "addon_id": addon_id}
    now = datetime.now(timezone.utc).isoformat()
    connection.execute(
        "UPDATE customer_addons SET state='active', activated_at=? "
        "WHERE business_id=? AND addon_id=?",
        (now, business_id, addon_id))
    connection.commit()
    return {"business_id": business_id, "addon_id": addon_id,
            "state": "active"}


def active_addons(connection: sqlite3.Connection,
                  business_id: str) -> list[str]:
    """Add-on IDs currently active for a business."""
    rows = connection.execute(
        "SELECT addon_id FROM customer_addons "
        "WHERE business_id=? AND state='active'",
        (business_id,)).fetchall()
    return [r[0] for r in rows]
