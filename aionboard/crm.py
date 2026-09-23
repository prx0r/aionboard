"""Private prospect CRM with provenance and contact controls.

The CRM is intentionally local SQLite. Research records are never marketing
permission by themselves.
"""

from __future__ import annotations

import re
import sqlite3
from datetime import datetime, timezone
from typing import Iterable, Mapping, MutableMapping

SCHEMA_VERSION = 1
ALLOWED_CHANNELS = {"phone", "email", "linkedin"}
ALLOWED_OUTCOMES = {
    "interested",
    "not_interested",
    "no_answer",
    "callback",
    "do_not_contact",
}
ALLOWED_TPS_LISTS = {"TPS", "CTPS", "INTERNAL"}
ALLOWED_TPS_RESULTS = {"clear", "blocked", "unknown"}
POSTCODE_OUTWARD_PATTERN = re.compile(r"^[A-Z]{1,2}\d{1,2}[A-Z]?$")
POSTCODE_INWARD_PATTERN = re.compile(r"^(.+?)([0-9][A-Z]{2})$")


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def connect(db_path: str = ":memory:") -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    init_db(connection)
    return connection


def init_db(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS prospects (
            id INTEGER PRIMARY KEY,
            company_number TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            postcode TEXT NOT NULL,
            region TEXT NOT NULL,
            sic_codes TEXT NOT NULL,
            status TEXT NOT NULL,
            cluster TEXT NOT NULL,
            source TEXT NOT NULL,
            source_path TEXT NOT NULL,
            imported_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY,
            company_number TEXT NOT NULL REFERENCES prospects(company_number) ON DELETE CASCADE,
            channel TEXT NOT NULL,
            detail TEXT NOT NULL,
            verified INTEGER NOT NULL DEFAULT 0,
            permission TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS contact_attempts (
            id INTEGER PRIMARY KEY,
            contact_id INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
            company_number TEXT NOT NULL REFERENCES prospects(company_number) ON DELETE CASCADE,
            channel TEXT NOT NULL,
            outcome TEXT NOT NULL,
            notes TEXT NOT NULL DEFAULT '',
            attempted_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS tps_checks (
            id INTEGER PRIMARY KEY,
            company_number TEXT NOT NULL REFERENCES prospects(company_number) ON DELETE CASCADE,
            checked_at TEXT NOT NULL,
            list_name TEXT NOT NULL,
            result TEXT NOT NULL,
            notes TEXT NOT NULL DEFAULT ''
        );

        CREATE INDEX IF NOT EXISTS idx_contacts_company ON contacts(company_number);
        CREATE INDEX IF NOT EXISTS idx_attempts_company ON contact_attempts(company_number);
        CREATE INDEX IF NOT EXISTS idx_tps_company ON tps_checks(company_number);
        """
    )
    connection.commit()


def parse_region(postcode: str | None) -> str:
    """Derive a UK outward-code area without claiming it is verified."""
    if postcode is None:
        return ""
    text = str(postcode).strip().upper()
    if not text:
        return ""
    compact = text.replace(" ", "")
    inward_match = POSTCODE_INWARD_PATTERN.match(compact)
    if inward_match and POSTCODE_OUTWARD_PATTERN.match(inward_match.group(1)):
        return inward_match.group(1)
    outward = text.split()[0]
    if POSTCODE_OUTWARD_PATTERN.match(outward):
        return outward
    return ""


def normalize_sic_codes(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        codes = [part.strip() for part in value.split(",")]
    elif isinstance(value, (list, tuple)):
        codes = [str(part).strip() for part in value]
    else:
        codes = [str(value).strip()]
    return ",".join(code for code in codes if code)


def import_prospects(
    connection: sqlite3.Connection,
    rows: Iterable[Mapping[str, object]],
    *,
    source: str,
    source_path: str,
) -> dict[str, int]:
    """Import research prospects without creating marketing permission."""
    if not source.strip():
        raise ValueError("source is required")
    if not source_path.strip():
        raise ValueError("source_path is required")

    stats = {"imported": 0, "updated": 0, "skipped": 0}
    for row in rows:
        company_number = str(row.get("company_number", "")).strip().upper()
        name = str(row.get("name", "")).strip()
        postcode = str(row.get("postcode", "")).strip()
        status = str(row.get("status", "")).strip()
        cluster = str(row.get("cluster", "")).strip()
        sic_codes = normalize_sic_codes(row.get("sic_codes"))
        region_value = row.get("region")
        region = str(region_value).strip().upper() if region_value else parse_region(postcode)

        if not all([company_number, name, postcode, region, sic_codes, status, cluster]):
            stats["skipped"] += 1
            continue

        now = utcnow()
        existing = connection.execute(
            "SELECT id FROM prospects WHERE company_number = ?",
            (company_number,),
        ).fetchone()
        if existing is None:
            connection.execute(
                """
                INSERT INTO prospects
                (company_number, name, postcode, region, sic_codes, status, cluster,
                 source, source_path, imported_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    company_number,
                    name,
                    postcode,
                    region,
                    sic_codes,
                    status,
                    cluster,
                    source,
                    source_path,
                    now,
                    now,
                ),
            )
            stats["imported"] += 1
        else:
            connection.execute(
                """
                UPDATE prospects
                SET name = ?, postcode = ?, region = ?, sic_codes = ?, status = ?,
                    cluster = ?, source = ?, source_path = ?, updated_at = ?
                WHERE company_number = ?
                """,
                (
                    name,
                    postcode,
                    region,
                    sic_codes,
                    status,
                    cluster,
                    source,
                    source_path,
                    now,
                    company_number,
                ),
            )
            stats["updated"] += 1

    connection.commit()
    return stats


def get_prospect(connection: sqlite3.Connection, company_number: str) -> dict | None:
    row = connection.execute(
        "SELECT * FROM prospects WHERE company_number = ?",
        (company_number.strip().upper(),),
    ).fetchone()
    return dict(row) if row else None


def add_contact(
    connection: sqlite3.Connection,
    *,
    company_number: str,
    channel: str,
    detail: str,
    verified: bool,
    permission: str,
) -> int:
    """Store a contact detail only after it has been verified elsewhere."""
    normalized_number = company_number.strip().upper()
    if get_prospect(connection, normalized_number) is None:
        raise ValueError("unknown prospect")
    if channel not in ALLOWED_CHANNELS:
        raise ValueError(f"unsupported channel: {channel}")
    normalized_detail = detail.strip()
    if not normalized_detail:
        raise ValueError("contact detail is required")
    if not verified:
        raise ValueError("contact detail must be verified before storage")
    if not permission.strip():
        raise ValueError("permission or legal basis is required")

    cursor = connection.execute(
        """
        INSERT INTO contacts
        (company_number, channel, detail, verified, permission, created_at)
        VALUES (?, ?, ?, 1, ?, ?)
        """,
        (normalized_number, channel, normalized_detail, permission.strip(), utcnow()),
    )
    connection.commit()
    return int(cursor.lastrowid)


def record_tps_check(
    connection: sqlite3.Connection,
    *,
    company_number: str,
    list_name: str,
    result: str,
    notes: str = "",
) -> int:
    normalized_number = company_number.strip().upper()
    if get_prospect(connection, normalized_number) is None:
        raise ValueError("unknown prospect")
    if list_name not in ALLOWED_TPS_LISTS:
        raise ValueError(f"unsupported suppression list: {list_name}")
    if result not in ALLOWED_TPS_RESULTS:
        raise ValueError(f"unsupported TPS result: {result}")

    cursor = connection.execute(
        """
        INSERT INTO tps_checks
        (company_number, checked_at, list_name, result, notes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (normalized_number, utcnow(), list_name, result, notes.strip()),
    )
    connection.commit()
    return int(cursor.lastrowid)


def assert_contact_allowed(connection: sqlite3.Connection, company_number: str) -> bool:
    normalized_number = company_number.strip().upper()
    if get_prospect(connection, normalized_number) is None:
        raise ValueError("unknown prospect")

    blocked = connection.execute(
        """
        SELECT 1 FROM tps_checks
        WHERE company_number = ? AND result = 'blocked'
        LIMIT 1
        """,
        (normalized_number,),
    ).fetchone()
    if blocked:
        return False

    opted_out = connection.execute(
        """
        SELECT 1 FROM contact_attempts
        WHERE company_number = ? AND outcome = 'do_not_contact'
        LIMIT 1
        """,
        (normalized_number,),
    ).fetchone()
    return opted_out is None


def record_contact_attempt(
    connection: sqlite3.Connection,
    *,
    contact_id: int,
    outcome: str,
    notes: str = "",
) -> int:
    contact = connection.execute(
        "SELECT * FROM contacts WHERE id = ?",
        (contact_id,),
    ).fetchone()
    if contact is None:
        raise ValueError("unknown contact")
    if outcome not in ALLOWED_OUTCOMES:
        raise ValueError(f"unsupported outcome: {outcome}")
    if not assert_contact_allowed(connection, str(contact["company_number"])):
        raise PermissionError("contact is suppressed")

    cursor = connection.execute(
        """
        INSERT INTO contact_attempts
        (contact_id, company_number, channel, outcome, notes, attempted_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            contact_id,
            str(contact["company_number"]),
            str(contact["channel"]),
            outcome,
            notes.strip(),
            utcnow(),
        ),
    )
    connection.commit()
    return int(cursor.lastrowid)


def serialize_row(row: MutableMapping[str, object] | sqlite3.Row) -> dict:
    return dict(row)
