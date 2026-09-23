"""Outreach tracking and management."""

from datetime import datetime, timedelta
from pipeline.db import get_db, record_outreach, schedule_followup
from pipeline.templates import get_initial_template, get_followup_template, format_template


def _check_consent(db_conn, prospect_id: int) -> dict:
    """Check if prospect has given marketing consent.

    Returns {"ok": bool, "reason": str}
    """
    # Check for explicit opt-out / suppression
    row = db_conn.execute(
        "SELECT stage FROM prospects WHERE id=?", (prospect_id,)
    ).fetchone()
    if row and row["stage"] == "churned":
        return {"ok": False, "reason": "prospect_churned"}

    # Check contacts table for do_not_contact or TPS block
    contact = db_conn.execute(
        """SELECT outcome FROM contact_attempts
           WHERE contact_id IN (
               SELECT id FROM contacts WHERE prospect_id=?
           )
           ORDER BY attempted_at DESC LIMIT 1""",
        (prospect_id,)
    ).fetchone()
    if contact and contact["outcome"] == "do_not_contact":
        return {"ok": False, "reason": "do_not_contact"}

    # Check if TPS blocked
    suppressed = db_conn.execute(
        """SELECT 1 FROM tps_checks
           WHERE prospect_id=? AND result='blocked' LIMIT 1""",
        (prospect_id,)
    ).fetchone()
    if suppressed:
        return {"ok": False, "reason": "tps_blocked"}

    return {"ok": True, "reason": "consent_ok"}


def _cancel_pending_followups(db_conn, prospect_id: int):
    """Cancel all pending follow-ups for a prospect (e.g. after opt-out)."""
    db_conn.execute(
        "UPDATE followups SET status='skipped' WHERE prospect_id=? AND status='pending'",
        (prospect_id,)
    )


def start_outreach(db_conn, prospect_id: int, channel: str = "whatsapp") -> dict:
    """Start outreach to a prospect.

    Checks consent and suppression before recording any outbound message.
    Does NOT record outreach as "sent" unless messaging provider confirms.
    """
    prospect = db_conn.execute("SELECT * FROM prospects WHERE id=?", (prospect_id,)).fetchone()
    if not prospect:
        return {"error": "Prospect not found"}
    
    if prospect["stage"] != "new":
        return {"error": f"Prospect already in stage: {prospect['stage']}"}

    # P0-3: Check consent and suppression before any outreach
    consent = _check_consent(db_conn, prospect_id)
    if not consent["ok"]:
        return {"error": f"Outreach blocked: {consent['reason']}"}
    
    # Get template
    template = get_initial_template(prospect["vertical"], channel)
    
    # Format with prospect data
    message = format_template(template, {
        "name": prospect["director_name"].split(",")[0].strip() if prospect["director_name"] else "there",
        "business": prospect["business_name"],
        "vertical": prospect["vertical"],
        "city": prospect["city"],
        "rating": prospect["rating"] or "N/A",
        "reviews": prospect["review_count"] or "N/A",
    })
    
    # P0-3: Send via messaging provider — only record if provider confirms
    from pipeline.messaging import send_message
    result = send_message(prospect["phone"], message, channel)

    if not result["ok"]:
        return {
            "prospect": prospect["business_name"],
            "channel": channel,
            "sent": False,
            "status": result.get("status", "drafted"),
            "note": result.get("note", "Message not sent — provider did not confirm"),
        }

    # Provider confirmed — record outreach
    outreach_id = record_outreach(db_conn, prospect_id, channel, "outbound", message, f"initial_{channel}")
    
    # Schedule follow-ups
    now = datetime.now()
    schedule_followup(db_conn, prospect_id, "send_message", channel, "day2", now + timedelta(days=2))
    schedule_followup(db_conn, prospect_id, "send_message", channel, "day5", now + timedelta(days=5))
    schedule_followup(db_conn, prospect_id, "send_message", channel, "day12", now + timedelta(days=12))
    
    db_conn.commit()
    
    return {
        "outreach_id": outreach_id,
        "prospect": prospect["business_name"],
        "channel": channel,
        "message": message,
        "sent": True,
        "status": result.get("status", "sent"),
        "followups_scheduled": 3,
    }


def record_reply(db_conn, prospect_id: int, message: str, channel: str = "whatsapp") -> dict:
    """Record an inbound reply from a prospect."""
    outreach_id = record_outreach(db_conn, prospect_id, channel, "inbound", message)
    
    # Update sentiment
    positive_words = ["interested", "yes", "sure", "love", "great", "perfect", "thanks"]
    negative_words = ["no", "not interested", "busy", "later", "stop"]
    
    msg_lower = message.lower()
    if any(w in msg_lower for w in positive_words):
        sentiment = "positive"
        # Move to interested stage
        db_conn.execute(
            "UPDATE prospects SET stage='interested', stage_changed_at=? WHERE id=?",
            (datetime.now().isoformat(), prospect_id)
        )
    elif any(w in msg_lower for w in negative_words):
        sentiment = "negative"
        # Move to churned stage and cancel pending follow-ups
        db_conn.execute(
            "UPDATE prospects SET stage='churned', stage_changed_at=? WHERE id=?",
            (datetime.now().isoformat(), prospect_id)
        )
        _cancel_pending_followups(db_conn, prospect_id)
    else:
        sentiment = "neutral"
    
    db_conn.execute(
        "UPDATE conversations SET sentiment=? WHERE prospect_id=?",
        (sentiment, prospect_id)
    )
    
    # Cancel pending follow-ups if replied (any reply, not just negative)
    if sentiment != "neutral":
        db_conn.execute(
            "UPDATE followups SET status='skipped' WHERE prospect_id=? AND status='pending'",
            (prospect_id,)
        )
    
    db_conn.commit()
    
    return {
        "outreach_id": outreach_id,
        "sentiment": sentiment,
        "stage": db_conn.execute("SELECT stage FROM prospects WHERE id=?", (prospect_id,)).fetchone()["stage"],
    }


def get_outreach_queue(db_conn, limit: int = 50) -> list:
    """Get prospects ready for outreach."""
    return db_conn.execute(
        """SELECT p.*, c.first_contact_at, c.last_contact_at, c.response_count, c.sentiment, c.next_action
           FROM prospects p 
           LEFT JOIN conversations c ON p.id = c.prospect_id
           WHERE p.stage = 'new' 
           ORDER BY p.score DESC 
           LIMIT ?""",
        (limit,)
    ).fetchall()


def get_followup_queue(db_conn, limit: int = 50) -> list:
    """Get prospects with due follow-ups."""
    return db_conn.execute(
        """SELECT f.*, p.business_name, p.phone, p.vertical, p.city, p.director_name
           FROM followups f 
           JOIN prospects p ON f.prospect_id = p.id
           WHERE f.status = 'pending' AND f.scheduled_at <= ?
           ORDER BY f.scheduled_at
           LIMIT ?""",
        (datetime.now().isoformat(), limit)
    ).fetchall()


def get_conversion_candidates(db_conn) -> list:
    """Get prospects ready for conversion to paid."""
    return db_conn.execute(
        """SELECT p.*, o.started_at, o.week2_checkin_at, o.week4_review_at, o.feedback
           FROM prospects p 
           JOIN onboardings o ON p.id = o.prospect_id
           WHERE p.stage = 'onboarded' AND o.status = 'active'
           AND o.week4_review_at <= ?
           ORDER BY o.week4_review_at""",
        (datetime.now().isoformat(),)
    ).fetchall()


def start_onboarding(db_conn, prospect_id: int) -> dict:
    """Start free onboarding for a prospect."""
    now = datetime.now()
    db_conn.execute(
        """INSERT INTO onboardings (prospect_id, started_at, week2_checkin_at, week4_review_at, status)
           VALUES (?, ?, ?, ?, 'active')""",
        (prospect_id, now.isoformat(), (now + timedelta(weeks=2)).isoformat(), (now + timedelta(weeks=4)).isoformat())
    )
    db_conn.execute(
        "UPDATE prospects SET stage='onboarded', stage_changed_at=? WHERE id=?",
        (now.isoformat(), prospect_id)
    )
    
    # Schedule check-ins
    schedule_followup(db_conn, prospect_id, "check_in", "whatsapp", "week2_checkin", now + timedelta(weeks=2))
    schedule_followup(db_conn, prospect_id, "review", "whatsapp", "week4_review", now + timedelta(weeks=4))
    
    db_conn.commit()
    return {"status": "onboarding_started", "prospect_id": prospect_id}


def convert_to_paid(db_conn, prospect_id: int, amount: float, package: str) -> dict:
    """Convert an onboarding to a paid customer."""
    now = datetime.now()
    db_conn.execute(
        """UPDATE onboardings SET converted_to_paid=1, paid_amount=?, paid_at=?, status='completed'
           WHERE prospect_id=? AND status='active'""",
        (amount, now.isoformat(), prospect_id)
    )
    db_conn.execute(
        "UPDATE prospects SET stage='paying', stage_changed_at=? WHERE id=?",
        (now.isoformat(), prospect_id)
    )
    db_conn.commit()
    return {"status": "converted", "prospect_id": prospect_id, "amount": amount, "package": package}


def get_pipeline_summary(db_conn) -> dict:
    """Get summary of pipeline status."""
    stages = db_conn.execute(
        "SELECT stage, COUNT(*) as count FROM prospects GROUP BY stage"
    ).fetchall()
    
    stage_counts = {row["stage"]: row["count"] for row in stages}
    total = sum(stage_counts.values())
    
    # Outreach stats
    today = datetime.now().date().isoformat()
    messages_today = db_conn.execute(
        "SELECT COUNT(*) FROM outreach WHERE sent_at>=?", (today,)
    ).fetchone()[0]
    
    responses_today = db_conn.execute(
        "SELECT COUNT(*) FROM outreach WHERE direction='inbound' AND sent_at>=?", (today,)
    ).fetchone()[0]
    
    # Onboarding stats
    active_onboardings = db_conn.execute(
        "SELECT COUNT(*) FROM onboardings WHERE status='active'"
    ).fetchone()[0]
    
    conversions = db_conn.execute(
        "SELECT COUNT(*), COALESCE(SUM(paid_amount),0) FROM onboardings WHERE converted_to_paid=1"
    ).fetchone()
    
    # Conversion rate
    contacted = stage_counts.get("contacted", 0) + stage_counts.get("responded", 0) + stage_counts.get("interested", 0) + stage_counts.get("onboarded", 0) + stage_counts.get("paying", 0)
    response_rate = (stage_counts.get("responded", 0) + stage_counts.get("interested", 0) + stage_counts.get("onboarded", 0) + stage_counts.get("paying", 0)) / contacted * 100 if contacted > 0 else 0
    
    return {
        "total_prospects": total,
        "stages": stage_counts,
        "contacted": contacted,
        "response_rate": round(response_rate, 1),
        "messages_today": messages_today,
        "responses_today": responses_today,
        "active_onboardings": active_onboardings,
        "conversions": conversions[0],
        "total_revenue": conversions[1],
    }
