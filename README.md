# Panache Homes AI Lead Assistant

A premium luxury real estate lead qualification portal and SaaS admin dashboard. The platform leverages advanced conversational AI to naturally qualify international buyers for Dubai real estate, grade leads, structure payment schedules, and synchronize data directly to a central Google Sheets CRM.

---

## Technical Stack
- **Frontend/UI**: Streamlit (Python) with highly polished custom CSS (Navy, Gold, and Slate/White luxury theme).
- **Database**: SQLite (SQLAlchemy) for structured lead profiles, conversation records, and metadata.
- **Services**:
  - `llm_service`: Integrates Gemini (via google-generativeai) for natural conversational dialogue, intent extraction, and automated lead summaries, with a robust fallback state-machine.
  - `sheets_service`: Synchronizes structured leads (Timestamp, Name, Country, Budget, Payment, Timeline, Purpose, Grade, Summary) to Google Sheets CRM.
  - `scoring_service`: Implements deterministic BANT grading engine classifying leads into Grades A, B, C, or D.

---

## Folder Structure
```
├── app.py                   # Main Streamlit application
├── database.py              # SQLite models, schemas, and connection engine
├── knowledge_base.json      # Grounding knowledge base (Visa rules, fees, etc.)
├── styles.py                # Premium CSS styling injectors
├── README.md                # Project documentation
├── reflection_document.md   # Architectural decisions & trade-offs log
├── services/
│   ├── llm_service.py       # Gemini API caller and fallback dialogue simulator
│   ├── sheets_service.py    # Google Sheets connector
│   └── scoring_service.py   # Deterministic BANT grading engine
├── assets/                  # Logos and visual properties
├── screenshots/             # Interface screengrabs
└── docs/                    # Architecture diagrams & manuals
```

---

## Installation & How to Run

1. Clone or copy this repository to your workspace.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your Google Gemini API key:
   - On Windows (PowerShell):
     ```powershell
     $env:GEMINI_API_KEY="your-gemini-api-key"
     ```
   - On Linux/macOS:
     ```bash
     export GEMINI_API_KEY="your-gemini-api-key"
     ```
4. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```
5. Open your browser and navigate to `http://localhost:8501`.

---

## Google Sheets Integration Setup
The Google Sheets integration connects automatically using your Google Cloud Service Account.
1. Place your Google Sheets Service Account credentials JSON file in the project directory named `credentials.json` (or set the file path in app settings).
2. Share your destination Google Sheet with the client email listed in the credentials JSON.
3. The system will automatically detect the spreadsheet and sync qualified leads.

---

## Project Walkthrough & Personas
You can test the system using the pre-programmed client personas:
- **Michael (USA - Grade A)**: Budget of AED 2.5M, remote buyer, cash payment, looking to close in 1-3 months.
- **Priya (India - Grade B)**: Budget of AED 1.2M, buying a primary residence, using a bank mortgage, looking to buy in 3-6 months.
- **Sara (UK - Grade C)**: Budget of AED 800k, looking for high-yield holiday apartments.
