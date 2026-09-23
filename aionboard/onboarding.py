"""Configurable onboarding engine.

Packages combine a shared core checklist with vertical-specific tasks.
Completion (onboarded) is separate from aftercare (support window).
"""

from __future__ import annotations

import sqlite3

from .crm import utcnow

PACKAGES = {
    "standard-ai-setup": {
        "price_gbp": 499,
        "support_days": 14,
        "description": "Full assisted setup for 2-10 person businesses.",
    },
    "muse-quickstart": {
        "price_gbp": 20,
        "support_days": 7,
        "description": "Tightly standardised assisted onboarding for sole traders.",
    },
}

CORE_TASKS = (
    "discovery",
    "email_authorization",
    "calendar_authorization",
    "owner_message_approval",
    "training",
    "handover",
)

# Vertical-specific tasks layered on top of the core checklist.
VERTICAL_TASKS: dict[str, tuple[str, ...]] = {
    "electrician": (
        "enquiry_workflow",
        "price_book_approval",
        "quote_draft",
        "owner_quote_approval",
        "scheduling_proposal",
        "google_profile_assistance",
        "fourteen_day_fixes",
    ),
    "nails": (
        "booking_workflow",
        "service_menu_approval",
        "deposit_reminder_preparation",
        "rebooking_workflow",
        "google_profile_assistance",
        "fourteen_day_fixes",
    ),
    "lashes": (
        "booking_workflow",
        "treatment_menu_approval",
        "patch_test_workflow",
        "deposit_reminder_preparation",
        "rebooking_workflow",
        "google_profile_assistance",
        "fourteen_day_fixes",
    ),
    "hair": (
        "booking_workflow",
        "service_area_profile",
        "service_menu_approval",
        "deposit_reminder_preparation",
        "portfolio_organization",
        "rebooking_workflow",
        "google_profile_assistance",
        "fourteen_day_fixes",
    ),
    "cleaners": (
        "recurring_scheduling_workflow",
        "service_menu_approval",
        "quote_follow_up_preparation",
        "owner_message_approval",
        "payment_reminder_preparation",
        "customer_management_organization",
        "google_profile_assistance",
        "fourteen_day_fixes",
    ),
    "dog-groomers": (
        "booking_workflow",
        "service_menu_approval",
        "pet_record_organization",
        "deposit_reminder_preparation",
        "waiting_list_workflow",
        "google_profile_assistance",
        "fourteen_day_fixes",
    ),
}

# Three underlying recipes; verticals map to the closest one.
RECIPES = {
    "appointment-led-beauty": ("nails", "lashes", "hair", "beauty"),
    "recurring-local-services": ("cleaners", "dog-groomers", "gardeners-window-cleaners"),
    "enquiry-led-mobile-services": ("electrician", "car-detailers", "driving-instructors", "weddings"),
}


def recipe_for(vertical: str) -> str:
    for recipe, verticals in RECIPES.items():
        if vertical in verticals:
            return recipe
    raise ValueError(f"no recipe for vertical: {vertical}")


def tasks_for(vertical: str) -> tuple[str, ...]:
    """Shared core plus vertical overlay. No electrician tasks leak into nails."""
    overlay = VERTICAL_TASKS.get(vertical)
    if overlay is None:
        raise ValueError(f"no task overlay for vertical: {vertical}")
    seen: list[str] = []
    for task in CORE_TASKS + overlay:
        if task not in seen:
            seen.append(task)
    return tuple(seen)


def create_onboarding(
    connection: sqlite3.Connection,
    *,
    business_id: str,
    vertical: str,
    package: str,
) -> int:
    """Create an onboarding run. Package determines price and support window."""
    if package not in PACKAGES:
        raise ValueError(f"unsupported package: {package}")
    tasks_for(vertical)  # validates vertical support
    if not business_id.strip():
        raise ValueError("business_id is required")

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS onboardings (
            id INTEGER PRIMARY KEY,
            business_id TEXT NOT NULL,
            vertical TEXT NOT NULL,
            package TEXT NOT NULL,
            support_ends_at TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS onboarding_tasks (
            id INTEGER PRIMARY KEY,
            onboarding_id INTEGER NOT NULL REFERENCES onboardings(id) ON DELETE CASCADE,
            task TEXT NOT NULL,
            owner TEXT NOT NULL DEFAULT '',
            authorization TEXT NOT NULL DEFAULT '',
            action TEXT NOT NULL DEFAULT '',
            verification TEXT NOT NULL DEFAULT '',
            evidence TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'not_started',
            updated_at TEXT NOT NULL,
            UNIQUE(onboarding_id, task)
        )
        """
    )
    cursor = connection.execute(
        "INSERT INTO onboardings (business_id, vertical, package, support_ends_at, created_at) VALUES (?, ?, ?, ?, ?)",
        (business_id.strip(), vertical, package, "", utcnow()),
    )
    onboarding_id = int(cursor.lastrowid)
    now = utcnow()
    for task in tasks_for(vertical):
        connection.execute(
            "INSERT INTO onboarding_tasks (onboarding_id, task, status, updated_at) VALUES (?, ?, 'not_started', ?)",
            (onboarding_id, task, now),
        )
    connection.commit()
    return onboarding_id


def set_onboarding_task(
    connection: sqlite3.Connection,
    *,
    onboarding_id: int,
    task: str,
    status: str,
    owner: str = "",
    authorization: str = "",
    action: str = "",
    verification: str = "",
    evidence: str = "",
) -> None:
    """Advance an onboarding task. Same evidence rules as installs."""
    row = connection.execute(
        "SELECT id FROM onboardings WHERE id = ?", (onboarding_id,)
    ).fetchone()
    if row is None:
        raise ValueError("unknown onboarding")

    from .installs import STATUSES, OWNER_TYPES

    if task not in tasks_for(
        get_onboarding(connection, onboarding_id)["onboarding"]["vertical"]
    ):
        raise ValueError(f"task not in package for this vertical: {task}")
    if status not in STATUSES:
        raise ValueError(f"unknown status: {status}")
    owner = owner.strip()
    authorization = authorization.strip()
    action = action.strip()
    verification = verification.strip()
    evidence = evidence.strip()
    if status in {"in_progress", "blocked", "verified"}:
        if not owner or owner not in OWNER_TYPES:
            raise ValueError("valid owner is required")
        if not authorization or not action:
            raise ValueError("authorization and action are required")
    if status == "verified" and not (verification and evidence):
        raise ValueError("verification and evidence are required")

    cursor = connection.execute(
        """
        UPDATE onboarding_tasks
        SET owner = ?, authorization = ?, action = ?, verification = ?,
            evidence = ?, status = ?, updated_at = ?
        WHERE onboarding_id = ? AND task = ?
        """,
        (owner, authorization, action, verification, evidence, status, utcnow(), onboarding_id, task),
    )
    if cursor.rowcount == 0:
        raise ValueError("unknown onboarding task")
    connection.commit()


def get_onboarding(connection: sqlite3.Connection, onboarding_id: int) -> dict:
    row = connection.execute(
        "SELECT * FROM onboardings WHERE id = ?", (onboarding_id,)
    ).fetchone()
    if row is None:
        raise ValueError("unknown onboarding")
    tasks = connection.execute(
        "SELECT * FROM onboarding_tasks WHERE onboarding_id = ? ORDER BY task",
        (onboarding_id,),
    ).fetchall()
    return {"onboarding": dict(row), "tasks": [dict(t) for t in tasks]}


def is_onboarded(connection: sqlite3.Connection, onboarding_id: int) -> bool:
    """Onboarded when every task is verified. Support window is separate."""
    state = get_onboarding(connection, onboarding_id)
    expected = set(tasks_for(state["onboarding"]["vertical"]))
    actual = {t["task"]: t["status"] for t in state["tasks"]}
    return expected == set(actual.keys()) and all(
        actual[t] == "verified" for t in expected
    )


def support_active(connection: sqlite3.Connection, onboarding_id: int, support_ends_at: str) -> bool:
    """Aftercare window check. Kept separate from completion."""
    connection.execute(
        "UPDATE onboardings SET support_ends_at = ? WHERE id = ?",
        (support_ends_at, onboarding_id),
    )
    connection.commit()
    state = get_onboarding(connection, onboarding_id)
    ends = state["onboarding"]["support_ends_at"]
    if not ends:
        return False
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat() < ends
