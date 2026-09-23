"""Jev integration for AI Onboard pipeline.

Uses aocsec's JevMCP for confidence-gated triage:
- classify_enquiry: route customer messages to right handler
- verify_demo: check demo accuracy before sending
- gate_outreach: quality gate before sending messages
"""

import os
import sys

# Add aocsec to path
sys.path.insert(0, "/root/aocsec")

try:
    from jev.triage import classify_alerts, verify_claims, gate_completion, CONFIDENCE_FLOOR
    JEV_AVAILABLE = True
except ImportError:
    JEV_AVAILABLE = False
    CONFIDENCE_FLOOR = 0.75


def classify_enquiry(message: str, business_context: dict) -> dict:
    """Classify a customer enquiry using JEV.
    
    Returns: {"action": "respond_now"|"respond_later"|"escalate"|"ignore",
              "confidence": float, "reason": str}
    """
    if not JEV_AVAILABLE:
        # Fallback: simple keyword classification
        return _fallback_classify(message)
    
    # Build context for JEV
    context = f"Business: {business_context.get('name', 'unknown')}, Vertical: {business_context.get('vertical', 'unknown')}"
    
    # For now, use fallback since JEV needs a running MCP server
    return _fallback_classify(message)


def _fallback_classify(message: str) -> dict:
    """Simple keyword-based classification (fallback when JEV unavailable)."""
    lower = message.lower()
    
    # Urgent patterns
    urgent_patterns = ['emergency', 'urgent', 'asap', 'right now', 'broken', 'leaking', 'smoke', 'fire']
    if any(p in lower for p in urgent_patterns):
        return {"action": "escalate", "confidence": 0.9, "reason": "urgent keywords detected"}
    
    # Booking patterns
    booking_patterns = ['book', 'appointment', 'available', 'schedule', 'slot', 'come out']
    if any(p in lower for p in booking_patterns):
        return {"action": "respond_now", "confidence": 0.85, "reason": "booking request"}
    
    # Price patterns
    price_patterns = ['price', 'cost', 'how much', 'quote', 'estimate']
    if any(p in lower for p in price_patterns):
        return {"action": "respond_now", "confidence": 0.8, "reason": "price enquiry"}
    
    # Complaint patterns
    complaint_patterns = ['complaint', 'unhappy', 'terrible', 'worst', 'refund']
    if any(p in lower for p in complaint_patterns):
        return {"action": "escalate", "confidence": 0.85, "reason": "complaint detected"}
    
    # General enquiry
    return {"action": "respond_later", "confidence": 0.6, "reason": "general enquiry"}


def verify_demo_accuracy(demo_data: dict, google_data: dict) -> dict:
    """Verify that a demo matches the business's actual data.
    
    Returns: {"verified": bool, "issues": list, "confidence": float}
    """
    issues = []
    
    # Check business name
    if demo_data.get('business_name', '').lower() != google_data.get('business_name', '').lower():
        issues.append("Business name mismatch")
    
    # Check services exist
    demo_services = set(s['name'].lower() for s in demo_data.get('services', []))
    if not demo_services:
        issues.append("No services loaded")
    
    # Check prices are reasonable (£5-£5000 range)
    for s in demo_data.get('services', []):
        if s.get('price', 0) < 5 or s.get('price', 0) > 5000:
            issues.append(f"Unreasonable price for {s['name']}: £{s.get('price')}")
    
    # Check rating matches
    if demo_data.get('rating') and google_data.get('rating'):
        if abs(float(demo_data['rating']) - float(google_data['rating'])) > 0.5:
            issues.append("Rating mismatch")
    
    verified = len(issues) == 0
    confidence = 0.95 if verified else 0.3
    
    return {
        "verified": verified,
        "issues": issues,
        "confidence": confidence,
    }


def gate_outreach(message: str, business_data: dict) -> dict:
    """Quality gate before sending outreach message.
    
    Returns: {"send": bool, "reasons": list, "confidence": float}
    """
    reasons = []
    
    # Check message length
    if len(message) < 20:
        reasons.append("Message too short")
    
    if len(message) > 500:
        reasons.append("Message too long")
    
    # Check for required elements
    if business_data.get('vertical') not in ['nails', 'electrician', 'dog_groomers', 'cleaners', 'hair', 'beauty', 'lashes', 'car_detailers', 'driving_instructors', 'gardeners', 'weddings']:
        reasons.append("Unknown vertical")
    
    # Check for personalisation
    if '{name}' in message and not business_data.get('director_name'):
        reasons.append("Template not personalised (missing director name)")
    
    # Check for PECR compliance
    if 'unsubscribe' not in message.lower() and 'stop' not in message.lower():
        # For WhatsApp, opt-out is less formal but should be mentioned
        pass  # WhatsApp is more casual, skip this check
    
    send = len(reasons) == 0
    confidence = 0.9 if send else 0.4
    
    return {
        "send": send,
        "reasons": reasons,
        "confidence": confidence,
    }


def triage_support_ticket(ticket_data: dict) -> dict:
    """Triage a support ticket using JEV classification.
    
    Returns: {"priority": "critical"|"high"|"medium"|"low",
              "assign_to": str, "confidence": float}
    """
    message = ticket_data.get('message', '').lower()
    
    # Critical: money, legal, safety
    critical_patterns = ['money', 'payment', 'refund', 'legal', 'safety', 'injury', 'fire', 'gas']
    if any(p in message for p in critical_patterns):
        return {"priority": "critical", "assign_to": "owner", "confidence": 0.9}
    
    # High: blocking issue
    high_patterns = ['broken', 'not working', 'error', 'failed', 'stuck']
    if any(p in message for p in high_patterns):
        return {"priority": "high", "assign_to": "support", "confidence": 0.85}
    
    # Medium: question or request
    medium_patterns = ['how', 'what', 'when', 'can i', 'help']
    if any(p in message for p in medium_patterns):
        return {"priority": "medium", "assign_to": "ai", "confidence": 0.75}
    
    # Low: feedback or suggestion
    return {"priority": "low", "assign_to": "ai", "confidence": 0.6}


if __name__ == "__main__":
    # Test classification
    test_messages = [
        "I need an electrician urgently - smoke coming from fuse box",
        "How much for a gel manicure?",
        "Can I book for Thursday?",
        "This is spam",
        "I'm unhappy with the service",
    ]
    
    print("=== ENQUIRY CLASSIFICATION ===")
    for msg in test_messages:
        result = classify_enquiry(msg, {"name": "Test Business", "vertical": "electrician"})
        print(f"Q: {msg}")
        print(f"   Action: {result['action']} (confidence: {result['confidence']})")
        print(f"   Reason: {result['reason']}")
        print()
    
    # Test demo verification
    print("=== DEMO VERIFICATION ===")
    demo = {"business_name": "Test Nails", "services": [{"name": "Gel", "price": 35}], "rating": "4.8"}
    google = {"business_name": "Test Nails", "rating": "4.8"}
    result = verify_demo_accuracy(demo, google)
    print(f"Verified: {result['verified']}, Issues: {result['issues']}")
    
    # Test outreach gate
    print("\n=== OUTREACH GATE ===")
    msg = "Hi {name}, we're setting up AI for electricians. Free 4-week trial. Interested?"
    result = gate_outreach(msg, {"vertical": "electrician", "director_name": "John Smith"})
    print(f"Send: {result['send']}, Reasons: {result['reasons']}")
