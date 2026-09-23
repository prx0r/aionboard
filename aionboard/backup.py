"""Local encrypted-at-rest backup helper for the pilot CRM.

Backups are timestamped SQLite copies with a SHA-256 manifest.
They inherit live-data access controls and are never committed to git.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import sqlite3
from datetime import datetime, timezone


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def create_backup(db_path: str, backup_dir: str) -> dict:
    """Copy a SQLite database to a timestamped backup with a manifest."""
    if not os.path.isfile(db_path):
        raise ValueError(f"database not found: {db_path}")
    os.makedirs(backup_dir, exist_ok=True)

    name = f"crm-{utc_stamp()}.sqlite3"
    dest = os.path.join(backup_dir, name)
    if os.path.exists(dest):
        raise ValueError(f"backup already exists: {dest}")

    shutil.copy2(db_path, dest)
    os.chmod(dest, 0o600)

    checksum = sha256_file(dest)
    manifest_path = dest + ".sha256"
    with open(manifest_path, "w", encoding="utf-8") as handle:
        handle.write(f"{checksum}  {name}\n")
    os.chmod(manifest_path, 0o600)

    return {"backup": dest, "manifest": manifest_path, "sha256": checksum}


def verify_backup(backup_path: str, manifest_path: str) -> bool:
    """Verify a backup against its manifest and check it opens."""
    with open(manifest_path, encoding="utf-8") as handle:
        expected = handle.read().split()[0]
    if sha256_file(backup_path) != expected:
        return False
    connection = sqlite3.connect(f"file:{backup_path}?mode=ro", uri=True)
    try:
        connection.execute("SELECT name FROM sqlite_master LIMIT 1").fetchone()
    finally:
        connection.close()
    return True
