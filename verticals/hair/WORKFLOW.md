# Mobile hairdresser workflow

> The actual day-to-day. What happens, where the pain is, what the AI does.

## The day (research-backed)

| Time | What happens | Pain | AI/WhatsApp solution |
|------|-------------|------|---------------------|
| 8:00-8:30 | Check diary, plan route, load kit | 3 clients in 3 different postcodes, didn't plan route | WhatsApp: "Your day: 9am colour + cut (Sarah, SW1 — 25min drive), 12pm blow-dry (Megan, SE15 — 20min), 2:30 braids (Fatima, E17 — 35min), 5pm cut (Linda, N16 — 15min). Suggested route: SW1→SE15→E17→N16" |
| 8:30-9:15 | Drive to Client 1 | Wasted 20min because of roadworks, client doesn't know | AI sent traffic alert: "Heavy traffic on A3 — leave 10min early. Client notified you'll arrive at 9:10" |
| 9:15-11:15 | Client 1: Full colour + cut (2hrs) | — | — |
| 11:15-11:45 | Drive to Client 2 | — | AI: "Client 2 confirmed you're en route. ETA 12:05" |
| 12:00-12:45 | Client 2: Blow-dry (45 min) | — | — |
| 12:45-1:15 | Lunch (in the car) + respond to DMs | DMs asking "do you travel to [area]?" — losing jobs because reply took 2 hours | AI handles: "Yes! I cover [postcode area]. Travel fee: £5-15 depending on distance. Want to book?" |
| 1:15-2:15 | Drive to Client 3 | — | AI: "Client 3 needs patch test confirmation. Checking..." |
| 2:15-5:00 | Client 3: Box braids (2.75hrs) | — | — |
| 5:00-5:30 | Drive to Client 4 | — | AI: "Running 10min late. Client Linda notified." |
| 5:30-6:15 | Client 4: Cut + finish (45 min) | — | — |
| 7:00-7:30 | Home admin | Forgot to note travel mileage for tax; forgot which client used which products | AI: "Today's mileage: 42 miles. Products used: colour (Wella 7/0), developer (6%). COSHH logged." |

## The 5-message WhatsApp sequence per visit

1. **Booking confirmation** — "You're booked for balayage + cut on Thursday 10am at your home (SW11). Deposit of £20 collected. Travel fee: £10. Total: £[amount]. Note: colour services require a patch test 24-48hr before."
2. **48hr reminder** — "Hi Sarah! Your balayage is tomorrow at 10am. Please have clean, dry hair. No heavy products. Reply YES to confirm: [link]"
3. **2hr reminder (travel day)** — "On my way! I'll arrive at 10am. Parking: [any notes?]. I'll text when I'm 5 min away."
4. **Post-service** — "Thanks Sarah! Your colour looks stunning. Aftercare: wait 48hr before washing, use colour-safe shampoo, avoid heat for 24hr. Leave a review: [Google link]. Book your next colour refresh in 8-12 weeks: [booking link]"
5. **Colour cycle reminder (week 8)** — "Hi Sarah! Your roots will be needing a refresh soon. Want to book your next colour appointment? [booking link]"

## Travel area check (AI handles before booking is confirmed)

| Step | AI action | Human action |
|------|-----------|-------------|
| Enquiry arrives | Asks postcode: "What's your postcode? I cover [X, Y, Z areas]" | None |
| Postcode in range | Confirms: "Great! I come to you. Travel fee: £[X]. Want to book?" | None |
| Postcode out of range | Politely declines: "Sorry, that's outside my travel area. I cover [list]. Want me to recommend someone?" | None (or confirms recommendation) |
| Travel fee calculated | Added to booking total, shown in confirmation | None |
| Traffic/delay alert | AI monitors route, alerts client if ETA shifts | None |

## Service area pricing guide

| Distance | Travel fee | Typical for |
|----------|-----------|-------------|
| 0-5 miles | Free / £5 | Local regulars |
| 5-10 miles | £8-12 | Standard service area |
| 10-15 miles | £12-18 | Extended area |
| 15-20 miles | £15-25 | Premium travel jobs |
| 20+ miles | Case-by-case | Wedding/event bookings only |

## What the AI agent does at each step

| Step | What AI does | What human does |
|------|-------------|----------------|
| Enquiry arrives | Asks postcode, confirms service area, calculates travel fee, shows portfolio, offers slots | None |
| Booking confirmed | Sends confirmation + deposit receipt + travel details + patch test flag (for colour) | Confirms in booking app |
| 48hr before | Sends prep instructions (clean hair, no product, etc.) | None |
| 2hr before | Sends ETA and arrival text | Drives to client |
| En route | Traffic monitoring, client notification of delays | Drives |
| During service | — | Performs the service |
| Post-service | Sends aftercare + review request + rebooking link | Takes before/after photo |
| Colour cycle reminder | Sends rebooking prompt at 8-12 weeks depending on service | None |
| End of day | AI compiles: mileage log, products used, COSHH entries | Reviews and approves |

## The intake form (WhatsApp conversation)

AI collects this BEFORE the appointment:

1. **Service desired** — "What are you after? Cut, colour, blow-dry, braids, extensions?"
2. **Your postcode** — "What's your postcode? I'll check if I cover your area."
3. **Colour consultation (if applicable)** — AI collects: current colour, target colour, reference photos, hair history (previous colour, bleaching, relaxers), budget range
4. **Hair length/type** — "Long/short/thick/thin? Helps me prep the right kit."
5. **Allergies/medical** — "Any allergies to hair products? Medical conditions I should know about?"
6. **Preferred date/time + location** — "When works best? And confirm your address for the home visit."
7. **Deposit payment** — "To secure your slot: £[amount] deposit: [Stripe link]"

## Colour consultation flow (AI-managed)

| Step | AI collects | Why |
|------|------------|-----|
| Current colour | "What colour is your hair now? (natural, dyed, bleached)" | Prevents wrong formula |
| Target colour | "What are you aiming for? Send inspo photos" | Matches expectations |
| Hair history | "Any previous colour, bleach, relaxers, or henna?" | Safety + colour accuracy |
| Last salon visit | "When did you last have your hair done and what was done?" | Timing for regrowth |
| Budget | "What's your budget range? Full balayage starts at £[X]" | No surprises |
| Patch test | "Colour needs a patch test 24-48hr before. When can you pop in?" | Legal requirement |

## Key metrics

| Metric | Target | How to measure |
|--------|--------|----------------|
| DM response time | <5 min (between appointments) | AI logs timestamps |
| No-show rate | <5% | Deposits + reminders |
| Travel efficiency | <30 min dead time between clients | AI route optimisation |
| Rebook rate | >60% | Cycle reminders → booking conversion |
| Review rate | >25% | Post-service WhatsApp → Google review link clicks |
| Revenue per day | £250+ | 4-5 clients x avg £50-70 service value |
| Colour rebook rate | >75% | 8-12 week reminders are highest-converting |
| COSHH compliance | 100% | AI prompts daily log |

## What the top 10% do differently

- **Postcode gate at first message** — no wasted conversations with out-of-area clients. AI handles politely
- **Travel fee upfront** — included in every quote, never a surprise at the door
- **Route-optimised scheduling** — AI clusters nearby postcodes, avoids backtracking across the city
- **Colour consultation photos saved** — before/after colour photos build a powerful portfolio (with client permission)
- **Traffic-aware departure alerts** — AI checks route before each drive, adjusts departure time
- **End-of-day mileage + COSHH auto-log** — saves 30 min admin every evening
- **Wedding/event upsell** — AI identifies bookings near wedding dates, suggests bridal packages
