"""Outreach message templates per vertical and pipeline stage."""

# Initial outreach templates (WhatsApp)
INITIAL_TEMPLATES = {
    "nails": {
        "whatsapp": "Hi {name}, I saw your work on Google — really impressive reviews ({rating}★, {reviews} reviews). We're setting up AI assistants for nail techs on WhatsApp that handle enquiries, bookings, and reminders 24/7. Looking for 20 businesses to test it free for 4 weeks. Takes 15 minutes to set up. Interested?",
        "email": "Subject: Free AI setup for {business} — 4-week trial\n\nHi {name},\n\nI found {business} on Google and was impressed by your {rating}★ rating with {reviews} reviews.\n\nWe're setting up AI assistants for nail businesses that handle WhatsApp enquiries, bookings, and reminders automatically — 24/7.\n\nWe're offering 20 businesses a free 4-week trial. Takes 15 minutes to set up.\n\nInterested?\n\nBest,\n[Your name]\nAI Onboard",
    },
    "electrician": {
        "whatsapp": "Hi {name}, we're setting up AI for electricians that answers missed calls, drafts quotes from your price book, and follows up automatically. Looking for 4 electricians in {city} to test it free for 4 weeks. Takes 15 minutes. Interested?",
        "email": "Subject: Free AI setup for {business} — missed call recovery\n\nHi {name},\n\nWe're helping electricians in {city} capture missed calls and follow up on quotes automatically.\n\nThe AI answers when you're on the tools, drafts quotes from your price book, and sends follow-ups at day 2, 5, and 12.\n\nFree 4-week trial for 4 businesses. Takes 15 minutes to set up.\n\nInterested?\n\nBest,\n[Your name]\nAI Onboard",
    },
    "dog_groomers": {
        "whatsapp": "Hi {name}, we're building AI for dog groomers that handles bookings, reminders, and rebooking by breed interval. Looking for 3 groomers in {city} to test free for 4 weeks. Takes 15 minutes. Interested?",
        "email": "Subject: Free AI setup for {business} — breed-aware booking\n\nHi {name},\n\nWe're building an AI assistant for dog groomers that:\n- Answers booking enquiries 24/7\n- Reminds clients at breed-specific intervals\n- Fills cancellation slots from a waiting list\n\nFree 4-week trial for 3 businesses. Takes 15 minutes to set up.\n\nInterested?\n\nBest,\n[Your name]\nAI Onboard",
    },
    "cleaners": {
        "whatsapp": "Hi {name}, we're setting up AI for cleaners that handles recurring bookings, key access instructions, and invoice chasing. Looking for 3 cleaners in {city} to test free for 4 weeks. Takes 15 minutes. Interested?",
        "email": "Subject: Free AI setup for {business} — recurring bookings + invoicing\n\nHi {name},\n\nWe're helping cleaners automate recurring bookings, key access instructions, and invoice chasing.\n\nFree 4-week trial for 3 businesses. Takes 15 minutes to set up.\n\nInterested?\n\nBest,\n[Your name]\nAI Onboard",
    },
    "hair": {
        "whatsapp": "Hi {name}, I saw your work on Google — great reviews. We're setting up AI for hairdressers that handles bookings, reminders, and travel-area checks. Looking for 2 salons in {city} to test free for 4 weeks. Takes 15 minutes. Interested?",
        "email": "Subject: Free AI setup for {business} — booking + reminders\n\nHi {name},\n\nWe're setting up AI assistants for hairdressers that handle WhatsApp enquiries, bookings, and reminders.\n\nFree 4-week trial for 2 businesses. Takes 15 minutes to set up.\n\nInterested?\n\nBest,\n[Your name]\nAI Onboard",
    },
    "beauty": {
        "whatsapp": "Hi {name}, we're setting up AI for beauty therapists that handles bookings, patch test reminders, and aftercare messages. Looking for 2 salons in {city} to test free for 4 weeks. Takes 15 minutes. Interested?",
        "email": "Subject: Free AI setup for {business} — booking + safety compliance\n\nHi {name},\n\nWe're setting up AI assistants for beauty businesses that handle bookings, patch test reminders, and aftercare.\n\nFree 4-week trial for 2 businesses. Takes 15 minutes to set up.\n\nInterested?\n\nBest,\n[Your name]\nAI Onboard",
    },
    "lashes": {
        "whatsapp": "Hi {name}, we're setting up AI for lash techs that handles bookings, allergy declarations, and refill reminders. Looking for 1 lash tech in {city} to test free for 4 weeks. Takes 15 minutes. Interested?",
        "email": "Subject: Free AI setup for {business} — lash bookings + safety\n\nHi {name},\n\nWe're setting up AI assistants for lash businesses that handle bookings, allergy declarations, and refill reminders.\n\nFree 4-week trial. Takes 15 minutes to set up.\n\nInterested?\n\nBest,\n[Your name]\nAI Onboard",
    },
    "car_detailers": {
        "whatsapp": "Hi {name}, we're setting up AI for mobile detailers that handles quote intake, photo collection, and before/after workflows. Looking for 2 detailers in {city} to test free for 4 weeks. Takes 15 minutes. Interested?",
        "email": "Subject: Free AI setup for {business} — quote intake + photo workflow\n\nHi {name},\n\nWe're helping mobile detailers automate quote intake, collect vehicle photos, and manage before/after workflows.\n\nFree 4-week trial for 2 businesses. Takes 15 minutes to set up.\n\nInterested?\n\nBest,\n[Your name]\nAI Onboard",
    },
    "driving_instructors": {
        "whatsapp": "Hi {name}, we're setting up AI for driving instructors that handles lesson booking, pupil progress tracking, and test-date coordination. Looking for 2 instructors in {city} to test free for 4 weeks. Takes 15 minutes. Interested?",
        "email": "Subject: Free AI setup for {business} — lesson booking + progress tracking\n\nHi {name},\n\nWe're setting up AI assistants for driving instructors that handle lesson booking, pupil progress, and test coordination.\n\nFree 4-week trial for 2 businesses. Takes 15 minutes to set up.\n\nInterested?\n\nBest,\n[Your name]\nAI Onboard",
    },
    "gardeners": {
        "whatsapp": "Hi {name}, we're setting up AI for gardeners/window cleaners that handles round scheduling, customer notifications, and invoice chasing. Looking for 1 business in {city} to test free for 4 weeks. Takes 15 minutes. Interested?",
        "email": "Subject: Free AI setup for {business} — round scheduling + invoicing\n\nHi {name},\n\nWe're helping gardeners and window cleaners automate round scheduling, customer notifications, and invoice chasing.\n\nFree 4-week trial. Takes 15 minutes to set up.\n\nInterested?\n\nBest,\n[Your name]\nAI Onboard",
    },
    "weddings": {
        "whatsapp": "Hi {name}, we're setting up AI for wedding vendors that handles lead qualification, proposal follow-up, and supplier referrals. Looking for 1 vendor in {city} to test free for 4 weeks. Takes 15 minutes. Interested?",
        "email": "Subject: Free AI setup for {business} — lead qualification + follow-up\n\nHi {name},\n\nWe're setting up AI assistants for wedding vendors that handle lead qualification, proposal follow-up, and supplier referrals.\n\nFree 4-week trial. Takes 15 minutes to set up.\n\nInterested?\n\nBest,\n[Your name]\nAI Onboard",
    },
}

# Follow-up templates
FOLLOWUP_TEMPLATES = {
    "day2": {
        "whatsapp": "Hi {name}, just checking — did you see my message about the free AI setup? Happy to answer any questions.",
        "email": "Subject: Quick follow-up — free AI setup for {business}\n\nHi {name},\n\nJust checking if you saw my message about the free 4-week trial.\n\nHappy to answer any questions or jump on a quick call.\n\nBest,\n[Your name]",
    },
    "day5": {
        "whatsapp": "Hi {name}, last note from me — if the timing isn't right, no worries. Just let me know and I'll close the file.",
        "email": "Subject: Closing the loop — free AI setup for {business}\n\nHi {name},\n\nJust a final note. If the timing isn't right, no problem at all.\n\nIf you'd like to try it later, just reply to this email.\n\nBest,\n[Your name]",
    },
    "day12": {
        "whatsapp": "Hi {name}, this is my last message. If you'd like to try the free setup in the future, just reply. Otherwise I'll close the file. No hard feelings!",
        "email": "Subject: Last note — free AI setup for {business}\n\nHi {name},\n\nThis is my last message about the free trial.\n\nIf you'd like to try it in the future, just reply to this email.\n\nAll the best,\n[Your name]",
    },
}

# Onboarding check-in templates
ONBOARDING_TEMPLATES = {
    "week2_checkin": "Hi {name}, how's the AI assistant going? Any questions or issues? Reply here or book a 15-min call: [link]",
    "week4_review": "Hi {name}, it's been 4 weeks! Here's what the AI did: [metrics]. If you want to keep it running, it's £20 one-off. If you want ongoing support, that's £50/month. Want to continue?",
}

# Referral template
REFERRAL_TEMPLATE = "Hi {name}, thanks for using AI Onboard! If you refer a friend, you both get a free website (£10 value). Just have them mention your name when they sign up."


def format_template(template: str, data: dict) -> str:
    """Format a template with prospect data."""
    try:
        return template.format(**data)
    except KeyError as e:
        return template  # Return unformatted if missing data


def get_initial_template(vertical: str, channel: str = "whatsapp") -> str:
    """Get initial outreach template for a vertical."""
    templates = INITIAL_TEMPLATES.get(vertical, INITIAL_TEMPLATES["nails"])
    return templates.get(channel, templates.get("whatsapp", ""))


def get_followup_template(followup_type: str, channel: str = "whatsapp") -> str:
    """Get follow-up template."""
    templates = FOLLOWUP_TEMPLATES.get(followup_type, {})
    return templates.get(channel, templates.get("whatsapp", ""))
