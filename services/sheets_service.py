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
    
    if not creds_json or not sheet_url:
        raise ValueError("Google Sheets integration is not fully configured in settings.")
        
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_data = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_data, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url).sheet1
    return sheet

def sync_lead_to_sheets(lead_data):
    """
    Appends lead_data to Google Sheets. Fallbacks to simulation if not configured.
    """
    try:
        sheet = get_sheets_client()
        
        # Verify header exists, if not write header
        headers = ["Timestamp", "Name", "Country", "Budget", "Payment Method", "Timeline", "Purpose", "Lead Grade", "Conversation Summary"]
        try:
            existing_headers = sheet.row_values(1)
            if not existing_headers:
                sheet.append_row(headers)
        except Exception:
            sheet.append_row(headers)
            
        from datetime import datetime
        timestamp = lead_data.get("created_at") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        name = f"{lead_data.get('first_name', '')} {lead_data.get('last_name', '')}".strip()
        
        row = [
            timestamp,
            name,
            lead_data.get("country", ""),
            lead_data.get("budget", ""),
            lead_data.get("payment_method", ""),
            lead_data.get("timeline", ""),
            lead_data.get("purpose", ""),
            lead_data.get("grade", ""),
            lead_data.get("ai_summary", "")
        ]
        sheet.append_row(row)
        return True, "Successfully synced to Google Sheets!"
    except Exception as e:
        # Return friendly message for simulator fallback
        return False, f"Simulation Sync: Lead captured locally. To write to active Sheets, configure Service Account credentials in the Settings panel. (Error: {str(e)})"
