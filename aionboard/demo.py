"""Fictional electrician demonstration."""

from __future__ import annotations

DEMO_BUSINESS = {
    "business_id": "DEMO-ELEC-MANCHESTER-001",
    "name": "Fictional Manchester Electrical Co.",
    "vertical": "electrician",
    "postcode": "M1 1AA",
    "region": "Manchester",
}
DEMO_CUSTOMER = {
    "name": "Fictional Customer",
    "phone": "+44 7700 900100",
    "address": "1 Fictional Street, Manchester M1 1AA",
    "job_type": "consumer_unit_replacement",
    "description": "Fictional consumer-unit replacement enquiry",
}
PRICE_BOOK = {
    "consumer_unit_replacement": {
        "labour_low_gbp": 400,
        "labour_high_gbp": 500,
        "approved_by": "Fictional Owner",
        "requires_site_visit_or_photos": True,
    }
}


def run_demo() -> dict:
    """Run a deterministic demo using only fictional data."""
    quote = {
        "job_type": DEMO_CUSTOMER["job_type"],
        "labour_low_gbp": PRICE_BOOK["consumer_unit_replacement"]["labour_low_gbp"],
        "labour_high_gbp": PRICE_BOOK["consumer_unit_replacement"]["labour_high_gbp"],
        "status": "draft",
        "sent": False,
        "approval_required": True,
    }
    return {
        "fictional": True,
        "business": DEMO_BUSINESS,
        "customer": DEMO_CUSTOMER,
        "simulated_integrations": ["email", "calendar", "scheduling"],
        "steps": [
            {
                "name": "email_intake",
                "mode": "simulated",
                "result": "Fictional enquiry classified as consumer-unit replacement.",
            },
            {
                "name": "quote_draft",
                "mode": "price-book",
                "result": "Draft quote prepared from the fictional approved price book.",
                "quote": quote,
            },
            {
                "name": "owner_approval",
                "mode": "required",
                "result": "Owner approval is required before sending.",
            },
            {
                "name": "scheduling_proposal",
                "mode": "simulated",
                "result": "Two fictional availability windows proposed.",
            },
            {
                "name": "handover_evidence",
                "mode": "generated",
                "result": "All steps are recorded in the demo handover.",
            },
        ],
        "live_external_sends": 0,
        "notes": (
            "This is a fictional demonstration. No production email, calendar, "
            "voice, WhatsApp, Google, Meta, payment, or customer system was used."
        ),
    }


def demo_summary(result: dict | None = None) -> str:
    result = result or run_demo()
    quote = result["steps"][1]["quote"]
    return (
        "FICTIONAL ELECTRICIAN DEMO\n"
        f"Business: {result['business']['name']}\n"
        f"Customer: {result['customer']['name']}\n"
        f"Quote draft: £{quote['labour_low_gbp']}-£{quote['labour_high_gbp']} labour, status={quote['status']}\n"
        f"Live external sends: {result['live_external_sends']}\n"
        "Owner approval remains required before any outbound message."
    )
