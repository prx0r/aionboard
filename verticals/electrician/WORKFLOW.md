# Electrician workflow

> The actual day-to-day. What happens, where the pain is, what the AI does.

## The day (research-backed)

| Time | What happens | Pain | AI/WhatsApp solution |
|------|-------------|------|---------------------|
| 6:00–6:30 | Check phone, emails, WhatsApp | 4 missed calls overnight | AI answered: "Sorry I missed you, I'm on a job. Send photos + details and I'll quote within the hour" |
| 6:30–7:15 | Drive to first job / supply run | — | Route optimised by AI |
| 7:30–12:00 | Job 1 | Can't answer phone while on tools | AI answers every call: qualifies job type, captures photos, drafts quote |
| 12:00–12:30 | Lunch + admin | Responding to messages | AI has already drafted quotes from morning calls — approve and send |
| 12:30–17:00 | Job 2/3 | — | — |
| 17:30–19:00 | "The Second Shift" — paperwork | Certificates, invoicing, compliance | AI drafts invoices from job notes, auto-sends EICR reminders |
| 19:00–21:00 | Chasing payments | Awkward conversations | AI sends payment reminders at 7/14/28 days |
| 21:00+ | WhatsApp enquiries from 9-5 workers | Evening messages | AI handles: "Thanks for your message. I'll get back to you first thing" |

## The missed-call recovery flow

```
Call comes in → AI answers
  ↓
Qualifies: EICR? EV charger? Fault? New build? Emergency?
  ↓
If emergency: "I'll call you back in 5 minutes" + alert electrician
If standard: "Send me photos and I'll have a price to you within the hour"
  ↓
Customer sends photos via WhatsApp
  ↓
AI drafts quote from price book → electrician approves → sent
  ↓
Day 2: Auto follow-up if no response
Day 5: "Currently booking 2 weeks out. If you'd like it this month, let me know"
Day 12: "Last note from me. If timing isn't right, no problem"
```

## Quote follow-up sequence (WhatsApp)

| Day | Message | Purpose |
|-----|---------|---------|
| 0 | Quote sent with pay-deposit link | Commitment |
| 2 | "Just checking the quote came through OK. Happy to answer questions." | Gentle nudge |
| 5 | "Currently booking 2 weeks out. If you'd like it this month, let me know." | Urgency |
| 12 | "Last note from me. If timing isn't right, no problem — just let me know and I'll close the file." | Final |

## The invoice + payment flow

```
Job completed on site
  ↓
AI drafts invoice from job notes + price book
  ↓
Electrician approves on phone
  ↓
Invoice sent via WhatsApp with Stripe pay link
  ↓
"Thanks for choosing [business]. Tap to pay: [link]"
  ↓
If unpaid at 7 days: "Friendly reminder — invoice [X] is outstanding. Tap to pay: [link]"
If unpaid at 14 days: "Second reminder — invoice [X] is now 14 days overdue"
If unpaid at 28 days: "Final reminder before we pass to our accounts team"
```

## OZEV grant workflow

```
Customer enquires about EV charger
  ↓
AI qualifies: home owner? off-street parking? eligible property?
  ↓
If eligible: "Great! You qualify for the £500 OZEV grant. I'll include it in your quote."
  ↓
Customer applies online → voucher issued
  ↓
Electrician installs → photographs chargepoint + parking + building
  ↓
Electrician submits voucher with: invoice, photos, EICR, DNO notification
  ↓
Grant deducted from invoice — customer pays net amount
```

## EICR rebooking workflow

```
EICR issued with 5-year expiry date
  ↓
AI logs expiry date in system
  ↓
90 days before expiry: "Hi [name], your EICR expires [date]. Want me to book your retest?"
  ↓
30 days before: "Your EICR expires in 1 month. I have availability on [dates]."
  ↓
7 days before: "Last chance — your EICR expires [date]. After that, your landlord insurance may be void."
  ↓
If no response: flag to electrician for manual follow-up
```

## What the AI agent does at each step

| Step | AI action | Human action |
|------|-----------|-------------|
| Call missed | Answers, qualifies, captures details | Calls back if emergency |
| Photos received | Drafts quote from price book | Approves and sends |
| Quote sent | Sends follow-up at day 2/5/12 | Nothing |
| Job completed | Drafts invoice, sends with pay link | Approves |
| Invoice unpaid | Sends payment reminders at 7/14/28 days | Nothing |
| EICR expiry | Sends rebooking reminder at 90/30/7 days | Nothing |
| Job done | Sends Google review request | Nothing |

## Key metrics

| Metric | Target | How |
|--------|--------|-----|
| Missed call capture rate | 100% | AI answers every call |
| Quote response time | <1 hour | AI drafts from photos |
| Quote follow-up rate | 100% (3 touches) | Automated |
| Invoice payment time | <7 days | Auto-reminders |
| EICR rebook rate | >80% | Expiry alerts |
| Revenue per day | £400+ | 2–3 jobs × £200–350 |

## What the top 10% do differently

- Quote within 30 minutes of receiving photos, not 24 hours
- Always include 3 pricing tiers (good/better/best) in every quote
- Send before/after photos on every job — builds trust and referral
- Collect Google review on site, not a week later ("Mind leaving a quick review while it's fresh?")
- Follow up every completed job with a 12-month warranty reminder
- Track EICR expiry dates proactively — 60% of rebookings come from expiry alerts
- Offer payment plans on jobs over £500 — reduces sticker shock, increases close rate
