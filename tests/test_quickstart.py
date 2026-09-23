"""End-to-end acceptance: fictional nail technician, no company number.

Exercises the full £20 muse-quickstart journey: business creation without
Companies House identity, consents, onboarding with evidence, integration
records, manual generation, and the seven-day support workflow. Proves POW
opportunity consent stays optional throughout.
"""

import unittest

from aionboard import connect, init_business_tables
from aionboard.businesses import (
    create_business,
    get_business,
    has_consent,
    marketing_allowed,
    record_consent,
)
from aionboard.integrations import (
    init_integration_tables,
    is_connected,
    record_integration,
)
from aionboard.manual import generate_manual
from aionboard.onboarding import (
    create_onboarding,
    get_onboarding,
    is_onboarded,
    resume_onboarding,
    tasks_for,
)
from aionboard.onboarding import set_onboarding_task
from aionboard.support import (
    init_support_tables,
    open_ticket,
    resolve_ticket,
    support_stats,
)


class NailTechQuickstartTest(unittest.TestCase):
    def test_fictional_nail_tech_full_journey(self):
        connection = connect()
        init_business_tables(connection)
        init_integration_tables(connection)
        init_support_tables(connection)

        # 1. Sole trader with no company number gets a canonical business_id.
        business_id = create_business(
            connection,
            display_name="Fictional Nails by Aisha",
            kind="sole_trader",
            vertical="nails",
        )
        business = get_business(connection, business_id)
        self.assertIsNotNone(business)
        self.assertIsNone(business["company_number"])
        self.assertEqual(business["kind"], "sole_trader")

        # 2. Onboarding consent granted; marketing and POW consent absent.
        record_consent(
            connection, business_id=business_id, purpose="onboarding", status="granted"
        )
        self.assertTrue(has_consent(connection, business_id, "onboarding"))
        self.assertFalse(has_consent(connection, business_id, "pow_opportunity_alerts"))
        self.assertFalse(marketing_allowed(connection, business_id, "sms"))

        # 3. Create the £20 muse-quickstart onboarding for nails.
        onboarding_id = create_onboarding(
            connection,
            business_id=business_id,
            vertical="nails",
            package="muse-quickstart",
        )
        expected_tasks = set(tasks_for("nails"))
        # Nails must not require electrician quoting tasks.
        self.assertNotIn("price_book_approval", expected_tasks)
        self.assertNotIn("quote_draft", expected_tasks)
        self.assertIn("booking_workflow", expected_tasks)

        # 4. Verify every task with evidence (account verification results).
        for task in sorted(expected_tasks):
            set_onboarding_task(
                connection,
                onboarding_id=onboarding_id,
                task=task,
                status="verified",
                owner="agent",
                authorization="customer",
                prerequisites="Customer present with account access.",
                execution_method="manual",
                action=f"Configured {task} with the customer present.",
                verification="Customer demonstrated the workflow unaided.",
                evidence=f"demo-evidence-{task}",
                recovery_action=f"Re-run {task} from handover; no external duplicate.",
            )
        self.assertTrue(is_onboarded(connection, onboarding_id))

        # 4b. Resume is idempotent: verified work is skipped, never re-executed.
        resumed = resume_onboarding(connection, onboarding_id)
        self.assertEqual(set(resumed["skip_verified"]), expected_tasks)
        self.assertEqual(resumed["needs_recovery"], [])
        self.assertEqual(resumed["pending"], [])

        # 5. Record integration states; nothing is marked connected without proof.
        record_integration(
            connection,
            business_id=business_id,
            app="Booksy",
            connection_offered=True,
            auth_status="granted",
            permissions_granted="read bookings",
            actions_tested="deposit policy read",
            manual_remainder="reminder setup done in-app by customer",
        )
        self.assertTrue(is_connected(connection, business_id, "Booksy"))
        record_integration(
            connection,
            business_id=business_id,
            app="WhatsApp Cloud API",
            connection_offered=False,
            auth_status="unsupported",
            manual_remainder="WhatsApp Business app used instead",
        )
        self.assertFalse(is_connected(connection, business_id, "WhatsApp Cloud API"))

        # 6. Generate the teaching manual from verified state.
        state = get_onboarding(connection, onboarding_id)
        manual = generate_manual(
            business_name="Fictional Nails by Aisha",
            vertical="nails",
            workflows=["booking_workflow", "deposit_reminder_preparation"],
            accounts=[
                {"name": "Booksy", "owner": "customer", "status": "configured"},
                {"name": "Gmail", "owner": "customer", "status": "authorized"},
            ],
            support_days=7,
        )
        self.assertIn("Fictional Nails by Aisha", manual)
        self.assertIn("Prompt 1", manual)
        self.assertIn("Removing our access", manual)
        self.assertIn("approval", manual.lower())
        _ = state  # state verified onboarded above

        # 7. Open and close a support request; guide resolves it, no human minutes.
        ticket_id = open_ticket(
            connection,
            business_id=business_id,
            question="How do I change my deposit amount?",
        )
        resolve_ticket(
            connection, ticket_id=ticket_id, resolved_by="guide", human_minutes=0
        )
        stats = support_stats(connection, business_id)
        self.assertEqual(stats["total"], 1)
        self.assertEqual(stats["guide_resolved"], 1)
        self.assertEqual(stats["human_minutes"], 0)
        self.assertEqual(stats["open"], 0)

        # 8. POW opportunity marketing remains optional and off.
        self.assertFalse(has_consent(connection, business_id, "pow_opportunity_alerts"))
        record_consent(
            connection,
            business_id=business_id,
            purpose="marketing",
            channel="sms",
            status="granted",
        )
        self.assertTrue(marketing_allowed(connection, business_id, "sms"))
        # Marketing consent does not imply POW consent.
        self.assertFalse(has_consent(connection, business_id, "pow_opportunity_alerts"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
