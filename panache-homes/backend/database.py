import sqlite3
import json
from datetime import datetime

DB_FILE = "panache_leads.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Create leads table
    c.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone TEXT,
            company TEXT,
            country TEXT,
            budget TEXT,
            property_interest TEXT,
            payment_method TEXT,
            timeline TEXT,
            purpose TEXT,
            score INTEGER DEFAULT 0,
            grade TEXT,
            status TEXT DEFAULT 'New',
            notes TEXT,
            ai_summary TEXT,
            generated_email TEXT,
            chat_transcript TEXT,
            synced_to_sheets INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Create configuration table
    c.execute('''
        CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_lead(lead_data):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO leads (
            first_name, last_name, email, phone, company, country, 
            budget, property_interest, payment_method, timeline, purpose, score, grade, status, 
            notes, ai_summary, generated_email, chat_transcript
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        lead_data.get('first_name'),
        lead_data.get('last_name'),
        lead_data.get('email'),
        lead_data.get('phone'),
        lead_data.get('company', ''),
        lead_data.get('country', ''),
        lead_data.get('budget', ''),
        lead_data.get('property_interest', ''),
        lead_data.get('payment_method', ''),
        lead_data.get('timeline', ''),
        lead_data.get('purpose', ''),
        lead_data.get('score', 0),
        lead_data.get('grade', 'C'),
        lead_data.get('status', 'New'),
        lead_data.get('notes', ''),
        lead_data.get('ai_summary', ''),
        lead_data.get('generated_email', ''),
        json.dumps(lead_data.get('chat_transcript', []))
    ))

    lead_id = c.lastrowid
    conn.commit()
    conn.close()
    return lead_id

def get_all_leads():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM leads ORDER BY created_at DESC")
    rows = c.fetchall()
    leads = [dict(row) for row in rows]
    conn.close()
    return leads

def update_lead_status(lead_id, status):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE leads SET status = ? WHERE id = ?", (status, lead_id))
    conn.commit()
    conn.close()

def update_lead_sync_status(lead_id, synced):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE leads SET synced_to_sheets = ? WHERE id = ?", (1 if synced else 0, lead_id))
    conn.commit()
    conn.close()

def delete_lead(lead_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM leads WHERE id = ?", (lead_id,))
    conn.commit()
    conn.close()

def get_config(key, default=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT value FROM config WHERE key = ?", (key,))
    row = c.fetchone()
    conn.close()
    if row:
        return row[0]
    return default

def set_config(key, value):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", (key, str(value)))
    conn.commit()
    conn.close()

def get_lead(lead_id):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

# Initialize on import
init_db()
