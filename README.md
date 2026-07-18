# 🏡 Panache Homes AI Lead Assistant

<p align="center">

![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite)
![Google Gemini](https://img.shields.io/badge/Google-Gemini_AI-orange)
![Google Sheets](https://img.shields.io/badge/Google-Sheets-green?logo=googlesheets)
![Render](https://img.shields.io/badge/Backend-Render-46E3B7)
![Vercel](https://img.shields.io/badge/Frontend-Vercel-black?logo=vercel)

</p>

---

## 📖 Overview

Panache Homes AI Lead Assistant is a full-stack AI-powered CRM designed for luxury real estate lead qualification.

The system interacts with potential property buyers, intelligently collects lead information using the **BANT Framework (Budget, Authority, Need, Timeline)**, grades the lead, generates an AI-powered advisory, synchronizes qualified leads with Google Sheets, and provides an analytics dashboard for administrators.

---

# 🚀 Live Demo

### 🌐 Frontend

https://panache-homes-ai-assistant.vercel.app

### ⚙️ Backend API

https://panache-backend-jb54.onrender.com

### 📘 API Documentation (Swagger)

https://panache-backend-jb54.onrender.com/docs

---

# ✨ Features

## 🤖 AI Chat Assistant

- Conversational lead qualification
- Context-aware responses
- Dubai property recommendations
- Knowledge Pack integration
- AI-generated conversation summaries

---

## 📊 BANT Lead Qualification

Automatically evaluates leads based on:

- 💰 Budget
- 👤 Authority
- 🎯 Need
- ⏳ Timeline

Generates:

- Grade A
- Grade B
- Grade C
- Grade D

---

## 📄 PDF Advisory Reports

Automatically generates:

- Lead summary
- Qualification report
- Personalized advisory
- Downloadable PDF

---

## 📈 CRM Dashboard

Features include:

- Total Leads
- Today's Leads
- Grade Analytics
- Lead Pipeline
- Status Tracking
- Google Sheets Connection Status

---

## 📑 Google Sheets Integration

Automatically syncs:

- Lead Name
- Country
- Budget
- Timeline
- Purpose
- Grade
- AI Summary

---

## 🔐 Authentication

- JWT Authentication
- Protected Admin Dashboard
- Secure Login

---

# 🛠 Tech Stack

## Frontend

- Next.js 16
- React
- TypeScript
- Tailwind CSS
- Axios

---

## Backend

- FastAPI
- Python
- SQLite
- JWT Authentication

---

## AI

- Google Gemini API

---

## Integrations

- Google Sheets API
- PDF Generation

---

## Deployment

Frontend

- Vercel

Backend

- Render

---

# 📂 Project Structure

```
panache-homes/

├── backend/
│   ├── api.py
│   ├── database.py
│   ├── services/
│   ├── knowledge_base.json
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── app/
│   └── package.json
│
└── README.md
```

---

# 📸 Screenshots


🏠 Home Page

![Home Page](screenshot/homepage.png)

---

🤖 AI Chat Assistant

![AI Chat Assistant](screenshot/ai-chat-assistant.png)

---

🏙️ Property Gallery

![Property Gallery](screenshot/property-gallery.png)

---

🌍 Community Explorer

![Community Explorer](screenshot/community-explorer.png)

---

📋 Lead Pipeline

![Lead Pipeline](screenshot/lead-pipeline.png)

---

📊 CRM Dashboard

![CRM Dashboard](screenshot/crm-dashboard.png)

---

📄 Google Sheets Integration

![Google Sheets](screenshot/google-sheets.png)

---

📑 PDF Advisory Report

![PDF Report](screenshot/pdf-report.png)

---

📈 CRM Analytics

![CRM Analytics](screenshot/charts.png)

# 🔄 Workflow

```
Visitor

↓

AI Chat Assistant

↓

Lead Qualification

↓

BANT Scoring

↓

SQLite Database

↓

Google Sheets

↓

CRM Dashboard

↓

PDF Advisory Report
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
