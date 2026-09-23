# Lash artist rulebook

> What "correct" means for this vertical and every way the AI gets it wrong. Built from research; must be validated against real jobs and updated after every mistake caught. This is the moat.

## How to use this file

Every time we deliver work for a lash artist customer and something goes wrong, add it here with the fix. After 50 jobs this list is worth more than the model. A competitor can copy our tools; they can't copy this.

---

## No-show prevention (PP-008)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 1 | Deposit amount doesn't match treatment length | Customer no-shows a 2-hr volume set for £5 deposit when the chair costs £50+ | Set deposits at 20-30% of treatment value, minimum £10 |
| 2 | Deposit deadline too late | Customer books, never pays, no-shows | Deposit due within 2 hours of booking, auto-cancel after |
| 3 | Reminder sent too early | Customer forgets by appointment day | Send 48hr + 2hr reminders, not 7 days |
| 4 | Reminder tone too formal | Feels like a bank, not a studio | Friendly tone: "See you Thursday! Quick reminder — your volume lashes are at 2pm" |
| 5 | No cancellation policy stated upfront | Customer disputes deposit when they cancel late | State cancellation window in booking confirmation (24hr or 48hr) |
| 6 | No-show fee not enforced | Artist eats the cost, learns nothing | Auto-charge no-show fee after grace period; log it |
| 7 | Repeat no-shower not flagged | Same person keeps wasting slots | Track no-show rate per customer; flag at 2+ no-shows |

## DM triage and booking (PP-002)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 8 | Quick reply sends before customer finishes typing | Feels robotic, answers wrong question | Only trigger quick reply after message is complete |
| 9 | Price quote doesn't match actual treatment | Customer shows up expecting £25, price is £65 | Pull prices from approved price book only |
| 10 | Availability shown for wrong location | Artist works from home on certain days, studio on others | Link availability to location/treatment, not just calendar |
| 11 | Deposit link sent without treatment confirmation | Customer confused about what they're depositing for | Confirm treatment + time + price before sending deposit link |
| 12 | Instagram DM enquiry answered, TikTok DM missed | Enquiries split across platforms, some fall through | All DMs route to same triage; if not possible, document which platforms are monitored |
| 13 | After-hours enquiry auto-replies with "we'll get back to you" but nobody follows up | Customer goes to next artist | Auto-reply acknowledges; next-morning follow-up is mandatory |
| 14 | Enquiry labelled "booked" when they only asked about price | Pipeline data is wrong, follow-up never happens | Enquiry stages: new → quoted → deposit_paid → booked → completed |

## Patch test and safety (SAFETY-PATCH-TEST)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 15 | Patch test not scheduled before first lash tint or lift | Allergic reaction, liability, COSHH breach | Require patch-test booking 24-48hr before any chemical treatment |
| 16 | Patch test result not recorded | No proof of safety check if reaction occurs | Record date, product used, and result in customer file |
| 17 | Patch test expired — customer had one 6 months ago but product changed | Allergic sensitisation risk | Patch test valid for 6 months per product; retest after expiry |
| 18 | AI suggests treatment without asking about allergies | Customer with formaldehyde/latex adhesive allergies gets booked for contraindicated service | Ask about allergies and eye conditions during intake; flag in profile |
| 19 | Allergy info not passed to booking notes | Artist uses adhesive customer is allergic to | Link allergy notes to customer profile; flag on every booking |
| 20 | COSHH data sheets not maintained for adhesives and tints | Legal requirement, not optional | Track product safety data sheets; flag when missing |
| 21 | Client arrives with eye infection and treatment proceeds | Infection spread, liability | Ask client to confirm no eye infection in 48hr reminder; refuse if present |

## Refill intervals and rebooking (PP-038)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 22 | Win-back sent too early | Customer just had lashes done, feels spammed | Wait minimum 2 weeks before rebooking reminder |
| 23 | Win-back sent too late | Customer already booked refill elsewhere | Send at typical interval: classic=2-3wk, volume=2-3wk, lift=6-8wk |
| 24 | Win-back message is generic | "Hey, haven't seen you!" — no personal touch | Reference last treatment: "Your volume set from 2 weeks ago — time for a refill?" |
| 25 | No refill interval tracked per treatment type | Can't predict when customer needs rebooking | Map each treatment: classic lashes=2-3wk, volume=2-3wk, lift=tint=6-8wk |
| 26 | Win-back sent without approval | Artist didn't want to message that customer | Every outbound win-back requires owner approval |
| 27 | Rebooking link goes to wrong booking page | Customer clicks, can't book, gives up | Verify booking link works for the specific treatment before including |
| 28 | Prepaid package balance not tracked | Customer has 3 refills left, nobody reminds them | Track package balances and expiry; send reminders |

## Reviews and reputation (PP-060)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 29 | Review request sent before treatment is complete | Customer hasn't seen final result, rates low | Send review request 24hr after appointment, not during |
| 30 | Review request goes to wrong platform | Artist cares about Instagram, request goes to Google | Ask which platform matters most; send there only |
| 31 | No response to negative review | Bad review sits unanswered, looks like artist doesn't care | Respond within 24hr: acknowledge, offer to make it right, take offline |
| 32 | Review request doesn't mention what to include | "Great service!" — no detail, no SEO value | Suggest: "Mention the treatment, the location, and what you liked" |
| 33 | Same review request template every time | Feels spammy, lower response rate | Vary the message; reference the actual treatment |

## Pricing and payments

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 34 | Price book outdated | AI quotes old prices, artist has to correct, customer annoyed | Verify price book monthly; flag when last updated |
| 35 | Deposit doesn't cover material cost for volume/hybrid sets | Artist loses money on expensive adhesive and lash supplies | Higher deposits for volume and hybrid sets |
| 36 | Travel charge not included for mobile artists | Quoted £35, actual is £45 with travel | Include travel in quote if mobile; state it explicitly |
| 37 | Group booking deposit is per-person, not per-group | 4 people book, only 1 deposit paid | Calculate deposit per person for group bookings |

## Legal and data protection

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 38 | Client photos stored without consent | GDPR breach, reputational damage | Record explicit consent for before/after photos; delete on request |
| 39 | Under-18 appointment without guardian consent | Safeguarding issue | Flag under-18 bookings; require guardian contact |
| 40 | Tips not passed through correctly | Legal requirement under Fair Tips Act 2023 | Allocate 100% of qualifying tips; document policy |
| 41 | Card data stored by artist | PCI DSS breach | Never store raw card numbers; use Stripe/Square tokenisation only |
| 42 | Allergy records not retained securely | Health data is special category under UK GDPR | Store allergy and patch-test records with encryption; delete on request |

---

## Review cadence

- After every job: check if anything went wrong. If yes, add to this list.
- Weekly: review all entries, remove any that are no longer relevant.
- After 50 jobs: this list is the product. Protect it.
