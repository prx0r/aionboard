"""Tests for stack capture, backups, and MCP tool contracts."""

import json
import os
import tempfile
import unittest
from pathlib import Path

from aionboard import (
    audit_history,
    connect,
    fleet_support_report,
    get_prospect,
    import_prospects,
    init_approval_tables,
    init_support_tables,
    issue_approval,
    list_stack,
    open_ticket,
    record_stack_item,
    redeem_approval,
    resolve_ticket,
)
from aionboard.backup import create_backup, verify_backup

REPO_ROOT = Path(__file__).resolve().parents[1]


def sample_prospect():
    return {
        "company_number": "TEST12345",
        "name": "Fictional Test Electrical Ltd",
        "postcode": "M1 1AA",
        "region": "M1",
        "sic_codes": "43210",
        "status": "active",
        "cluster": "electrical",
    }


class StackCaptureTests(unittest.TestCase):
    def setUp(self):
        self.connection = connect()
        import_prospects(
            self.connection,
            [sample_prospect()],
            source="test-source",
            source_path="test/path.csv",
        )

    def test_record_and_list_stack(self):
        item_id = record_stack_item(
            self.connection,
            company_number="TEST12345",
            tool="Tradify",
            category="job management",
            verdict="import-from",
            access="customer export received",
            verified=True,
        )
        self.assertGreater(item_id, 0)
        items = list_stack(self.connection, "TEST12345")
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["tool"], "Tradify")
        self.assertEqual(items[0]["verdict"], "import-from")

    def test_duplicate_tool_updates(self):
        first = record_stack_item(
            self.connection, company_number="TEST12345", tool="Xero"
        )
        second = record_stack_item(
            self.connection,
            company_number="TEST12345",
            tool="Xero",
            verdict="integrate",
            access="OAuth granted",
            verified=True,
        )
        self.assertEqual(first, second)
        items = list_stack(self.connection, "TEST12345")
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["access"], "OAuth granted")

    def test_replace_requires_customer_approval(self):
        with self.assertRaises(ValueError):
            record_stack_item(
                self.connection,
                company_number="TEST12345",
                tool="Tradify",
                verdict="replace",
                access="we decided to migrate them",
            )
        item_id = record_stack_item(
            self.connection,
            company_number="TEST12345",
            tool="Tradify",
            verdict="replace",
            access="customer approval recorded 2026-09-23",
        )
        self.assertGreater(item_id, 0)

    def test_unknown_prospect_rejected(self):
        with self.assertRaises(ValueError):
            record_stack_item(
                self.connection, company_number="NOPE99999", tool="Xero"
            )


class BackupTests(unittest.TestCase):
    PASSPHRASE = "test-passphrase-for-encrypted-backups"

    def _seed_db(self, db_path):
        connection = connect(db_path)
        import_prospects(
            connection,
            [sample_prospect()],
            source="test-source",
            source_path="test/path.csv",
        )
        connection.close()

    def test_backup_verify_and_restore(self):
        from aionboard.backup import restore_backup

        with tempfile.TemporaryDirectory() as directory:
            db_path = os.path.join(directory, "crm.sqlite3")
            self._seed_db(db_path)

            backup_dir = os.path.join(directory, "backups")
            result = create_backup(db_path, backup_dir, passphrase=self.PASSPHRASE)
            self.assertTrue(os.path.isfile(result["backup"]))
            self.assertTrue(os.path.isfile(result["manifest"]))
            self.assertTrue(
                verify_backup(result["backup"], result["manifest"], passphrase=self.PASSPHRASE)
            )

            restored = os.path.join(directory, "restored.sqlite3")
            restore_backup(result["backup"], restored, passphrase=self.PASSPHRASE)
            connection = connect(restored)
            prospect = get_prospect(connection, "TEST12345")
            connection.close()
            self.assertIsNotNone(prospect)

    def test_verify_rejects_tampered_backup(self):
        with tempfile.TemporaryDirectory() as directory:
            db_path = os.path.join(directory, "crm.sqlite3")
            self._seed_db(db_path)

            backup_dir = os.path.join(directory, "backups")
            result = create_backup(db_path, backup_dir, passphrase=self.PASSPHRASE)
            with open(result["backup"], "ab") as handle:
                handle.write(b"tampered")
            self.assertFalse(
                verify_backup(result["backup"], result["manifest"], passphrase=self.PASSPHRASE)
            )

    def test_wrong_passphrase_rejected(self):
        from aionboard.backup import restore_backup

        with tempfile.TemporaryDirectory() as directory:
            db_path = os.path.join(directory, "crm.sqlite3")
            self._seed_db(db_path)

            backup_dir = os.path.join(directory, "backups")
            result = create_backup(db_path, backup_dir, passphrase=self.PASSPHRASE)
            self.assertFalse(
                verify_backup(result["backup"], result["manifest"], passphrase="wrong-passphrase")
            )
            with self.assertRaises(ValueError):
                restore_backup(
                    result["backup"],
                    os.path.join(directory, "restored.sqlite3"),
                    passphrase="wrong-passphrase",
                )

    def test_missing_database_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                create_backup(
                    os.path.join(directory, "missing.sqlite3"),
                    os.path.join(directory, "backups"),
                    passphrase=self.PASSPHRASE,
                )

    def test_passphrase_required(self):
        with tempfile.TemporaryDirectory() as directory:
            db_path = os.path.join(directory, "crm.sqlite3")
            self._seed_db(db_path)
            with self.assertRaises(ValueError):
                create_backup(
                    db_path, os.path.join(directory, "backups"), passphrase=""
                )


class AuthenticatedApprovalTests(unittest.TestCase):
    def setUp(self):
        self.connection = connect()
        init_approval_tables(self.connection)

    def _issue(self, **overrides):
        params = {
            "business_id": "biz-test-001",
            "approver": "Fictional Owner",
            "action": "send-quote",
            "target": "quote-001",
            "payload": {"total_gbp": 380},
        }
        params.update(overrides)
        return issue_approval(self.connection, **params)

    def test_redeem_happy_path(self):
        token = self._issue()
        receipt = redeem_approval(
            self.connection,
            token=token,
            business_id="biz-test-001",
            action="send-quote",
            target="quote-001",
            payload={"total_gbp": 380},
        )
        self.assertTrue(receipt["authorized"])
        self.assertFalse(receipt["sent"])

    def test_replay_rejected(self):
        token = self._issue()
        kwargs = {
            "business_id": "biz-test-001",
            "action": "send-quote",
            "target": "quote-001",
            "payload": {"total_gbp": 380},
        }
        redeem_approval(self.connection, token=token, **kwargs)
        with self.assertRaises(PermissionError):
            redeem_approval(self.connection, token=token, **kwargs)

    def test_payload_mismatch_rejected(self):
        token = self._issue()
        with self.assertRaises(PermissionError):
            redeem_approval(
                self.connection,
                token=token,
                business_id="biz-test-001",
                action="send-quote",
                target="quote-001",
                payload={"total_gbp": 9999},
            )

    def test_wrong_customer_rejected(self):
        token = self._issue()
        with self.assertRaises(PermissionError):
            redeem_approval(
                self.connection,
                token=token,
                business_id="biz-test-999",
                action="send-quote",
                target="quote-001",
                payload={"total_gbp": 380},
            )

    def test_expired_token_rejected(self):
        token = self._issue(ttl_seconds=1)
        import time

        time.sleep(1.1)
        with self.assertRaises(PermissionError):
            redeem_approval(
                self.connection,
                token=token,
                business_id="biz-test-001",
                action="send-quote",
                target="quote-001",
                payload={"total_gbp": 380},
            )

    def test_audit_trail_recorded(self):
        token = self._issue()
        redeem_approval(
            self.connection,
            token=token,
            business_id="biz-test-001",
            action="send-quote",
            target="quote-001",
            payload={"total_gbp": 380},
        )
        history = audit_history(self.connection, "biz-test-001")
        actions = [entry["action"] for entry in history]
        self.assertIn("approval_issued", actions)
        self.assertIn("approval_redeemed", actions)


class FleetReportTests(unittest.TestCase):
    def test_fleet_viability_flag(self):
        connection = connect()
        init_support_tables(connection)
        t1 = open_ticket(connection, business_id="biz-a", question="Q1")
        resolve_ticket(connection, ticket_id=t1, resolved_by="guide", human_minutes=0)
        t2 = open_ticket(connection, business_id="biz-b", question="Q2")
        resolve_ticket(connection, ticket_id=t2, resolved_by="human", human_minutes=30)
        report = fleet_support_report(connection, viability_minutes=20)
        self.assertEqual(report["businesses"], 2)
        self.assertFalse(report["viable"])
        self.assertEqual(report["over_threshold"], ["biz-b"])

    def test_empty_fleet_is_viable(self):
        connection = connect()
        init_support_tables(connection)
        report = fleet_support_report(connection)
        self.assertTrue(report["viable"])
        self.assertEqual(report["total_tickets"], 0)


class McpContractTests(unittest.TestCase):
    def test_tools_contract_is_valid(self):
        with open(REPO_ROOT / "mcp" / "tools.json", encoding="utf-8") as handle:
            contract = json.load(handle)
        self.assertEqual(contract["protocol"], "mcp-tools/1")
        names = [tool["name"] for tool in contract["tools"]]
        for required in (
            "vertical_lookup",
            "install_status",
            "record_contact_attempt",
            "set_install_task",
            "generate_handover",
            "draft_quote",
        ):
            self.assertIn(required, names)
        for tool in contract["tools"]:
            self.assertIn(tool["kind"], {"read", "write"})
            if tool["kind"] == "write":
                self.assertNotEqual(
                    tool["approval"], "none", msg=f"{tool['name']} needs approval"
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
