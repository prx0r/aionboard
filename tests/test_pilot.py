"""Acceptance tests for the AI Onboard sales-to-installation pilot."""

import csv
import os
import tempfile
import unittest
from pathlib import Path

from aionboard import (
    add_contact,
    approve_action,
    assert_contact_allowed,
    assert_customer_isolation,
    canonical_domain,
    connect,
    create_install,
    execute_outbound,
    generate_handover,
    get_install,
    get_prospect,
    import_prospects,
    is_complete,
    parse_region,
    record_contact_attempt,
    record_tps_check,
    render_site,
    run_demo,
    scan_text,
    set_task,
    write_handover,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
PROSPECT_CSV = REPO_ROOT / "prospects_electrical.csv"


def sample_rows(limit=120):
    with PROSPECT_CSV.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = []
        for row in reader:
            rows.append(row)
            if len(rows) >= limit:
                break
        return rows


class CrmImportTests(unittest.TestCase):
    def test_duplicate_imports_update_rather_than_duplicate(self):
        connection = connect()
        rows = sample_rows()
        first = import_prospects(
            connection,
            rows,
            source="powuk-ch_capacity",
            source_path="data/normalized/ch_capacity/2026/09/22/001226.jsonl",
        )
        second = import_prospects(
            connection,
            rows,
            source="powuk-ch_capacity",
            source_path="data/normalized/ch_capacity/2026/09/22/001226.jsonl",
        )
        self.assertGreater(first["imported"], 0)
        self.assertEqual(second["imported"], 0)
        self.assertEqual(second["updated"], len(rows))
        self.assertEqual(second["skipped"], 0)
        prospect = get_prospect(connection, rows[0]["company_number"])
        assert prospect is not None
        self.assertEqual(prospect["source"], "powuk-ch_capacity")
        self.assertIn("ch_capacity", prospect["source_path"])

    def test_geographic_parsing(self):
        self.assertEqual(parse_region("S5 9LG"), "S5")
        self.assertEqual(parse_region("m1 1aa"), "M1")
        self.assertEqual(parse_region("EC1A 1BB"), "EC1A")
        self.assertEqual(parse_region(""), "")
        self.assertEqual(parse_region(None), "")

    def test_incomplete_rows_are_skipped(self):
        connection = connect()
        stats = import_prospects(
            connection,
            [{"company_number": "", "name": "Missing number"}],
            source="test-source",
            source_path="test/path.csv",
        )
        self.assertEqual(stats, {"imported": 0, "updated": 0, "skipped": 1})

    def test_import_requires_provenance(self):
        connection = connect()
        with self.assertRaises(ValueError):
            import_prospects(
                connection,
                sample_rows(limit=1),
                source="",
                source_path="test/path.csv",
            )


class ContactControlTests(unittest.TestCase):
    def setUp(self):
        self.connection = connect()
        import_prospects(
            self.connection,
            sample_rows(limit=3),
            source="test-source",
            source_path="test/path.csv",
        )
        self.company = sample_rows(limit=1)[0]["company_number"]

    def test_contact_details_require_verification_and_permission(self):
        with self.assertRaises(ValueError):
            add_contact(
                self.connection,
                company_number=self.company,
                channel="phone",
                detail="+44 7700 900100",
                verified=False,
                permission="explicit consent",
            )
        contact_id = add_contact(
            self.connection,
            company_number=self.company,
            channel="phone",
            detail="+44 7700 900100",
            verified=True,
            permission="explicit consent",
        )
        self.assertTrue(assert_contact_allowed(self.connection, self.company))
        attempt_id = record_contact_attempt(
            self.connection,
            contact_id=contact_id,
            outcome="callback",
            notes="Requested callback Friday.",
        )
        self.assertGreater(attempt_id, 0)

    def test_suppression_list_enforcement(self):
        contact_id = add_contact(
            self.connection,
            company_number=self.company,
            channel="phone",
            detail="+44 7700 900101",
            verified=True,
            permission="explicit consent",
        )
        record_tps_check(
            self.connection,
            company_number=self.company,
            list_name="TPS",
            result="blocked",
        )
        self.assertFalse(assert_contact_allowed(self.connection, self.company))
        with self.assertRaises(PermissionError):
            record_contact_attempt(
                self.connection,
                contact_id=contact_id,
                outcome="interested",
            )

    def test_do_not_contact_is_respected(self):
        contact_id = add_contact(
            self.connection,
            company_number=self.company,
            channel="email",
            detail="owner@example.com",
            verified=True,
            permission="explicit consent",
        )
        record_contact_attempt(
            self.connection,
            contact_id=contact_id,
            outcome="do_not_contact",
        )
        self.assertFalse(assert_contact_allowed(self.connection, self.company))
        with self.assertRaises(PermissionError):
            record_contact_attempt(
                self.connection,
                contact_id=contact_id,
                outcome="callback",
            )


class InstallStateTests(unittest.TestCase):
    def setUp(self):
        self.connection = connect()
        self.install_id = create_install(
            self.connection,
            business_id="DEMO-ELEC-MANCHESTER-001",
        )

    def test_failed_google_verification_cannot_complete(self):
        set_task(
            self.connection,
            install_id=self.install_id,
            task="google_profile_assistance",
            status="blocked",
            owner="agent",
            authorization="customer",
            action="Google verification was requested through the ordinary interface.",
            verification="Google has not confirmed verification.",
            evidence="Verification dashboard shows pending.",
        )
        self.assertFalse(is_complete(self.connection, self.install_id))

    def test_failed_oauth_is_blocked_not_verified(self):
        set_task(
            self.connection,
            install_id=self.install_id,
            task="calendar_authorization",
            status="blocked",
            owner="customer",
            authorization="customer",
            action="OAuth consent failed before calendar access was granted.",
            verification="No calendar token was issued.",
            evidence="OAuth error response retained in the private CRM.",
        )
        state = get_install(self.connection, self.install_id)
        task = next(item for item in state["tasks"] if item["task"] == "calendar_authorization")
        self.assertEqual(task["status"], "blocked")
        self.assertFalse(is_complete(self.connection, self.install_id))

    def test_unavailable_platform_capability_is_separate(self):
        with self.assertRaises(ValueError):
            set_task(
                self.connection,
                install_id=self.install_id,
                task="meta_production_integration",
                status="verified",
                owner="agent",
                authorization="customer",
                action="Configured Meta production integration.",
                verification="Verified.",
                evidence="Evidence.",
            )

    def test_verified_install_requires_evidence(self):
        with self.assertRaises(ValueError):
            set_task(
                self.connection,
                install_id=self.install_id,
                task="training",
                status="verified",
                owner="agent",
                authorization="customer",
                action="Training completed.",
                verification="Customer confirmed understanding.",
                evidence="",
            )
        self.assertFalse(is_complete(self.connection, self.install_id))


class ApprovalIsolationTests(unittest.TestCase):
    def test_outbound_requires_matching_approval(self):
        approval = approve_action(
            client_id="DEMO-ELEC-MANCHESTER-001",
            action="send-quote",
            target="quote-DEMO-001",
            approver="Fictional Owner",
        )
        receipt = execute_outbound(
            approval=approval,
            client_id="DEMO-ELEC-MANCHESTER-001",
            action="send-quote",
            target="quote-DEMO-001",
        )
        self.assertFalse(receipt["sent"])
        self.assertTrue(receipt["authorized"])
        with self.assertRaises(PermissionError):
            execute_outbound(
                approval=approval,
                client_id="DEMO-ELEC-MANCHESTER-001",
                action="send-invoice",
                target="quote-DEMO-001",
            )

    def test_customer_isolation(self):
        client_a = {
            "client_id": "client-a",
            "credential_refs": ["cred-a-1"],
            "storage_paths": ["clients/client-a"],
        }
        client_b = {
            "client_id": "client-b",
            "credential_refs": ["cred-b-1"],
            "storage_paths": ["clients/client-b"],
        }
        self.assertTrue(assert_customer_isolation(client_a, client_b))
        with self.assertRaises(ValueError):
            assert_customer_isolation(
                client_a,
                {
                    "client_id": "client-b",
                    "credential_refs": ["cred-a-1"],
                    "storage_paths": ["clients/client-b"],
                },
            )

    def test_secret_scan_finds_test_credential(self):
        findings = scan_text('api_key = "sk-test-abcdefghijklmnopqrstuvwxyz"')
        self.assertTrue(findings)


class DemoHandoverTests(unittest.TestCase):
    def test_demo_is_fictional_with_no_live_sends(self):
        result = run_demo()
        self.assertTrue(result["fictional"])
        self.assertEqual(result["live_external_sends"], 0)
        self.assertIn("simulated", [step["mode"] for step in result["steps"]])
        quote = result["steps"][1]["quote"]
        self.assertEqual(quote["status"], "draft")
        self.assertFalse(quote["sent"])
        self.assertTrue(quote["approval_required"])

    def test_handover_is_accurate_and_secret_free(self):
        markdown = generate_handover(
            business={"business_id": "DEMO-ELEC-MANCHESTER-001", "name": "Fictional Manchester Electrical Co."},
            package="standard-ai-setup",
            tasks=[
                {
                    "task": "quote_draft",
                    "status": "verified",
                    "action": "Draft prepared.",
                    "verification": "Draft matches price book.",
                    "evidence": "demo-quote-DEMO-001",
                },
                {
                    "task": "google_profile_assistance",
                    "status": "blocked",
                    "action": "Verification requested.",
                    "verification": "Google has not confirmed verification.",
                    "evidence": "Dashboard shows pending.",
                },
            ],
            accounts=[{"name": "Customer Gmail", "owner": "customer", "status": "authorized"}],
            permissions=[{"scope": "Read Gmail enquiries", "granted_to": "AI Onboard", "method": "OAuth"}],
            subscriptions=[{"name": "No recurring AI Onboard subscription", "payer": "n/a", "amount": "£0"}],
            test_results=[
                {"name": "SMS delivery test", "result": "failed", "evidence": "Provider returned no delivery receipt."},
                {"name": "Quote approval test", "result": "passed", "evidence": "Owner approval recorded."},
            ],
            revocation=["Remove AI Onboard OAuth access.", "Rotate shared passwords."],
        )
        self.assertIn("Pending third-party approvals", markdown)
        self.assertIn("Revoke access", markdown)
        self.assertIn("failed", markdown)
        self.assertEqual(scan_text(markdown), [])

    def test_handover_file_is_restricted(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "handover", "DEMO.md")
            returned = write_handover(
                path,
                "# Handover\n\n## Configured accounts\n\n## Ownership and permissions\n",
            )
            self.assertEqual(returned, path)
            self.assertEqual(oct(os.stat(path).st_mode & 0o777), "0o600")


class WebsiteTests(unittest.TestCase):
    def test_website_states_scope_price_booking_privacy(self):
        from aionboard.website import render_site

        html = render_site()
        self.assertIn("aionboard.co.uk", html)
        self.assertIn("£499", html)
        self.assertIn("mailto:hello@aionboard.co.uk", html)
        self.assertIn("TPS", html)
        self.assertIn("suppression", html)
        self.assertIn("No completed customer installation is claimed", html)
        for forbidden in [
            "appear in ChatGPT",
            "guaranteed placement",
            "typical payback",
            "Most Tradify users",
            "60% of calls",
        ]:
            self.assertNotIn(forbidden, html)

    def test_canonical_domain(self):
        self.assertEqual(canonical_domain(), "https://aionboard.co.uk")


if __name__ == "__main__":
    unittest.main(verbosity=2)
