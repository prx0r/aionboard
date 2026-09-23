# Gardeners & window cleaners workflow

> **Live platform:** Meta Business Agent (WhatsApp Business app) — available in UK now. Muse personal agent is US-only, no UK date.

> The actual day-to-day. What happens, where the pain is, what the AI does.

## The day (research-backed)

| Time | What happens | Pain | AI/WhatsApp solution |
|------|-------------|------|---------------------|
| 7:30-8:00 | Check round, load van | — | AI sends today's round at 7am |
| 8:00-8:15 | Drive to first property | — | Route optimised |
| 8:15-9:00 | Round 1 (3-4 houses) | Missed customers (not home) | AI texts: "Window clean today! If you're not home, we'll come back tomorrow" |
| 9:00-9:15 | Drive to next cluster | — | — |
| 9:15-11:00 | Round 2 (4-5 houses) | — | — |
| 11:00-11:15 | Break | — | — |
| 11:15-1:00 | Round 3 | — | — |
| 1:00-1:30 | Lunch | — | — |
| 1:30-3:30 | Round 4 | — | — |
| 3:30-4:00 | Drive back / admin | — | — |
| 4:00-5:00 | Admin: invoicing, rescheduling | Hours of chasing | AI sends invoices, chases payments |

## The round-specific flow

### Round management flow

```
AI knows: customer list, visit frequency (4/6/8 weekly), last visit date, area clusters
  ↓
AI generates optimal round for each day
  ↓
7am: "Today's round: [list of addresses]. 12 stops, 18 miles, finish by 3:30pm"
  ↓
AI texts each customer morning of their clean:
  "Window clean day! We'll be at your property today. If you need to reschedule, reply RESCHEDULE"
  ↓
Cleaner arrives → GPS check-in → cleans → GPS check-out
  ↓
AI sends invoice with payment link
  ↓
AI schedules next visit based on frequency
```

### Invoice and payment automation

```
Job completed → GPS check-out
  ↓
AI generates invoice: property address, service, amount
  ↓
Invoice sent via WhatsApp: "Window clean complete at [address]! Invoice: £[amount]. Tap to pay: [link]"
  ↓
If unpaid at 7 days: "Friendly reminder — invoice for [address] is outstanding"
  ↓
If unpaid at 14 days: "Invoice [X] is now 14 days overdue. Please settle at your earliest convenience"
  ↓
Standing order setup offered after 3rd clean
```

### Seasonal workflow (gardeners)

| Season | AI trigger | Services offered | Message |
|--------|-----------|-----------------|---------|
| Spring (Mar-May) | First warm week | Lawn mowing restart, hedge cutting, weeding, spring clean | `Spring is here! Time for your garden tidy-up. Book now before we fill up` |
| Summer (Jun-Aug) | Weekly mowing cycle | Regular mowing, strimming, watering checks | `Your lawn is due for a cut. Book your next visit?` |
| Autumn (Sep-Nov) | First leaf fall | Leaf clearance, gutter cleaning, lawn treatment | `Leaf fall season! Book your autumn tidy-up` |
| Winter (Dec-Feb) | — | Fence repairs, pressure washing (weather permitting) | `We'll see you in spring! In the meantime, need any winter services?` |

### Frequency management

```
New client signs up
  ↓
AI: "How often would you like your windows cleaned?"
  ↓
Options: 4 weekly (most popular), 6 weekly, 8 weekly
  ↓
AI calculates: last clean + frequency = next scheduled date
  ↓
AI sends morning-of text: "Window clean today!"
  ↓
If not home: AI texts "Not a problem! We'll come back tomorrow"
  ↓
If home: GPS check-in → clean → GPS check-out → invoice
  ↓
AI schedules next visit based on frequency
  ↓
Cycle repeats automatically
```

### Missed customer handling

```
Cleaner arrives at property
  ↓
GPS check-in logged
  ↓
Nobody home (if key access not available)
  ↓
AI texts client: "Hi! We're at your property for the window clean. Not a problem — we'll come back tomorrow. If you'd prefer a different day, reply RESCHEDULE"
  ↓
If client replies: AI reschedules to agreed date
  ↓
If no reply: AI schedules return visit for next day in same area
  ↓
Cleaner moves to next property on round
```

### Garden-only seasonal upsell

```
Lawn mowing customer (summer)
  ↓
AI detects autumn approaching
  ↓
AI: "Summer mowing is winding down! Would you like us to handle your autumn leaf clearance? £25 for a standard garden"
  ↓
If yes: Added to autumn schedule
  ↓
If no: AI notes preference, offers again next year
  ↓
Spring: "Spring is here! Ready to restart lawn mowing? Same schedule as last year?"
  ↓
Customer confirms → season starts automatically
```

## WhatsApp-first features

- **Morning round notification**: Each customer gets "Window clean today!" — if not home, they know to reschedule or expect a return visit
- **Standing order via WhatsApp**: After 3rd clean, AI offers monthly auto-payment — no invoicing, no chasing
- **Seasonal upsell prompts**: Gardeners get spring/autumn/summer messages timed to weather — no manual outreach needed
- **Missed-visit auto-reschedule**: Not home? AI texts, client replies, rescheduled for next day — no phone tag
- **Instant payment link**: Invoice arrives as WhatsApp message with tap-to-pay — 70% pay same day

## GPS/photo tracking

| Event | What's logged | How |
|-------|--------------|-----|
| Morning dispatch | Route plan, stop count, mileage, finish time | AI sends at 7am |
| Per-property check-in | GPS + timestamp + address match | Auto on arrival |
| Per-property check-out | GPS + timestamp + duration | Auto on departure |
| Completion photo (optional) | Clean windows / tidy garden | Cleaner prompted |
| End of day | Total stops, mileage, revenue, efficiency score | Auto-generated |
| Weekly summary | Rounds completed, revenue, retention rate, gaps filled | Auto-generated |

## What the AI agent does at each step

| Step | AI action | Human action |
|------|-----------|-------------|
| 7:00am | Send today's round: addresses, mileage, finish time | Cleaner loads van |
| 7:30am | Text each customer: "Window clean today!" | — |
| Per-property | Log GPS check-in, start timer | Cleaner checks in |
| Completion | Log GPS check-out, send invoice via WhatsApp | Cleaner moves to next |
| End of day | Send revenue summary, update schedules | Cleaner reviews |
| 7 days unpaid | Auto-chase invoice | — |
| 14 days unpaid | Second chase, firmer tone | — |
| After 3rd clean | Offer standing order setup | — |
| Season change | Send seasonal upsell to garden clients | — |
| Monthly | Send round efficiency report | — |

## Key metrics

| Metric | Target | How |
|--------|--------|-----|
| Round utilisation | >90% | AI fills gaps, optimises routes |
| Invoice payment time | <7 days | Auto-send + auto-chase |
| Customer retention | >85% | Recurring schedule + skip-one easy |
| Route efficiency | <15% drive time | AI optimisation |
| Revenue per round per day | £200+ | 10-15 properties × £15-25 |
| Referral rate | >15% | Ask after every 5th visit |
| Missed-visit recovery | >80% | Auto-reschedule to next day |
| Standing order adoption | >40% | Offer after 3rd clean |
| Seasonal upsell conversion | >25% | Timed prompts for garden clients |
| Average revenue per property/year | £80-120 | 4/6/8 weekly × £15-25 |

## What the top 10% do differently

- **Standing order is default**: Offers standing order after 3rd clean — eliminates invoicing entirely, cash flow is predictable
- **Morning text to every customer**: "Window clean today!" — reduces missed visits by 60%, clients rearrange if needed
- **Route clusters by area**: Never drive across town — AI groups properties by neighbourhood, minimises drive time
- **GPS check-in/check-out on every property**: Proves work was done, tracks time per property, identifies inefficiencies
- **Seasonal garden upsell timed to weather**: Not calendar — actual weather triggers. Warm spring = "lawn mowing ready", first frost = "garden winterised"
- **Referral ask on every 5th visit**: "We clean [neighbour]'s house too — if you know anyone on [street], share this link for £10 off" — builds street-by-street density
- **Same-day invoice with pay link**: Invoice sent while still on the street — 70% paid same day, no chasing
- **Skip-one is easy**: Client replies "skip" — AI handles it, no guilt, no friction — they come back next cycle
