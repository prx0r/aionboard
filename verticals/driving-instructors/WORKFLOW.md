# Driving instructors workflow

> The actual day-to-day. What happens, where the pain is, what the AI does.

## The day (research-backed)

| Time | What happens | Pain | AI/WhatsApp solution |
|------|-------------|------|---------------------|
| 8:00–8:15 | Check diary, prep for first lesson | — | — |
| 8:30–9:30 | Lesson 1 | Phone rings during lesson | AI answers: "John is teaching at the moment. Reply to this message and he'll get back to you" |
| 9:30–10:00 | Drive to pickup | — | Auto-remind pupil: "Lesson at 10am. Pick-up at [address]" |
| 10:00–11:00 | Lesson 2 | — | — |
| 11:00–11:15 | Admin window | Responding to enquiries | AI has already qualified leads, sent pricing, booked trial lessons |
| 11:15–12:15 | Lesson 3 | — | — |
| 12:15–13:00 | Lunch + admin | — | — |
| 13:00–17:00 | Lessons 4–7 | — | — |
| 17:00–18:00 | Admin: progress tracking, test bookings, invoicing | Hours of paperwork | AI updates progress, sends invoices, chases payments |

## Enquiry flow (WhatsApp)

```
"Hi, I'm looking for driving lessons"
  ↓
AI: "Welcome! Are you a complete beginner or do you have some experience?"
  ↓
AI: "What area are you in?" → checks service area
  ↓
AI: "Lessons are £35/hr. I have availability on [days].
     Would you like a trial lesson?"
  ↓
Customer confirms → AI sends:
  "Trial lesson booked for [date/time].
   Pick-up at [address].
   Pay £35 to confirm: [Stripe link]"
  ↓
Reminder 24hr before: "Your lesson is tomorrow at [time]. See you at [address]!"
Reminder 1hr before: "See you in an hour! I'll be at [address]."
```

## Cancellation + waitlist flow

```
Pupil cancels
  ↓
AI: "No problem! I'll add you to the waitlist for earlier slots."
  ↓
AI logs cancellation reason (optional): work, illness, weather, nerves
  ↓
When slot opens: "Hi [name], I have a slot free on [date/time]. Want it?"
  ↓
If yes: confirmed + reminder sent
If no: next available pupil contacted
  ↓
Cancellation rate tracked → flag if >20% in a month
```

## Progress tracking (WhatsApp)

```
After each lesson:
  ↓
AI to instructor: "Log lesson notes for [pupil]?"
  ↓
Instructor: voice note or text with notes
  ↓
AI: updates progress, stores in pupil record
  ↓
AI to pupil (weekly):
  "Hi [name]! This week you covered: [topics].
   Next lesson focus: [topic].
   Test readiness: 72% — estimated [X] more lessons."
```

## Test booking workflow

```
AI monitors pupil progress
  ↓
When readiness >90%: "Ready to book test? I can check availability at [test centres]"
  ↓
AI checks GOV.UK availability
  ↓
AI books test via GOV.UK
  ↓
Sends confirmation:
  "Test booked for [date] at [centre].
   Lesson focus: [topics] until test.
   Pass rate at this centre: 48%."
  ↓
Sends reminder: 1 week, 1 day before
1 day before: "Good luck tomorrow! Key things to remember: [3 bullet points]"
```

## Block hire workflow ( intensive courses)

```
Pupil asks about intensive/course
  ↓
AI: "I offer 10/20/30-hour packages.
     10hr: £320 (save £30) — typically takes 4-6 weeks
     20hr: £620 (save £80) — typically takes 2-3 weeks
     30hr: £880 (save £170) — often enough for test
     Which suits you?"
  ↓
Pupil confirms → deposit link sent
  ↓
AI schedules: "Your course starts [date]. Lessons on [days] at [times].
Remaining balance split across weeks."
  ↓
AI tracks progress through package hours
  ↓
When hours low: "You have [X] hours left. After that, lessons are £35/hr.
Want to top up?"
```

## What the AI agent does at each step

| Step | AI action | Human action |
|------|-----------|-------------|
| Enquiry received | Qualifies experience level, area, availability | Nothing |
| Trial lesson booked | Sends confirmation + payment link | Nothing |
| 24hr/1hr before | Sends reminders to pupil | Nothing |
| During lesson | Answers calls: "John is teaching. Reply here" | Teaches |
| After lesson | Prompts instructor for notes, updates progress | Logs notes (voice/text) |
| Weekly update | Sends pupil progress summary | Nothing |
| Test ready | Checks GOV.UK, books test, sends confirmation | Nothing |
| Pupil cancels | Manages waitlist, fills slot | Nothing |
| Course running | Tracks hours remaining, prompts top-up | Nothing |
| Lesson done | Sends invoice after each lesson | Approves |

## Key metrics

| Metric | Target | How |
|--------|--------|-----|
| Enquiry response time | <5 min | AI handles 24/7 |
| Trial lesson conversion | >70% | Fast response + easy booking |
| Lesson utilisation | >85% | AI fills gaps from waitlist |
| Pass rate | >65% | Progress tracking + focused prep |
| Payment collection | Same-day | Auto-invoice after lesson |
| Cancellation rate | <15% | AI manages waitlist to recover slots |
| Block hire uptake | >30% of pupils | Upsell from trial lesson |

## What the top 10% do differently

- Respond to enquiries within 2 minutes — AI makes this automatic
- Send progress photos after each lesson: "Here's what [pupil] covered today"
- Offer a free theory test app alongside lessons — adds value at zero cost
- Track pass rates by test centre — route pupils to centres with highest pass rates
- Send a "congrats" message with Google review link the moment they pass
- Collect video testimonials from passing pupils — gold for social proof
- Offer a "bring a friend" referral discount (£20 off each) — word of mouth is everything
