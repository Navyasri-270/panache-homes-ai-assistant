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
def sync_lead_to_sheets(lead):
    """
    Writes a completed lead to Google Sheets.
    Returns (success, message).
    """
    try:
        sheet = get_sheets_client()

        sheet.append_row([
            lead.get("full_name", ""),
            lead.get("country", ""),
            lead.get("budget", ""),
            lead.get("payment_method", ""),
            lead.get("timeline", ""),
            lead.get("purpose", ""),
            lead.get("grade", ""),
            lead.get("ai_summary", ""),
        ])

        return True, "Lead successfully synced to Google Sheets."

    except Exception as e:
        return (
            False,
            f"Simulation Sync: Lead captured locally. To write to active Sheets, configure Service Account credentials in the Settings panel. (Error: {str(e)})",
        )

