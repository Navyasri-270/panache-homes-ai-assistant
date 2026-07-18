import os
import json
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

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

app = FastAPI(title="Panache Homes AI CRM API")

# Configure CORS for Next.js dev server communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
  purpose: str
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
            "img": "https://images.unsplash.com/photo-1597659829215-513fbf93c8c7?auto=format&fit=crop&w=600&q=80"
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
            "img": "https://images.unsplash.com/photo-1582672060674-bc2bd8022eb0?auto=format&fit=crop&w=600&q=80"
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
        summary = generate_conversation_summary(history)
        email_draft = generate_personalized_email(updated_lead, summary)

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
    summary = generate_conversation_summary(payload.chat_transcript)
    email_draft = generate_personalized_email(lead_dict, summary)
    
    lead_dict["ai_summary"] = summary
    lead_dict["generated_email"] = email_draft
    
    # Save to SQLite database
    lead_id = database.save_lead(lead_dict)
    
    # Sync to Google Sheets
    synced, message = sync_lead_to_sheets(lead_dict)
    if synced:
        database.update_lead_sync_status(lead_id, 1)
        
    return {
        "success": True,
        "lead_id": lead_id,
        "grade": grade,
        "synced": synced,
        "message": message
    }

@app.get("/api/leads")
def get_leads_list():
    return get_leads_from_sheets()

@app.post("/api/leads/status")
def update_status(payload: StatusPayload):
    database.update_lead_status(payload.id, payload.status)
    return {"success": True}

@app.get("/api/sheets/status")
def get_sheets_status():
    creds = database.get_config("google_sheets_creds")
    url = database.get_config("google_sheets_url")
    return {
        "configured": bool(creds and url),
        "url": url
    }

@app.post("/api/settings")
def update_settings(payload: Dict[str, str]):
    for k, v in payload.items():
        database.set_config(k, v)
    return {"success": True}
