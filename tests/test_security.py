"""Tests for redacted audit logging and rate limiting."""

import json
import unittest

from aionboard import (
    RateLimiter,
    audit_tool_call,
    connect,
    init_approval_tables,
    redact_args,
)


class RedactArgsTests(unittest.TestCase):
    def test_values_never_appear(self):
        redacted = redact_args(
            {"phone": "+44 7700 900100", "total_gbp": 380, "approved": True, "note": None}
        )
        blob = json.dumps(redacted)
        self.assertNotIn("+44 7700 900100", blob)
        self.assertNotIn("380", blob.replace(redacted["_hash"], ""))
        self.assertIn("_hash", redacted)
        self.assertEqual(redacted["phone"], {"type": "str", "length": 15})

    def test_same_args_same_hash(self):
        args = {"a": 1, "b": "x"}
        self.assertEqual(redact_args(args)["_hash"], redact_args(args)["_hash"])

    def test_different_args_different_hash(self):
        self.assertNotEqual(
            redact_args({"total_gbp": 380})["_hash"],
            redact_args({"total_gbp": 381})["_hash"],
        )

    def test_empty_args(self):
        redacted = redact_args(None)
        self.assertIn("_hash", redacted)


class AuditToolCallTests(unittest.TestCase):
    def test_audit_entry_redacted(self):
        connection = connect()
        init_approval_tables(connection)
        entry_id = audit_tool_call(
            connection,
            identity="biz-test-001",
            tool_name="draft_quote",
            arguments={"phone": "+44 7700 900100", "total_gbp": 380},
            scopes=["quotes:draft"],
            result="success",
            latency_ms=42,
        )
        self.assertGreater(entry_id, 0)
        row = connection.execute(
            "SELECT * FROM audit_log WHERE id = ?", (entry_id,)
        ).fetchone()
        self.assertNotIn("+44 7700 900100", row["detail"])
        detail = json.loads(row["detail"])
        self.assertEqual(detail["result"], "success")
        self.assertEqual(detail["scopes"], ["quotes:draft"])

    def test_denials_logged(self):
        connection = connect()
        init_approval_tables(connection)
        audit_tool_call(
            connection,
            identity="biz-test-001",
            tool_name="send-payment",
            arguments={},
            scopes=["quotes:draft"],
            result="denied_auth",
        )
        rows = connection.execute(
            "SELECT * FROM audit_log WHERE business_id = ?", ("biz-test-001",)
        ).fetchall()
        self.assertEqual(len(rows), 1)

    def test_bad_result_rejected(self):
        connection = connect()
        init_approval_tables(connection)
        with self.assertRaises(ValueError):
            audit_tool_call(
                connection,
                identity="biz-test-001",
                tool_name="draft_quote",
                arguments={},
                scopes=[],
                result="maybe",
            )


class RateLimiterTests(unittest.TestCase):
    def test_allows_up_to_limit(self):
        limiter = RateLimiter(max_calls=3, window_seconds=60)
        self.assertTrue(limiter.check("client-a", "draft_quote", now=1000.0))
        self.assertTrue(limiter.check("client-a", "draft_quote", now=1001.0))
        self.assertTrue(limiter.check("client-a", "draft_quote", now=1002.0))
        self.assertFalse(limiter.check("client-a", "draft_quote", now=1003.0))

    def test_window_slides(self):
        limiter = RateLimiter(max_calls=1, window_seconds=60)
        self.assertTrue(limiter.check("client-a", "draft_quote", now=1000.0))
        self.assertFalse(limiter.check("client-a", "draft_quote", now=1059.0))
        self.assertTrue(limiter.check("client-a", "draft_quote", now=1061.0))

    def test_per_client_and_tool(self):
        limiter = RateLimiter(max_calls=1, window_seconds=60)
        self.assertTrue(limiter.check("client-a", "tool-one", now=1000.0))
        self.assertTrue(limiter.check("client-b", "tool-one", now=1000.0))
        self.assertTrue(limiter.check("client-a", "tool-two", now=1000.0))
        self.assertFalse(limiter.check("client-a", "tool-one", now=1001.0))

    def test_bad_config_rejected(self):
        with self.assertRaises(ValueError):
            RateLimiter(max_calls=0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
