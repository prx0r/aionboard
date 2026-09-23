# Driving instructor rulebook

> What "correct" means for this vertical and every way the AI gets it wrong. Built from research; must be validated against real jobs and updated after every mistake caught. This is the moat.

## How to use this file

Every time we deliver work for a driving instructor customer and something goes wrong, add it here with the fix. After 50 jobs this list is worth more than the model. A competitor can copy our tools; they can't copy this.

---

## Scheduling (DISCOVERY-SCHEDULING)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 1 | AI books lesson when instructor is already committed | Double-booking; customer shows up, no instructor | Check calendar before confirming any booking |
| 2 | Cancellation slot not offered to waiting list | Instructor sits idle for an hour, waiting-list pupil misses a chance | Auto-notify waiting list when cancellation occurs; require instructor approval before filling |
| 3 | Lesson scheduled during test-prep block | Instructor reserves final lessons for test candidates, AI books a beginner in that slot | Respect test-prep scheduling preferences; ask about slot allocation during intake |
| 4 | Break times not blocked | AI books back-to-back all day, instructor burns out | Import break preferences; block them in calendar |
| 5 | Pickup/dropoff location not captured | Instructor drives 20 minutes to pick up a pupil, loses billable time | Capture pickup location during booking; flag if outside usual radius |
| 6 | Waiting-list position not communicated | Pupil doesn't know where they are, calls repeatedly for updates | Share waiting-list position on request; update when it changes |
| 7 | Same-day cancellation filled too aggressively | Instructor gets a same-day fill but had planned admin time | Respect same-day preferences; don't fill without explicit approval |

## Progress tracking (DISCOVERY-PROGRESS)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 8 | Progress recorded in notebook, lost when pupil switches instructor | New instructor starts from scratch, pupil repeats lessons | Digital progress record follows the pupil; shared only with permission |
| 9 | AI logs "test ready" without instructor judgment | Pupil thinks they're ready, books test, fails | Only instructor marks "test ready"; AI records and tracks |
| 10 | Skills covered not tracked | Instructor can't remember what was covered last lesson, wastes time reviewing | Log each lesson's focus areas; surface at next lesson |
| 11 | Progress shared with parent without pupil consent (adult pupil) | Privacy issue, trust broken | Default: share with pupil only. Parent access requires explicit pupil consent (or guardian consent for under-18s) |
| 12 | Theory test progress not tracked | Pupil focuses on practical, theory expires or delays practical test | Track theory test pass/expiry; remind before expiry |

## Test coordination

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 13 | Test date booked without final lessons scheduled | Instructor can't guarantee availability for final prep | When test date set, offer to schedule final prep lessons immediately |
| 14 | Test cancelled and rebooked without updating instructor | Instructor shows up or doesn't, no test happening | Require test-date changes to be communicated; confirm with instructor |
| 15 | Mock test not scheduled before practical test | Pupil goes into test cold, higher fail rate | Suggest mock test 1-2 weeks before practical test date |
| 16 | Theory test expiry not tracked | Theory pass expires after 2 years; pupil loses it | Track theory pass date; remind at 18 months, 21 months |

## Cancellations and payments

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 17 | No cancellation policy stated upfront | Pupil cancels 1 hour before, instructor loses income | State cancellation policy during booking confirmation (24hr or 48hr) |
| 18 | Block booking payment not tracked | Pupil pays for 10 lessons, 6 used, 4 "lost" | Track block usage; remind pupil when running low |
| 19 | Cancellation fee not enforced | Instructor eats the cost, learns nothing | Auto-charge or auto-deduct from block after grace period |
| 20 | Late cancellation leaves gap unfilled | Instructor has 1 hour free, could have booked someone else | Auto-offer to waiting list on cancellation; require approval |

## Safeguarding (under-18s)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 21 | Under-18 pupil booked without guardian contact | Safeguarding obligation not met; no emergency contact | Require guardian name and phone for under-18 bookings |
| 22 | Progress shared with guardian without pupil knowledge (16-17yr old) | Trust issue; 16-17yr olds have partial consent rights | Clarify consent boundaries; under-16 = guardian default; 16-17 = ask the pupil |
| 23 | Lesson notes contain safeguarding-relevant info not flagged | Instructor notices something, doesn't know how to escalate | Include safeguarding guidance in handover; know who to contact |

## Pricing and packages

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 24 | Price book doesn't differentiate by lesson type | Intensive course quoted same as weekly lesson | Price book must include: single lesson, block of 5/10/20, intensive course, theory session |
| 25 | Pass-plus or advanced driving not priced | Instructor offers pass-plus, AI quotes lesson rate | Include all post-test services in price book |
| 26 | Block-booking discount not applied | Pupil pays full price for 10 lessons, doesn't see the saving | Apply block discount automatically in quote; show per-lesson and total |

## General

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 27 | AI promises test date that isn't available | Pupil books theory/practical, DVSA has no slot on that day | Link to DVSA availability for reference; never guarantee a specific date |
| 28 | AI promises ADI when instructor is PDI | Different qualification levels, different legal obligations | Capture and display instructor grade (ADI/PDI); reference correctly |
| 29 | Handover doesn't explain how to update prices | Instructor changes prices, AI still quotes old ones | Handover includes: "To update prices, edit [file] and tell us" |
| 30 | Support window expires but instructor still needs help | 7-day window too short for some | Track support usage; flag if no contact by day 5 |

---

## Review cadence

- After every job: check if anything went wrong. If yes, add to this list.
- Weekly: review all entries, remove any that are no longer relevant.
- After 50 jobs: this list is the product. Protect it.
