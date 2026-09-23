# Dog groomers workflow

> The actual day-to-day. What happens, where the pain is, what the AI does.

## The day (research-backed)

| Time | What happens | Pain | AI/WhatsApp solution |
|------|-------------|------|---------------------|
| 7:30-8:30 | Arrive, clean, sanitize, review schedule | — | AI sends day summary at 7am |
| 8:30-9:00 | First drop-off + intake | Phone ringing, can't answer mid-groom | AI answers: breed, service, allergies, pickup time |
| 9:00-11:00 | Groom #1 (2hrs for medium dog) | Owner calls "is my dog ready?" | "We've started [dog's name]! Here's a photo 📸" |
| 11:00-11:15 | Clean between dogs | — | — |
| 11:15-1:15 | Groom #2 | — | — |
| 1:15-1:45 | Lunch | — | — |
| 1:45-3:45 | Groom #3 | — | — |
| 4:00-6:00 | Groom #4 | — | — |
| 6:00-6:30 | Final clean, prep tomorrow | — | AI sends tomorrow's schedule |

## The groomer-specific flow

### Breed-aware booking flow

```
"Hi, I'd like to book a groom for my dog"
  ↓
AI: "What breed is your dog?"
  ↓
Customer: "Cockapoo"
  ↓
AI: "Cockapoos typically need 90 minutes. Services: bath & blow-dry (£35), full groom (£45), puppy's first groom (£30). What would you prefer?"
  ↓
Customer: "Full groom"
  ↓
AI: "£45 for a full groom. Available: [dates/times]. Which suits you?"
  ↓
Customer picks slot
  ↓
AI: "Booked! [date] at [time] for [dog's name]'s full groom (£45). Any allergies or behavioural notes we should know about?"
  ↓
Customer provides notes → stored in pet profile
```

### 5-message WhatsApp sequence per visit

| # | When | Message |
|---|------|---------|
| 1 | Booking | `[Dog's name] is booked for [service] on [date] at [time]. £[amount]. See you then! 🐾` |
| 2 | 48hr reminder | `Reminder: [dog's name]'s groom is tomorrow at [time]. Reply YES to confirm or tap to reschedule [link]` |
| 3 | 2hr reminder | `[Dog's name] is up next! Drop-off at [time] please 🐕` |
| 4 | In-progress | `We've started [dog's name]'s groom! Here's a photo of the happy pup 📸` |
| 5 | Ready | `[Dog's name] is ready! Total: £[amount]. Tap to pay: [link]. See you soon! 🐾` |

### Breed-specific rebooking automation

| Breed group | Rebook cycle | First reminder |
|-------------|-------------|---------------|
| Poodle, Bichon, Doodle | 6 weeks | Week 5 |
| Cockapoo, Schnauzer | 6-8 weeks | Week 6 |
| Shih Tzu, Maltese, Yorkie | 4-6 weeks | Week 4 |
| Labrador, Golden (de-shed) | 8-10 weeks | Week 8 |
| Terrier, Westie | 6-8 weeks | Week 6 |
| Husky, Malamute (de-shed) | 8-12 weeks | Week 8 |

### Waiting list automation

```
Client cancels tomorrow's appointment
  ↓
AI spots empty slot
  ↓
AI texts waiting list (ranked by wait time):
  "[Dog's name] has a slot open tomorrow at 10am for a full groom. First to reply gets it!"
  ↓
First response → auto-booked → confirmation sent
  ↓
Average time to fill: 12 minutes
```

### Mobile groomer GPS flow

```
Morning route planned by AI
  ↓
Groomer loads van, AI sends: "Route: 4 stops, 23 miles, finish by 5:30pm"
  ↓
15 min before arrival: Auto-text client "On my way! ETA 12 minutes"
  ↓
GPS check-in at client address (auto-logged)
  ↓
Groom
  ↓
GPS check-out → auto-logged
  ↓
Drive to next client (route already optimised)
  ↓
End of day: AI sends mileage report, revenue per stop, route efficiency
```

### Dog profile management

```
First visit
  ↓
AI creates profile: name, breed, age, weight, coat condition
  ↓
AI stores: allergies, behavioural notes, preferred groomer, last service
  ↓
Return visit
  ↓
AI loads profile: "Welcome back, [dog's name]! Last full groom was [date]. Ready for the same?"
  ↓
Groomer sees: notes from last visit ("nervous around ears, prefers treats")
  ↓
After groom: AI asks "How did [dog's name] do today? Any notes for next time?"
  ↓
Notes stored → next groomer sees them
```

## WhatsApp-first features

- **Breed-aware booking**: Customer says breed, AI suggests service + price + time — no back-and-forth
- **Photo delivery**: Groomer sends "happy pup" photo mid-groom — eliminates "is my dog ready?" calls
- **Breed-timed rebooking**: AI knows Poodles need 6-week intervals, Goldens need 8 — rebooks automatically
- **Waiting list fill**: Cancellation auto-blasts waitlist, first responder gets slot — average 12min fill
- **Pet profile notes**: Allergies, behavioural quirks, preferences stored in WhatsApp thread — accessible to any groomer

## GPS/photo tracking

| Event | What's logged | How |
|-------|--------------|-----|
| Morning dispatch | Route plan, 4 stops, mileage estimate | AI sends at 7am |
| 15min before arrival | Auto-text to client with ETA | Triggered by route position |
| GPS check-in | Latitude/longitude, timestamp, address match | Auto on arrival |
| Intake photo | Dog's condition on arrival | Groomer prompted |
| Mid-groom photo | Happy pup photo | Groomer prompted (optional) |
| Completion photo | Finished groom, before/after | Groomer prompted |
| GPS check-out | Latitude/longitude, timestamp, duration | Auto on departure |
| End of day | Mileage report, revenue/stop, route efficiency | Auto-generated |

## What the AI agent does at each step

| Step | AI action | Human action |
|------|-----------|-------------|
| 7:00am | Send day summary: 4 grooms, breed list, total revenue | Groomer reviews schedule |
| Before first drop-off | Set up intake questions (breed, service, allergies) | — |
| Client messages | AI handles booking, breed info, pricing, scheduling | Groomer grooms |
| At check-in | Log GPS, prompt intake photo, send arrival msg | Groomer checks in dog |
| Mid-groom | Send progress photo to owner (if groomer takes one) | Groomer works |
| Completion | Send ready msg + invoice + payment link | Groomer finishes |
| Payment received | Log payment, update pet profile, schedule next visit | — |
| 48hr before next breed interval | Send rebooking reminder | Client responds |
| Cancellation received | Auto-blast waiting list | — |

## Key metrics

| Metric | Target | How |
|--------|--------|-----|
| Calendar utilisation | >90% | Breed-aware scheduling + waitlist |
| No-show rate | <5% | Deposits + reminders |
| Rebooking rate | >80% | Breed-interval automation |
| Time to fill cancellation | <15 min | Automated waitlist blast |
| Revenue per groomer per day | £300+ | 4-6 grooms × £50-75 |
| Google reviews | >50 | Ask at photo delivery |
| Average transaction value | £55 | Upsell de-shed, teeth cleaning, blueberry facial |
| Client lifetime value | £1,500+ | 8 grooms/year × £55 × 3+ years |
| Admin time saved | 6hrs/week | AI handles booking, reminders, payments |

## What the top 10% do differently

- **Breed-specific timing**: Knows Poodles need 6-week rebooks, Goldens 8 — sends rebooking prompt before coat gets matted
- **Photo-first delivery**: Sends mid-groom photo to every owner — eliminates "is my dog ready?" calls completely
- **Waitlist under 15 minutes**: Cancellation goes to full waitlist instantly — fills 90%+ of gaps same day
- **Deposit on booking**: Takes £10-15 deposit via WhatsApp pay link — no-show rate drops to <3%
- **Pet profile continuity**: Stores allergies, behavioural notes, groomer preferences — any staff can pick up where left off
- **De-shed upsell for double-coated breeds**: Proactively offers de-shed package for Huskies, Goldens, Labs — adds £15-20 per visit
- **Google review at peak happiness**: Asks for review right after sending completion photo — response rate 3x higher than email
