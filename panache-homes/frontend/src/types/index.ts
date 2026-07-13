export interface Property {
  id: string;
  title: string;
  community: string;
  price: string;
  roi: string;
  desc: string;
  img: string;
}

export interface LeadData {
  first_name?: string;
  last_name?: string;
  email?: string;
  phone?: string;
  budget?: string;
  property_interest?: string;
  payment_method?: string;
  timeline?: string;
  purpose?: string;
  country?: string;
  grade?: "A" | "B" | "C" | "D" | "";
  ai_summary?: string;
  created_at?: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}
