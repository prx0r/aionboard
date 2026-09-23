# Gardener and window cleaner rulebook

> What "correct" means for this vertical and every way the AI gets it wrong. Built from research; must be validated against real jobs and updated after every mistake caught. This is the moat.

## How to use this file

Every time we deliver work for a gardener or window cleaner customer and something goes wrong, add it here with the fix. After 50 jobs this list is worth more than the model. A competitor can copy our tools; they can't copy this.

---

## Round management (PP-024, PP-066)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 1 | Paper round book is only copy | One lost notebook = entire customer base gone | Digitise round; back up customer and payment records |
| 2 | Verbal credits never recorded | Cleaner did a free window clean "because it was quick" — no audit trail | Every skip, credit, or freebie logged with reason and date |
| 3 | Round order not optimised | Visits spread across town = wasted travel time | Verify route order; group by street/area before first run |
| 4 | New customer added to round without checking density | Adding one customer 30 minutes away breaks the route economics | Check postcode density before adding; flag if >15 min from nearest existing customer |
| 5 | Customer on round doesn't match billing records | Cleaned but never invoiced; or invoiced but not cleaned | Cross-check round list against billing monthly |
| 6 | Round digitisation doesn't preserve original order | Reimported list is alphabetical, not geographic | Preserve original route sequence during import; verify with customer |

## Recurring bookings and weather (PP-073)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 7 | Recurring visit confirmed without checking weather | Window cleaner arrives in heavy rain, can't work | Check weather forecast 24hr before outdoor visits; flag if >80% rain chance |
| 8 | Weather reschedule doesn't notify customer | Cleaner decides not to come, customer doesn't know | Every weather-related reschedule triggers customer notification |
| 9 | Rescheduled visit not added to next available slot | Customer misses a visit with no replacement | Reschedule creates a new booking in the next available window |
| 10 | Monthly garden visit scheduled for same date regardless of season | Garden doesn't need monthly attention in December | Seasonal frequency adjustment: monthly Mar-Oct, bi-monthly Nov-Feb (or customer-defined) |
| 11 | Garden visit scheduled during dark hours | Short winter days; cleaner can't see what they're doing | Time visits within daylight hours; adjust schedule seasonally |

## First-visit pricing (PP-061)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 12 | First clean priced as standard clean | First window clean takes 2-3x longer; cleaner loses money | First clean or deep clean priced separately from recurring visits |
| 13 | First-visit scope not agreed in writing | Customer expects full garden overhaul; cleaner planned a tidy-up | Agree scope at booking; send written confirmation of what's included |
| 14 | First clean quoted but extras not itemised | "Garden clearance" doesn't mention green waste removal cost | Itemise all extras in quote; customer approves each |
| 15 | Price book doesn't distinguish first vs recurring | AI quotes recurring price for first visit | Price book must have separate line items for first-visit and recurring |

## Payment chasing (PP-073)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 16 | Failed Direct Debit not flagged for 2 weeks | Cleaner loses 2+ visits worth of revenue | Check mandate status after each failed collection; flag same day |
| 17 | Chase message sent with no payment link | Customer agrees to pay but has no easy way to do it | Every chase includes a direct payment link |
| 18 | Chase tone too aggressive on first attempt | Customer feels threatened, cancels service | First chase is friendly: "Quick reminder — your payment didn't go through. Here's the link." |
| 19 | No escalation path for chronic non-payers | Cleaner keeps working for free | After 3 failed chases, escalate to owner for decision: enforce or write off |
| 20 | Chase sent to wrong contact method | Customer changed email, never updated | Verify contact method before sending; bounce = immediate flag |
| 21 | Cash customers never invoiced | Verbal agreement to pay, no record, no chase | Invoice generated and sent after every visit; no exceptions |

## Seasonal variability (PP-061)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 22 | Garden visits scheduled at same frequency all year | Garden doesn't need weekly visits in winter; wasted trips | Seasonal frequency: weekly Mar-Sep, fortnightly Oct-Feb (or customer-defined) |
| 23 | Leaf-clearing visits not scheduled in autumn | Customer expects it, cleaner forgets | Flag autumn leaf season; offer add-on visits Sep-Nov |
| 24 | Gutter cleaning not flagged for autumn | Customers forget; cleaner misses upsell | Flag gutter cleaning Sep-Nov; offer as add-on |
| 25 | First frost date not considered for garden tasks | Tender plants damaged; customer blames cleaner | Last garden visit before frost; communicate seasonal wind-down |

## Window cleaning specifics (HSE compliance)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 26 | Window cleaner works at height without risk assessment | Legal requirement under Work at Height Regulations 2005 | Verify risk assessment for ladder/pole work on file |
| 27 | Water-fed pole used near electrics without caution | Safety risk | Flag properties with overhead power lines or external sockets |
| 28 | COSHH assessment not completed for cleaning chemicals | Legal requirement | Every product used must have a current COSHH sheet on file |

## Legal and waste (gardening)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 29 | Green waste disposed of without waste carrier licence | Legal requirement in England; fines up to £5,000 | Verify waste carrier registration if gardener removes waste |
| 30 | Waste mixed with household waste | Fly-tipping liability if waste is traced back | Separate green waste; use licensed disposal facility |
| 31 | Hedge cutting during bird nesting season | Wildlife and Countryside Act 1981 violation | No hedge cutting Mar-Aug; flag in calendar |

## Reviews and reputation

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 32 | Review request sent same day as visit | Customer hasn't assessed the result yet | Send 48hr after visit for garden; 24hr for window clean |
| 33 | Review request doesn't specify platform | Customer posts to Facebook, cleaner needs Google | Ask which platform matters; send there only |
| 34 | No response to negative review | Bad review sits unanswered, trust erodes | Respond within 24hr: acknowledge, offer to make it right, take offline |

## General

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 35 | AI promises a service the business doesn't offer | Customer expects patio cleaning, cleaner only does windows | Only reference services in approved service menu |
| 36 | AI promises same-day visit when diary is full | Customer books, then gets cancelled, trust broken | Check availability before confirming |
| 37 | Handover doesn't explain how to update prices | Business changes prices, AI still quotes old ones | Handover includes: "To update prices, edit [file] and tell us" |
| 38 | Support window expires but business still needs help | 7-day window too short for some | Track support usage; flag if no contact by day 5 |

---

## Review cadence

- After every job: check if anything went wrong. If yes, add to this list.
- Weekly: review all entries, remove any that are no longer relevant.
- After 50 jobs: this list is the product. Protect it.
