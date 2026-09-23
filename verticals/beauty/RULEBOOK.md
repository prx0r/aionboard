# Beauty treatment rulebook

> What "correct" means for this vertical and every way the AI gets it wrong. Built from research; must be validated against real jobs and updated after every mistake caught. This is the moat.

## How to use this file

Every time we deliver work for a beauty treatment customer and something goes wrong, add it here with the fix. After 50 jobs this list is worth more than the model. A competitor can copy our tools; they can't copy this.

---

## No-show prevention (PP-008)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 1 | Deposit amount doesn't match treatment length | Customer no-shows a 90-min facial for £5 deposit when the room costs £40+ | Set deposits at 20-30% of treatment value, minimum £10 |
| 2 | Deposit deadline too late | Customer books, never pays, no-shows | Deposit due within 2 hours of booking, auto-cancel after |
| 3 | Reminder sent too early | Customer forgets by appointment day | Send 48hr + 2hr reminders, not 7 days |
| 4 | Reminder tone too formal | Feels like a bank, not a salon | Friendly tone: "See you Thursday! Quick reminder — your hydrating facial is at 2pm" |
| 5 | No cancellation policy stated upfront | Customer disputes deposit when they cancel late | State cancellation window in booking confirmation (24hr or 48hr) |
| 6 | No-show fee not enforced | Practitioner eats the cost, learns nothing | Auto-charge no-show fee after grace period; log it |
| 7 | Repeat no-shower not flagged | Same person keeps wasting slots | Track no-show rate per customer; flag at 2+ no-shows |

## DM triage and booking (PP-002)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 8 | Quick reply sends before customer finishes typing | Feels robotic, answers wrong question | Only trigger quick reply after message is complete |
| 9 | Price quote doesn't match actual treatment | Customer shows up expecting £25, price is £45 | Pull prices from approved price book only |
| 10 | Availability shown for wrong location | Practitioner works from home on certain days, clinic on others | Link availability to location/treatment, not just calendar |
| 11 | Deposit link sent without treatment confirmation | Customer confused about what they're depositing for | Confirm treatment + time + price before sending deposit link |
| 12 | Instagram DM enquiry answered, TikTok DM missed | Enquiries split across platforms, some fall through | All DMs route to same triage; if not possible, document which platforms are monitored |
| 13 | After-hours enquiry auto-replies with "we'll get back to you" but nobody follows up | Customer goes to next practitioner | Auto-reply acknowledges; next-morning follow-up is mandatory |
| 14 | Enquiry labelled "booked" when they only asked about price | Pipeline data is wrong, follow-up never happens | Enquiry stages: new → quoted → deposit_paid → booked → completed |

## Patch test and safety (PP-038)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 15 | Patch test not scheduled before first tint or chemical treatment | Allergic reaction, liability, COSHH breach | Require patch-test booking 24-48hr before any chemical treatment |
| 16 | Patch test result not recorded | No proof of safety check if reaction occurs | Record date, product used, and result in customer file |
| 17 | Patch test expired — customer had one 6 months ago but product changed | Allergic sensitisation risk | Patch test valid for 6 months per product; retest after expiry |
| 18 | AI suggests treatment without asking about allergies | Customer with nickel/lash adhesive allergies gets booked for contraindicated service | Ask about allergies and skin conditions during intake; flag in profile |
| 19 | Allergy info not passed to booking notes | Practitioner uses product customer is allergic to | Link allergy notes to customer profile; flag on every booking |
| 20 | COSHH data sheets not maintained for products | Legal requirement, not optional | Track product safety data sheets; flag when missing |

## Rebooking and win-back (PP-037 implicit via packages)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 21 | Win-back sent too early | Customer just had treatment done, feels spammed | Wait minimum 2 weeks before rebooking reminder |
| 22 | Win-back sent too late | Customer already booked elsewhere | Send at typical interval: facial=4-6wk, waxing=3-4wk, tinting=3-4wk |
| 23 | Win-back message is generic | "Hey, haven't seen you!" — no personal touch | Reference last treatment: "Your hydrating facial from 4 weeks ago — time for a refresh?" |
| 24 | No treatment interval tracked per service type | Can't predict when customer needs rebooking | Map each service to its interval: facial=4-6wk, waxing=3-4wk, tinting=3-4wk |
| 25 | Win-back sent without approval | Practitioner didn't want to message that customer | Every outbound win-back requires owner approval |
| 26 | Rebooking link goes to wrong booking page | Customer clicks, can't book, gives up | Verify booking link works for the specific treatment before including |

## Reviews and reputation (PP-060)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 27 | Review request sent before treatment is complete | Customer hasn't seen final result, rates low | Send review request 24hr after appointment, not during |
| 28 | Review request goes to wrong platform | Practitioner cares about Google, request goes to Facebook | Ask which platform matters most; send there only |
| 29 | No response to negative review | Bad review sits unanswered, looks like practitioner doesn't care | Respond within 24hr: acknowledge, offer to make it right, take offline |
| 30 | Review request doesn't mention what to include | "Great service!" — no detail, no SEO value | Suggest: "Mention the treatment, the location, and what you liked" |
| 31 | Same review request template every time | Feels spammy, lower response rate | Vary the message; reference the actual treatment |

## Pricing and payments

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 32 | Price book outdated | AI quotes old prices, practitioner has to correct, customer annoyed | Verify price book monthly; flag when last updated |
| 33 | Deposit doesn't cover material cost for premium treatments | Practitioner loses money on expensive product treatments | Higher deposits for chemical peels, specialist facials, tinting |
| 34 | Travel charge not included for mobile practitioners | Quoted £35, actual is £45 with travel | Include travel in quote if mobile; state it explicitly |
| 35 | Group booking deposit is per-person, not per-group | 4 people book, only 1 deposit paid | Calculate deposit per person for group bookings |

## Legal and data protection

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 36 | Client photos stored without consent | GDPR breach, reputational damage | Record explicit consent for before/after photos; delete on request |
| 37 | Under-18 appointment without guardian consent | Safeguarding issue | Flag under-18 bookings; require guardian contact |
| 38 | Tips not passed through correctly | Legal requirement under Fair Tips Act 2023 | Allocate 100% of qualifying tips; document policy |
| 39 | Card data stored by practitioner | PCI DSS breach | Never store raw card numbers; use Stripe/Square tokenisation only |

---

## Review cadence

- After every job: check if anything went wrong. If yes, add to this list.
- Weekly: review all entries, remove any that are no longer relevant.
- After 50 jobs: this list is the product. Protect it.
