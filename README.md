# AI Onboard pilot implementation

Pilot-only repository. There are no completed paying customer installations recorded here.

## Run checks

```bash
python3 -m unittest discover -s tests -v
```

Expected: 19 tests pass.

## Narrow pilot scope

See `OFFER.md`. The standard £499 setup covers:

- Existing customer-authorized email and calendar workflows
- Enquiry capture
- Quote drafts from an approved price book
- Owner approval before outbound sends
- Google Business Profile assistance
- Training and written handover
- Fourteen days of fixes

Website builds, live voice service, Meta production integration, custom integrations, and lead generation are separate future offerings.

## Local pilot commands

```bash
# Generate the static pilot site
python3 -c "from aionboard.website import write_site; print(write_site())"

# Run the fictional electrician demo
python3 -c "from aionboard.demo import demo_summary; print(demo_summary())"
```

Runtime CRM databases and generated customer handovers stay local and are ignored by git. Research records are not marketing permission.
