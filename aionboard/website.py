"""Minimal pilot website content."""

from __future__ import annotations

import os

SITE_DOMAIN = "aionboard.co.uk"
BOOKING_EMAIL = "hello@aionboard.co.uk"
STANDARD_PRICE_GBP = 20
QUICKSTART_PRICE_GBP = 20


def canonical_domain() -> str:
    return f"https://{SITE_DOMAIN}"


def render_site() -> str:
    return f"""<!doctype html>
<html lang=\"en-GB\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>AI Onboard — Pilot AI Setup for UK Trades</title>
  <meta name=\"description\" content=\"Pilot AI setup for existing UK trades workflows, with training and written handover.\" />
</head>
<body>
  <main>
    <h1>AI Onboard pilot</h1>
    <p><strong>Status:</strong> pilot. No completed customer installation is claimed on this page.</p>

    <h2>Standard setup — £{STANDARD_PRICE_GBP} one-off</h2>
    <ul>
      <li>Setup for existing customer-authorized email and calendar workflows</li>
      <li>Enquiry capture using customer-approved contact details</li>
      <li>Quote drafting from a customer-approved price book</li>
      <li>Owner approval before outbound quotes, bookings, payments, or messages</li>
      <li>Google Business Profile assistance through Google’s ordinary interface</li>
      <li>Live training session</li>
      <li>Written handover</li>
      <li>Fourteen days of fixes for configured workflows</li>
    </ul>

    <h2>Muse Quickstart — £{QUICKSTART_PRICE_GBP} one-off</h2>
    <p>For sole traders. One priority workflow, guided connection to apps you already use, personalised assistant setup, training, personalised manual, and seven days of setup support. Third-party software charges are shown before installation.</p>

    <h2>Not included in either package</h2>
    <ul>
      <li>New or rebuilt website</li>
      <li>Live voice service</li>
      <li>WhatsApp, Facebook, Instagram, or Meta production integration</li>
      <li>Custom integrations</li>
      <li>Lead generation</li>
      <li>Guaranteed search, Maps, ChatGPT, or AI-assistant placement</li>
    </ul>

    <h2>Customer-owned costs</h2>
    <p>Domains, hosting, telephony, messaging, AI-model usage, software subscriptions, verification costs, and payment-processing fees remain the customer’s responsibility unless separately quoted in writing.</p>

    <h2>Try the demo assistant</h2>
    <p><a href="chat.html">Ask what the £20 setup covers</a> — answers come only from our published research, with sources shown. It cannot access accounts or send messages.</p>

    <h2>Book a pilot discussion</h2>
    <p>Email <a href=\"mailto:{BOOKING_EMAIL}?subject=Pilot%20installation%20request\">{BOOKING_EMAIL}</a> with your business name, postcode, current software, and the workflow you want help with.</p>

    <h2>Privacy and contact rules</h2>
    <p>We verify contact sources, record permission or legal basis, screen live marketing calls against TPS, CTPS, and our suppression list, and respect objections. Research records are not marketing permission.</p>
  </main>
</body>
</html>
"""


def write_site(path: str = "site/index.html") -> str:
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(render_site())
    return path


def build_knowledge_bundle(path: str = "site/knowledge.json") -> str:
    """Export graph nodes as a static bundle for the demo chatbot."""
    import json

    from .graph import build_graph

    graph = build_graph()
    bundle = [
        {"id": node_id, **node}
        for node_id, node in sorted(graph["nodes"].items())
    ]
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(bundle, handle, indent=1)
    return path


def render_chat_page() -> str:
    return """<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AI Onboard — Ask about the £20 setup</title>
  <meta name="description" content="Demo assistant answering from AI Onboard's published research. No live AI, no account access." />
</head>
<body>
  <main>
    <h1>Ask about the £20 setup</h1>
    <p><strong>Demo assistant.</strong> Answers come only from our published
    research files, with sources shown. It cannot access your accounts,
    book anything, or send messages.</p>
    <div id="chat-log" aria-live="polite"></div>
    <form id="chat-form">
      <label for="chat-input">Your question</label>
      <input id="chat-input" type="text" autocomplete="off"
        placeholder="e.g. nail no-shows, MTD thresholds, what's included for £20?" />
      <button type="submit">Ask</button>
    </form>
    <p>Try: <em>what does £20 get me</em> · <em>nail no-shows</em> ·
    <em>MTD thresholds</em> · <em>do you move money</em></p>
    <p><a href="index.html">Back to AI Onboard pilot</a></p>
  </main>
<script>
const STOPWORDS = new Set(["what","how","does","do","is","are","the","a","an","to","for","my","i","it","of","in","on","me","you","your"]);
let NODES = [];
fetch("knowledge.json").then(r => r.json()).then(data => { NODES = data; });
function tokens(s) {
  return (s.toLowerCase().match(/[a-z0-9]+/g) || []).filter(t => !STOPWORDS.has(t));
}
function answer(question) {
  const query = new Set(tokens(question));
  if (query.size === 0) {
    return "Ask about a specific trade, pain point, tool, or regulation — for example 'nail no-shows' or 'MTD thresholds'.";
  }
  const scored = [];
  for (const node of NODES) {
    const nodeTokens = new Set(tokens(node.id + " " + node.text));
    let overlap = 0;
    for (const t of query) { if (nodeTokens.has(t)) overlap++; }
    if (overlap > 0) scored.push([overlap, node]);
  }
  scored.sort((a, b) => b[0] - a[0]);
  if (scored.length === 0) {
    return "I don't have verified information on that yet. Try a trade, pain, tool, or regulation — for example 'electrician quotes' or 'VAT threshold'.";
  }
  const lines = ["Here's what our research covers:"];
  for (const [, node] of scored.slice(0, 5)) {
    lines.push("- [" + node.kind + "] " + node.text + " (source: " + node.source + ")");
  }
  return lines.join("\\n");
}
document.getElementById("chat-form").addEventListener("submit", function (e) {
  e.preventDefault();
  const input = document.getElementById("chat-input");
  const log = document.getElementById("chat-log");
  const q = document.createElement("p");
  q.textContent = "You: " + input.value;
  log.appendChild(q);
  const a = document.createElement("p");
  a.style.whiteSpace = "pre-wrap";
  a.textContent = "Assistant: " + answer(input.value);
  log.appendChild(a);
  input.value = "";
});
</script>
</body>
</html>
"""


def write_chat_page(path: str = "site/chat.html") -> str:
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(render_chat_page())
    return path


def render_dashboard() -> str:
    return """<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AI Onboard — Customer dashboard (demo layout)</title>
  <meta name="description" content="Demo layout of the customer dashboard. All data shown is fictional." />
</head>
<body>
  <main>
    <h1>Your dashboard</h1>
    <p><strong>Demo layout.</strong> Every value below is fictional placeholder
    data showing what a live dashboard will display once connected.</p>

    <h2>Installation status — DEMO DATA</h2>
    <ul>
      <li>Discovery: verified</li>
      <li>Booking workflow: verified</li>
      <li>Google Business Profile: pending (awaiting Google)</li>
      <li>Training: not started</li>
      <li>Handover: not started</li>
    </ul>

    <h2>Support window — DEMO DATA</h2>
    <p>6 days remaining. 2 questions asked, both resolved by the guide, 0 human minutes used.</p>

    <h2>Opportunities near you — DEMO DATA</h2>
    <ul>
      <li>Planning approval: single-storey extension, M14 [relevance 2] — signal, not a confirmed job</li>
      <li>Procurement: facilities maintenance tender, M15 [relevance 1] — signal, not a confirmed job</li>
    </ul>
    <p>Reply APPROVE before we contact anyone on your behalf.</p>

    <h2>Your buddy</h2>
    <p><a href="chat.html">Ask the demo assistant</a> — answers from published research with sources shown.</p>

    <h2>Add-ons (separately priced, separately consented)</h2>
    <ul>
      <li>Lead alerts — weekly scored signals</li>
      <li>Ad creation — TikTok slideshows via our content pipeline</li>
      <li>Analytics — views → chats → emails → installs per creative</li>
    </ul>
    <p><a href="index.html">Back to AI Onboard pilot</a></p>
  </main>
</body>
</html>
"""


def write_dashboard(path: str = "site/dashboard.html") -> str:
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(render_dashboard())
    return path
