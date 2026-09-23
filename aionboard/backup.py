"""Consistent, verified, encrypted backups for the pilot CRM.

Uses SQLite's online backup API (safe against concurrent writes),
verifies with PRAGMA integrity_check, and encrypts with Fernet
(AES-128-CBC + HMAC) before writing to disk. Backups inherit live-data
access controls and are never committed to git.
"""

from __future__ import annotations

import base64
import hashlib
import os
import sqlite3
from datetime import datetime, timezone

from cryptography.fernet import Fernet, InvalidToken


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def derive_key(passphrase: str, salt: bytes) -> bytes:
    """Derive a Fernet key from a passphrase with Scrypt."""
    from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return base64.urlsafe_b64encode(kdf.derive(passphrase.encode("utf-8")))


def _consistent_copy(source_path: str, dest_path: str) -> None:
    """Copy via the SQLite backup API so concurrent writes can't corrupt it."""
    source = sqlite3.connect(f"file:{source_path}?mode=ro", uri=True)
    try:
        dest = sqlite3.connect(dest_path)
        try:
            source.backup(dest)
        finally:
            dest.close()
    finally:
        source.close()


def _integrity_ok(db_path: str) -> bool:
    connection = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        row = connection.execute("PRAGMA integrity_check").fetchone()
    finally:
        connection.close()
    return row is not None and row[0] == "ok"


def create_backup(db_path: str, backup_dir: str, *, passphrase: str) -> dict:
    """Create an encrypted backup. Passphrase comes from the operator, never git."""
    if not os.path.isfile(db_path):
        raise ValueError(f"database not found: {db_path}")
    if not passphrase:
        raise ValueError("passphrase is required")
    os.makedirs(backup_dir, exist_ok=True)

    name = f"crm-{utc_stamp()}.sqlite3.enc"
    dest = os.path.join(backup_dir, name)
    if os.path.exists(dest):
        raise ValueError(f"backup already exists: {dest}")

    tmp_plain = dest + ".plain.tmp"
    try:
        _consistent_copy(db_path, tmp_plain)
        if not _integrity_ok(tmp_plain):
            raise ValueError("backup failed integrity check")
        with open(tmp_plain, "rb") as handle:
            plaintext = handle.read()
        salt = os.urandom(16)
        token = Fernet(derive_key(passphrase, salt)).encrypt(plaintext)
        with open(dest, "wb") as handle:
            handle.write(salt + token)
        os.chmod(dest, 0o600)
    finally:
        if os.path.exists(tmp_plain):
            os.remove(tmp_plain)

    checksum = sha256_file(dest)
    manifest_path = dest + ".sha256"
    with open(manifest_path, "w", encoding="utf-8") as handle:
        handle.write(f"{checksum}  {name}\n")
    os.chmod(manifest_path, 0o600)

    return {"backup": dest, "manifest": manifest_path, "sha256": checksum}


def verify_backup(backup_path: str, manifest_path: str, *, passphrase: str) -> bool:
    """Verify checksum, decrypt, and run integrity_check on the restored copy."""
    with open(manifest_path, encoding="utf-8") as handle:
        expected = handle.read().split()[0]
    if sha256_file(backup_path) != expected:
        return False
    with open(backup_path, "rb") as handle:
        blob = handle.read()
    salt, token = blob[:16], blob[16:]
    try:
        plaintext = Fernet(derive_key(passphrase, salt)).decrypt(token)
    except InvalidToken:
        return False
    tmp_path = backup_path + ".verify.tmp"
    try:
        with open(tmp_path, "wb") as handle:
            handle.write(plaintext)
        return _integrity_ok(tmp_path)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def restore_backup(backup_path: str, dest_path: str, *, passphrase: str) -> str:
    """Decrypt a backup to a new database file and verify it."""
    if os.path.exists(dest_path):
        raise ValueError(f"destination already exists: {dest_path}")
    with open(backup_path, "rb") as handle:
        blob = handle.read()
    salt, token = blob[:16], blob[16:]
    try:
        plaintext = Fernet(derive_key(passphrase, salt)).decrypt(token)
    except InvalidToken as exc:
        raise ValueError("wrong passphrase or corrupted backup") from exc
    with open(dest_path, "wb") as handle:
        handle.write(plaintext)
    os.chmod(dest_path, 0o600)
    if not _integrity_ok(dest_path):
        os.remove(dest_path)
        raise ValueError("restored database failed integrity check")
    return dest_path
