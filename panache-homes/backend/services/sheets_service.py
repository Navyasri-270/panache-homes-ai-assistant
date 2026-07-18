import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from database import get_config

def get_sheets_client():
    """
    Attempts to initialize Google Sheets client using configured Service Account JSON.
    Returns client and sheet instance, or raises Exception if not configured.
    """
    creds_json = get_config("google_sheets_creds")
    sheet_url = get_config("google_sheets_url")
    
    # Fallback to environment variables or credentials.json if DB is empty
    if not creds_json:
        creds_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
        if os.path.exists(creds_path):
            with open(creds_path, "r") as f:
                creds_json = f.read()
                
    if not sheet_url:
        sheet_id = os.getenv("GOOGLE_SHEETS_ID")
        if sheet_id:
            sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
        else:
            sheet_url = os.getenv("GOOGLE_SHEETS_URL")
            
    if not creds_json or not sheet_url:
        raise ValueError("Google Sheets integration is not fully configured in settings.")
        
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_data = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_data, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url).sheet1
    return sheet

def get_leads_from_sheets():
    try:
        sheet = get_sheets_client()
        records = sheet.get_all_records()

        leads = []

        for i, row in enumerate(records, start=1):
            name = row.get("Name", "")
            first_name = name.split(" ")[0] if name else ""
            last_name = " ".join(name.split(" ")[1:]) if len(name.split()) > 1 else ""

            leads.append({
                "id": i,
                "first_name": first_name,
                "last_name": last_name,
                "email": "",
                "country": row.get("Country", ""),
                "budget": row.get("Budget", ""),
                "payment_method": row.get("Payment Method", ""),
                "timeline": row.get("Timeline", ""),
                "purpose": row.get("Purpose", ""),
                "grade": row.get("Lead Grade", ""),
                "ai_summary": row.get("Conversation Summary", ""),
                "created_at": row.get("Timestamp", ""),
                "status": "New",
                "synced_to_sheets": True
            })

        leads.reverse()
        return leads

    except Exception as e:
        print("Google Sheets Read Error:", e)
        return []
    