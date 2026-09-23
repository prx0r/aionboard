# Cleaners workflow

> The actual day-to-day. What happens, where the pain is, what the AI does.

## The day (research-backed)

| Time | What happens | Pain | AI/WhatsApp solution |
|------|-------------|------|---------------------|
| 7:00-7:30 | Travel to first client | Key access? Alarm code? | AI sends access instructions at 6am |
| 7:30-8:00 | GPS check-in, take BEFORE photos | No proof of work | Auto GPS log + photo prompt |
| 8:00-10:30 | Client 1 (2.5hr weekly clean) | — | — |
| 10:30-11:00 | Travel to client 2 | — | Route optimised |
| 11:00-13:00 | Client 2 | — | — |
| 13:00-13:30 | Lunch | — | — |
| 13:30-15:30 | Client 3 | — | — |
| 15:30-17:30 | Client 4 | — | — |
| 17:30-18:30 | Admin: invoicing, scheduling, WhatsApp | Hours of admin | AI drafts invoices, sends payment links |

## The cleaner-specific flow

### 5-message WhatsApp sequence per clean

| # | When | Message |
|---|------|---------|
| 1 | Day before | `Hi [name]! Cleaning tomorrow at [time] at [address]. Anything special you'd like us to focus on? Reply or just say no worries!` |
| 2 | 2hr before | `On our way! ETA [X] minutes. We'll let ourselves in with the key safe.` |
| 3 | Arrival | `We've arrived! Starting with [room]. Before photos taken.` |
| 4 | Completion | `All done! Here's what we did: [checklist]. Before/after photos attached. Invoice sent: [link]. Tap to pay.` |
| 5 | 48hr after | `Hope you're enjoying the fresh home! Would you like us to book your next clean? [booking link]` |

### Key access flow

```
New client books
  ↓
AI: "How will we access the property?"
  ↓
Options: key safe (preferred), smart lock, client present, key collection
  ↓
If key safe: "Please set a 4-digit code and share it here. We'll use it on arrival and never share it."
  ↓
Access instructions stored in job record
  ↓
Cleaner gets: address + access code + alarm instructions + special requests
  ↓
After clean: key returned to safe, code confirmed
```

### Recurring schedule management

```
Client books weekly clean
  ↓
AI creates recurring schedule: every [day] at [time]
  ↓
AI sends weekly confirmation: "See you Thursday!"
  ↓
If client wants to skip: "No problem! Skip this Thursday? Your next one is [date]"
  ↓
If client wants to reschedule: "How about Friday instead? Same time?"
  ↓
AI handles all back-and-forth — cleaner just shows up
```

### Win-back automation

```
60 days since last clean
  ↓
AI: "Hi [name]! We haven't seen you in a while. Everything OK? Would you like to rebook?"
  ↓
If no response at 7 days: "Just checking in! We have availability this week if you'd like a clean."
  ↓
If interested: "Great! Here are available slots: [list]. Tap to book."
  ↓
If no response at 21 days: "We miss you! Here's 10% off your next clean: [code]"
```

### Before/after photo workflow

```
Arrival
  ↓
GPS clock-in (auto-logged)
  ↓
Take BEFORE photos (kitchen, bathrooms, living areas, any issues)
  ↓
Photos auto-tagged: GPS + timestamp + property address
  ↓
Clean
  ↓
Take AFTER photos (same rooms, same angles)
  ↓
Auto-generate proof report: before | after | checklist completed
  ↓
Send to client via WhatsApp: "All done! Here's the proof. Invoice attached."
  ↓
Client shares on Nextdoor/Facebook = free marketing
```

## WhatsApp-first features

- **Access code relay**: Client shares key safe code via WhatsApp, AI stores it, cleaner receives it on morning of clean — no app download required
- **Photo proof loop**: Cleaner sends before/after photos in-thread, client sees them as WhatsApp images, can forward to neighbours
- **Skip/reschedule via reply**: Client replies "skip" or "move to Friday" — AI handles it, no login, no portal
- **Instant payment**: Invoice arrives as WhatsApp message with tap-to-pay link, no account needed
- **Referral prompt**: After 5th clean, AI sends: "Know someone who'd love a fresh home? Share this link and you both get £10 off"

## GPS/photo tracking

| Event | What's logged | How |
|-------|--------------|-----|
| Morning dispatch | Route plan, estimated arrival | AI sends at 7am |
| GPS check-in | Latitude/longitude, timestamp, address match | Auto on arrival |
| Before photos | 3-6 photos with GPS overlay | Cleaner prompted at check-in |
| Mid-clean | Optional progress photo | Cleaner prompted at halfway |
| After photos | Same angles as before, GPS overlay | Cleaner prompted at completion |
| GPS check-out | Latitude/longitude, timestamp, duration | Auto on departure |
| Proof report | Before/after side-by-side, checklist, duration | Auto-generated, sent to client |

## What the AI agent does at each step

| Step | AI action | Human action |
|------|-----------|-------------|
| 6:00am | Send access instructions + alarm codes to cleaner | Cleaner reviews |
| 7:00am | Send today's route + client list + special requests | Cleaner loads van |
| Arrival | Log GPS, prompt before photos, send arrival msg to client | Cleaner checks in, takes photos |
| During clean | — | Cleaner cleans |
| Completion | Log GPS check-out, send completion msg + invoice to client | Cleaner takes after photos, taps to send |
| End of day | Send revenue summary, update recurring schedules | Cleaner reviews |
| 48hr after | Send rebook prompt to client | Client responds |
| 60 days inactive | Trigger win-back sequence | — |
| After 5th clean | Send referral prompt | — |

## Key metrics

| Metric | Target | How |
|--------|--------|-----|
| Recurring retention | >85% | Weekly confirmation + skip-one easy |
| Win-back recovery | >15% | 60/67/90 day automated sequence |
| Invoice payment time | Same-day | Auto-send with pay link on completion |
| Before/after photo rate | 100% | Auto-prompted at job start/end |
| Referral rate | >20% | Ask after every 5th clean |
| Average revenue per clean | £45-65 | Upsell deep clean, oven, fridge |
| Client lifetime value | £1,200+ | Weekly clean × 52 weeks × £45+ |
| Admin time saved | 8hrs/week | AI handles invoicing, scheduling, comms |

## What the top 10% do differently

- **Never miss a photo**: Before/after photos on every job — clients share them, becomes organic marketing
- **Same-day invoicing**: Invoice sent while still at the property — gets paid same day, no chasing
- **Key safe is standard**: 95% of clients on key safe access — eliminates "are you home?" calls
- **Weekly confirmation**: Sends "See you Thursday!" every week — clients feel cared for, skip rate drops
- **Deep clean upsell**: Offers deep clean add-on every 4th visit — adds £30-50 per clean without new client acquisition
- **Referral programme running**: After every 5th clean, asks for referral — builds pipeline passively
- **48-hour rebook prompt**: Client gets rebook message before they even think about it — locks in recurring revenue
