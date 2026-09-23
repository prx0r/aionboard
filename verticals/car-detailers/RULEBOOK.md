# Car detailer rulebook

> What "correct" means for this vertical and every way the AI gets it wrong. Built from research; must be validated against real jobs and updated after every mistake caught. This is the moat.

## How to use this file

Every time we deliver work for a car detailer customer and something goes wrong, add it here with the fix. After 50 jobs this list is worth more than the model. A competitor can copy our tools; they can't copy this.

---

## Quote intake (DISCOVERY-QUOTE-INTAKE)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 1 | Quote request doesn't capture vehicle type | Mini valet on a van is not the same as a saloon; wrong price, wrong time | Require: make, model, body type (saloon/hatch/SUV/van) |
| 2 | No condition photos requested | Customer says "it's fine inside", detailer arrives to a bin on wheels | Request 3-5 photos: exterior, interior front, interior rear, boot, any problem areas |
| 3 | Location details incomplete | Detailer arrives at wrong address or can't find water access | Capture: full address, access notes, water/electric availability |
| 4 | Timing not captured | Customer wants it done Saturday, detailer is fully booked | Capture: preferred date, flexibility (exact / this week / whenever) |
| 5 | Quote sent without owner approval | AI quotes £120, owner would charge £180 for this vehicle condition | Every quote requires owner approval before sending |
| 6 | Interior-only or exterior-only detail requested, AI quotes full package | Customer expects £60, gets quoted £150 | Match quote to requested scope: exterior only, interior only, or full |

## Repeat bookings (DISCOVERY-REPEAT)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 7 | No follow-up after completed detail | Customer goes 6 months without a wash, detailer loses repeat revenue | Send consent-based reminder at typical interval (4-8 weeks for maintenance, 3-4 months for full) |
| 8 | Win-back sent too early | Customer just had car done, feels spammed | Minimum 3 weeks before rebooking reminder |
| 9 | Win-back sent too late | Customer already found someone else | Track typical interval per service type; send at 80% of interval |
| 10 | Win-back message is generic | "Hey, time for a wash!" — no personal touch | Reference last service: "Your full detail on the BMW from last month — the ceramic coat is due for a top-up" |
| 11 | Repeat offer doesn't account for seasonality | Winter details are different from summer maintenance | Adjust service suggestions by season: winter = protection package, summer = maintenance wash |

## Weather and travel

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 12 | Jobs booked in rain with no shelter plan | Mobile detailer can't do exterior work in the rain, wastes travel time | Check weather forecast 48h before; flag outdoor jobs in rain; confirm covered area availability |
| 13 | Travel time not accounted for in scheduling | Detailer double-books, arrives late to both jobs | Include travel time between jobs; buffer 30min for mobile work |
| 14 | Remote location quoted without travel surcharge | 45-minute drive eats into margins | Include travel in quote for jobs beyond defined radius |
| 15 | Multiple jobs in same area not batched | Detailer drives across town twice in one day | Group nearby jobs on same day when possible |

## Vehicle condition and photos

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 16 | Photos not received before quoting | Quote is guesswork; actual price is 50% more | Block quote until photos are received |
| 17 | Customer photos hide damage | Detailer blamed for pre-existing scratches | Request photos of all panels; note pre-existing damage in job record before starting |
| 18 | AI promises "like new" result on heavily worn interior | Customer expects miracles, leaves disappointed | Set honest expectations: "We can significantly improve it, but deep stains and tears may need specialist work" |
| 19 | Vehicle modifications not flagged | Aftermarket tint, wraps, or coatings affect service approach | Ask about modifications in intake; flag in job notes |

## Pricing and payments

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 20 | Price book doesn't differentiate by vehicle size | Hatchback quoted same as large SUV, 2 hours extra work | Price tiers: small (hatch/saloon), medium (estate/SUV), large (van/4x4) |
| 21 | Deposit not taken for full details | Detailer drives 30min, customer cancels on arrival | Require deposit for services over £80 or over 2 hours |
| 22 | Add-ons not priced upfront | Customer expects headlight restoration included in full detail | List all add-ons with prices in quote; customer selects before work starts |
| 23 | Payment method not confirmed before arrival | Detailer finishes, customer wants to pay by card but no reader | Confirm payment method during booking: card, cash, bank transfer |

## Safety and compliance

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 24 | Wastewater discharged into surface drain | Pollution offence, fine from environment agency | Confirm drainage available; note pollution prevention obligations |
| 25 | Customer's property damaged during service | Liability dispute, reputation damage | Photograph vehicle and surroundings before starting; note any pre-existing damage |
| 26 | No insurance confirmation | Detailer working without cover, customer has no recourse | Verify public liability insurance; include in intake |

## General

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 27 | AI promises same-day booking when diary is full | Customer expects car done today, detailer is booked out 3 days | Check availability before confirming |
| 28 | AI promises results that require specialist equipment | Customer expects paint correction with a bucket and sponge | Only promise services in approved service menu with confirmed equipment |
| 29 | Handover doesn't explain how to update prices | Detailer changes prices, AI still quotes old ones | Handover includes: "To update prices, edit [file] and tell us" |
| 30 | Support window expires but detailer still needs help | 7-day window too short for some | Track support usage; flag if no contact by day 5 |

---

## Review cadence

- After every job: check if anything went wrong. If yes, add to this list.
- Weekly: review all entries, remove any that are no longer relevant.
- After 50 jobs: this list is the product. Protect it.
