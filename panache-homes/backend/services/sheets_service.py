import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from database import get_config


def get_sheets_client():
    """
    Initializes Google Sheets client.

    Priority:
    1. Admin Settings (SQLite)
    2. Render Environment Variables
    3. Local credentials.json
    """

    # First preference: values stored from Admin Settings
    creds_json = (
        get_config("google_sheets_creds")
        or os.getenv("GOOGLE_SHEETS_CREDS")
    )

    sheet_url = (
        get_config("google_sheets_url")
        or os.getenv("GOOGLE_SHEETS_URL")
    )

    # Local development fallback
    if not creds_json:
        creds_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
        if os.path.exists(creds_path):
            with open(creds_path, "r") as f:
                creds_json = f.read()

    # Support GOOGLE_SHEETS_ID as well
    if not sheet_url:
        sheet_id = os.getenv("GOOGLE_SHEETS_ID")
        if sheet_id:
            sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"

    if not creds_json or not sheet_url:
        raise ValueError(
            "Google Sheets integration is not fully configured."
        )

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    creds_data = json.loads(creds_json)

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_data,
        scope,
    )

    client = gspread.authorize(creds)

    sheet = client.open_by_url(sheet_url).sheet1

    return sheet


def sync_lead_to_sheets(lead_data):
    """
    Writes completed lead to Google Sheets.
    """

    try:
        sheet = get_sheets_client()

        headers = [
            "Timestamp",
            "Name",
            "Country",
            "Budget",
            "Payment Method",
            "Timeline",
            "Purpose",
            "Lead Grade",
            "Conversation Summary",
        ]

        try:
            existing_headers = sheet.row_values(1)

            if not existing_headers:
                sheet.append_row(headers)

        except Exception:
            sheet.append_row(headers)

        from datetime import datetime
        from zoneinfo import ZoneInfo
        timestamp = (
            lead_data.get("created_at")
            or datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
        )

        full_name = (
            f"{lead_data.get('first_name', '')} "
            f"{lead_data.get('last_name', '')}"
        ).strip()

        row = [
            timestamp,
            full_name,
            lead_data.get("country", ""),
            lead_data.get("budget", ""),
            lead_data.get("payment_method", ""),
            lead_data.get("timeline", ""),
            lead_data.get("purpose", ""),
            lead_data.get("grade", ""),
            lead_data.get("ai_summary", ""),
        ]

        sheet.append_row(row)

        return True, "Successfully synced to Google Sheets!"

    except Exception as e:
        return (
            False,
            f"Simulation Sync: Lead captured locally. "
            f"To write to active Sheets, configure "
            f"Service Account credentials in the Settings panel. "
            f"(Error: {str(e)})",
        )