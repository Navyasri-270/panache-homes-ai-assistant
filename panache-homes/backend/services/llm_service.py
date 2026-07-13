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
        return genai.GenerativeModel("gemini-flash-latest")
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
You must answer questions ONLY using the provided knowledge base below. Under no circumstances should you use external internet knowledge or guess facts. Never answer outside the provided knowledge base. If the user asks a question outside the Knowledge Pack (such as sports, politics, movies, weather, or general knowledge), you MUST respond exactly with:
"I'm designed specifically to assist with Panache Homes and Dubai real estate. I can't answer general knowledge or entertainment questions. I'd be happy to help with Dubai property investment, Golden Visa eligibility, payment plans, taxes, rental yields, or our premium communities."

KNOWLEDGE BASE:
{kb_str}

CONVERSATIONAL RULES:
1. Be extremely friendly, professional, warm, and polite. Tone should feel like high-end luxury concierge service.
2. Answer questions about Dubai property ownership, Golden Visas, ROI, taxes, and process ONLY using the provided knowledge base.
3. NEVER use internet knowledge, never invent facts, and never guess.
4. If the user asks about information, properties, or details that are NOT explicitly included in the knowledge base, you MUST respond exactly with:
   "I'm designed specifically to assist with Panache Homes and Dubai real estate. I can't answer general knowledge or entertainment questions. I'd be happy to help with Dubai property investment, Golden Visa eligibility, payment plans, taxes, rental yields, or our premium communities."
5. If the user asks a Knowledge Pack question, answer it immediately using ONLY the provided knowledge base, and then naturally return to the qualification flow by asking for the next missing field in the same response.
6. You must collect the following details ONE AT A TIME. DO NOT ask multiple qualification questions in a single response:
   - Name (First and Last)
   - Country of residence
   - Budget in AED
   - Payment Method (Cash or Mortgage)
   - Purchase Timeline
   - Purpose (Investment or Personal)
7. Do NOT repeat questions that have already been answered.
8. Currently, the missing fields are: {missing_str}. Focus on requesting the next missing detail organically.
9. Once all fields are collected, warmly thank them and let them know a senior advisor will reach out to them on WhatsApp/Email.
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
                model_name="gemini-flash-latest",
                system_instruction=system_instruction
            )
            response = model.generate_content(contents)
            return response.text
        except Exception as e:
            import sys
            print(f"Gemini API Error (falling back to simulation): {str(e)}", file=sys.stderr)
            # Fail gracefully to the simulated agent so the application remains fully testable
            return get_simulated_response(chat_history, current_lead)
    
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
    has_personal = any(k in clean for k in ["personal", "family", "own use", "live in it", "for myself", "holiday home"])
    
    if has_investment and has_personal:
        return "Investment & Personal Use"
    elif has_investment:
        return "Investment"
    elif has_personal:
        return "Personal Use"
    return purpose_str.title()

def parse_name(user_messages, user_text):
    # Try standard name match first (e.g. "my name is Michael", "i'm Michael", "call me Michael")
    name_match = re.search(r"(?i)\b(?:my name is|i am|i'm|call me|name is)\b\s*([a-zA-Z]{2,15})(?:\s+([a-zA-Z]{2,15}))?", user_text)
    if name_match:
        first = name_match.group(1).strip().title()
        last = name_match.group(2).strip().title() if name_match.group(2) else ""
        return first, last
    
    # Fallback: check email containing message
    for msg in user_messages:
        if "@" in msg:
            msg_clean = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", "", msg).strip()
            msg_clean = re.sub(r"(?i)\b(?:my name is|i am|i'm|this is|here is|hello|hi|good morning|good afternoon|email|email:)\b", "", msg_clean).strip()
            parts = msg_clean.split()
            if parts:
                first = parts[0].strip(",").title()
                last = parts[1].strip(",").title() if len(parts) > 1 else ""
                if first.lower() not in ["email", "email:"]:
                    return first, last
    return "", ""

def parse_country(text):
    text_lower = text.lower()
    clean_text = re.sub(r"[^\w\s]", " ", text_lower)
    words = clean_text.split()
    if "india" in words:
        return "India"
    if "texas" in words or "us" in words or "usa" in words or "united states" in text_lower or "america" in text_lower:
        return "US"
    if "london" in words or "uk" in words or "united kingdom" in text_lower or "britain" in text_lower:
        return "UK"
    country_match = re.search(r"(?:from|in|live in|reside in) ([a-zA-Z\s]{3,20})", text, re.IGNORECASE)
    if country_match:
        candidate = country_match.group(1).strip().title()
        if not any(k in candidate.lower() for k in ["cash", "mortgage", "ready", "immediate", "dubai", "invest", "personal"]):
            return candidate
    return ""

def parse_budget(text):
    text_lower = text.lower()
    match = re.search(r"(\d+(?:\.\d+)?)\s*(million|m\b)", text_lower)
    if match:
        val = float(match.group(1))
        return str(int(val * 1_000_000))
    
    nums = re.findall(r"\b\d[\d,.]*\b", text_lower)
    for num in nums:
        cleaned = num.replace(",", "")
        if "." in cleaned:
            try:
                val = float(cleaned)
                if val >= 10000:
                    return str(int(val))
            except ValueError:
                pass
        else:
            if cleaned.isdigit() and int(cleaned) >= 10000:
                return cleaned
    return ""

def get_simulated_response(chat_history, current_lead):
    """
    Simulated agent that asks precisely one question at a time for missing fields,
    with robust skip handling, validation, and graceful recovery.
    """
    if not chat_history:
        return "Welcome to Panache Homes."
        
    last_user_message = chat_history[-1]["content"].lower().strip() if chat_history else ""
    
    # 1. Detect if the user's message is a Knowledge Pack or Out-of-Scope question BEFORE parsing it as a BANT answer
    kb_answers = []
    
    # Define keywords for semantic matching
    fee_keywords = ["tax", "fee", "oqood", "dld", "cost", "charge", "vat", "buying fee"]
    currency_keywords = ["currency", "dirham", "rate", "usd", "swing", "peg", "pegged", "dollar", "aed", "stability"]
    visa_keywords = ["golden visa", "visa", "residency", "passport", "citizen", "10-year", "10 year"]
    yield_keywords = ["yield", "roi", "return", "rent", "profit", "guarantee"]
    remote_keywords = ["remote", "signing", "wire", "attorney", "from home", "online", "distance"]
    plan_keywords = ["payment", "plan", "booking", "instalment", "milestone", "handover", "down payment"]
    company_keywords = ["panache", "about", "who are you", "company", "brokerage", "what does", "who is"]
    community_keywords = ["community", "communities", "location", "area", "neighborhood", "palm jumeirah", "dubai marina", "downtown", "dubai hills"]
    
    # Fees & Taxes
    if any(k in last_user_message for k in fee_keywords):
        kb_answers.append("Dubai properties carry a 4% Dubai Land Department (DLD) registration fee on the property price, plus an AED 3,000 oqood fee for off-plan purchases. There is 0% annual property tax and 0% capital gains tax.")
        
    # Currency Peg
    if any(k in last_user_message for k in currency_keywords):
        kb_answers.append("Regarding currency risk: The UAE Dirham is pegged to the USD at a fixed exchange rate of 3.6725, meaning USD investors carry no currency risk.")
        
    # Golden Visa
    if any(k in last_user_message for k in visa_keywords):
        kb_answers.append("An investment of AED 2 Million in Dubai property qualifies you for the UAE 10-Year Golden Visa.")
        
    # Yields & ROI
    if any(k in last_user_message for k in yield_keywords):
        if "marina" in last_user_message:
            kb_answers.append("In Dubai Marina, the average rental yield/ROI is around 8.2% due to high occupancy rates and tourist demand.")
        else:
            kb_answers.append("Rental yields in Dubai are usually between 6%–8%. Please note we never guarantee returns.")
        
    # Remote Signing
    if any(k in last_user_message for k in remote_keywords):
        kb_answers.append("Customers can complete the purchase remotely through Digital Signing, International Wire Transfer, and Power of Attorney.")
        
    # Payment Plans
    if any(k in last_user_message for k in plan_keywords):
        if "palm" in last_user_message:
            kb_answers.append("For Palm Jumeirah properties, premium payment schedules such as 20/80 (20% booking, 80% on handover) or tailored construction milestones are available.")
        else:
            kb_answers.append("Payment plans usually consist of a 10%–20% booking amount, construction instalments, and a final payment on handover.")

    # Company Info
    if any(k in last_user_message for k in company_keywords):
        kb_answers.append("Panache Homes is a luxury real estate consultancy based in Dubai specializing in premium off-plan and secondary market properties. We help investors and home buyers with property selection, investment advice, Golden Visa assistance, and complete purchase support.")

    # Communities
    if any(k in last_user_message for k in community_keywords):
        if "marina" in last_user_message:
            kb_answers.append("Dubai Marina is a vibrant waterfront community featuring skyscrapers overlooking a canal harbor with high rental demand.")
        elif "palm" in last_user_message:
            kb_answers.append("Palm Jumeirah is a world-famous man-made island hosting beach villas, high-end resorts, and premium luxury penthouses.")
        else:
            kb_answers.append("Panache Homes offers premium property listings across Dubai's most exclusive communities, including Palm Jumeirah, Downtown Dubai, Dubai Hills Estate, and Dubai Marina.")

    # Check for out-of-scope question
    is_question = "?" in last_user_message or any(last_user_message.startswith(w) for w in ["who ", "what ", "why ", "where ", "how ", "when ", "is ", "are ", "can ", "do ", "does "])
    all_kb_keywords = fee_keywords + currency_keywords + visa_keywords + yield_keywords + remote_keywords + plan_keywords + company_keywords + community_keywords
    is_kb_matched = len(kb_answers) > 0 or any(k in last_user_message for k in ["panache", "about"])
    
    is_out_of_scope = is_question and not is_kb_matched

    # Helper function to find the next missing question prompt
    def get_next_missing_question():
        if not current_lead.get("first_name"):
            return "To begin curating the best options for you, could you please share your full name?"
        if not current_lead.get("email"):
            return f"Thank you, {current_lead.get('first_name')}. Could you share your email address?"
        if not current_lead.get("country"):
            return "Which country are you residing in currently?"
        if not current_lead.get("budget"):
            return "To recommend the best investment opportunities, could you share your approximate investment budget in AED?"
        if not current_lead.get("payment_method"):
            return "Will this purchase be made via Cash or do you plan to explore a Mortgage in Dubai?"
        if not current_lead.get("timeline"):
            return "When are you planning to purchase your property?"
        if not current_lead.get("purpose"):
            return "Will this property be for investment or personal use?"
        return "Thank you for sharing your requirements! I have recorded your preferences. A senior private client advisor from Panache Homes will contact you shortly via WhatsApp and email with our off-market portfolio."

    # Handle KB questions
    if kb_answers:
        combined = " ".join(kb_answers)
        # If Golden Visa was answered, and the budget is Unconfirmed/empty, reset it to ask for budget again!
        if ("Visa" in combined or "residency" in last_user_message) and (not current_lead.get("budget") or current_lead.get("budget") == "Unconfirmed"):
            current_lead["budget"] = ""
            return combined + " To recommend the best investment opportunities, could you share your approximate investment budget in AED?"
        return combined + " " + get_next_missing_question()

    # Handle out-of-scope questions
    if is_out_of_scope:
        refusal = "I'm designed specifically to assist with Panache Homes and Dubai real estate. I can't answer general knowledge or entertainment questions. I'd be happy to help with Dubai property investment, Golden Visa eligibility, payment plans, taxes, rental yields, or our premium communities."
        return refusal + " " + get_next_missing_question()

    # 2. If it is NOT a question, proceed with parsing it as a BANT answer based on the last assistant question!
    skip_keywords = ["skip", "next", "pass", "not sure", "don't want to say", "no comment", "secret", "private", "later", "explore", "exploring", "browse", "browsing", "look around", "looking around", "just looking", "not ready", "don't ready", "dont ready", "no details", "not sharing", "nothing", "no", "don't know", "dont know", "browsing only", "just looking", "prefer not to answer", "exploration", "explore only"]
    is_skip = any(k in last_user_message for k in skip_keywords)

    last_assistant_question = ""
    for msg in reversed(chat_history[:-1]):
        if msg["role"] == "assistant":
            last_assistant_question = msg["content"].lower()
            break

    # Try standard parse_name on user's input at any time if name is missing
    if not current_lead.get("first_name") or current_lead.get("first_name") == "Anonymous":
        first, last = parse_name([chat_history[-1]], chat_history[-1]["content"])
        if first:
            current_lead["first_name"] = first
            current_lead["last_name"] = last if last else ""

    # Parse based on context of the last question asked
    if "name" in last_assistant_question:
        if is_skip:
            current_lead["first_name"] = "Anonymous"
            current_lead["last_name"] = "Visitor"
        else:
            first, last = parse_name([chat_history[-1]], chat_history[-1]["content"])
            if first:
                current_lead["first_name"] = first
                current_lead["last_name"] = last if last else ""
            else:
                parts = chat_history[-1]["content"].strip().split()
                exclude_words = ["hello", "hi", "welcome", "about", "panache", "skip", "just", "exploring", "browsing", "look", "roi", "yield", "visa", "payment", "average", "rules", "how", "what", "where"]
                if len(parts) <= 3 and not any(w in chat_history[-1]["content"].lower() for w in exclude_words):
                    current_lead["first_name"] = parts[0].title()
                    current_lead["last_name"] = parts[1].title() if len(parts) > 1 else ""
                else:
                    current_lead["first_name"] = "Anonymous"
                    current_lead["last_name"] = "Visitor"

    elif "share your email" in last_assistant_question or "email address" in last_assistant_question:
        if is_skip:
            current_lead["email"] = "Unconfirmed"
        else:
            email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", chat_history[-1]["content"])
            if email_match:
                current_lead["email"] = email_match.group(0)
            else:
                email_asks = sum(1 for msg in chat_history if msg["role"] == "assistant" and ("share your email" in msg["content"].lower() or "email address" in msg["content"].lower()))
                if email_asks >= 2:
                    current_lead["email"] = "Unconfirmed"
                else:
                    return f"Thank you, {current_lead.get('first_name')}. Could you share your email address?"

    elif "which country" in last_assistant_question or "residing" in last_assistant_question:
        if is_skip:
            current_lead["country"] = "Unspecified"
        else:
            parsed_c = parse_country(chat_history[-1]["content"])
            current_lead["country"] = parsed_c if parsed_c else chat_history[-1]["content"].strip().title()

    elif "approximate investment budget" in last_assistant_question or "budget in aed" in last_assistant_question:
        budget_asks = sum(1 for msg in chat_history if msg["role"] == "assistant" and ("approximate investment budget" in msg["content"].lower() or "budget in aed" in msg["content"].lower()))
        if is_skip or budget_asks >= 2:
            current_lead["budget"] = "Unconfirmed"
            asked_timeline = any("completely fine to browse" in msg["content"].lower() or "just exploring" in msg["content"].lower() for msg in chat_history if msg["role"] == "assistant")
            msg_prefix = "No problem. I'll mark your budget as unconfirmed and continue helping you."
            if not asked_timeline:
                return msg_prefix + " Do you have a general purchase timeline, or are you just exploring? Also, please let me know if you have any questions."
            else:
                return msg_prefix + " " + get_next_missing_question()
        else:
            norm_budget = parse_budget(chat_history[-1]["content"])
            if not norm_budget:
                norm_budget = normalize_budget(chat_history[-1]["content"])
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

    elif "planning to purchase" in last_assistant_question or "just exploring" in last_assistant_question:
        timeline_asks = sum(1 for msg in chat_history if msg["role"] == "assistant" and ("purchase timeline" in msg["content"].lower() or "planning to purchase" in msg["content"].lower() or "just exploring" in msg["content"].lower()))
        if is_skip or timeline_asks >= 2:
            current_lead["timeline"] = "Flexible"
            msg_prefix = "No problem. I'll mark your timeline as unconfirmed and continue helping you."
            return msg_prefix + " " + get_next_missing_question()
        else:
            current_lead["timeline"] = normalize_timeline(chat_history[-1]["content"])

    elif "investment or personal use" in last_assistant_question or "property be for" in last_assistant_question:
        if is_skip:
            current_lead["purpose"] = "Investment & Personal Use"
        else:
            current_lead["purpose"] = normalize_purpose(chat_history[-1]["content"])

    # Parse answers in user's last message to dynamically catch keywords in case they voluntarily typed it
    if "from" in last_user_message or "live in" in last_user_message:
        if not current_lead.get("country"):
            parsed_c = parse_country(chat_history[-1]["content"])
            current_lead["country"] = parsed_c if parsed_c else chat_history[-1]["content"]
            
    if "cash" in last_user_message and not current_lead.get("payment_method"):
        current_lead["payment_method"] = "Cash"
    elif "mortgage" in last_user_message and not current_lead.get("payment_method"):
        current_lead["payment_method"] = "Mortgage"

    return get_next_missing_question()

def extract_lead_profile(chat_history):
    """
    Extracts structured fields from the conversation.
    Returns a dict with extracted lead parameters.
    """
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
    
    user_messages = [m["content"] for m in chat_history if m["role"] == "user"]
    user_text = " ".join(user_messages)
    all_text = " ".join([m["content"] for m in chat_history])
    
    # Extract Email
    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", user_text)
    if email_match:
        profile["email"] = email_match.group(0)
    else:
        # Check if they were asked for email
        email_asked = any("share your email" in msg["content"].lower() or "email address" in msg["content"].lower() for msg in chat_history if msg["role"] == "assistant")
        if email_asked:
            profile["email"] = "Unconfirmed"
        
    # Extract Phone
    phone_match = re.search(r"(\+\d{1,3}[- ]?)?\d{9,12}", user_text)
    if phone_match:
        profile["phone"] = phone_match.group(0)

    # Extract Name from email containing message or scanning first-name answering messages
    first_name_extracted = ""
    last_name_extracted = ""
    
    # Try standard parse_name on combined text first
    first, last = parse_name(user_messages, user_text)
    if first:
        first_name_extracted = first
        last_name_extracted = last
    else:
        # Scan chat history for message answering the name prompt
        for idx, msg in enumerate(chat_history):
            if msg["role"] == "user":
                is_answering_name = False
                if idx > 0 and chat_history[idx-1]["role"] == "assistant" and "name" in chat_history[idx-1]["content"].lower():
                    is_answering_name = True
                    
                if is_answering_name:
                    content = msg["content"].strip()
                    parts = content.split()
                    exclude_words = ["hello", "hi", "welcome", "about", "panache", "skip", "just", "exploring", "browsing", "look", "roi", "yield", "visa", "payment", "average", "rules", "how", "what", "where"]
                    if len(parts) <= 3 and not any(w in content.lower() for w in exclude_words):
                        first_name_extracted = parts[0].title()
                        last_name_extracted = parts[1].title() if len(parts) > 1 else ""
                        break

    if first_name_extracted:
        profile["first_name"] = first_name_extracted
        profile["last_name"] = last_name_extracted if last_name_extracted else ""

    # Country heuristics (Common countries checking)
    parsed_c = parse_country(user_text)
    if parsed_c:
        profile["country"] = parsed_c

    # Budget heuristics
    parsed_b = parse_budget(user_text)
    if parsed_b:
        profile["budget"] = parsed_b
            
    # Timeline heuristics
    for msg in user_messages:
        msg_clean = msg.lower()
        if "immediate" in msg_clean or "now" in msg_clean or "asap" in msg_clean or "right away" in msg_clean:
            profile["timeline"] = "Immediate"
            break
        elif "month" in msg_clean or "flexible" in msg_clean or "later" in msg_clean:
            profile["timeline"] = normalize_timeline(msg_clean)
            break

    if not profile["timeline"]:
        timeline_match = re.search(r"(immediate|now|asap|\d ?month|year)", user_text, re.IGNORECASE)
        if timeline_match:
            profile["timeline"] = normalize_timeline(timeline_match.group(0))

    # Purpose heuristics
    for msg in user_messages:
        msg_clean = msg.lower()
        if "invest" in msg_clean or "roi" in msg_clean or "yield" in msg_clean or "rent" in msg_clean:
            profile["purpose"] = "Investment"
            break
        elif "personal" in msg_clean or "family" in msg_clean or "own use" in msg_clean or "live in it" in msg_clean or "for myself" in msg_clean or "holiday home" in msg_clean:
            profile["purpose"] = "Personal Use"
            break


    # Properties
    if "villa" in all_text.lower():
        profile["property_interest"] = "Villa"
    elif "penthouse" in all_text.lower():
        profile["property_interest"] = "Penthouse"
    elif "apartment" in all_text.lower():
        profile["property_interest"] = "Apartment"

    # Fill default names for complete profile fallback
    if not profile["first_name"] and not profile["last_name"]:
        profile["first_name"] = "Anonymous"
        profile["last_name"] = "Visitor"
    elif not profile["first_name"]:
        profile["first_name"] = "Anonymous"
    if not profile["notes"]:
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
    purpose = current_lead.get('purpose', 'Investment')
    method = current_lead.get('payment_method', 'Cash')
    
    return f"Client {name} from {country} is interested in Dubai property for {purpose.lower()}. They have a budget of AED {budget} and plan to purchase within {timeline} using {method}."
