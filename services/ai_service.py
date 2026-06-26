import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# ─── Keyword-based Fallback ───────────────────────────────────────────────────

KEYWORD_MAP = {
    "ai": "AI Automation",
    "artificial intelligence": "AI Automation",
    "chatbot": "AI Automation",
    "machine learning": "AI Automation",
    "ml": "AI Automation",
    "automation": "AI Automation",
    "bot": "AI Automation",
    "web": "Web Development",
    "website": "Web Development",
    "landing page": "Web Development",
    "frontend": "Web Development",
    "backend": "Web Development",
    "app": "App Development",
    "mobile": "App Development",
    "android": "App Development",
    "ios": "App Development",
    "flutter": "App Development",
    "data": "Data Analytics",
    "analytics": "Data Analytics",
    "dashboard": "Data Analytics",
    "report": "Data Analytics",
    "visualization": "Data Analytics",
    "crm": "CRM / Sales",
    "sales": "CRM / Sales",
    "lead": "CRM / Sales",
    "marketing": "Digital Marketing",
    "seo": "Digital Marketing",
    "social media": "Digital Marketing",
    "ads": "Digital Marketing",
    "cloud": "Cloud & DevOps",
    "devops": "Cloud & DevOps",
    "aws": "Cloud & DevOps",
    "azure": "Cloud & DevOps",
    "gcp": "Cloud & DevOps",
    "docker": "Cloud & DevOps",
    "ecommerce": "E-Commerce",
    "shop": "E-Commerce",
    "store": "E-Commerce",
    "payment": "E-Commerce",
}

URGENCY_HIGH = ["urgent", "asap", "immediately", "critical", "emergency", "priority", "today"]
URGENCY_LOW = ["explore", "maybe", "just looking", "info", "information", "curious", "later"]


def _keyword_classify(requirement: str):
    req_lower = requirement.lower()

    # Determine category
    category = "General Inquiry"
    for keyword, cat in KEYWORD_MAP.items():
        if keyword in req_lower:
            category = cat
            break

    # Determine priority
    if any(w in req_lower for w in URGENCY_HIGH):
        priority = "High"
    elif any(w in req_lower for w in URGENCY_LOW):
        priority = "Low"
    else:
        priority = "Medium"

    return category, priority


def classify_lead(requirement: str):
    """
    Classify a lead's requirement into category + priority.
    Uses Gemini API if key is provided, otherwise falls back to keyword matching.
    Returns (category: str, priority: str)
    """
    if GEMINI_API_KEY:
        try:
            import google.generativeai as genai

            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")

            prompt = f"""You are a lead classification assistant. Classify the following business requirement.

Requirement: "{requirement}"

Available categories (choose exactly one):
- AI Automation
- Web Development
- App Development
- Data Analytics
- CRM / Sales
- Digital Marketing
- Cloud & DevOps
- E-Commerce
- General Inquiry

Priority levels (choose exactly one):
- High (urgent, critical, ASAP)
- Medium (normal business need)
- Low (exploratory, just looking)

Respond ONLY in this exact format (two lines):
Category: <category>
Priority: <priority>"""

            response = model.generate_content(prompt)
            lines = [ln.strip() for ln in response.text.strip().split("\n") if ln.strip()]
            category = lines[0].replace("Category:", "").strip()
            priority = lines[1].replace("Priority:", "").strip()

            # Validate
            valid_cats = [
                "AI Automation", "Web Development", "App Development",
                "Data Analytics", "CRM / Sales", "Digital Marketing",
                "Cloud & DevOps", "E-Commerce", "General Inquiry",
            ]
            valid_pris = ["High", "Medium", "Low"]
            if category not in valid_cats:
                category = "General Inquiry"
            if priority not in valid_pris:
                priority = "Medium"

            return category, priority

        except Exception:
            pass  # Fall back to keywords on any error

    return _keyword_classify(requirement)
