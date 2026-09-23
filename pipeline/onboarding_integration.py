"""Wire aocsec onboarding into the outreach pipeline.

Uses aocsec's 8-stage pipeline for tracking free trial progress.
"""

import os
import sys

# Add aocsec to path
sys.path.insert(0, "/root/aocsec")

try:
    from onboarding.pipeline import init_onboarding_tables, register_prospect, record_evidence, advance, pipeline_status
    from onboarding.yesflow import run_yes_flow
    from onboarding.runbooks import runbook_for
    from onboarding.followups import followups_for
    AOCSEC_AVAILABLE = True
except ImportError:
    AOCSEC_AVAILABLE = False


def init_onboarding(conn):
    """Initialize onboarding tables."""
    if AOCSEC_AVAILABLE:
        init_onboarding_tables(conn)
        return True
    return False


def start_trial(conn, business_id: str, name: str, vertical: str, postcode: str) -> dict:
    """Start a free trial for a business."""
    if not AOCSEC_AVAILABLE:
        return {"error": "aocsec not available"}
    
    # Register prospect
    register_prospect(conn, business_id=business_id, name=name, vertical=vertical, postcode=postcode)
    
    # Record consent
    record_evidence(conn, business_id, "contacted", "first_touch", "free_trial_signup")
    record_evidence(conn, business_id, "interested", "positive_response", "trial_requested")
    record_evidence(conn, business_id, "consent_recorded", "consent_basis", "free_trial")
    
    # Advance to eligible
    advance(conn, business_id)
    advance(conn, business_id)
    advance(conn, business_id)
    
    # Get status
    status = pipeline_status(conn, business_id)
    
    return {
        "business_id": business_id,
        "status": status,
        "message": f"Free trial started for {name}",
    }


def get_trial_status(conn, business_id: str) -> dict:
    """Get the status of a free trial."""
    if not AOCSEC_AVAILABLE:
        return {"error": "aocsec not available"}
    
    status = pipeline_status(conn, business_id)
    return status


def get_install_runbook(vertical: str) -> list:
    """Get the installation runbook for a vertical."""
    if not AOCSEC_AVAILABLE:
        return []
    
    return runbook_for(vertical)


def get_followup_items(conn, business_id: str) -> list:
    """Get follow-up items for a business."""
    if not AOCSEC_AVAILABLE:
        return []
    
    return followups_for(conn, business_id)


if __name__ == "__main__":
    import sqlite3
    
    print("=== aocsec Onboarding Integration ===")
    print(f"aocsec available: {AOCSEC_AVAILABLE}")
    
    if AOCSEC_AVAILABLE:
        # Create in-memory database
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        
        # Initialize
        init_onboarding(conn)
        
        # Start a trial
        result = start_trial(conn, "test-001", "Test Business", "nails", "M1 1AA")
        print(f"Trial started: {result}")
        
    # Get runbook
    runbook = get_install_runbook("nails")
    print(f"\nNails runbook: {len(runbook.get('steps', []))} steps")
    for step in runbook.get('steps', [])[:3]:
        print(f"  - {step['id']}: {step['detail']}")
        
        conn.close()
