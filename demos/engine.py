"""Demo template engine. Generates per-vertical, per-business demos."""

import json
import os
from pathlib import Path

DEMO_DIR = Path(__file__).parent
TEMPLATES_DIR = DEMO_DIR / "templates"
GENERATED_DIR = DEMO_DIR / "generated"

# Vertical-specific configs
VERTICAL_CONFIGS = {
    "nails": {
        "emoji": "💅",
        "color": "#FF6B9D",
        "tagline": "AI Booking Assistant",
        "services": [
            {"name": "Gel Manicure", "price": 35, "duration": 45},
            {"name": "Acrylic Full Set", "price": 55, "duration": 90},
            {"name": "Gel Polish", "price": 25, "duration": 30},
            {"name": "Pedicure", "price": 40, "duration": 60},
            {"name": "Nail Art", "price": 5, "duration": 15},
            {"name": "Infill", "price": 30, "duration": 45},
            {"name": "Removal", "price": 10, "duration": 15},
        ],
        "greeting": "Hi! I'm the AI assistant for {business}. Ask me anything about our nail services.",
        "sample_questions": [
            "How much for gel nails?",
            "Do you do acrylics?",
            "What's your availability this week?",
            "Do you do nail art?",
        ],
    },
    "electrician": {
        "emoji": "⚡",
        "color": "#FFD700",
        "tagline": "AI Quote Assistant",
        "services": [
            {"name": "Extra Socket", "price": 95, "duration": 60},
            {"name": "Consumer Unit Replacement", "price": 450, "duration": 240},
            {"name": "EICR Certificate", "price": 150, "duration": 180},
            {"name": "EV Charger Install", "price": 800, "duration": 360},
            {"name": "Fault Finding", "price": 90, "duration": 60},
            {"name": "Light Fitting", "price": 75, "duration": 45},
            {"name": "Rewire", "price": 3500, "duration": 2880},
        ],
        "greeting": "📞 Missed call? No problem. I'll handle it while you're on the tools. Tell me what you need and I'll draft a quote from {business}'s price book.",
        "sample_questions": [
            "I need 3 extra sockets in my kitchen",
            "How much for an EICR certificate?",
            "Can you install an EV charger?",
            "I have a fault — lights keep tripping",
        ],
    },
    "dog_groomers": {
        "emoji": "🐕",
        "color": "#8B4513",
        "tagline": "AI Booking Assistant",
        "services": [
            {"name": "Bath & Blow-dry", "price": 35, "duration": 60},
            {"name": "Full Groom", "price": 45, "duration": 90},
            {"name": "Puppy's First Groom", "price": 30, "duration": 45},
            {"name": "De-shed Treatment", "price": 50, "duration": 75},
            {"name": "Nail Trim", "price": 10, "duration": 15},
            {"name": "Teeth Brushing", "price": 5, "duration": 10},
        ],
        "greeting": "Hi! I'm the booking assistant for {business}. What breed is your dog?",
        "sample_questions": [
            "I have a Cockapoo",
            "How much for a full groom?",
            "Do you do puppy grooms?",
            "What's your availability?",
        ],
    },
    "cleaners": {
        "emoji": "🧹",
        "color": "#4CAF50",
        "tagline": "AI Scheduling Assistant",
        "services": [
            {"name": "Weekly Clean", "price": 80, "duration": 120},
            {"name": "Fortnightly Clean", "price": 90, "duration": 120},
            {"name": "Deep Clean", "price": 150, "duration": 240},
            {"name": "End of Tenancy", "price": 200, "duration": 300},
            {"name": "Spring Clean", "price": 180, "duration": 240},
            {"name": "Window Cleaning", "price": 40, "duration": 60},
        ],
        "greeting": "Hi! I'm the scheduling assistant for {business}. I handle recurring bookings, key access, and invoicing. How can I help?",
        "sample_questions": [
            "I need a weekly clean",
            "How much for a deep clean?",
            "Can you do fortnightly?",
            "What's your availability?",
        ],
    },
    "hair": {
        "emoji": "💇",
        "color": "#9C27B0",
        "tagline": "AI Booking Assistant",
        "services": [
            {"name": "Cut & Blow-dry", "price": 45, "duration": 60},
            {"name": "Balayage", "price": 120, "duration": 180},
            {"name": "Colour", "price": 80, "duration": 120},
            {"name": "Highlights", "price": 90, "duration": 150},
            {"name": "Blow-dry", "price": 25, "duration": 30},
            {"name": "Braids", "price": 60, "duration": 90},
            {"name": "Extensions", "price": 200, "duration": 240},
        ],
        "greeting": "Hi! I'm the booking assistant for {business}. What service are you after?",
        "sample_questions": [
            "I want a balayage",
            "How much for a cut?",
            "Do you do extensions?",
            "What's your availability?",
        ],
    },
    "beauty": {
        "emoji": "✨",
        "color": "#E91E63",
        "tagline": "AI Booking Assistant",
        "services": [
            {"name": "Facial", "price": 55, "duration": 60},
            {"name": "Lash Lift", "price": 65, "duration": 75},
            {"name": "Brow Lamination", "price": 45, "duration": 45},
            {"name": "Waxing", "price": 25, "duration": 30},
            {"name": "Tinting", "price": 20, "duration": 30},
            {"name": "Dermaplaning", "price": 50, "duration": 45},
        ],
        "greeting": "Hi! I'm the booking assistant for {business}. What treatment are you after?",
        "sample_questions": [
            "I want a lash lift",
            "How much for a facial?",
            "Do you do brow lamination?",
            "What's your availability?",
        ],
    },
    "lashes": {
        "emoji": "👁️",
        "color": "#FF5722",
        "tagline": "AI Booking Assistant",
        "services": [
            {"name": "Classic Lashes", "price": 65, "duration": 90},
            {"name": "Volume Lashes", "price": 85, "duration": 120},
            {"name": "Hybrid Lashes", "price": 75, "duration": 105},
            {"name": "Infill", "price": 40, "duration": 45},
            {"name": "Lash Tint", "price": 15, "duration": 20},
            {"name": "Lash Removal", "price": 15, "duration": 20},
        ],
        "greeting": "Hi! I'm the booking assistant for {business}. What service?",
        "sample_questions": [
            "Classic lashes please",
            "How much for infills?",
            "Do you do volume lashes?",
            "What's your availability?",
        ],
    },
    "car_detailers": {
        "emoji": "🚗",
        "color": "#2196F3",
        "tagline": "AI Quote Assistant",
        "services": [
            {"name": "Basic Valet", "price": 40, "duration": 60},
            {"name": "Full Valet", "price": 80, "duration": 120},
            {"name": "Premium Detail", "price": 150, "duration": 240},
            {"name": "Ceramic Coating", "price": 300, "duration": 360},
            {"name": "Interior Deep Clean", "price": 60, "duration": 90},
            {"name": "Engine Bay Clean", "price": 40, "duration": 45},
        ],
        "greeting": "Hi! I'm the quote assistant for {business}. What vehicle do you need done?",
        "sample_questions": [
            "BMW 3 Series, full valet",
            "How much for ceramic coating?",
            "Do you do engine bay cleaning?",
            "What's your availability?",
        ],
    },
    "driving_instructors": {
        "emoji": "🚗",
        "color": "#FF9800",
        "tagline": "AI Booking Assistant",
        "services": [
            {"name": "1-Hour Lesson", "price": 35, "duration": 60},
            {"name": "2-Hour Lesson", "price": 60, "duration": 120},
            {"name": "5-Lesson Block", "price": 275, "duration": 300},
            {"name": "10-Lesson Block", "price": 500, "duration": 600},
            {"name": "Intensive Course", "price": 1500, "duration": 3600},
            {"name": "Pass Plus", "price": 200, "duration": 360},
        ],
        "greeting": "Hi! I'm the booking assistant for {business}. Are you a new learner or taking lessons?",
        "sample_questions": [
            "Complete beginner here",
            "How much for 10 lessons?",
            "Do you do intensive courses?",
            "What's your availability?",
        ],
    },
    "gardeners": {
        "emoji": "🌿",
        "color": "#4CAF50",
        "tagline": "AI Scheduling Assistant",
        "services": [
            {"name": "Lawn Mowing", "price": 25, "duration": 30},
            {"name": "Hedge Cutting", "price": 40, "duration": 60},
            {"name": "Garden Tidy", "price": 50, "duration": 90},
            {"name": "Leaf Clearance", "price": 35, "duration": 60},
            {"name": "Window Cleaning", "price": 15, "duration": 30},
            {"name": "Pressure Washing", "price": 80, "duration": 120},
        ],
        "greeting": "Hi! I'm the scheduling assistant for {business}. What do you need done?",
        "sample_questions": [
            "Weekly lawn mowing",
            "How much for window cleaning?",
            "Do you do hedge cutting?",
            "What's your availability?",
        ],
    },
    "weddings": {
        "emoji": "💒",
        "color": "#E91E63",
        "tagline": "AI Lead Assistant",
        "services": [
            {"name": "Photography (6 hours)", "price": 1200, "duration": 360},
            {"name": "Photography (10 hours)", "price": 1800, "duration": 600},
            {"name": "Videography", "price": 1500, "duration": 600},
            {"name": "Engagement Shoot", "price": 250, "duration": 60},
            {"name": "Album Design", "price": 300, "duration": 0},
            {"name": "Second Shooter", "price": 400, "duration": 360},
        ],
        "greeting": "Hi! I'm the booking assistant for {business}. Congratulations on your engagement! What's your wedding date?",
        "sample_questions": [
            "Getting married in June",
            "How much for photography?",
            "Do you do videography?",
            "What packages do you offer?",
        ],
    },
}


def generate_demo_html(vertical: str, business_name: str, business_data: dict = None) -> str:
    """Generate a demo HTML page for a business."""
    config = VERTICAL_CONFIGS.get(vertical, VERTICAL_CONFIGS["nails"])
    
    # Build knowledge base from config + business data
    knowledge = {
        "business": business_name,
        "vertical": vertical,
        "services": config["services"],
        "greeting": config["greeting"].format(business=business_name),
    }
    if business_data:
        knowledge.update(business_data)
    
    # Generate services HTML
    services_html = ""
    for s in config["services"]:
        services_html += f'<div class="service">{config["emoji"]} {s["name"]} — £{s["price"]}</div>\n'
    
    # Generate sample questions HTML
    questions_html = ""
    for q in config["sample_questions"]:
        questions_html += f'<button class="sample-q" onclick="sendSample(\'{q}\')">{q}</button>\n'
    
    # Build HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{business_name} — AI {config['tagline']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f5f5; height: 100vh; display: flex; flex-direction: column; }}
        .header {{ background: {config['color']}; color: white; padding: 16px 20px; display: flex; align-items: center; gap: 12px; }}
        .header h1 {{ font-size: 18px; font-weight: 600; }}
        .header .tagline {{ font-size: 12px; opacity: 0.9; }}
        .chat {{ flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 12px; }}
        .message {{ max-width: 80%; padding: 12px 16px; border-radius: 18px; line-height: 1.4; font-size: 14px; }}
        .bot {{ background: white; align-self: flex-start; border-bottom-left-radius: 4px; box-shadow: 0 1px 2px rgba(0,0,0,0.1); }}
        .user {{ background: {config['color']}; color: white; align-self: flex-end; border-bottom-right-radius: 4px; }}
        .services {{ background: white; padding: 16px; margin: 0 16px 12px; border-radius: 12px; box-shadow: 0 1px 2px rgba(0,0,0,0.1); }}
        .services h3 {{ font-size: 14px; margin-bottom: 8px; color: #333; }}
        .service {{ padding: 6px 0; font-size: 13px; color: #555; }}
        .sample-questions {{ display: flex; flex-wrap: wrap; gap: 8px; padding: 0 16px 12px; }}
        .sample-q {{ background: white; border: 1px solid #ddd; border-radius: 20px; padding: 8px 14px; font-size: 12px; cursor: pointer; transition: all 0.2s; }}
        .sample-q:hover {{ background: {config['color']}; color: white; border-color: {config['color']}; }}
        .input-area {{ padding: 12px 16px; background: white; border-top: 1px solid #eee; display: flex; gap: 8px; }}
        .input-area input {{ flex: 1; border: 1px solid #ddd; border-radius: 24px; padding: 12px 16px; font-size: 14px; outline: none; }}
        .input-area input:focus {{ border-color: {config['color']}; }}
        .input-area button {{ background: {config['color']}; color: white; border: none; border-radius: 50%; width: 44px; height: 44px; cursor: pointer; font-size: 18px; }}
        .footer {{ text-align: center; padding: 8px; font-size: 11px; color: #999; }}
        .typing {{ display: none; }}
        .typing span {{ display: inline-block; width: 8px; height: 8px; background: #999; border-radius: 50%; margin: 0 2px; animation: bounce 1.4s infinite; }}
        .typing span:nth-child(2) {{ animation-delay: 0.2s; }}
        .typing span:nth-child(3) {{ animation-delay: 0.4s; }}
        @keyframes bounce {{ 0%, 80%, 100% {{ transform: translateY(0); }} 40% {{ transform: translateY(-6px); }} }}
        .trial-badge {{ background: rgba(255,255,255,0.2); padding: 4px 10px; border-radius: 12px; font-size: 11px; margin-left: auto; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>{config['emoji']} {business_name}</h1>
            <div class="tagline">{config['tagline']} — powered by AI Onboard</div>
        </div>
        <div class="trial-badge">FREE 7-DAY TRIAL</div>
    </div>
    
    <div class="chat" id="chat">
        <div class="message bot">{config['greeting'].format(business=business_name)}</div>
        
        <div class="services">
            <h3>{config['emoji']} Our Services</h3>
            {services_html}
        </div>
    </div>
    
    <div class="sample-questions" id="sampleQs">
        <div style="width:100%;font-size:12px;color:#999;margin-bottom:4px;">Try asking:</div>
        {questions_html}
    </div>
    
    <div class="input-area">
        <input type="text" id="userInput" placeholder="Type a message..." onkeypress="if(event.key==='Enter')sendMessage()">
        <button onclick="sendMessage()">→</button>
    </div>
    
    <div class="footer">Free 7-day trial • No credit card required • Cancel anytime</div>

    <script>
    const knowledge = {json.dumps(knowledge)};
    
    function sendSample(q) {{
        document.getElementById('userInput').value = q;
        sendMessage();
    }}
    
    function sendMessage() {{
        const input = document.getElementById('userInput');
        const msg = input.value.trim();
        if (!msg) return;
        
        addMessage(msg, 'user');
        input.value = '';
        
        document.getElementById('sampleQs').style.display = 'none';
        
        setTimeout(() => {{
            const response = generateResponse(msg);
            addMessage(response, 'bot');
        }}, 800);
    }}
    
    function addMessage(text, type) {{
        const chat = document.getElementById('chat');
        const div = document.createElement('div');
        div.className = 'message ' + type;
        div.textContent = text;
        chat.appendChild(div);
        chat.scrollTop = chat.scrollHeight;
    }}
    
    function generateResponse(msg) {{
        const lower = msg.toLowerCase();
        const services = knowledge.services;
        
        // Check for price queries
        for (const s of services) {{
            if (lower.includes(s.name.toLowerCase()) || lower.includes(s.name.split(' ')[0].toLowerCase())) {{
                return `${{s.name}} at ${{knowledge.business}} costs £${{s.price}}. It takes about ${{s.duration}} minutes. Would you like to book?`;
            }}
        }}
        
        // Check for availability queries
        if (lower.includes('availab') || lower.includes('book') || lower.includes('appointment')) {{
            return `I have availability this week! Let me check the diary... I have slots on Thursday at 2pm and Friday at 10am. Which works better?`;
        }}
        
        // Check for general pricing
        if (lower.includes('price') || lower.includes('cost') || lower.includes('how much')) {{
            let priceList = services.map(s => `${{s.name}} — £${{s.price}}`).join('\\n');
            return `Our services and prices:\\n\\n${{priceList}}\\n\\nWhich service are you interested in?`;
        }}
        
        // Check for location/postcode
        if (lower.includes('postcode') || lower.includes('location') || lower.includes('area')) {{
            return `We serve the local area. What's your postcode? I'll check if you're within our range.`;
        }}
        
        // Check for reviews
        if (lower.includes('review') || lower.includes('rating')) {{
            return `${{knowledge.business}} has excellent reviews! Check us out on Google to see what our customers say.`;
        }}
        
        // Check for contact
        if (lower.includes('contact') || lower.includes('phone') || lower.includes('email')) {{
            return `You can reach us via this chat, or check our website for contact details. I'm here to help right now!`;
        }}
        
        // Default response
        return `Thanks for your message! I can help with booking, pricing, and availability. What would you like to know about our services?`;
    }}
    </script>
</body>
</html>"""
    
    return html


def generate_demo(vertical: str, business_name: str, business_data: dict = None) -> str:
    """Generate and save a demo page. Returns the file path."""
    slug = business_name.lower().replace(" ", "-").replace("'", "")
    slug = "".join(c for c in slug if c.isalnum() or c == "-")
    
    output_dir = GENERATED_DIR / vertical
    output_dir.mkdir(parents=True, exist_ok=True)
    
    html = generate_demo_html(vertical, business_name, business_data)
    
    output_path = output_dir / f"{slug}.html"
    output_path.write_text(html)
    
    return str(output_path)


def generate_all_demos():
    """Generate demos for all businesses in our prospect list."""
    import csv
    
    prospects_file = DEMO_DIR.parent / "data" / "prospects" / "serpapi_all_verticals.csv"
    if not prospects_file.exists():
        print("No prospects file found")
        return
    
    generated = 0
    with open(prospects_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            vertical = row.get("vertical", "")
            business = row.get("businessName", "")
            if vertical in VERTICAL_CONFIGS and business:
                path = generate_demo(vertical, business, {
                    "phone": row.get("phone", ""),
                    "address": row.get("address", ""),
                    "rating": row.get("rating", ""),
                    "reviews": row.get("reviewCount", ""),
                    "website": row.get("website", ""),
                })
                generated += 1
    
    print(f"Generated {generated} demos")


if __name__ == "__main__":
    generate_all_demos()
