"""Wire WhatsApp into the outreach pipeline.

Uses influence's WhatsApp adapter for real messaging.
Falls back to stubs when no credentials are present.

Message states:
  drafted  — message composed but not sent (stub / no provider)
  sent     — provider accepted the message (real send confirmed)
  delivered — provider confirmed delivery to device
"""

import os
import sys

# Add influence to path
sys.path.insert(0, "/root/influence/stevejobless")

try:
    from stevejobless.channels import send_whatsapp, send_sms, whatsapp_configured
    WHATSAPP_AVAILABLE = True
except ImportError:
    WHATSAPP_AVAILABLE = False


def send_message(phone: str, message: str, channel: str = "whatsapp") -> dict:
    """Send a message via WhatsApp or SMS.

    Returns: {
        "ok": bool,        # True only if provider confirmed acceptance
        "status": str,     # drafted | sent | delivered
        "stubbed": bool,   # True if no real provider was used
        "channel": str,
        "note": str,
    }
    """
    if channel == "whatsapp":
        if WHATSAPP_AVAILABLE:
            result = send_whatsapp(phone, message)
            provider_ok = result.get("ok", False) and not result.get("stubbed", True)
            return {
                "ok": provider_ok,
                "status": "sent" if provider_ok else "drafted",
                "stubbed": result.get("stubbed", True),
                "channel": "whatsapp",
                "note": result.get("note", ""),
            }
        else:
            # Stub mode — message was NOT sent
            return {
                "ok": False,
                "status": "drafted",
                "stubbed": True,
                "channel": "whatsapp",
                "note": "Stub only — WhatsApp not configured. Set WHATSAPP_TOKEN for live sends. Message was NOT delivered.",
                "to": phone,
                "message": message[:200],
            }
    
    elif channel == "sms":
        if WHATSAPP_AVAILABLE:
            result = send_sms(phone, message)
            provider_ok = result.get("ok", False) and not result.get("stubbed", True)
            return {
                "ok": provider_ok,
                "status": "sent" if provider_ok else "drafted",
                "stubbed": result.get("stubbed", True),
                "channel": "sms",
                "note": result.get("note", ""),
            }
        else:
            return {
                "ok": False,
                "status": "drafted",
                "stubbed": True,
                "channel": "sms",
                "note": "Stub only — SMS not configured. Set TELNYX_API_KEY for live sends. Message was NOT delivered.",
                "to": phone,
                "message": message[:200],
            }
    
    return {"ok": False, "status": "drafted", "stubbed": False, "channel": channel, "note": f"Unknown channel: {channel}"}


def send_outreach(prospect_id: int, db_conn, channel: str = "whatsapp") -> dict:
    """Send outreach message to a prospect.

    Only records outreach in DB if the messaging provider confirmed delivery.
    Stubs are reported as status="drafted" and NOT recorded as sent.
    """
    from pipeline.db import record_outreach
    from pipeline.outreach import get_outreach_queue
    from pipeline.templates import get_initial_template, format_template
    
    # Get prospect
    prospect = db_conn.execute("SELECT * FROM prospects WHERE id=?", (prospect_id,)).fetchone()
    if not prospect:
        return {"error": "Prospect not found"}
    
    if not prospect["phone"]:
        return {"error": "No phone number"}
    
    # Get template
    template = get_initial_template(prospect["vertical"], channel)
    
    # Format message
    message = format_template(template, {
        "name": prospect["director_name"].split(",")[0].strip() if prospect["director_name"] else "there",
        "business": prospect["business_name"],
        "vertical": prospect["vertical"],
        "city": prospect["city"],
        "rating": prospect["rating"] or "N/A",
        "reviews": prospect["review_count"] or "N/A",
    })
    
    # Send via provider
    result = send_message(prospect["phone"], message, channel)
    
    # Only record outreach if provider confirmed the send
    if result["ok"]:
        record_outreach(db_conn, prospect_id, channel, "outbound", message, f"initial_{channel}")
    
    return {
        "prospect": prospect["business_name"],
        "phone": prospect["phone"],
        "channel": channel,
        "sent": result["ok"],
        "status": result.get("status", "drafted"),
        "stubbed": result.get("stubbed", True),
        "message": message,
    }


def send_followup(prospect_id: int, db_conn, followup_type: str, channel: str = "whatsapp") -> dict:
    """Send a follow-up message to a prospect.

    Only records outreach in DB if the messaging provider confirmed delivery.
    """
    from pipeline.db import record_outreach
    from pipeline.templates import get_followup_template, format_template
    
    prospect = db_conn.execute("SELECT * FROM prospects WHERE id=?", (prospect_id,)).fetchone()
    if not prospect:
        return {"error": "Prospect not found"}
    
    if not prospect["phone"]:
        return {"error": "No phone number"}
    
    template = get_followup_template(followup_type, channel)
    message = format_template(template, {
        "name": prospect["director_name"].split(",")[0].strip() if prospect["director_name"] else "there",
        "business": prospect["business_name"],
    })
    
    result = send_message(prospect["phone"], message, channel)
    
    # Only record outreach if provider confirmed the send
    if result["ok"]:
        record_outreach(db_conn, prospect_id, channel, "outbound", message, f"followup_{followup_type}")
    
    return {
        "prospect": prospect["business_name"],
        "phone": prospect["phone"],
        "channel": channel,
        "sent": result["ok"],
        "status": result.get("status", "drafted"),
        "stubbed": result.get("stubbed", True),
        "message": message,
    }


if __name__ == "__main__":
    # Test WhatsApp
    print("=== WhatsApp Configuration ===")
    print(f"WhatsApp configured: {WHATSAPP_AVAILABLE and whatsapp_configured()}")
    print(f"WhatsApp module available: {WHATSAPP_AVAILABLE}")
    
    # Test send
    result = send_message("07858358562", "Test message from AI Onboard", "whatsapp")
    print(f"\nSend result: {result}")
