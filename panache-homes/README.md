# Panache Homes AI Lead Assistant

A premium, luxury-focused AI CRM and Lead Qualification assistant designed for Panache Homes in Dubai. This application combines a Next.js frontend with a FastAPI backend, providing intelligent BANT (Budget, Authority, Need, Timeline) grading, dynamic Google Sheets syncing, automatic PDF advisory generation, and robust analytics visualizations.

---

## 🏗️ System Architecture

The application is decoupled into two core components:
1. **Frontend (`/frontend`)**: Built with React 19, Next.js (App Router), TailwindCSS, Lucide-React, and Recharts.
2. **Backend (`/backend`)**: Powered by FastAPI, SQLite (via `database.py`), Gemini AI (for NLP entity extraction), and ReportLab (for PDF exports).

For a visual breakdown of data flow and components, see the generated [4_architecture.png](4_architecture.png) and [4_architecture.txt](4_architecture.txt) at the root of the repository.

---

## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* Node.js 18+
* Gemini API Key (Optional; falls back to a deterministic rule-based simulation engine if not configured)

---

### Step 1: Run the Backend API

1. Navigate to the backend directory and install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Create a `.env` file (copied from the root `.env.example`) and insert your API key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. Run the Uvicorn server:
   ```bash
   uvicorn api:app --host 127.0.0.1 --port 8000 --reload
   ```
   * The API will run at `http://127.0.0.1:8000`. 
   * Verify it is live by navigating to the health check endpoint: `http://127.0.0.1:8000/api/health`.

---

### Step 2: Run the Next.js Frontend

1. Navigate to the frontend directory and install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Launch the Next.js development server:
   ```bash
   npm run dev
   ```
   * Open your browser and navigate to `http://localhost:3000`.

---

## 🔑 Administrative Access

To access the CRM Admin Panel and view user analytics:
* **Login URL**: `http://localhost:3000/login` (or `/admin` / `/dashboard`)
* **Username**: `admin@panachehomes.ae`
* **Password**: `admin123`

---

## 🌟 Key Features

1. **AI Property Advisor**: Interactive qualifying chatbot that answers questions using the local Knowledge Pack (ROI, Visa eligibility, buying fees) and collects customer BANT details.
2. **BANT Scoring Engine**: Dynamically scores leads into Grades A, B, C, or D.
3. **Google Sheets Sync**: Real-time synchronization of qualified leads to an administrative spreadsheet using OAuth2 Service Accounts.
4. **CRM Dashboard**: Real-time charts (BANT Grade distribution, daily/monthly leads volume, regional demand, budgets) built using Recharts.
5. **Interactive Leads Drawer**: Slide-out panel for administrative management, follow-up automation, status transitions, and outreach WhatsApp copy generation.
6. **PDF Dossier Export**: Compile and download styled PDFs detailing BANT criteria, full transcripts with timestamps, and custom payment schedules.

---

## 📁 Repository Deliverables
- **[3_prompt.txt](3_prompt.txt)**: Unedited system prompt controlling the Gemini AI agent.
- **[4_architecture.png](4_architecture.png) / [txt](4_architecture.txt)**: Minimalist system architecture diagram and narrative.
- **[5_workflow.png](5_workflow.png) / [json](5_workflow.json)**: Lead qualification workflow diagram and JSON mapping schema.
- **[6_reflection.txt](6_reflection.txt)**: Project development reflections and future roadmap.
