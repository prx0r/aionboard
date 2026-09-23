# Hairdresser rulebook

> What "correct" means for this vertical and every way the AI gets it wrong. Built from research; must be validated against real jobs and updated after every mistake caught. This is the moat.

## How to use this file

Every time we deliver work for a hairdresser customer and something goes wrong, add it here with the fix. After 50 jobs this list is worth more than the model. A competitor can copy our tools; they can't copy this.

---

## No-show prevention (PP-008)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 1 | Deposit amount doesn't match service length | Customer no-shows a 2-hair colour for £5 deposit when the chair costs £60+ | Set deposits at 20-30% of service value, minimum £10 |
| 2 | Deposit deadline too late | Customer books, never pays, no-shows | Deposit due within 2 hours of booking, auto-cancel after |
| 3 | Reminder sent too early | Customer forgets by appointment day | Send 48hr + 2hr reminders, not 7 days |
| 4 | Reminder tone too formal | Feels like a bank, not a salon | Friendly tone: "See you Thursday! Quick reminder — your colour is at 2pm" |
| 5 | No cancellation policy stated upfront | Customer disputes deposit when they cancel late | State cancellation window in booking confirmation (24hr or 48hr) |
| 6 | No-show fee not enforced | Hairdresser eats the cost, learns nothing | Auto-charge no-show fee after grace period; log it |
| 7 | Repeat no-shower not flagged | Same person keeps wasting slots | Track no-show rate per customer; flag at 2+ no-shows |

## DM triage and booking (PP-002)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 8 | Quick reply sends before customer finishes typing | Feels robotic, answers wrong question | Only trigger quick reply after message is complete |
| 9 | Price quote doesn't match actual service | Customer shows up expecting £25, price is £45 | Pull prices from approved price book only |
| 10 | Availability shown for wrong location | Hairdresser works from home on certain days, salon on others | Link availability to location/service, not just calendar |
| 11 | Deposit link sent without service confirmation | Customer confused about what they're depositing for | Confirm service + time + price before sending deposit link |
| 12 | Instagram DM enquiry answered, TikTok DM missed | Enquiries split across platforms, some fall through | All DMs route to same triage; if not possible, document which platforms are monitored |
| 13 | After-hours enquiry auto-replies with "we'll get back to you" but nobody follows up | Customer goes to next hairdresser | Auto-reply acknowledges; next-morning follow-up is mandatory |
| 14 | Enquiry labelled "booked" when they only asked about price | Pipeline data is wrong, follow-up never happens | Enquiry stages: new → quoted → deposit_paid → booked → completed |

## Service area and travel (HAIR-SERVICE-AREA)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 15 | Customer books without mentioning they're out of area | Hairdresser arrives to find a 40-mile trip, wastes time or loses money | Ask for postcode at enquiry; state travel radius and fees upfront |
| 16 | Travel charge not included in quoted price | Customer expects £35, actual is £50 with travel | Include travel in quote for mobile services; state it explicitly |
| 17 | Service area not defined on booking profile | Enquiries from 50 miles away, all rejected | Set clear travel radius on Google Business Profile and booking tools |
| 18 | No travel fee tiering for distance bands | Same charge for 5 miles and 25 miles | Define distance bands: local (free), mid-range (£X), long-distance (£Y) |
| 19 | Preparation time not blocked in calendar | Back-to-back bookings with no travel/setup buffer | Block 30min before and after mobile appointments for travel and setup |

## Rebooking and win-back (PP-037)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 20 | Win-back sent too early | Customer just had hair done, feels spammed | Wait minimum 3 weeks before rebooking reminder |
| 21 | Win-back sent too late | Customer already booked elsewhere | Send at typical interval: cut=6-8wk, colour=4-6wk, braids=4-6wk |
| 22 | Win-back message is generic | "Hey, haven't seen you!" — no personal touch | Reference last service: "Your balayage from 5 weeks ago — roots showing yet?" |
| 23 | No maintenance interval tracked per service type | Can't predict when customer needs rebooking | Map each service: cut=6-8wk, colour regrowth=4-6wk, braids=4-6wk |
| 24 | Win-back sent without approval | Hairdresser didn't want to message that customer | Every outbound win-back requires owner approval |
| 25 | Rebooking link goes to wrong booking page | Customer clicks, can't book, gives up | Verify booking link works for the specific service before including |

## Reviews and reputation (PP-060)

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 26 | Review request sent before service is complete | Customer hasn't seen final result, rates low | Send review request 24hr after appointment, not during |
| 27 | Review request goes to wrong platform | Hairdresser cares about Google, request goes to Facebook | Ask which platform matters most; send there only |
| 28 | No response to negative review | Bad review sits unanswered, looks like hairdresser doesn't care | Respond within 24hr: acknowledge, offer to make it right, take offline |
| 29 | Review request doesn't mention what to include | "Great service!" — no detail, no SEO value | Suggest: "Mention the service, the location, and what you liked" |
| 30 | Same review request template every time | Feels spammy, lower response rate | Vary the message; reference the actual service |

## Safety and compliance

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 31 | Patch test not recorded before colour or chemical treatment | Allergic reaction, liability, COSHH breach | Require patch-test confirmation before first use of new product |
| 32 | Allergy info not passed to booking notes | Hairdresser uses dye on dye-allergic customer | Link allergy notes to customer profile; flag on booking |
| 33 | COSHH records not maintained | Legal requirement, not optional | Track product safety data sheets; flag when missing |
| 34 | Ventilation not considered for chemical treatments | Respiratory irritation, HSE guidance breach | Note COSHH ventilation requirements in treatment notes |
| 35 | Under-18 appointment without guardian consent | Safeguarding issue | Flag under-18 bookings; require guardian contact |

## Pricing and payments

| # | What goes wrong | Why it matters | Fix |
|---|----------------|----------------|-----|
| 36 | Price book outdated | AI quotes old prices, hairdresser has to correct, customer annoyed | Verify price book monthly; flag when last updated |
| 37 | Travel charge not included for mobile hairdressers | Quoted £35, actual is £50 with travel | Include travel in quote if mobile; state it explicitly |
| 38 | Group booking deposit is per-person, not per-group | 4 people book, only 1 deposit paid | Calculate deposit per person for group bookings |
| 39 | Chair-rental income splitting unclear | Chair-rental model has different economics, AI quotes wrong base | Understand business model before quoting; chair-rental has different margins |

---

## Review cadence

- After every job: check if anything went wrong. If yes, add to this list.
- Weekly: review all entries, remove any that are no longer relevant.
- After 50 jobs: this list is the product. Protect it.
