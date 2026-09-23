# Car detailers workflow

> The actual day-to-day. What happens, where the pain is, what the AI does.

## The day (research-backed)

| Time | What happens | Pain | AI/WhatsApp solution |
|------|-------------|------|---------------------|
| 7:30–8:00 | Pre-route checks, load van | — | — |
| 8:00–8:15 | Drive to client, GPS check-in | Client asks "where are you?" | Auto-ETA: "On my way! ETA 12 minutes" |
| 8:15–10:30 | Detail #1 | Can't send photos while working | After: auto-send before/after photos |
| 10:30–11:00 | Drive to #2 | — | Route optimised |
| 11:00–13:00 | Detail #2 | — | — |
| 13:00–13:30 | Lunch + van clean | — | — |
| 13:30–15:30 | Detail #3 | — | — |
| 16:00–18:00 | Detail #4 | — | — |
| 18:00–19:00 | End-of-day: sanitize, invoicing | Hours of admin | AI drafts invoices from job notes |

## Quote intake flow (WhatsApp)

```
Customer sends: "Hi, I need my car detailed"
  ↓
AI: "What's the vehicle? What service are you after?"
    Options: Basic (£80) | Premium (£120) | Ceramic Coating (£250)
  ↓
Customer sends photos of vehicle
  ↓
AI: "Based on the photos, I'd recommend [service] at [price].
     I'm in your area on [dates]. Shall I book you in?"
  ↓
Customer confirms → deposit link sent → booked
  ↓
Confirmation: "You're booked for [date] at [time].
I'll come to you. Address: [address].
Deposit of [£X] received. Remaining balance due on completion."
```

## Before/after photo workflow

```
Arrival at job
  ↓
GPS clock-in (auto-logged)
  ↓
Take BEFORE photos: all 4 angles + interior + any damage
  ↓
Photos auto-tagged: GPS + timestamp + vehicle reg
  ↓
Detail
  ↓
Take AFTER photos (same angles)
  ↓
Auto-generate comparison: before | after
  ↓
Send to customer via WhatsApp:
  "All done! Here's the difference. Tap to pay: [link]"
  ↓
Include: "If you're happy, a quick Google review means a lot: [link]"
  ↓
Customer shares on social = free marketing
```

## GPS tracking for mobile detailers

| Feature | How it works |
|---------|-------------|
| Auto check-in | GPS detects arrival at client address |
| On-my-way alert | Auto-text 15 min before with ETA |
| Route optimisation | AI orders stops by postcode + traffic |
| Mileage tracking | Auto-log for tax deductions |
| Offline mode | Cache bookings, sync when reconnected |
| Revenue per mile | Know if the day was worth the miles |

## Repeat-service upsell workflow

```
Detail completed → job logged with service type + vehicle
  ↓
AI calculates next service window:
  - Basic: every 3 months
  - Premium: every 4 months
  - Ceramic coating: every 12 months (top-up)
  ↓
30 days before due: "Hi [name], your [service] is due next month.
I have availability on [dates]. Want me to book you in?"
  ↓
If no response: follow-up at 14 days, 7 days
  ↓
If booked: send confirmation + deposit link
```

## Damage documentation flow

```
Before photos reveal existing damage
  ↓
AI flags to detailer: "Note: scratch on rear bumper, kerb mark on front left alloy"
  ↓
Detailer confirms or adds to notes
  ↓
AI includes in quote: "Your vehicle has existing [damage]. This won't be corrected by [service].
If you'd like it addressed, I can add [repair] for [price]."
  ↓
Protects detailer from blame + upsells
```

## What the AI agent does at each step

| Step | AI action | Human action |
|------|-----------|-------------|
| Enquiry received | Qualifies vehicle, service, location, timing | Nothing |
| Photos received | Drafts quote with service recommendation | Approves and sends |
| Quote sent | Sends follow-up at day 2/5/12 | Nothing |
| Job booked | Sends confirmation + deposit link | Nothing |
| Arrival (GPS) | Auto check-in, alerts client | Nothing |
| Job completed | Sends before/after photos + invoice + pay link | Reviews and approves photos |
| Invoice unpaid | Sends payment reminders at 7/14/28 days | Nothing |
| Service due | Sends repeat-service reminder at 30/14/7 days | Nothing |
| Job done | Sends Google review request | Nothing |

## Key metrics

| Metric | Target | How |
|--------|--------|-----|
| Quote-to-booking rate | >60% | Fast response + photos |
| Before/after photo rate | 100% | Auto-prompted at job completion |
| Revenue per day | £300+ | 3–4 details × £80–120 |
| Route efficiency | <20% drive time | AI route optimisation |
| Google reviews | >50 | Request at photo delivery |
| Repeat booking rate | >40% | Auto-reminders at service interval |
| Damage documentation rate | 100% | Auto-flagged from before photos |

## What the top 10% do differently

- Send before/after photos within 10 minutes of finishing — not end of day
- Always upsell ceramic coating on premium details — "Your paint would really benefit"
- Include a damage report with every quote — sets expectations, avoids disputes
- Offer monthly packages (£280/month for 2 details) — locks in recurring revenue
- Take 360° video walkthrough on high-ticket jobs — irrefutable proof of condition
- Collect Google review on-site: "Mind leaving a quick review? I'll send you the link now"
- Track cost-per-mile on every route — drop jobs that don't hit £1.50/mile threshold
