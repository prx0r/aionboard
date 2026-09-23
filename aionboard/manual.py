"""Customer-facing teaching manual generator.

Built from verified installation state: an easy guide, ready prompts,
weekly checklist, privacy and approval explanations, troubleshooting,
and access-removal instructions. No secrets, no customer PII beyond
what the customer approved for the manual.
"""

from __future__ import annotations

from .security import scan_text

GENERIC_PROMPTS = [
    "Here are my services, prices and working hours. Help me organise them into a clear service menu.",
    "Draft a friendly reply to a customer asking about availability. Include my booking link and don't promise a slot you haven't checked.",
    "Help me plan three social posts this week using photos of my own work.",
    "Organise my business expenses from this export. Flag anything unclear and don't submit tax returns or move money.",
    "Walk me through my weekly business checklist. Tell me which tasks you can do with my connected apps and which need my approval.",
]


def vertical_prompts(
    vertical: str, workflows: list[str], capabilities: list[str] | None = None
) -> list[str]:
    """Five to ten useful prompts: generic base plus workflow-specific extras.

    Prompts are filtered against confirmed capabilities: a prompt that needs
    a capability the customer doesn't have is excluded rather than implied.
    """
    prompts = list(GENERIC_PROMPTS)
    extras: dict[str, list[tuple[str, str]]] = {
        "nails": [
            (
                "Draft a deposit reminder for a nail appointment tomorrow, using my cancellation policy.",
                "booking",
            ),
            (
                "Help me write an Instagram caption for this set, with my booking link and location.",
                "social",
            ),
        ],
        "lashes": [
            (
                "Check this client's patch-test record before I confirm their lash appointment.",
                "booking",
            ),
            (
                "Draft a refill reminder for clients due in the next two weeks.",
                "booking",
            ),
        ],
        "hair": [
            (
                "Draft a reply asking a new client for their service area postcode and inspiration photo.",
                "booking",
            ),
            (
                "Help me write a rebooking message for colour clients due for a refresh.",
                "booking",
            ),
        ],
        "electrician": [
            (
                "Draft a quote from my approved price book for this job description. Do not send it.",
                "quoting",
            ),
            (
                "Summarise today's new enquiries with job type and urgency.",
                "enquiries",
            ),
        ],
        "cleaners": [
            (
                "List paused plans and draft a win-back message for each.",
                "booking",
            ),
            (
                "Prepare this week's recurring schedule from my client list.",
                "scheduling",
            ),
        ],
        "beauty": [
            (
                "Draft a rebooking message for clients due for their next treatment.",
                "booking",
            ),
            (
                "Help me write a service description with prices for my booking page.",
                "social",
            ),
        ],
        "dog-groomers": [
            (
                "List dogs due for grooming in the next two weeks and draft reminders.",
                "booking",
            ),
            (
                "Prepare a waiting-list message for the next cancelled slot.",
                "scheduling",
            ),
        ],
        "gardeners-window-cleaners": [
            (
                "List this week's round visits with any skips or credits noted.",
                "scheduling",
            ),
            (
                "Draft a payment reminder for overdue round customers.",
                "booking",
            ),
        ],
        "car-detailers": [
            (
                "Prepare a quote request checklist for this vehicle: size, condition photos, location.",
                "quoting",
            ),
            (
                "Draft a follow-up for quotes older than 48 hours. Do not send it.",
                "enquiries",
            ),
        ],
        "driving-instructors": [
            (
                "Show my lesson schedule this week and any waiting-list gaps.",
                "scheduling",
            ),
            (
                "Draft a reminder for pupils with lessons tomorrow.",
                "booking",
            ),
        ],
        "weddings": [
            (
                "Prepare an enquiry qualification checklist: date, venue, party size, package.",
                "enquiries",
            ),
            (
                "Draft a proposal from my approved packages. Do not send it.",
                "quoting",
            ),
        ],
    }
    for prompt, capability in extras.get(vertical, []):
        if capabilities is None or capability in capabilities:
            prompts.append(prompt)
    return prompts[:10]


def generate_manual(
    *,
    business_name: str,
    vertical: str,
    workflows: list[str],
    accounts: list[dict],
    support_days: int,
    capabilities: list[str] | None = None,
    uploadable: bool = False,
) -> str:
    """Generate the teaching pack. Rejected if secrets are detected.

    When uploadable is true, account details are replaced with a generic
    non-sensitive version safe to paste into an assistant.
    """
    name = business_name.strip()
    if not name:
        raise ValueError("business_name is required")
    prompts = vertical_prompts(vertical, workflows, capabilities)
    prompt_block = "\n\n".join(
        f"Prompt {i + 1}\n\n{prompt}\n\nCopy" for i, prompt in enumerate(prompts)
    )
    if uploadable:
        account_lines = (
            "- Your accounts stay in your control. This uploadable copy "
            "contains no account names, identifiers, or customer records."
        )
    else:
        account_lines = "\n".join(
            f"- {a.get('name', '?')}: owner={a.get('owner', '?')}, status={a.get('status', '?')}"
            for a in accounts
        )
    workflow_lines = "\n".join(f"- {w}" for w in workflows) or "- (none configured yet)"

    markdown = f"""# Your AI setup manual — {name}

This guide covers what was configured, how to use it, and how to remove our access.

## What was set up

{workflow_lines}

## Your accounts

{account_lines}

All accounts remain yours. We hold no passwords. Access was granted by you and can be revoked by you at any time.

## Your first prompts

{prompt_block}

Illustrative prompts. What the assistant can actually do depends on your connected apps and permissions.

## Weekly checklist

1. Review new enquiries and confirm nothing is waiting on you.
2. Check upcoming bookings, deposits, and reminders.
3. Follow up quotes or proposals older than 48 hours.
4. Ask for a review after completed work.
5. Review this week's expenses against your accounting software.

## Privacy and approvals

- The assistant drafts; you approve. Nothing sends, books, or pays without your tap.
- Chat logs are personal data. Tell customers how you handle them.
- Marketing messages need separate consent per channel.
- Your financial and customer records are not shared with anyone unless you separately agree.

## Troubleshooting

- Booking link not working: check the link in your bio matches your booking platform exactly.
- Reminders not sending: check the reminder settings in your booking platform, not the assistant.
- Quote looks wrong: do not send it. Fix the price book first, then re-draft.
- Something broken from this installation: contact us within your support window and quote your handover reference.

## Support window

{support_days} days of setup support from installation. Automated guide answers first; a human intervenes when the agreed installation doesn't work. Unrestricted bespoke development is not included.

## Removing our access

1. Remove our OAuth grants in each connected app's settings.
2. Change any shared passwords we used during setup.
3. Delete any API tokens created for the installation.
4. Ask us to confirm deletion of our copies of your configuration.
"""
    findings = scan_text(markdown)
    if findings:
        raise ValueError("manual must not contain secrets")
    return markdown
