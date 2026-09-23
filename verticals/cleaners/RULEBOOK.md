# Cleaner rulebook

> What "correct" means for this vertical and every way the AI gets it wrong. Built from research; must be validated against real jobs and updated after every mistake caught. This is the moat.

## How to use this file

Every time we deliver work for a cleaner customer and something goes wrong, add it here with the fix. After 50 jobs this list is worth more than the model. A competitor can copy our tools; they can't copy this.

---

## Recurring scheduling (PP-064)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 1 | Fortnightly cadence set as weekly by default | Cleaner billed for visits they didn't do, customer disputes | Confirm cadence explicitly: weekly, fortnightly, 4-weekly, or custom |
| 2 | Skip-one-occurrence cancels entire series | Customer takes a holiday, loses their regular slot permanently | "Skip" must remove one occurrence only; series continues as before |
| 3 | Bank holiday visits not flagged in advance | Cleaner arrives to a locked house, wastes travel time | Flag bank holidays 3 days before; offer reschedule or skip |
| 4 | Cadence change doesn't update next-visit date | Cleaner thinks visit is Monday, customer thinks Wednesday | When cadence changes, recalculate and confirm next 3 visit dates |
| 5 | Seasonal variation not captured (e.g. school holidays) | Customer skips every July but calendar doesn't know | Ask at onboarding: "Any regular skip periods?" and set annual blocks |

## Key and alarm access (PP-064, unique to cleaners)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 6 | Alarm code stored in chat log | Data breach; alarm code exposed in message history | Store key/alarm details in secure field only, never in free-text notes |
| 7 | Key collection not confirmed before first visit | Cleaner arrives, no key, wasted trip | Confirm key handover method before first appointment |
| 8 | Alarm code changed but not updated | Cleaner triggers alarm, police called, trust destroyed | Prompt customer to confirm alarm details quarterly |
| 9 | Lockbox code shared verbally, never written down | Next cleaner doesn't have it, service disruption | Record in secure field; reference by field name, not value, in messages |

## Scheduling and calendar (PP-039)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 10 | AI books over an existing one-off deep clean | Customer double-booked, cleaner turned away | Check calendar before confirming any booking; flag conflicts |
| 11 | Same-day booking confirmed without checking cleaner availability | Cleaner not available, last-minute scramble | Require same-day bookings to check slot before confirming |
| 12 | Cancellation doesn't free the slot for waitlist | Lost revenue; slot sits empty | When a cancellation occurs, check if anyone is waiting for that slot |
| 13 | Recurring visit rescheduled but old slot still shows | Customer sees phantom availability, confusion | Reschedule must update both old and new slots atomically |

## Win-back (PP-025, PP-039)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 14 | Win-back sent during customer's known skip period | Feels spammy, customer ignored it anyway | Suppress win-back during documented skip periods |
| 15 | Win-back sent after 2 weeks of inactivity for a fortnightly customer | Customer hasn't missed a beat, feels spammed | Match win-back interval to their normal cadence (weekly = skip 2 weeks, fortnightly = skip 4 weeks) |
| 16 | Win-back doesn't reference the actual service | "We miss you!" — no context, no urgency | Reference last clean: "Your fortnightly kitchen clean hasn't been booked for 6 weeks — want to restart?" |
| 17 | No win-back sent when customer pauses plan voluntarily | Customer meant to restart, forgot, never came back | Pause triggers a "ready to restart?" message at their stated return date |

## Payment chasing (PP-073)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 18 | Failed Direct Debit not flagged for 2 weeks | Cleaner loses 2 visits worth of revenue before noticing | Check mandate status after each failed collection; flag same day |
| 19 | Chase message sent with no payment link | Customer agrees to pay but has no easy way to do it | Every chase includes a direct payment link |
| 20 | Chase tone too aggressive on first attempt | Customer feels threatened, cancels plan | First chase is friendly: "Quick reminder — your payment didn't go through. Here's the link to sort it." |
| 21 | No escalation path for chronic non-payers | Cleaner keeps cleaning for free | After 3 failed chases, escalate to owner for decision: enforce or write off |
| 22 | Chase sent to wrong contact method | Customer changed email, never updated | Verify contact method before sending; bounce = immediate flag |

## Pricing and quotes

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 23 | Deep clean priced as standard clean | Cleaner does 3x work for standard price | First clean or deep clean must be priced from approved price book, not auto-filled |
| 24 | Extras (oven, fridge, windows) not priced at quote | Customer expects oven clean included, it's £25 extra | Quote must itemise extras; customer approves each |
| 25 | Materials cost not included in quote | Cleaner absorbs product costs | Include materials in quote where applicable, or state "customer provides products" |
| 26 | Price book updated but old quotes still being sent | Customer quoted last year's price | Flag any quote older than 30 days for re-verification |

## Reviews and reputation (PP-079)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 27 | Review request sent same day as clean | Customer hasn't had time to assess quality | Send 24-48 hours after the clean, not same day |
| 28 | Review request doesn't specify platform | Customer posts to Facebook, cleaner needs Google | Ask which platform matters; send to that one only |
| 29 | No follow-up for negative feedback | Bad review sits unanswered, trust erodes | Private-message first: "Sorry to hear that — can we make it right?" before public response |

## Legal and safety

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 30 | COSHH assessment not completed for cleaning products | Legal liability if someone is harmed by a chemical | Every product used must have a current COSHH sheet on file |
| 31 | Key/alarm details shared over unsecured channel | Data protection breach | Key/alarm data stored in secure fields only; confirmed verbally or in-person |
| 32 | Cleaner enters property without confirming it's safe | Safeguarding and liability risk | First-visit protocol: confirm access method, key receipt, alarm details in writing |

## General

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 33 | AI promises a service the cleaner doesn't offer | Customer expects ironing, cleaner doesn't iron | Only reference services in approved service menu |
| 34 | AI promises same-day clean when diary is full | Customer books, then gets cancelled, trust broken | Check availability before confirming |
| 35 | Handover doesn't explain how to update prices | Cleaner changes prices, AI still quotes old ones | Handover includes: "To update prices, edit [file] and tell us" |
| 36 | Support window expires but cleaner still needs help | 7-day window too short for some | Track support usage; flag if no contact by day 5 |

---

## Review cadence

- After every job: check if anything went wrong. If yes, add to this list.
- Weekly: review all entries, remove any that are no longer relevant.
- After 50 jobs: this list is the product. Protect it.
