import os
from dotenv import load_dotenv
load_dotenv()
import json
import sqlite3
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
from services.sheets_service import (sync_lead_to_sheets,get_sheets_client,)


# JWT Configurations
SECRET_KEY = "panache_homes_super_secret_admin_key"
ALGORITHM = "HS256"
security = HTTPBearer()

def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_admin(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Not authorized to access administrator resources.")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid session token.")

from fastapi.responses import FileResponse, StreamingResponse

# Import existing backend modules
import database
from services.scoring_service import calculate_lead_grade
from services.sheets_service import sync_lead_to_sheets
from services.llm_service import (
    generate_chatbot_response, 
    extract_lead_profile, 
    generate_personalized_email, 
    generate_conversation_summary
)
from services.pdf_service import generate_lead_pdf

app = FastAPI(title="Panache Homes AI CRM API")

# Configure CORS for Next.js dev server communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://panache-homes-ai-assistant.vercel.app",
        "https://panache-homes-ai-assistant-9z767alq2.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
  role: str
  content: str

class ChatPayload(BaseModel):
  messages: List[ChatMessage]
  current_lead: Dict[str, Any]

class LeadPayload(BaseModel):
  first_name: str
  last_name: str
  email: str
  phone: str
  country: str
  budget: str
  payment_method: str
  timeline: str
  purpose: str;
  property_interest: Optional[str] = "";
  chat_transcript: List[Dict[str, str]]
  grade: Optional[str] = "C"

class StatusPayload(BaseModel):
  id: int
  status: str

@app.on_event("startup")
def startup():
    database.init_db()

@app.get("/api/properties")
def get_properties():
    return [
        {
            "title": "Burj Khalifa Sky Residence",
            "community": "Downtown Dubai",
            "price": "Starting AED 4.5M",
            "roi": "ROI 7.8%",
            "desc": "Ultra-high-end sky apartments with panoramic fountain views and private concierge.",
            "img": "https://images.unsplash.com/photo-1526495124232-a04e1849168a?auto=format&fit=crop&w=600&q=80"
        },
        {
            "title": "Palm Jumeirah Signature Villa",
            "community": "Palm Jumeirah",
            "price": "Starting AED 18.0M",
            "roi": "ROI 6.5%",
            "desc": "Stunning custom beachfront mansion with private pool, direct sea access, and lush gardens.",
            "img": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=600&q=80"
        },
        {
            "title": "Marina Gate Premium Apartment",
            "community": "Dubai Marina",
            "price": "Starting AED 2.8M",
            "roi": "ROI 8.2%",
            "desc": "Modern luxury high-rise apartment with panoramic marina views, rooftop pool, and health club.",
            "img": "https://images.unsplash.com/photo-1528702748617-c64d49f918af?auto=format&fit=crop&w=600&q=80"
        },
        {
            "title": "Dubai Hills Estate Gated Mansion",
            "community": "Dubai Hills Estate",
            "price": "Starting AED 12.5M",
            "roi": "ROI 7.2%",
            "desc": "Luxury estate villa built directly on the championship golf course with infinity pool.",
            "img": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=600&q=80"
        },
        {
            "title": "Burj Al Arab Sunset Duplex",
            "community": "Jumeirah",
            "price": "Starting AED 9.2M",
            "roi": "ROI 6.8%",
            "desc": "Exclusive duplex residence offering unmatched sunset views over the Arabian Gulf.",
            "img": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=600&q=80"
        },
        {
            "title": "One Canal Private Penthouses",
            "community": "Dubai Water Canal",
            "price": "Starting AED 15.0M",
            "roi": "ROI 7.0%",
            "desc": "Ultra-luxury full-floor penthouse with private terrace pool and custom automated design.",
            "img": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=600&q=80"
        },
        {
            "title": "Arabian Ranches Family Villa",
            "community": "Arabian Ranches III",
            "price": "Starting AED 3.8M",
            "roi": "ROI 7.5%",
            "desc": "Tranquil family villa with expansive landscaped garden, family parks, and community pools.",
            "img": "https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=600&q=80"
        },
        {
            "title": "Business Bay Canal Suite",
            "community": "Business Bay",
            "price": "Starting AED 1.8M",
            "roi": "ROI 8.5%",
            "desc": "Elegant modern executive apartment with water views and premium workspace facilities.",
            "img": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=600&q=80"
        }
    ]

@app.get("/api/communities")
def get_communities_endpoint():
    return [
        {
            "name": "Downtown Dubai",
            "desc": "The prestigious center of Dubai containing Burj Khalifa, Dubai Mall, and luxury skyscrapers.",
            "roi": "7.8% Average ROI",
            "highlights": "Capital of tourism, premium high-rise yields, strong demand.",
            "img": "/images/luxury_apartment.jpg"
        },
        {
            "name": "Palm Jumeirah",
            "desc": "World-famous man-made island hosting beach villas and high-end resorts.",
            "roi": "6.5% Average ROI",
            "highlights": "ビーチフロントの高級不動産, limited land supply driving value appreciation.",
            "img": "/images/luxury_villa.jpg"
        },
        {
            "name": "Dubai Marina",
            "desc": "Vibrant waterfront community featuring skyscrapers overlooking a canal harbor.",
            "roi": "8.2% Average ROI",
            "highlights": "High rental demand from expatriates, waterfront dining, yacht access.",
            "img": "/images/dubai_skyline.jpg"
        },
        {
            "name": "Dubai Hills Estate",
            "desc": "Family-centric golf community with parks, international schools, and hospital centers.",
            "roi": "7.2% Average ROI",
            "highlights": "Green landscapes, championship golf club, premium villas.",
            "img": "/images/luxury_villa.jpg"
        },
        {
            "name": "Business Bay",
            "desc": "The commercial center of Dubai situated directly on the Dubai Water Canal.",
            "roi": "8.5% Average ROI",
            "highlights": "Ideal for professionals, canal walk lifestyle, high occupancies.",
            "img": "/images/luxury_apartment.jpg"
        },
        {
            "name": "Arabian Ranches",
            "desc": "Established premium villa sub-neighborhood focusing on tranquil desert environments.",
            "roi": "7.5% Average ROI",
            "highlights": "Private gardens, family clubs, stable long-term tenancies.",
            "img": "/images/luxury_villa.jpg"
        }
    ]

@app.post("/api/chat")
def chat_endpoint(payload: ChatPayload):
    history = [{"role": msg.role, "content": msg.content} for msg in payload.messages]
    
    # Run the entity extractor from backend
    extracted = extract_lead_profile(history)
    
    # Merge extracted details with frontend current_lead values
    updated_lead = payload.current_lead.copy()
    for k, v in extracted.items():
        if v:
            updated_lead[k] = v
            
    # Generate bot response using backend prompt engine
    reply = generate_chatbot_response(history, updated_lead)
    
    # Calculate grade using scoring rules engine
    grade = calculate_lead_grade(updated_lead)
    
    # Determine if BANT is complete
    required = ["first_name", "country", "budget", "payment_method", "timeline", "purpose"]
    is_complete = all(bool(updated_lead.get(f)) for f in required)
    
    summary = ""
    email_draft = ""
    if is_complete:
        summary = generate_conversation_summary(history, updated_lead)
        # Add summary to lead data before generating email if needed
        lead_with_summary = updated_lead.copy()
        lead_with_summary["notes"] = f"{lead_with_summary.get('notes', '')}\nSummary: {summary}".strip()
        email_draft = generate_personalized_email(lead_with_summary)

    return {
        "reply": reply,
        "current_lead": updated_lead,
        "grade": grade,
        "qualification_complete": is_complete,
        "summary": summary,
        "email_draft": email_draft
    }

@app.post("/api/leads")
def create_lead(payload: LeadPayload):
    lead_dict = payload.dict()
    
    # Calculate lead grade
    grade = calculate_lead_grade(lead_dict)
    lead_dict["grade"] = grade
    
    # Generate AI metrics
    summary = generate_conversation_summary(payload.chat_transcript, lead_dict)
    lead_with_summary = lead_dict.copy()
    lead_with_summary["notes"] = f"{lead_with_summary.get('notes', '')}\nSummary: {summary}".strip()
    email_draft = generate_personalized_email(lead_with_summary)
    
    lead_dict["ai_summary"] = summary
    lead_dict["generated_email"] = email_draft
    
    # Save to SQLite database
    lead_id = database.save_lead(lead_dict)
    
    # Sync to Google Sheets
    synced, message = sync_lead_to_sheets(lead_dict)
    print("Google Sheets:", synced, message)
    if synced:
        database.update_lead_sync_status(lead_id, 1)
        
    return {
        "success": True,
        "lead_id": lead_id,
        "grade": grade,
        "synced": synced,
        "message": message
    }

@app.post("/api/google-sync")
def google_sync_endpoint(payload: Dict[str, Any]):
    synced, message = sync_lead_to_sheets(payload)
    return {
        "success": synced,
        "message": message
    }

class LoginPayload(BaseModel):
    username: str
    password: str

@app.post("/api/login")
def login_endpoint(payload: LoginPayload):
    username = payload.username.strip().lower()
    password = payload.password.strip()
    if username == "admin@panachehomes.ae" and password == "admin123":
        token = create_access_token({"sub": username, "role": "admin"})
        return {"access_token": token, "token_type": "bearer", "username": username}
    raise HTTPException(status_code=401, detail="Invalid administrator credentials.")



@app.get("/api/leads")
def get_leads_list():
    return database.get_all_leads()

@app.get("/api/leads/{lead_id}/pdf")
def get_lead_pdf_endpoint(lead_id: int):
    import tempfile
    lead = database.get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    pdf_buffer = generate_lead_pdf(lead)
    
    # Save pdf buffer to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_file.write(pdf_buffer.getvalue())
    temp_file.close()
    
    filename = f"Panache_Homes_Report_{lead.get('first_name')}_{lead.get('last_name')}.pdf"
    return FileResponse(
        temp_file.name,
        media_type="application/pdf",
        filename=filename
    )

@app.post("/api/leads/status")
def update_status(payload: StatusPayload, admin: dict = Depends(get_current_admin)):
    database.update_lead_status(payload.id, payload.status)
    return {"success": True}

@app.get("/api/sheets/status")
def get_sheets_status(admin: dict = Depends(get_current_admin)):
    try:
        # Reuse the same logic used for syncing
        sheet = get_sheets_client()

        # Simple call to verify access
        sheet.title

        return {
            "configured": True,
            "connected": True,
            "url": sheet.spreadsheet.url
        }

    except Exception as e:
        return {
            "configured": False,
            "connected": False,
            "error": str(e)
        }

@app.post("/api/settings")
def update_settings(payload: Dict[str, str], admin: dict = Depends(get_current_admin)):
    for k, v in payload.items():
        database.set_config(k, v)
    return {"success": True}

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected"
    }
