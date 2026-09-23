# Beauty therapist workflow

> The actual day-to-day. What happens, where the pain is, what the AI does.

## The day (research-backed)

| Time | What happens | Pain | AI/WhatsApp solution |
|------|-------------|------|---------------------|
| 8:30-9:00 | Prep room, check appointment book, confirm patch tests due today | Can't see which clients need patch tests before arrival | WhatsApp: "Your day: 9am facial (Lisa), 10:30 brow lamination + tint (Nadia — patch test done), 12pm waxing (Sophie — PATCH TEST DUE), 2pm lash lift (Emma), 3:30 dermaplaning (Rachel)" |
| 9:00-10:00 | Client 1: Classic facial (60 min) | — | — |
| 10:00-10:30 | Clean room, sterilize tools | — | None (physical task) |
| 10:30-12:00 | Client 2: Brow lamination + tint (90 min) | — | — |
| 12:00-12:45 | Lunch + respond to DMs | 15 DMs, half asking "do you do lash lifts?" (already on website) | AI handles: "Yes! Lash lifts are £45. Patch test needed 24-48hr before. Want to book?" |
| 12:45-1:15 | Client 3: Waxing (30 min) | — | — |
| 1:15-1:45 | Room turnover + lunch overflow | Running behind because facial ran over | AI adjusts remaining day: "Running 15min late — notifying Emma" |
| 2:00-3:00 | Client 4: Lash lift (60 min) | — | — |
| 3:15-4:15 | Client 5: Dermaplaning (60 min) | — | — |
| 5:00-5:30 | End-of-day admin | Forgot to record which wax was used on Sophie (COSHH) | AI reminds: "Log today's COSHH: Sophie — hot wax, strip wax" |
| 6:00-6:30 | After-hours DMs | Price enquiries, "can you do Saturday?", package questions | AI handles all: price, availability, deposit, confirmation |

## The 5-message WhatsApp sequence per visit

1. **Booking confirmation** — "You're booked for a lash lift + tint on Thursday 2pm at [salon]. Important: we need a patch test 24-48hr before. Reply to this message and we'll arrange it."
2. **Patch test reminder (48hr before)** — "Don't forget your patch test! Drop in anytime today or tomorrow between 9am-5pm. It takes 5 minutes."
3. **24hr reminder** — "All clear for tomorrow! Your lash lift + tint is at 2pm. Please come with clean, makeup-free lashes. See you then!"
4. **Post-service** — "Thanks Lisa! Your lashes look incredible. Aftercare: avoid water for 24hr, no oil-based products for 48hr, brush daily. Leave a review: [Google link]. Book your next lift in 6-8 weeks: [booking link]"
5. **Cycle reminder (week 6)** — "Hi Lisa! Your lash lift will be due a refresh soon. Book your next appointment: [link]"

## Patch test safety flow (tinting, lash lift, chemical treatments)

| Step | Timing | AI action | Human action |
|------|--------|-----------|-------------|
| Treatment requires patch test | At booking | Flags requirement: "This treatment needs a patch test 24-48hr before" | None |
| Patch test due | 48hr before | Sends reminder with drop-in times | None |
| Patch test completed | Same day | Records: client name, date, product used, result (clear/reaction) | Performs patch test, reports result |
| Patch test clear | Before appointment | Confirms: "All clear for your appointment tomorrow!" | None |
| Patch test reaction | Before appointment | Cancels appointment, advises: "Please consult your GP. We'll reschedule when safe" | Contacts client if needed |
| No patch test on file | Day of | Blocks appointment: "We can't proceed without a patch test. Let's reschedule" | None (AI enforces) |

## Treatment-specific aftercare messages

| Treatment | Aftercare message (sent post-service) | Next reminder |
|-----------|--------------------------------------|---------------|
| Facial | "Avoid makeup for 12hr. Use SPF 30+ for 48hr. Don't exfoliate for 5 days." | 4-6 weeks |
| Waxing | "Avoid hot baths, swimming, deodorant for 24hr. Exfoliate in 48hr to prevent ingrowns." | 4-6 weeks |
| Brow lamination | "Keep brows dry for 24hr. Brush upward daily. Avoid makeup for 24hr." | 6-8 weeks |
| Brow tint | "Avoid face wash on brows for 24hr. Tint lasts 4-6 weeks." | 4-6 weeks |
| Lash lift | "No water for 24hr. No mascara for 48hr. Avoid oil-based products. Brush lashes daily." | 6-8 weeks |
| Lash tint | "Avoid rubbing eyes for 24hr. Tint lasts 3-4 weeks." | 3-4 weeks |
| Dermaplaning | "No active skincare for 48hr. Use gentle cleanser. SPF daily for 5 days." | 4-6 weeks |
| Chemical peel | "Don't pick peeling skin. SPF 50+ daily. No retinol for 5 days." | 4-8 weeks |

## What the AI agent does at each step

| Step | What AI does | What human does |
|------|-------------|----------------|
| Enquiry arrives | Answers treatment Qs, checks if patch test needed, offers slots, collects deposit | Nothing |
| Booking confirmed | Sends confirmation + flags patch test requirement + deposit receipt | None |
| 48hr before (patch test clients) | Sends patch test drop-in reminder | None |
| 24hr before | Sends prep instructions (clean skin, no makeup, etc.) | None |
| During treatment | — | Performs treatment, records COSHH, records patch test if new product |
| Post-service | Sends aftercare + review request + rebooking link with correct cycle | Takes before/after photo (with consent) |
| Cycle reminder | Sends rebooking prompt at optimal interval per treatment | None |
| Package expiry (30 days out) | "Your 6-facial package has 2 sessions left. Book your next visit!" | None |

## The intake form (WhatsApp conversation)

AI collects this BEFORE the appointment:

1. **Treatment desired** — "What can we help you with? Facial, waxing, tint, brow lamination, lash lift?"
2. **Patch test history** — "Have you had this treatment with us before? When was your last patch test?"
3. **Allergies/medical conditions** — "Any allergies, skin conditions, medications, or pregnancy I should know about?" (relevant for COSHH + safety)
4. **Skin type/concerns** (for facials) — "What's your main skin concern? Oily, dry, sensitive, acne, ageing?"
5. **Preferred date/time** — "When works best? [available slots] or book directly: [link]"
6. **Deposit payment** — "To secure your slot: [Stripe link]"

## Key metrics

| Metric | Target | How to measure |
|--------|--------|----------------|
| DM response time | <2 min | AI logs response timestamps |
| No-show rate | <3% | Deposits + reminders |
| Patch test compliance | 100% for applicable treatments | AI blocks bookings without valid patch test |
| Rebook rate | >65% | Cycle reminders → booking conversion |
| Review rate | >30% | Post-service WhatsApp → Google review link clicks |
| Revenue per room per day | £250+ | 4-6 clients x avg £45-65 treatment value |
| Package redemption rate | >85% | Track package sales vs redemptions |
| COSHH record completeness | 100% | AI prompts daily end-of-day check |

## What the top 10% do differently

- **Patch test at first enquiry, not at booking** — catches allergies before deposit, avoids awkward cancellations
- **Aftercare message includes photo** — "Here's what your brows should look like at day 3" reduces anxious follow-up DMs
- **Seasonal treatment prompts** — "Summer's coming! Book your leg wax + tan prep package" (AI sends seasonal prompts to full client list)
- **Package upsell at repeat visit** — "You've had 3 facials this quarter — a package would save you £30" (AI calculates and suggests)
- **Treatment stacking suggestions** — "Your lash lift is booked — want to add a tint? Just £15 more" (AI suggests at booking)
- **Allergy records stored securely** — never in chat screenshots, always in proper records with date, product, result
- **COSHH logged same-day** — AI prompts end-of-day: "Log today's chemical usage before you go"
