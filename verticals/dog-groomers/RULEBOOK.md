# Dog groomer rulebook

> What "correct" means for this vertical and every way the AI gets it wrong. Built from research; must be validated against real jobs and updated after every mistake caught. This is the moat.

## How to use this file

Every time we deliver work for a dog groomer customer and something goes wrong, add it here with the fix. After 50 jobs this list is worth more than the model. A competitor can copy our tools; they can't copy this.

---

## Scheduling and breed intervals (PP-013)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 1 | All dogs booked on same interval regardless of breed | Poodle needs grooming every 4-6 weeks; Staffy every 8-12. Same interval = over-groomed or under-groomed | Map breed to recommended interval; set per-pet cadence |
| 2 | Booking tool defaults to 4-week interval | Groomer has to manually adjust every pet | Set breed-specific defaults during onboarding |
| 3 | Groomer's schedule doesn't reflect actual working days | AI offers Saturday when groomer doesn't work Saturdays | Import working hours first; never offer unavailable slots |
| 4 | Mobile groomer route not considered when booking | 3 appointments spread across town = 2 hours travel | Group nearby appointments; check route before confirming |
| 5 | Double-booked groomer across salon and mobile | Same groomer, same time, two locations | Single calendar source of truth; check before confirming any booking |

## Waiting lists (PP-043)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 6 | Cancellation leaves empty slot, no one notified | Lost revenue; groomer sits idle | When a slot opens, notify waiting list for that day/service type |
| 7 | Waiting list is paper-based, never checked | Customers who want slots don't get them | Digitise waiting list; auto-notify on cancellation |
| 8 | No limit on waiting list notifications | Groomer gets 20 messages for one slot | Notify first 3 on the list; rotate if no response within 24hr |
| 9 | Waiting list doesn't capture pet size or service type | Not all cancellations suit all dogs | Capture: pet name, breed, service needed, preferred days |

## Pet records and safety (unique to groomers)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 10 | AI auto-books a dog with known aggression issues without flagging | Safety risk to groomer and other pets | Aggression/behaviour flags must block auto-booking; require human confirmation |
| 11 | Medical conditions (skin issues, lumps, injuries) not in booking notes | Groomer unprepared, potential injury to dog | Medical flags attached to pet profile; visible in booking notes |
| 12 | Pet weight or size not recorded | Groomer arrives with wrong equipment | Record weight/size at onboarding; update annually |
| 13 | Allergy information lost between visits | Groomer uses wrong product, allergic reaction | Allergy notes on pet profile; linked to product COSHH sheet |
| 14 | AI shares pet medical details in outbound message | Data protection breach; medical data in chat logs | Medical/behaviour data stays in secure profile fields; never in customer-facing messages |

## Reminders (PP-065)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 15 | Reminder sent too early | Customer forgets by appointment day | Send 48hr + 2hr reminders, not 7 days |
| 16 | Reminder doesn't include prep instructions | Owner arrives with matted dog, groomer needs extra time | Include: "Please brush your dog before the appointment if possible" |
| 17 | Reminder sent to wrong owner | Multi-dog household, wrong person gets the message | Verify primary contact per pet at onboarding |
| 18 | No reminder for rebooking at next interval | Customer has to remember to book again | Auto-prompt at breed-specific interval: "Time to book [Dog Name]'s next groom?" |
| 19 | Same reminder template for every breed | Feels generic, lower engagement | Reference the actual dog: "Max is due for his clip next week!" |

## Reviews and reputation (PP-079)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 20 | Review request sent before owner has seen the dog | Owner hasn't picked up yet, rates low | Send review request 24hr after appointment, not during |
| 21 | Review request doesn't mention the dog by name | Generic review, less compelling for future customers | "How was Max's groom? We'd love your feedback" |
| 22 | No response to negative review | Bad review sits unanswered, looks like groomer doesn't care | Respond within 24hr: acknowledge, offer to make it right, take offline |
| 23 | Photo of finished groom not sent to owner | Owner can't share on social media, no word-of-mouth | Send photo with service summary; owner permission to share |

## Marketplace migration (PP-013)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 24 | Rover/Wag fees eat into margins on repeat clients | 20% marketplace fee on a client who's been 10 times | Identify repeat marketplace clients; offer direct booking with consent |
| 25 | Migration offered without client consent | Client didn't agree to share details elsewhere | Every migration requires explicit client consent |
| 26 | Marketplace kept for all bookings after migration | Groomer still paying fees for direct-repeat clients | Migrate repeat clients to direct; keep marketplace for discovery only |

## Pricing and payments

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 27 | Price varies by dog size but booking tool doesn't capture size | Customer books small-dog price for a Great Dane | Require weight/size at booking; price adjusts accordingly |
| 28 | Extras (teeth cleaning, nail filing, de-shedding) not priced | Customer expects all-inclusive, groomer charges extra | Price book must itemise extras; quote confirms what's included |
| 29 | Deposit not taken for first-time customers | No-show on first visit, groomer loses a slot | Require deposit for new customers; auto-collect |
| 30 | Payment not taken at time of service | Customer promises to pay later, forgets | Payment due at collection; card on file for auto-charge |

## Legal and compliance

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 31 | Animal Welfare Act duty of care not documented | Legal requirement for boarding/daycare; grooming falls under welfare duty | Document welfare protocol: what happens if dog is injured or in distress |
| 32 | No incident record for cuts, nicks, or reactions | Liability risk; no evidence if dispute arises | Log every incident: date, pet, issue, action taken, owner notified |
| 33 | Insurance not verified before onboarding | Groomer operates uninsured, our liability | Verify public liability insurance at intake; record in CRM |

## General

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 34 | AI promises a service the groomer doesn't offer | Customer expects hand-stripping, groomer only does clippering | Only reference services in approved service menu |
| 35 | AI promises same-day booking when diary is full | Customer books, then gets cancelled, trust broken | Check availability before confirming |
| 36 | Handover doesn't explain how to update prices | Groomer changes prices, AI still quotes old ones | Handover includes: "To update prices, edit [file] and tell us" |
| 37 | Support window expires but groomer still needs help | 7-day window too short for some | Track support usage; flag if no contact by day 5 |

---

## Review cadence

- After every job: check if anything went wrong. If yes, add to this list.
- Weekly: review all entries, remove any that are no longer relevant.
- After 50 jobs: this list is the product. Protect it.
