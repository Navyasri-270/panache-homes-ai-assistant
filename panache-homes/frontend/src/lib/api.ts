import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  timeout: 120000, // 120-second timeout to handle slow Gemini free-tier responses
  headers: {
    "Content-Type": "application/json",
  },
});

// Response interceptor to catch timeouts or unauthorized states
API.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === "ECONNABORTED") {
      console.error("API connection timed out. Retrying request...");
    }
    return Promise.reject(error);
  }
);

// Request interceptor to automatically attach authorization Bearer token
API.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("admin_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface LeadProfile {
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  country: string;
  budget: string;
  payment_method: string;
  timeline: string;
  purpose: string;
  property_interest?: string;
}

export const api = {
  // Fetch property items
  async getProperties() {
    try {
      const response = await API.get("/properties");
      return response.data;
    } catch (err) {
      console.error("Error fetching properties", err);
      throw err;
    }
  },

  // Fetch luxury communities dossiers
  async getCommunities() {
    try {
      const response = await API.get("/communities");
      return response.data;
    } catch (err) {
      console.error("Error fetching communities list", err);
      throw err;
    }
  },

  // Authorize administrator session
  async login(payload: any) {
    try {
      const response = await API.post("/login", payload);
      if (response.data.access_token) {
        localStorage.setItem("admin_token", response.data.access_token);
        localStorage.setItem("admin_user", response.data.username);
      }
      return response.data;
    } catch (err) {
      console.error("Error logging in administrator session", err);
      throw err;
    }
  },

  // Post chat conversation logs
  async sendChatMessage(messages: ChatMessage[], currentLead: LeadProfile) {
    try {
      const response = await API.post("/chat", { messages, current_lead: currentLead });
      return response.data;
    } catch (err) {
      console.error("Error sending chat message", err);
      throw err;
    }
  },

  // Save qualified BANT details
  async saveLead(leadData: LeadProfile & { chat_transcript: ChatMessage[] }) {
    try {
      const response = await API.post("/leads", leadData);
      return response.data;
    } catch (err) {
      console.error("Error saving lead profile", err);
      throw err;
    }
  },

  // Direct sync client profile to Google Sheets
  async syncToGoogle(leadData: LeadProfile) {
    try {
      const response = await API.post("/google-sync", leadData);
      return response.data;
    } catch (err) {
      console.error("Error syncing lead to Google Sheets", err);
      throw err;
    }
  },

  // Retrieve lead profiles list
  async getLeads() {
    try {
      const response = await API.get("/leads");
      return response.data;
    } catch (err) {
      console.error("Error getting leads pipeline", err);
      throw err;
    }
  },

  // Update lead CRM stage status
  async updateLeadStatus(id: number, status: string) {
    try {
      const response = await API.post("/leads/status", { id, status });
      return response.data;
    } catch (err) {
      console.error("Error updating lead status", err);
      throw err;
    }
  },

  // Get Google Sheets sync configuration status
  async getSheetsStatus() {
    try {
      const response = await API.get("/sheets/status");
      return response.data;
    } catch (err) {
      console.error("Error checking sheets status", err);
      throw err;
    }
  },

  // Update Sheets API integration key configurations
  async updateSettings(settings: Record<string, string>) {
    try {
      const response = await API.post("/settings", settings);
      return response.data;
    } catch (err) {
      console.error("Error saving settings config", err);
      throw err;
    }
  },

  async exportPDFTranscript(leadId: number) {
    try {
      const response = await API.get(`/leads/${leadId}/pdf`, {
        responseType: "blob"
      });
      const blob = new Blob([response.data], { type: "application/pdf" });
      const url = URL.createObjectURL(blob);
      const downloadAnchor = document.createElement("a");
      downloadAnchor.href = url;
      downloadAnchor.download = `Panache_Homes_Report_${leadId}.pdf`;
      downloadAnchor.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Error exporting transcript PDF", err);
      throw err;
    }
  }
};
