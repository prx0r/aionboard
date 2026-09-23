# DEMOS.md

> One free demo per vertical. Interactive, visual, personalised. The demo IS the product.

## The demo principle

**Don't tell them what it does. Let them try it themselves.**

Every demo:
1. Uses THEIR business data (name, services, prices)
2. Shows the AI working in real-time
3. Is accessible via a link they can share
4. Takes 30 seconds to try
5. Makes them want the full setup

---

## NAILS demo

### What it is

A WhatsApp-style chatbot that answers nail enquiries. Pre-loaded with their services and prices.

### How it works

```
User opens demo link
  ↓
Sees: "Hi! I'm AI assistant for [business name]. Ask me anything about nails."
  ↓
Types: "How much for gel nails?"
  ↓
AI responds: "Gel nails at [business] cost £35. Takes about 45 minutes.
Would you like to book? Here's the link: [booking link]"
  ↓
User: "Do you do acrylics?"
  ↓
AI: "Yes! Acrylic full sets are £55. We also do infills at £40.
Want to see our portfolio? [Instagram link]"
```

### Demo page design

```
┌─────────────────────────────────────────────────┐
│  💅 [Business Name] — AI Assistant              │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ Hi! I'm the AI assistant for            │   │
│  │ [Business Name]. Ask me anything        │   │
│  │ about our nail services.                │   │
│  │                                         │   │
│  │ 💅 Gel manicure — £35                   │   │
│  │ 💅 Acrylic full set — £55               │   │
│  │ 💅 Pedicure — £40                       │   │
│  │ 💅 Nail art — from £5                   │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ Type a message...                 [Send] │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ⚡ Powered by AI Onboard                      │
└─────────────────────────────────────────────────┘
```

### Tech to build

- Chat interface (reuse `site/chat.html`)
- Knowledge bundle from their profile
- Deploy to `demos.aionboard.co.uk/nails/[business-slug]`

### How to show it

> "Here's your AI assistant. Try asking it about your services."

[They type questions, see instant responses]

> "This is what your customers will see 24/7. Want to set it up on your WhatsApp?"

---

## ELECTRICIAN demo

### What it is

An AI that answers missed calls, drafts quotes, and follows up. Pre-loaded with their price book.

### How it works

```
User opens demo link
  ↓
Sees: "Missed call? No problem. I'll handle it."
  ↓
Types: "I need 3 extra sockets in my kitchen"
  ↓
AI responds: "I can help with that. For 3 extra sockets in a kitchen,
I'd estimate £285-£360 including materials. This includes:
- 3x double sockets
- 32A RCBO
- Cable and containment
- EIC certificate
Want me to book a site visit? What's your postcode?"
  ↓
User: "M1 1AA"
  ↓
AI: "Great! I have availability this Thursday or Friday.
Which works better? I'll send you a confirmation."
```

### Demo page design

```
┌─────────────────────────────────────────────────┐
│  ⚡ [Business Name] — AI Quote Assistant        │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ 📞 Missed call? No problem.             │   │
│  │ I'll handle it while you're on the tools.│   │
│  │                                         │   │
│  │ Tell me what you need and I'll draft     │   │
│  │ a quote from [Business]'s price book.   │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ I need 3 extra sockets in my kitchen    │   │
│  │                                 [Send]  │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ⚡ Powered by AI Onboard                      │
└─────────────────────────────────────────────────┘
```

### Tech to build

- Quote calculator from price book
- Site visit booking flow
- Deploy to `demos.aionboard.co.uk/electrician/[business-slug]`

---

## DOG GROOMERS demo

### What it is

An AI that books appointments, reminds at breed-specific intervals, and fills cancellations.

### How it works

```
User opens demo link
  ↓
Sees: "Hi! I'm the booking assistant for [Groomer]. What breed is your dog?"
  ↓
Types: "Cockapoo"
  ↓
AI: "Cockapoos typically need grooming every 6-8 weeks.
We offer: Bath & blow-dry (£35), Full groom (£45), Puppy's first groom (£30).
What would you prefer?"
  ↓
User: "Full groom"
  ↓
AI: "£45 for a full groom. I have availability:
- Thursday 2pm
- Friday 10am
- Saturday 11am
Which suits you?"
```

### Demo page design

```
┌─────────────────────────────────────────────────┐
│  🐕 [Groomer Name] — AI Booking Assistant       │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ Hi! I'm the booking assistant for       │   │
│  │ [Groomer]. What breed is your dog?      │   │
│  │                                         │   │
│  │ 🐕 Cockapoo — Full groom £45            │   │
│  │ 🐕 Labradoodle — Full groom £55         │   │
│  │ 🐕 Yorkshire Terrier — Full groom £35   │   │
│  │ 🐕 German Shepherd — De-shed £60        │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ What breed is your dog?          [Send] │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  🐕 Powered by AI Onboard                      │
└─────────────────────────────────────────────────┘
```

### Tech to build

- Breed-aware duration calculator
- Booking flow with availability
- Deploy to `demos.aionboard.co.uk/groomers/[business-slug]`

---

## CLEANERS demo

### What it is

An AI that schedules recurring cleans, sends key access instructions, and chases invoices.

### How it works

```
User opens demo link
  ↓
Sees: "Hi! I'm the scheduling assistant for [Cleaner]. How can I help?"
  ↓
Types: "I need a weekly clean"
  ↓
AI: "Great! I can set that up. What day works best?
- Monday
- Wednesday
- Friday
Also, how will we access the property?
- Key safe
- Smart lock
- I'll be home"
  ↓
User: "Wednesday, key safe"
  ↓
AI: "Perfect! Weekly cleans on Wednesdays, starting next week.
Please set a 4-digit code for your key safe and share it here.
I'll send you a confirmation with the access instructions."
```

### Demo page design

```
┌─────────────────────────────────────────────────┐
│  🧹 [Cleaner Name] — AI Scheduling Assistant    │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ Hi! I'm the scheduling assistant for    │   │
│  │ [Cleaner]. I handle recurring bookings, │   │
│  │ key access, and invoicing.              │   │
│  │                                         │   │
│  │ 🧹 Weekly clean — from £80              │   │
│  │ 🧹 Fortnightly clean — from £90         │   │
│  │ 🧹 Deep clean — from £150               │   │
│  │ 🧹 End of tenancy — from £200           │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ How can I help?                  [Send] │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  🧹 Powered by AI Onboard                      │
└─────────────────────────────────────────────────┘
```

---

## HAIR demo

### What it is

An AI that books appointments, collects colour consultations, and checks travel areas.

### How it works

```
User opens demo link
  ↓
Sees: "Hi! I'm the booking assistant for [Hairdresser]. What service are you after?"
  ↓
Types: "Balayage"
  ↓
AI: "Great choice! Balayage at [Hairdresser] is £120-£180 depending on
length and thickness. It takes about 2-3 hours.
Do you have a reference photo you'd like to share?
Also, what's your postcode? I'll check if you're in our travel area."
```

### Demo page design

```
┌─────────────────────────────────────────────────┐
│  💇 [Hairdresser Name] — AI Booking Assistant   │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ Hi! I'm the booking assistant for       │   │
│  │ [Hairdresser]. What service are you     │   │
│  │ after?                                  │   │
│  │                                         │   │
│  │ 💇 Cut & blow-dry — £45                 │   │
│  │ 💇 Balayage — from £120                 │   │
│  │ 💇 Colour — from £80                    │   │
│  │ 💇 Bridal hair — from £150              │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ What service?                     [Send]│   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  💇 Powered by AI Onboard                      │
└─────────────────────────────────────────────────┘
```

---

## BEAUTY demo

### What it is

An AI that books treatments, reminds about patch tests, and sends aftercare.

### How it works

```
User opens demo link
  ↓
Sees: "Hi! I'm the booking assistant for [Beauty]. What treatment are you after?"
  ↓
Types: "Lash lift"
  ↓
AI: "Great choice! A lash lift at [Beauty] is £65.
Important: we need a patch test 24-48 hours before your appointment.
Would you like to book the patch test first, or have you already had one?"
```

### Demo page design

```
┌─────────────────────────────────────────────────┐
│  ✨ [Beauty Name] — AI Booking Assistant        │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ Hi! I'm the booking assistant for       │   │
│  │ [Beauty]. What treatment are you after? │   │
│  │                                         │   │
│  │ ✨ Facial — £55                          │   │
│  │ ✨ Lash lift — £65                       │   │
│  │ ✨ Brow lamination — £45                 │   │
│  │ ✨ Waxing — from £25                     │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ What treatment?                  [Send] │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ✨ Powered by AI Onboard                      │
└─────────────────────────────────────────────────┘
```

---

## LASHES demo

### What it is

An AI that books lash appointments, collects allergy info, and reminds about refills.

### How it works

```
User opens demo link
  ↓
Sees: "Hi! I'm the booking assistant for [Lash Tech]. What service?"
  ↓
Types: "Classic lashes"
  ↓
AI: "Classic lashes at [Lash Tech] are £65 for the initial set,
and £40 for infills (every 2-3 weeks).
Before we book, I need to ask: do you have any known allergies
to lash adhesives or eye conditions?"
```

---

## CAR DETAILERS demo

### What it is

An AI that collects vehicle photos, drafts quotes, and documents before/after.

### How it works

```
User opens demo link
  ↓
Sees: "Hi! I'm the quote assistant for [Detailer]. What vehicle?"
  ↓
Types: "BMW 3 Series, needs a full valet"
  ↓
AI: "Great! For a BMW 3 Series full valet, I'd estimate £80-£120.
To give you an accurate quote, could you send me:
1. A photo of the exterior
2. A photo of the interior
3. Your postcode for travel
I'll have a quote back to you within the hour."
```

---

## DRIVING INSTRUCTORS demo

### What it is

An AI that books lessons, tracks pupil progress, and coordinates tests.

### How it works

```
User opens demo link
  ↓
Sees: "Hi! I'm the booking assistant for [Instructor]. Are you a new learner or taking lessons?"
  ↓
Types: "Complete beginner"
  ↓
AI: "Welcome! For a complete beginner, I'd recommend:
- 2-hour lesson — £60
- 5-lesson block — £275 (save £25)
- 10-lesson block — £500 (save £100)
What area are you in? I'll check availability."
```

---

## GARDENERS / WINDOW CLEANERS demo

### What it is

An AI that schedules rounds, notifies customers, and chases invoices.

### How it works

```
User opens demo link
  ↓
Sees: "Hi! I'm the scheduling assistant for [Gardener]. What do you need?"
  ↓
Types: "Weekly garden maintenance"
  ↓
AI: "Great! For weekly garden maintenance, I'd need to know:
1. Your postcode (for round planning)
2. Garden size (small/medium/large)
3. Any special requirements (hedge cutting, lawn treatment, etc.)
I'll check availability in your area."
```

---

## WEDDINGS demo

### What it is

An AI that qualifies leads, follows up on proposals, and refers suppliers.

### How we show it

> "Here's how your AI qualifies a wedding enquiry."

[Show: "Hi, I'm getting married in June at Manchester Town Hall. Looking for a photographer."]

[AI responds: "Congratulations! Manchester Town Hall is a beautiful venue.
June 2027? Let me check availability...
Great, I have June 14th and 21st available.
My packages start at £1,200 for 6 hours coverage.
Would you like to see my portfolio?"]

---

## How to build all demos

### Week 1: Template engine

Build a single template that works for all verticals:
- Chat interface (reuse `site/chat.html`)
- Knowledge bundle from profile
- Colour theme per vertical
- Deploy to `demos.aionboard.co.uk/[vertical]/[business-slug]`

### Week 2: Personalisation

For each business we contact:
1. Pull their data from our prospect list
2. Generate their knowledge bundle
3. Deploy their demo link
4. Include demo link in outreach message

### Week 3: Tracking

Track:
- Demo visits
- Messages sent in demo
- Conversion to trial
- Conversion to paid

---

## The demo link in outreach

### Email

> "Here's a demo of your AI assistant: https://demos.aionboard.co.uk/nails/yulia-hamilton
> Try asking it about your services."

### WhatsApp

> "Try your AI assistant: https://demos.aionboard.co.uk/nails/yulia-hamilton
> Ask it anything about your services. Takes 30 seconds."

### Cold call

> "I've set up a demo of your AI assistant. Can I send you the link? You can try it right now while we're on the phone."

---

## Success metrics

| Metric | Target | How we measure |
|--------|--------|---------------|
| Demo visits | 100/week | Analytics |
| Messages per demo | >3 | Chat logs |
| Demo → trial conversion | >20% | Signups |
| Trial → paid conversion | >50% | Payments |
| Time to first demo | <5 min after contact | Pipeline tracking |
