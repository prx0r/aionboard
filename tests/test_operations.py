"""Tests for stack capture, backups, and MCP tool contracts."""

import json
import os
import tempfile
import unittest
from pathlib import Path

from aionboard import connect, import_prospects, list_stack, record_stack_item
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
    def test_backup_and_verify(self):
        with tempfile.TemporaryDirectory() as directory:
            db_path = os.path.join(directory, "crm.sqlite3")
            connection = connect(db_path)
            import_prospects(
                connection,
                [sample_prospect()],
                source="test-source",
                source_path="test/path.csv",
            )
            connection.close()

            backup_dir = os.path.join(directory, "backups")
            result = create_backup(db_path, backup_dir)
            self.assertTrue(os.path.isfile(result["backup"]))
            self.assertTrue(os.path.isfile(result["manifest"]))
            self.assertTrue(verify_backup(result["backup"], result["manifest"]))

    def test_verify_rejects_tampered_backup(self):
        with tempfile.TemporaryDirectory() as directory:
            db_path = os.path.join(directory, "crm.sqlite3")
            connection = connect(db_path)
            connection.close()

            backup_dir = os.path.join(directory, "backups")
            result = create_backup(db_path, backup_dir)
            with open(result["backup"], "ab") as handle:
                handle.write(b"tampered")
            self.assertFalse(verify_backup(result["backup"], result["manifest"]))

    def test_missing_database_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                create_backup(
                    os.path.join(directory, "missing.sqlite3"),
                    os.path.join(directory, "backups"),
                )


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
