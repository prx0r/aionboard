# Lash and brow artist workflow

> The actual day-to-day. What happens, where the pain is, what the AI does.

## The day (research-backed)

| Time | What happens | Pain | AI/WhatsApp solution |
|------|-------------|------|---------------------|
| 8:30-9:00 | Prep station, check appointment book, verify patch tests | Can't remember who has valid patch tests on file | WhatsApp: "Your day: 9am classic fill (Zara — patch test OK), 10:30 volume full set (new client Priya — PATCH TEST NEEDED), 1pm lash lift + tint (Megan — patch test OK), 2:30 brow lamination (Chloe — no patch test required), 4pm hybrid fill (Aisha — patch test OK)" |
| 9:00-10:00 | Client 1: Classic infill (60 min) | — | — |
| 10:00-10:30 | Sanitize station, restock lashes/adhesive | — | None (physical task) |
| 10:30-12:30 | Client 2: Volume full set (new client, 120 min) | New client arrived without doing patch test | AI blocked this: "Priya's appointment cannot proceed — no patch test on file. Rescheduled to Friday after patch test today." |
| 12:30-1:00 | Lunch + DMs | 12 DMs: "how much for lashes?", "do you do volume?", "can I book Saturday?" | AI handles: answers prices, shows portfolio, offers slots, collects deposit |
| 1:00-2:00 | Client 3: Lash lift + tint (60 min) | — | — |
| 2:15-2:30 | Room turnover | — | None |
| 2:30-3:30 | Client 4: Brow lamination (60 min) | — | — |
| 3:45-4:45 | Client 5: Hybrid infill (60 min) | — | — |
| 5:30-6:00 | End-of-day admin | Forgot to note who needs infills next week | AI: "Infills due next week: Zara (classic, Fri), Aisha (hybrid, Sat). Ready to send reminders?" |

## The 5-message WhatsApp sequence per visit

1. **Booking confirmation** — "You're booked for volume lash extensions (full set) on Thursday 10:30am at [salon]. Deposit of £25 collected. Important: this treatment requires a patch test 24-48hr before — we'll arrange it."
2. **Patch test reminder (48hr before)** — "Hi Priya! Your patch test is needed before your lash appointment. Drop in today or tomorrow between 9am-5pm. Takes 5 minutes."
3. **24hr reminder** — "All set for tomorrow! Your volume lash appointment is at 10:30am. Please arrive with clean, makeup-free lashes. No waterproof mascara for 24hr before. See you!"
4. **Post-service** — "Thanks Priya! Your new lashes look gorgeous. Aftercare: no water for 4hr, no oil-based products for 24hr, brush lashes daily with the spoolie provided. Avoid rubbing eyes. Leave a review: [Google link]. Book your first infill in 2-3 weeks: [booking link]"
5. **Infill reminder (week 2-3)** — "Hi Priya! Your lashes will be needing a fill soon to keep them full. Book your infill: [link]. Classic fills are £25-35, volume £30-45."

## Infill cycle automation

| Service | Infill cycle | First reminder at | Revenue per visit |
|---------|-------------|-------------------|-------------------|
| Classic lashes | 2-3 weeks | Week 2 (day 14) | £25-35 |
| Volume lashes | 2-3 weeks | Week 2 (day 14) | £30-45 |
| Hybrid lashes | 2-3 weeks | Week 2 (day 14) | £28-40 |
| Lash lift | 6-8 weeks | Week 6 (day 42) | £40-55 |
| Lash tint | 3-4 weeks | Week 3 (day 21) | £15-20 |
| Brow lamination | 6-8 weeks | Week 6 (day 42) | £35-50 |
| Brow tint | 4-6 weeks | Week 4 (day 28) | £12-18 |
| Brow shaping | 3-4 weeks | Week 3 (day 21) | £10-15 |

## Allergy declaration flow (AI-managed, mandatory for new clients)

| Step | AI collects | Why | GDPR note |
|------|------------|-----|-----------|
| Previous lash experience | "Have you had lash extensions before? When and where?" | Safety baseline | Standard data |
| Known allergies | "Any known allergies? (latex, formaldehyde, adhesives, eye products)" | Prevents reactions | Standard data |
| Eye conditions | "Any eye conditions? (dry eye, blepharitis, conjunctivitis, styes)" | May affect application | Special category if medical |
| Medications | "Any medications that affect lashes? (Latisse, steroids, chemo)" | May affect retention | Special category if medical |
| Pregnancy | "Are you pregnant or breastfeeding? (adhesive fumes consideration)" | Safety precaution | Special category |
| Patch test result | Records: date, product, result (clear/reaction) | Legal requirement | Special category — medical record |

**GDPR special category note:** Allergy and medical records are GDPR special category data (Article 9). Must have explicit consent, stored securely, retained only as long as necessary, never in chat screenshots.

## What the AI agent does at each step

| Step | What AI does | What human does |
|------|-------------|----------------|
| Enquiry arrives | Answers price Qs, shows portfolio, collects allergy declaration for new clients, offers slots, collects deposit | None |
| Booking confirmed | Sends confirmation + patch test flag + deposit receipt | None |
| Patch test due (48hr before) | Sends drop-in reminder | None |
| Patch test completed | Records result, confirms or blocks appointment | Performs patch test, reports result |
| 24hr before | Sends prep instructions (clean lashes, no mascara) | None |
| During treatment | — | Applies lashes, records products used, takes before/after |
| Post-service | Sends aftercare + review request + infill booking link | None |
| Week 2-3 | Sends infill reminder | None |
| Infill overdue (week 4) | "Your lashes are looking sparse! Book this week to maintain fullness" | None |
| 60/90 day lapse | Win-back: "We miss you! Here's what's new in our lash menu" | None |

## The intake form (WhatsApp conversation)

AI collects this BEFORE the appointment:

1. **Treatment desired** — "Classic, volume, or hybrid lashes? Or lash lift, tint, or brow treatment?"
2. **New client check** — "Have you been to us before? If not, we'll need a quick allergy form."
3. **Allergy declaration** — Full allergy flow (see above) — mandatory for new clients
4. **Reference photos** — "What style are you after? Natural, dramatic, wispy, cat-eye? Send inspo photos!"
5. **Eye shape/preference** — "What's your eye shape? Helps me recommend the right style."
6. **Preferred date/time** — "When works best? [available slots] or book: [link]"
7. **Deposit payment** — "To secure your slot: £[amount]: [Stripe link]"

## Key metrics

| Metric | Target | How to measure |
|--------|--------|----------------|
| DM response time | <2 min | AI logs timestamps |
| No-show rate | <3% | Deposits + reminders |
| Patch test compliance | 100% | AI blocks bookings without valid test |
| Infill rebook rate | >80% | 2-3 week reminders → booking conversion |
| Review rate | >30% | Post-service WhatsApp → Google link clicks |
| Revenue per day | £200+ | 4-5 clients x avg £30-50 treatment value |
| Allergy record completeness | 100% new clients | AI enforces before booking confirmed |
| Retention rate (monthly) | >85% | Track active clients month-over-month |

## What the top 10% do differently

- **Allergy form at first DM, not at booking** — catches issues before deposit, avoids last-minute cancellations
- **Infill urgency messaging** — "Your lashes are looking sparse!" at week 4 converts better than gentle reminders
- **Before/after photos every infill** — shows lash health over time, builds trust, creates portfolio content
- **Lash care kit upsell** — "Your aftercare kit: cleanser, brush, sealant. £15 with your next infill." (AI suggests at post-service)
- **Membership/package model** — "Lash club: 4 infills/month for £90 (save £30)" (AI promotes to repeat clients)
- **Seasonal style prompts** — "Summer lash menu: waterproof mascara-safe options available" (AI sends seasonal to full list)
- **Retention tracking per client** — AI tracks which clients retain well vs poor, adjusts appointment spacing accordingly
