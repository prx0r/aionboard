# Nail technician workflow

> The actual day-to-day. What happens, where the pain is, what the AI does.

## The day (research-backed)

| Time | What happens | Pain | AI/WhatsApp solution |
|------|-------------|------|---------------------|
| 8:30-9:00 | Station setup, check appointment book | Can't see day at a glance; running late from school run | WhatsApp: "Your day: 9am gel fill (Sarah), 10:15 full set (new client Emma), 12:30 pedicure (Megan), 2pm acrylic fill + art (Priya), 3:30 gel manicure (Chloe), 5pm gel fill (Aisha)" |
| 9:00-10:00 | Client 1: Gel infill (55 min) | — | — |
| 10:00-10:15 | Sanitize station, restock files/buffs | Forgets which products ran low | None (physical task) |
| 10:15-11:45 | Client 2: Full set (new client, 90 min) | New client needs consultation; arrives without reference photos | Pre-arrival: WhatsApp collects reference photos, nail length preference, allergy info, service confirmed |
| 11:45-12:30 | Lunch + respond to DMs | 20 DMs unanswered, losing bookings to someone who replies faster | AI handles DMs 24/7: price, availability, deposit, confirmation |
| 12:30-1:45 | Client 3: Spa pedicure | — | — |
| 2:00-3:15 | Client 4: Acrylic fill + nail art | — | — |
| 3:30-4:15 | Client 5: Gel manicure | — | — |
| 5:00-5:45 | Client 6 | — | — |
| 6:30-7:00 | Close + admin | After-hours DM replies until 10pm; forgot to invoice for art add-on | AI handles after-hours: "I'll get back to you first thing." AI flags missed add-ons on invoice |

## The 5-message WhatsApp sequence per visit

1. **Booking confirmation** — "You're booked for gel infill on Thursday 2pm at [salon name]. Deposit of £10 collected. See you then!"
2. **48hr reminder** — "Hi Sarah! Just a reminder: your gel infill is tomorrow at 2pm. Reply YES to confirm or tap here to reschedule: [link]"
3. **2hr reminder** — "See you at 2pm today! Quick reminder: we're at [address]. Parking: [street nearby / salon car park]. See you soon!"
4. **Post-service** — "Thanks Sarah! Your nails look amazing. If you have 30 seconds, it would mean the world to leave a review: [Google link]. Ready to book your next infill in 3 weeks? [booking link]"
5. **Fill reminder (week 3)** — "Hi Sarah! It's been 3 weeks since your last gel infill — they'll be due a refresh soon. Want to book? [booking link]"

## Fill cycle automation

| Service | Cycle | First reminder at | Revenue per visit |
|---------|-------|-------------------|-------------------|
| Gel polish | 2-3 weeks | Week 2 (day 14) | £35-55 |
| Gel-X full set | 3-4 weeks | Week 2.5 (day 18) | £70-120 |
| Acrylic fill | 2-3 weeks | Week 2 (day 14) | £45-80 |
| SNS/dip powder | 3-5 weeks | Week 3 (day 21) | £55-85 |
| Gel pedicure | 4-6 weeks | Week 4 (day 28) | £50-75 |
| Nail art add-on | N/A (per visit) | Next booking prompt | £10-30 |

## What the AI agent does at each step

| Step | What AI does | What human does |
|------|-------------|----------------|
| Enquiry arrives (DM/WhatsApp) | Answers price Qs, shows portfolio samples, offers available slots, collects deposit | Nothing — AI handles |
| Booking confirmed | Sends confirmation + deposit receipt to client | Approves booking in booking app |
| 48hr before | Sends reminder with confirm/reschedule link | Checks nothing else is in the slot |
| 2hr before | Sends reminder with directions + parking | None |
| During appointment | — | Performs the nail service |
| Post-service | Sends review request + rebooking link with correct cycle timing | Applies top coat, takes before/after photo |
| Week 2-3 (cycle reminder) | Sends fill reminder with booking link | None |
| 30 day lapse | Sends gentle nudge: "Missing your nails? Book anytime" | None |
| 60 day lapse | Sends win-back: "We miss you! Here's 10% off your next visit" (owner-approved) | None |
| 90 day lapse | Final attempt: "Still thinking about it? Here's what's new: [portfolio link]" | None |

## The intake form (WhatsApp conversation)

AI collects this BEFORE the appointment:

1. **Service desired** — "What are you looking for today? Gel polish, full set, infill, pedicure, nail art?"
2. **Reference photos** — "Love to see what you're after! Send me any inspo photos" (WhatsApp image)
3. **Length/shape preference** — "Short and natural, medium square, long stiletto — what's your vibe?"
4. **Allergies/medical conditions** — "Any allergies I should know about? acrylic, latex, gel products?"
5. **Preferred date/time** — "When works best? I have [slots]. Or book directly: [link]"
6. **Deposit payment** — "To secure your slot, a £10 deposit is needed: [Stripe link]"

## Key metrics

| Metric | Target | How to measure |
|--------|--------|----------------|
| DM response time | <2 min (business hours), <10 min (after hours) | AI logs every response timestamp |
| No-show rate | <3% | Deposits + reminders → track in booking app |
| Fill rebook rate | >70% | Track fill reminder → booking conversion |
| Review rate | >30% | Post-service WhatsApp → Google review link clicks |
| Revenue per chair per day | £300+ | 6-8 clients x avg £40-55 service value |
| New client conversion | >60% | Enquiry → booked deposit within 24hr |
| Win-back rate (30/60/90) | >15% of lapsed clients | Lapse reminder → booking link clicks |

## What the top 10% do differently

- **Same-day deposit policy** — no deposit, no slot. AI enforces this consistently across every DM
- **Before/after photos every client** — builds portfolio automatically, posted to Instagram with client permission
- **Infill reminder at exactly 2 weeks** — not "when I remember." AI tracks per-client cycle and sends at optimal rebook window
- **Price book pinned in WhatsApp** — AI quotes from the owner's actual prices, never guesses
- **Review requested within 1 hour of service** — fresh experience = higher review quality
- **Cancellation policy stated upfront** — "Cancel within 24hr, deposit forfeited." AI repeats this in every confirmation
- **Aftercare tips sent same day** — "Avoid hot water for 2hr. Don't pick at the edges. Use cuticle oil daily." Reduces complaints and rework
