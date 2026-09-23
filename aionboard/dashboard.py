"""Live operator dashboard — stdlib HTTP, token-gated.

Pattern ported from powops/web/server.py: loopback bind, Bearer-or-query
token gate, strict CSP, JSON endpoints. Replaces the static mock in
site/dashboard.html with live CRM + powuk data.

Tabs: targets, opportunities, regulations, installs.
"""

from __future__ import annotations

import json
import os
import secrets
import sqlite3
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

BASE = Path(__file__).parent.parent
sys.path.insert(0, str(BASE))

from aionboard.assistant import (
    opportunities_for_target,
    profile_from_business,
    rules_for_target,
)

PORT = int(os.environ.get("AIONBOARD_PORT", "8797"))
DB_PATH = os.environ.get("AIONBOARD_DB", str(BASE / "data" / "crm.db"))
TOKEN_FILE = Path(os.environ.get(
    "AIONBOARD_TOKEN_FILE", str(Path.home() / ".aionboard" / "dashboard_token")))


def _get_token() -> str:
    env_token = os.environ.get("AIONBOARD_TOKEN")
    if env_token:
        return env_token
    if TOKEN_FILE.exists():
        return TOKEN_FILE.read_text().strip()
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    token = secrets.token_urlsafe(24)
    TOKEN_FILE.write_text(token)
    os.chmod(TOKEN_FILE, 0o600)
    return token


TOKEN = _get_token()


def _db() -> sqlite3.Connection | None:
    if not Path(DB_PATH).exists():
        return None
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


class Handler(BaseHTTPRequestHandler):
    server_version = "aionboard-dash/0.1"

    def _gate(self) -> bool:
        auth = self.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            if secrets.compare_digest(auth[7:], TOKEN):
                return True
        else:
            q = parse_qs(urlparse(self.path).query)
            if secrets.compare_digest(q.get("token", [""])[0], TOKEN):
                return True
        self._json({"error": "bad token"}, 401)
        return False

    def _headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy", "default-src 'self'")

    def _json(self, obj, code: int = 200):
        data = json.dumps(obj, default=str).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self._headers()
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if not self._gate():
            return
        u = urlparse(self.path)
        q = parse_qs(u.query)
        arg = lambda k, d="": q.get(k, [d])[0]

        if u.path == "/api/health":
            from datetime import datetime, timezone
            return self._json({"ok": True,
                               "time": datetime.now(timezone.utc).isoformat()})

        if u.path == "/api/targets":
            conn = _db()
            if conn is None:
                return self._json({"targets": [], "note": "no CRM database"})
            try:
                rows = conn.execute(
                    "SELECT business_id, name, vertical, postcode FROM businesses"
                ).fetchall()
                targets = [dict(r) for r in rows]
            except sqlite3.OperationalError:
                targets = []
            finally:
                conn.close()
            return self._json({"targets": targets, "count": len(targets)})

        if u.path == "/api/opportunities":
            business_id = arg("business_id")
            if not business_id:
                return self._json({"error": "missing ?business_id="}, 400)
            conn = _db()
            if conn is None:
                return self._json({"error": "no CRM database"}, 404)
            try:
                from aionboard.businesses import get_business
                rec = get_business(conn, business_id)
            finally:
                conn.close()
            if not rec:
                return self._json({"error": "unknown business"}, 404)
            profile = profile_from_business(dict(rec))
            try:
                opps = opportunities_for_target(profile)
            except Exception as e:
                return self._json({"error": f"matcher failed: {e}"}, 500)
            return self._json({"business_id": business_id,
                               "count": len(opps), "opportunities": opps})

        if u.path == "/api/regulations":
            vertical = arg("vertical")
            if not vertical:
                return self._json({"error": "missing ?vertical="}, 400)
            rules = rules_for_target(vertical, topic=arg("topic"))
            return self._json({"vertical": vertical, "count": len(rules),
                               "rules": rules})

        if u.path == "/api/installs":
            business_id = arg("business_id", "")
            conn = _db()
            if conn is None:
                return self._json({"installs": [], "note": "no CRM database"})
            try:
                if business_id:
                    rows = conn.execute(
                        "SELECT * FROM installs WHERE business_id = ?",
                        (business_id,)).fetchall()
                else:
                    rows = conn.execute("SELECT * FROM installs").fetchall()
                installs = [dict(r) for r in rows]
            except sqlite3.OperationalError:
                installs = []
            finally:
                conn.close()
            return self._json({"installs": installs, "count": len(installs)})

        return self._json({"error": "not found"}, 404)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print(f"AI Onboard dashboard listening on 127.0.0.1:{PORT}", flush=True)
    print(f"Token file: {TOKEN_FILE}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
