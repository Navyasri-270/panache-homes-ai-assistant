import os
import json
import re
import google.generativeai as genai
from database import get_config

# Load Knowledge Base
KB_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge_base.json")
try:
    with open(KB_FILE, "r") as f:
        knowledge_base = json.load(f)
except Exception:
    knowledge_base = {}

def get_gemini_client():
    api_key = get_config("gemini_api_key")
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-1.5-flash")
    return None

def build_system_prompt(current_lead):
    kb_str = json.dumps(knowledge_base, indent=2)
    # Determine what is missing
    missing_fields = []
    if not current_lead.get("first_name"): missing_fields.append("Name (First & Last)")
    if not current_lead.get("country"): missing_fields.append("Country of Residence")
    if not current_lead.get("budget"): missing_fields.append("Budget in AED")
    if not current_lead.get("payment_method"): missing_fields.append("Payment Method (Cash or Mortgage)")
    if not current_lead.get("timeline"): missing_fields.append("Purchase Timeline")
    if not current_lead.get("purpose"): missing_fields.append("Purpose (Investment or Personal)")
    
    missing_str = ", ".join(missing_fields) if missing_fields else "None (Fully qualified)"

    return f"""
You are a friendly, warm, polite, and professional real estate sales assistant representing 'Panache Homes' in Dubai.
Your role is to assist international buyers and qualify them naturally without making it feel like filling out a form.

CRITICAL INSTRUCTION:
You must answer questions ONLY using the provided knowledge base below. Under no circumstances should you use external internet knowledge or guess facts. Never answer outside the provided knowledge base. If the information is not explicitly stated in the knowledge base, you must trigger the fallback message.

KNOWLEDGE BASE:
{kb_str}

CONVERSATIONAL RULES:
1. Be extremely friendly, professional, warm, and polite. Tone should feel like high-end luxury concierge service.
2. Answer questions about Dubai property ownership, Golden Visas, ROI, taxes, and process ONLY using the provided knowledge base.
3. NEVER use internet knowledge, never invent facts, and never guess.
4. If the user asks about information, properties, or details that are NOT explicitly included in the knowledge base, you MUST respond exactly with:
   "I'm sorry. I can only answer questions that are included in the Panache Homes Knowledge Base. Please contact a Panache representative for additional information."
5. You must collect the following details ONE AT A TIME. DO NOT ask multiple qualification questions in a single response:
   - Name (First and Last)
   - Country of residence
   - Budget in AED
   - Payment Method (Cash or Mortgage)
   - Purchase Timeline
   - Purpose (Investment or Personal)
6. Do NOT repeat questions that have already been answered.
7. Currently, the missing fields are: {missing_str}. Focus on requesting the next missing detail organically.
8. Once all fields are collected, warmly thank them and let them know a senior advisor will reach out to them on WhatsApp/Email.
"""

def generate_chatbot_response(chat_history, current_lead):
    """
    Generate chatbot response using Gemini if configured, or elegant rule-based fallback.
    chat_history is a list of dicts: [{'role': 'user'|'assistant', 'content': str}]
    """
    client = get_gemini_client()
    if client:
        try:
            system_instruction = build_system_prompt(current_lead)
            # Convert history to format expected by SDK
            contents = []
            for msg in chat_history:
                contents.append({
                    "role": "user" if msg["role"] == "user" else "model",
                    "parts": [msg["content"]]
                })
            
            # Use system instruction directly in generation config
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=system_instruction
            )
            response = model.generate_content(contents)
            return response.text
        except Exception as e:
            return f"Excuse me, I'm experiencing a connection issue. Let me provide assistance. (Error: {str(e)})"
    
    # Elegant fallback simulated agent
    return get_simulated_response(chat_history, current_lead)

def normalize_budget(budget_str):
    if not budget_str:
        return ""
    # Clean up whitespace and symbols
    clean = str(budget_str).lower().replace(",", "").replace("aed", "").replace("dirham", "").replace("$", "").replace("usd", "").strip()
    
    # Check for million/m
    multiplier = 1
    if "million" in clean or "m" in clean:
        multiplier = 1000000
        clean = clean.replace("million", "").replace("m", "").strip()
    elif "thousand" in clean or "k" in clean:
        multiplier = 1000
        clean = clean.replace("thousand", "").replace("k", "").strip()
        
    # Extract first float/int match
    match = re.search(r"[-+]?\d*\.\d+|\d+", clean)
    if match:
        val = float(match.group(0)) * multiplier
        return str(int(val))
    return str(budget_str)

def normalize_timeline(timeline_str):
    if not timeline_str:
        return ""
    clean = str(timeline_str).lower().strip()
    if any(keyword in clean for keyword in ["immediate", "now", "asap", "this month", "ready"]):
        return "Immediate"
    elif "2" in clean or "two" in clean:
        return "2 Months"
    elif "3" in clean or "three" in clean:
        return "3 Months"
    elif "6" in clean or "six" in clean:
        return "6 Months"
    elif "1" in clean or "one" in clean or "year" in clean:
        return "1 Year"
    return timeline_str.title()

def normalize_purpose(purpose_str):
    if not purpose_str:
        return ""
    clean = str(purpose_str).lower().strip()
    has_investment = "invest" in clean
    has_personal = any(k in clean for k in ["personal", "live", "home", "reside"])
    
    if has_investment and has_personal:
        return "Investment & Personal Use"
    elif has_investment:
        return "Investment"
    elif has_personal:
        return "Personal Use"
    return purpose_str.title()

def get_simulated_response(chat_history, current_lead):
    """
    Simulated agent that asks precisely one question at a time for missing fields,
    with robust skip handling, validation, and graceful recovery.
    """
    if not chat_history:
        return "Welcome to Panache Homes."
        
    last_user_message = chat_history[-1]["content"].lower().strip() if chat_history else ""
    
    # Identify skip keywords
    skip_keywords = ["skip", "next", "pass", "not sure", "don't want to say", "no comment", "secret", "private", "later"]
    is_skip = any(k in last_user_message for k in skip_keywords)

    # Find the last question asked by the assistant to map the user's reply correctly
    last_assistant_question = ""
    for msg in reversed(chat_history[:-1]):
        if msg["role"] == "assistant":
            last_assistant_question = msg["content"].lower()
            break

    # Parse based on context of the last question asked
    if "full name" in last_assistant_question:
        if is_skip:
            current_lead["first_name"] = "Valued"
            current_lead["last_name"] = "Client"
        else:
            words = chat_history[-1]["content"].split()
            if len(words) >= 2:
                current_lead["first_name"] = words[0]
                current_lead["last_name"] = " ".join(words[1:])
            else:
                current_lead["first_name"] = chat_history[-1]["content"]
                current_lead["last_name"] = "Client"

    elif "which country" in last_assistant_question:
        if is_skip:
            current_lead["country"] = "Unspecified"
        else:
            current_lead["country"] = chat_history[-1]["content"]

    elif "approximate investment budget" in last_assistant_question:
        if is_skip:
            current_lead["budget"] = "Unconfirmed"
        else:
            norm_budget = normalize_budget(chat_history[-1]["content"])
            # If the normalized budget has no digits, it is invalid
            if not any(c.isdigit() for c in norm_budget):
                return "To recommend the best investment opportunities, could you share your approximate investment budget in AED? (Please specify a numerical amount, e.g. 1.5M or 2,000,000 AED)"
            current_lead["budget"] = norm_budget

    elif "cash or" in last_assistant_question:
        if is_skip:
            current_lead["payment_method"] = "Flexible"
        else:
            if "cash" in last_user_message:
                current_lead["payment_method"] = "Cash"
            elif "mortgage" in last_user_message:
                current_lead["payment_method"] = "Mortgage"
            else:
                current_lead["payment_method"] = "Flexible"

    elif "planning to purchase" in last_assistant_question:
        if is_skip:
            current_lead["timeline"] = "Flexible"
        else:
            current_lead["timeline"] = normalize_timeline(chat_history[-1]["content"])

    elif "investment or personal use" in last_assistant_question:
        if is_skip:
            current_lead["purpose"] = "Investment & Personal Use"
        else:
            current_lead["purpose"] = normalize_purpose(chat_history[-1]["content"])

    # Parse answers in user's last message to dynamically catch keywords in case they voluntarily typed it
    if "from" in last_user_message or "live in" in last_user_message:
        if not current_lead.get("country"):
            current_lead["country"] = chat_history[-1]["content"]
            
    if "cash" in last_user_message and not current_lead.get("payment_method"):
        current_lead["payment_method"] = "Cash"
    elif "mortgage" in last_user_message and not current_lead.get("payment_method"):
        current_lead["payment_method"] = "Mortgage"

    # Match property Q&As from knowledge base
    if "golden visa" in last_user_message:
        return "An investment of AED 2 Million in Dubai property qualifies you for the UAE 10-Year Golden Visa. To recommend the best investment opportunities, could you share your approximate investment budget in AED?"
    if any(k in last_user_message for k in ["tax", "fee", "oqood", "dld"]):
        return "Dubai properties carry a 4% Dubai Land Department Registration Fee and a AED 3000 Oqood Fee for off-plan purchases. There is 0% annual property tax and 0% capital gains tax. Which country are you residing in currently?"
    if any(k in last_user_message for k in ["yield", "roi", "return"]):
        return "Rental yields in Dubai are usually between 6%–8%. Please note we never guarantee returns. To suggest suitable properties, could you share your approximate investment budget in AED?"
    if any(k in last_user_message for k in ["currency", "dirham", "rate", "usd"]):
        return "The UAE Dirham is pegged to the USD at a fixed exchange rate of 3.6725, meaning USD investors carry no currency risk."
    if any(k in last_user_message for k in ["remote", "signing", "wire", "attorney"]):
        return "Customers can complete the purchase remotely through Digital Signing, International Wire Transfer, and Power of Attorney."
    if any(k in last_user_message for k in ["payment", "plan", "booking", "instalment"]):
        return "Payment plans usually consist of a 10%–20% booking amount, construction instalments, and a final payment on handover."

    # Catch general questions not matching the knowledge base
    if "?" in last_user_message or any(keyword in last_user_message for keyword in ["how", "why", "where", "what", "who", "when"]):
        kb_terms = ["golden visa", "tax", "fee", "oqood", "dld", "dirham", "usd", "exchange", "rate", "currency", "payment", "booking", "instalment", "handover", "yield", "roi", "return", "remote", "digital", "wire", "attorney", "panache"]
        if not any(term in last_user_message for term in kb_terms):
            return "I'm sorry. I can only answer questions that are included in the Panache Homes Knowledge Base. Please contact a Panache representative for additional information."

    # Find the first missing field and ask for it
    if not current_lead.get("first_name"):
        return "To begin curating the best options for you, could you please share your full name?"
    
    if not current_lead.get("country"):
        return f"Pleasure to meet you, {current_lead.get('first_name')}. Which country are you based in? This helps us guide you on international ownership regulations."
        
    if not current_lead.get("budget"):
        return "To recommend the best investment opportunities, could you share your approximate investment budget in AED?"

    if not current_lead.get("payment_method"):
        return "Understood. Will this purchase be made via Cash or do you plan to explore a Mortgage in Dubai?"

    if not current_lead.get("timeline"):
        return "When are you planning to purchase your property?"

    if not current_lead.get("purpose"):
        return "Will this property be for investment or personal use?"

    return "Thank you for sharing your requirements! I have recorded your preferences. A senior private client advisor from Panache Homes will contact you shortly via WhatsApp and email with our off-market portfolio."


def extract_lead_profile(chat_history):
    """
    Extracts structured fields from the conversation.
    Returns a dict with extracted lead parameters.
    """
    client = get_gemini_client()
    full_transcript = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in chat_history])
    
    if client:
        try:
            prompt = f"""
Analyze the following conversation transcript between a real estate assistant and an international buyer.
Extract the qualification details and return them strictly in JSON format with these exact keys:
- first_name
- last_name
- email
- phone
- country
- budget
- property_interest (e.g. Villa, Penthouse, Apartment)
- payment_method (e.g. Cash, Mortgage)
- timeline (e.g. Immediate, 3 Months, Flexible)
- purpose (e.g. Investment, Personal)
- notes (summary of their specific requirements)

If a field is not found in the transcript, set it to null or an empty string.

TRANSCRIPT:
{full_transcript}
"""
            response = client.generate_content(prompt)
            # Find JSON block
            json_match = re.search(r"\{.*\}", response.text, re.DOTALL)
            if json_match:
                res_data = json.loads(json_match.group(0))
                if res_data.get("budget"):
                    res_data["budget"] = normalize_budget(res_data["budget"])
                if res_data.get("timeline"):
                    res_data["timeline"] = normalize_timeline(res_data["timeline"])
                if res_data.get("purpose"):
                    res_data["purpose"] = normalize_purpose(res_data["purpose"])
                return res_data
        except Exception:
            pass

    # Simple heuristic fallback parser if LLM fails or is not configured
    profile = {
        "first_name": "",
        "last_name": "",
        "email": "",
        "phone": "",
        "country": "",
        "budget": "",
        "property_interest": "",
        "payment_method": "",
        "timeline": "",
        "purpose": "",
        "notes": ""
    }
    
    all_text = " ".join([m["content"] for m in chat_history])
    
    # Extract Email
    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", all_text)

    if email_match:
        profile["email"] = email_match.group(0)
        
    # Extract Phone (crude heuristic)
    phone_match = re.search(r"(\+\d{1,3}[- ]?)?\d{9,12}", all_text)
    if phone_match:
        profile["phone"] = phone_match.group(0)

    # Country heuristics
    country_match = re.search(r"(?:from|in|live in|reside in) ([a-zA-Z\s]{3,20})", all_text, re.IGNORECASE)
    if country_match:
        # Check that it's not a common keyword like "dubai" or "cash" or "mortgage" or "ready"
        candidate = country_match.group(1).strip().title()
        if not any(k in candidate.lower() for k in ["cash", "mortgage", "ready", "immediate", "dubai", "invest", "personal"]):
            profile["country"] = candidate

    # Name heuristics
    name_match = re.search(r"(?:my name is|i am|i'm) ([a-zA-Z]{2,15})(?: ([a-zA-Z]{2,15}))?", all_text, re.IGNORECASE)
    if name_match:
        profile["first_name"] = name_match.group(1).strip().title()
        if name_match.group(2):
            profile["last_name"] = name_match.group(2).strip().title()

    # Budget heuristics
    if "million" in all_text or "m" in all_text or any(c.isdigit() for c in all_text):
        budget_match = re.search(r"(\d+ ?million|\d+m|\d+)", all_text, re.IGNORECASE)
        if budget_match:
            profile["budget"] = normalize_budget(budget_match.group(0))
            
    # Timeline heuristics
    timeline_match = re.search(r"(immediate|now|asap|\d ?month|year)", all_text, re.IGNORECASE)
    if timeline_match:
        profile["timeline"] = normalize_timeline(timeline_match.group(0))

    # Purpose heuristics
    purpose_match = re.search(r"(invest|personal|live|home|reside)", all_text, re.IGNORECASE)
    if purpose_match:
        profile["purpose"] = normalize_purpose(purpose_match.group(0))

    # Properties
    if "villa" in all_text.lower():
        profile["property_interest"] = "Villa"
    elif "penthouse" in all_text.lower():
        profile["property_interest"] = "Penthouse"
    elif "apartment" in all_text.lower():
        profile["property_interest"] = "Apartment"

    # Fill default names for complete profile fallback
    profile["first_name"] = "International"
    profile["last_name"] = "Investor"
    profile["notes"] = "Interested in luxury Dubai properties."
    return profile

def generate_personalized_email(lead_data):
    """
    Generates a personalized introductory email based on the qualified lead details.
    """
    client = get_gemini_client()
    if client:
        try:
            prompt = f"""
Write a luxury sales introductory email from Panache Homes to this client:
Name: {lead_data.get('first_name')} {lead_data.get('last_name')}
Email: {lead_data.get('email')}
Property Interest: {lead_data.get('property_interest')}
Budget: {lead_data.get('budget')}
Timeline: {lead_data.get('timeline')}
Notes: {lead_data.get('notes')}

Make the email sound sophisticated, elite, and welcoming. Offer high-end property suggestions and request a brief private Zoom alignment call. Keep it concise, formal, and tailored.
"""
            response = client.generate_content(prompt)
            return response.text
        except Exception:
            pass
            
    # Elegant fallback template
    return f"""Subject: Exquisite Dubai Real Estate Opportunities - Panache Homes

Dear {lead_data.get('first_name', 'Valued Client')},

It was a pleasure speaking with you regarding your interest in Dubai's premier residential market. 

Based on your preference for a luxury {lead_data.get('property_interest', 'property')} and your budget range of {lead_data.get('budget', 'premium portfolio')}, we have curated a select group of off-market signature residences in Palm Jumeirah and Downtown Dubai that align with your vision.

We would be delighted to host a private virtual consultation to showcase these villas and apartments. Please let us know a suitable time for a brief Zoom meeting.

Warm regards,

Panache Homes Private Brokerage
Dubai Marina, UAE
"""

def generate_conversation_summary(chat_history, current_lead):
    """
    Generate conversation summary using Gemini if configured, or elegant fallback.
    """
    client = get_gemini_client()
    if client:
        try:
            full_transcript = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in chat_history])
            prompt = f"""
Write a brief, professional 2-3 sentence conversation summary of the following real estate qualification chat. Focus on their investment goals, timeline, and requirements. Do not include pricing formulas.

TRANSCRIPT:
{full_transcript}
"""
            response = client.generate_content(prompt)
            return response.text.strip()
        except Exception:
            pass
            
    # Heuristic fallback summary
    name = f"{current_lead.get('first_name', 'Client')} {current_lead.get('last_name', '')}".strip()
    country = current_lead.get('country', 'Unspecified')
    budget = current_lead.get('budget', 'Unconfirmed')
    timeline = current_lead.get('timeline', 'Flexible')
    purpose = current_lead.get('purpose', 'unspecified use')
    payment = current_lead.get('payment_method', 'flexible payment')
    
    return f"Client {name} from {country} is interested in Dubai property for {purpose.lower()}. They have a budget of AED {budget} and plan to purchase within {timeline} using {payment}."
