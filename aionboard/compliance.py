"""Versioned compliance-rules registry.

Each rule carries jurisdiction, industry, source URL, review date,
applicability conditions, required owner action, and escalation guidance.
These are reminders for the responsible operator — never legal
certification, competence determinations, or compliance guarantees.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from .crm import utcnow

RULES_VERSION = 1
REGISTRY_PATH = Path(__file__).resolve().parents[1] / "regulations" / "registry.json"


def load_registry() -> list[dict]:
    """Load the combined regulations registry. Single source of truth."""
    with open(REGISTRY_PATH, encoding="utf-8") as handle:
        data = json.load(handle)
    return data["rules"]


def _registry_as_seed() -> list[dict]:
    """Map registry entries onto the compliance_rules table schema."""
    seeds = []
    try:
        entries = load_registry()
    except (OSError, ValueError, KeyError):
        return list(SEED_RULES)
    for entry in entries:
        industries = entry.get("industries", [])
        seeds.append(
            {
                "rule_id": entry["id"],
                "jurisdiction": entry.get("jurisdiction", "UK"),
                "industry": ",".join(industries),
                "title": entry.get("law", ""),
                "detail": entry.get("detail", ""),
                "source_url": entry.get("source_url", ""),
                "review_date": entry.get("review_date", ""),
                "applies_when": entry.get("applies_when", ""),
                "owner_action": entry.get("owner_action", ""),
                "escalation": entry.get("escalation", ""),
            }
        )
    return seeds

# Seed rules. Review dates force re-verification; stale rules are errors.
SEED_RULES: tuple[dict[str, str], ...] = (
    {
        "rule_id": "MTD-ITSA-2026",
        "jurisdiction": "UK",
        "industry": "all",
        "title": "Making Tax Digital for Income Tax thresholds",
        "detail": "Digital records + quarterly updates: £50k+ from Apr 2026, £30k+ from Apr 2027, £20k+ from Apr 2028.",
        "source_url": "https://www.gov.uk/government/collections/making-tax-digital-for-income-tax-for-sole-traders-and-landlords-step-by-step",
        "review_date": "2026-09-23",
        "applies_when": "Sole trader or landlord above the qualifying-income threshold.",
        "owner_action": "Use compatible MTD software; do not rely on the assistant for filing.",
        "escalation": "Refer to accountant when thresholds or scope are unclear.",
    },
    {
        "rule_id": "VAT-90K",
        "jurisdiction": "UK",
        "industry": "all",
        "title": "VAT registration threshold",
        "detail": "Register at £90,000 taxable turnover over a rolling 12 months.",
        "source_url": "https://www.gov.uk/vat-registration-thresholds",
        "review_date": "2026-09-23",
        "applies_when": "Taxable turnover exceeds the threshold.",
        "owner_action": "Register and use MTD-compatible VAT software.",
        "escalation": "Refer to accountant for registration timing.",
    },
    {
        "rule_id": "HSE-HAIRDRESSING",
        "jurisdiction": "UK",
        "industry": "hair",
        "title": "Hairdressing dermatitis and respiratory risks",
        "detail": "HSE identifies dermatitis and respiratory risks from common hairdressing substances.",
        "source_url": "https://www.hse.gov.uk/hairdressing/",
        "review_date": "2026-09-23",
        "applies_when": "Colour, bleach, or chemical treatments are offered.",
        "owner_action": "Follow established patch-test and COSHH procedures.",
        "escalation": "Do not let the assistant certify procedures were followed.",
    },
    {
        "rule_id": "HSE-WORK-AT-HEIGHT",
        "jurisdiction": "UK",
        "industry": "gardeners-window-cleaners",
        "title": "Work at height planning and competence",
        "detail": "Avoid work at height where reasonably practicable; plan, competence, and equipment required.",
        "source_url": "https://www.hse.gov.uk/work-at-height/",
        "review_date": "2026-09-23",
        "applies_when": "Ladder or elevated window work is offered.",
        "owner_action": "Assess each job; the assistant must never declare a job safe.",
        "escalation": "Decline or refer jobs beyond competence and equipment.",
    },
    {
        "rule_id": "POLLUTION-WASHWATER",
        "jurisdiction": "UK",
        "industry": "car-detailers",
        "title": "Mobile washing wastewater disposal",
        "detail": "Prevent contaminated wastewater entering surface-water drains; arrangements vary and may need water-company permission.",
        "source_url": "https://www.gov.uk/guidance/pollution-prevention-for-businesses",
        "review_date": "2026-09-23",
        "applies_when": "Mobile washing with runoff is offered.",
        "owner_action": "Confirm disposal arrangement per job; keep it out of AI-verified claims.",
        "escalation": "Contact the relevant water company where required.",
    },
    {
        "rule_id": "PATCH-TEST-BEAUTY",
        "jurisdiction": "UK",
        "industry": "nails,lashes,hair,beauty",
        "title": "Patch-test and allergy records",
        "detail": "Patch tests and allergy records precede relevant colour and chemical treatments.",
        "source_url": "https://www.hse.gov.uk/hairdressing/",
        "review_date": "2026-09-23",
        "applies_when": "Colour, tint, peel, or chemical treatments are offered.",
        "owner_action": "Record patch-test date and result; block treatment without valid cover.",
        "escalation": "Refer reactions to medical help immediately.",
    },
)

# Activities that always enter the legal-review queue.
HIGH_RISK_ACTIVITIES = (
    "storing allergy records",
    "importing complete customer databases",
    "accessing bank accounts",
    "initiating payments",
    "recording calls",
    "deploying autonomous customer-facing voice agents",
)


def init_compliance_tables(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS compliance_rules (
            rule_id TEXT PRIMARY KEY,
            version INTEGER NOT NULL,
            jurisdiction TEXT NOT NULL,
            industry TEXT NOT NULL,
            title TEXT NOT NULL,
            detail TEXT NOT NULL,
            source_url TEXT NOT NULL,
            review_date TEXT NOT NULL,
            applies_when TEXT NOT NULL,
            owner_action TEXT NOT NULL,
            escalation TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS legal_review_queue (
            id INTEGER PRIMARY KEY,
            business_id TEXT NOT NULL,
            activity TEXT NOT NULL,
            reason TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'open',
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_legal_business ON legal_review_queue(business_id);
        """
    )
    for rule in _registry_as_seed():
        connection.execute(
            """
            INSERT INTO compliance_rules
            (rule_id, version, jurisdiction, industry, title, detail, source_url,
             review_date, applies_when, owner_action, escalation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(rule_id) DO UPDATE SET
                version=excluded.version, jurisdiction=excluded.jurisdiction,
                industry=excluded.industry, title=excluded.title, detail=excluded.detail,
                source_url=excluded.source_url, review_date=excluded.review_date,
                applies_when=excluded.applies_when, owner_action=excluded.owner_action,
                escalation=excluded.escalation
            """,
            (
                rule["rule_id"],
                RULES_VERSION,
                rule["jurisdiction"],
                rule["industry"],
                rule["title"],
                rule["detail"],
                rule["source_url"],
                rule["review_date"],
                rule["applies_when"],
                rule["owner_action"],
                rule["escalation"],
            ),
        )
    connection.commit()


def rules_for_industry(connection: sqlite3.Connection, industry: str) -> list[dict]:
    rows = connection.execute(
        "SELECT * FROM compliance_rules WHERE industry = 'all' OR industry LIKE ? ORDER BY rule_id",
        (f"%{industry.strip()}%",),
    ).fetchall()
    return [dict(row) for row in rows]


def queue_legal_review(
    connection: sqlite3.Connection, *, business_id: str, activity: str, reason: str = ""
) -> int:
    if not business_id.strip() or not activity.strip():
        raise ValueError("business_id and activity are required")
    cursor = connection.execute(
        "INSERT INTO legal_review_queue (business_id, activity, reason, created_at) VALUES (?, ?, ?, ?)",
        (business_id.strip(), activity.strip(), reason.strip(), utcnow()),
    )
    connection.commit()
    return int(cursor.lastrowid)


def needs_legal_review(activity: str) -> bool:
    lowered = activity.strip().lower()
    return any(high_risk in lowered for high_risk in HIGH_RISK_ACTIVITIES)


def stale_rules(connection: sqlite3.Connection, as_of: str) -> list[dict]:
    """Rules past their review date. Stale rules must be re-verified, not used."""
    rows = connection.execute(
        "SELECT * FROM compliance_rules WHERE review_date < ? ORDER BY review_date",
        (as_of,),
    ).fetchall()
    return [dict(row) for row in rows]
