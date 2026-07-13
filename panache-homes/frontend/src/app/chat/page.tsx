"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";
import { MessageSquare, Plus, Search, Send, ShieldAlert, Sparkles, Home, ArrowLeft, Download } from "lucide-react";
import { Avatar } from "@/components/ui/Avatar";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { Badge } from "@/components/ui/Badge";
import { api, ChatMessage, LeadProfile } from "@/lib/api";

interface ExtendedMessage {
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<ExtendedMessage[]>([
    { role: "assistant", content: "Welcome to Panache Homes.", timestamp: "Just now" },
    { role: "assistant", content: "🏙️ Dubai Property Investment Assistant", timestamp: "Just now" },
    { role: "assistant", content: "Hello! I am your AI Property Advisor. I can help you find high-yielding off-plan and secondary market opportunities. To start, may I have your name and email?", timestamp: "Just now" }
  ]);

  const [currentLead, setCurrentLead] = useState<LeadProfile>({
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    country: "",
    budget: "",
    payment_method: "",
    timeline: "",
    purpose: "",
    property_interest: ""
  });

  const [grade, setGrade] = useState<string>("C");
  const [isComplete, setIsComplete] = useState<boolean>(false);
  const [summary, setSummary] = useState<string>("");
  const [emailDraft, setEmailDraft] = useState<string>("");
  const [leadId, setLeadId] = useState<number | null>(null);

  const [inputVal, setInputVal] = useState("");
  const [searchVal, setSearchVal] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  const mockConversations = [
    { title: "Burj Khalifa Yields", date: "Today" },
    { title: "Dubai Hills Golf Villa", date: "Yesterday" },
    { title: "Golden Visa AED 2M+", date: "3 days ago" }
  ];

  const suggestedPrompts = [
    "Golden Visa rules for AED 2M+",
    "Payment plans for Palm Jumeirah",
    "Average ROI in Dubai Marina"
  ];

  // 1. Persistent session loading on mount
  useEffect(() => {
    if (typeof window !== "undefined") {
      const savedMessages = localStorage.getItem("chat_messages");
      if (savedMessages) setMessages(JSON.parse(savedMessages));
      
      const savedLead = localStorage.getItem("chat_lead");
      if (savedLead) setCurrentLead(JSON.parse(savedLead));
      
      const savedGrade = localStorage.getItem("chat_grade");
      if (savedGrade) setGrade(savedGrade);
      
      const savedComplete = localStorage.getItem("chat_complete");
      if (savedComplete) setIsComplete(savedComplete === "true");
      
      const savedSummary = localStorage.getItem("chat_summary");
      if (savedSummary) setSummary(savedSummary);
      
      const savedEmail = localStorage.getItem("chat_email");
      if (savedEmail) setEmailDraft(savedEmail);

      const savedLeadId = localStorage.getItem("chat_lead_id");
      if (savedLeadId) setLeadId(parseInt(savedLeadId, 10));
    }
  }, []);

  // 2. Persistent session saving on update
  useEffect(() => {
    if (typeof window !== "undefined") {
      localStorage.setItem("chat_messages", JSON.stringify(messages));
      localStorage.setItem("chat_lead", JSON.stringify(currentLead));
      localStorage.setItem("chat_grade", grade);
      localStorage.setItem("chat_complete", String(isComplete));
      localStorage.setItem("chat_summary", summary);
      localStorage.setItem("chat_email", emailDraft);
      if (leadId) {
        localStorage.setItem("chat_lead_id", String(leadId));
      } else {
        localStorage.removeItem("chat_lead_id");
      }
    }
  }, [messages, currentLead, grade, isComplete, summary, emailDraft, leadId]);

  // 3. Handle redirected property or community greeting context
  useEffect(() => {
    if (typeof window !== "undefined") {
      const selectedComm = sessionStorage.getItem("selected_community");
      const selectedProp = sessionStorage.getItem("selected_property");
      
      let welcomeMsg = "";
      if (selectedComm) {
        welcomeMsg = `I see you're interested in ${selectedComm}. I can help you with ROI, Golden Visa eligibility, payment plans, community information, and rental yields in this area. To get started, could you share your name and email?`;
        setCurrentLead(prev => ({ ...prev, property_interest: selectedComm }));
        sessionStorage.removeItem("selected_community");
      } else if (selectedProp) {
        welcomeMsg = `I see you're interested in ${selectedProp}. I can help you with ROI, Golden Visa eligibility, payment plans, community information, and rental yields for this listing. To get started, could you share your name and email?`;
        setCurrentLead(prev => ({ ...prev, property_interest: selectedProp }));
        sessionStorage.removeItem("selected_property");
      }

      if (welcomeMsg) {
        const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: welcomeMsg, timestamp: timeStr }
        ]);
      }
    }
  }, []);

  const getProgress = () => {
    const fields = ["first_name", "country", "budget", "payment_method", "timeline", "purpose"];
    const filled = fields.filter(f => !!(currentLead as any)[f]).length;
    return Math.round((filled / fields.length) * 100);
  };

  const qualificationFields = [
    { name: "Name", value: currentLead.first_name || "Waiting..." },
    { name: "Country", value: currentLead.country || "Waiting..." },
    { name: "Budget", value: currentLead.budget || "Waiting..." },
    { name: "Payment Method", value: currentLead.payment_method || "Waiting..." },
    { name: "Timeline", value: currentLead.timeline || "Waiting..." },
    { name: "Purpose", value: currentLead.purpose || "Waiting..." }
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputVal.trim()) return;

    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const userMsg = { role: "user" as const, content: inputVal, timestamp: timeStr };
    const newMsgs = [...messages, userMsg];
    setMessages(newMsgs);
    setInputVal("");
    setIsTyping(true);

    try {
      // Send chat history and current lead to FastAPI backend
      const payloadMessages = newMsgs.map(m => ({ role: m.role, content: m.content, timestamp: m.timestamp }));
      const res = await api.sendChatMessage(payloadMessages, currentLead);
      
      setIsTyping(false);
      const resTimeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      setMessages(prev => [...prev, { role: "assistant", content: res.reply, timestamp: resTimeStr }]);
      
      if (res.current_lead) {
        setCurrentLead(res.current_lead);
      }
      if (res.grade) {
        setGrade(res.grade);
      }
      if (res.qualification_complete !== undefined) {
        setIsComplete(res.qualification_complete);
      }
      if (res.summary) {
        setSummary(res.summary);
      }
      if (res.email_draft) {
        setEmailDraft(res.email_draft);
      }

      // Auto-save qualified lead upon BANT completion
      if (res.qualification_complete) {
        const saveRes = await api.saveLead({
          ...res.current_lead,
          chat_transcript: [...payloadMessages, { role: "assistant", content: res.reply, timestamp: resTimeStr }]
        });
        if (saveRes && saveRes.lead_id) {
          setLeadId(saveRes.lead_id);
        }
      }
    } catch (err) {
      setIsTyping(false);
      const errTimeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      setMessages(prev => [...prev, { role: "assistant", content: "I apologize, I ran into an error connecting to our system.", timestamp: errTimeStr }]);
    }
  };

  const handleResetSession = () => {
    setMessages([
      { role: "assistant", content: "Welcome to Panache Homes.", timestamp: "Just now" },
      { role: "assistant", content: "🏙️ Dubai Property Investment Assistant", timestamp: "Just now" },
      { role: "assistant", content: "Hello! I am your AI Property Advisor. I can help you find high-yielding off-plan and secondary market opportunities. To start, may I have your name and email?", timestamp: "Just now" }
    ]);
    setCurrentLead({
      first_name: "", last_name: "", email: "", phone: "",
      country: "", budget: "", payment_method: "", timeline: "", purpose: ""
    });
    setGrade("C");
    setIsComplete(false);
    setSummary("");
    setEmailDraft("");
    setLeadId(null);
    if (typeof window !== "undefined") {
      localStorage.removeItem("chat_messages");
      localStorage.removeItem("chat_lead");
      localStorage.removeItem("chat_grade");
      localStorage.removeItem("chat_complete");
      localStorage.removeItem("chat_summary");
      localStorage.removeItem("chat_email");
      localStorage.removeItem("chat_lead_id");
    }
  };

  return (
    <div className="flex h-screen bg-background overflow-hidden text-foreground">
      {/* 1. Left Sidebar: History Panel */}
      <aside className="w-72 border-r border-border bg-card flex flex-col h-full shrink-0">
        <div className="p-4 border-b border-border flex flex-col gap-3">
          <Button variant="outline" className="w-full flex items-center justify-start gap-2 border-dashed" onClick={handleResetSession}>
            <Plus className="w-4 h-4" /> New Consultation
          </Button>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted" />
            <input
              type="text"
              placeholder="Search history..."
              value={searchVal}
              onChange={(e) => setSearchVal(e.target.value)}
              className="w-full pl-9 pr-4 py-2 bg-muted/30 border border-border rounded-lg text-xs focus:outline-none focus:ring-1 focus:ring-accent"
            />
          </div>
        </div>
        
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          <div className="text-[10px] font-bold text-muted uppercase tracking-wider">Consultations</div>
          <div className="space-y-1">
            {mockConversations.map((chat, idx) => (
              <button key={idx} className="w-full flex items-center gap-3 p-3 rounded-lg text-left text-xs font-semibold hover:bg-muted/50 transition-colors cursor-pointer">
                <MessageSquare className="w-4 h-4 text-accent" />
                <div className="truncate flex-1">
                  <div className="truncate text-primary">{chat.title}</div>
                  <span className="text-[9px] text-muted">{chat.date}</span>
                </div>
              </button>
            ))}
          </div>
        </div>
      </aside>

      {/* 2. Main Chat Column */}
      <main className="flex-1 flex flex-col h-full bg-background relative">
        {/* Sticky Header */}
        <header className="h-16 border-b border-border bg-card/85 backdrop-blur-md px-6 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <Link href="/" className="p-1.5 rounded hover:bg-muted text-muted transition-colors">
              <ArrowLeft className="w-4 h-4" />
            </Link>
            <div>
              <h2 className="font-extrabold text-sm tracking-wide text-primary">🏢 PANACHE HOMES</h2>
              <span className="text-[10px] text-green-500 flex items-center gap-1 font-bold">
                <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse"></span> AI Online
              </span>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="sm" onClick={handleResetSession} className="text-xs">
              Reset Session
            </Button>
            <Link href="/">
              <Button variant="outline" size="sm" className="text-xs flex items-center gap-1.5">
                <Home className="w-3.5 h-3.5" /> Landing Page
              </Button>
            </Link>
          </div>
        </header>

        {/* Message container */}
        <div className="flex-1 overflow-y-auto p-8 space-y-6">
          <div className="max-w-3xl mx-auto space-y-6">
            {messages.map((msg, idx) => {
              const isAi = msg.role === "assistant";
              return (
                <div key={idx} className={`flex gap-4 ${isAi ? "justify-start" : "justify-end"}`}>
                  {isAi && <Avatar fallback="AI" className="bg-primary text-primary-foreground border-accent" />}
                  <div className="flex flex-col gap-1 max-w-[80%]">
                    <div className={`p-4 rounded-2xl text-sm leading-relaxed shadow-sm ${
                      isAi 
                        ? "bg-card border border-border text-foreground" 
                        : "bg-primary text-primary-foreground"
                    }`}>
                      {msg.content}
                    </div>
                    <span className={`text-[9px] text-muted font-bold block ${isAi ? "text-left" : "text-right"}`}>
                      {msg.timestamp}
                    </span>
                  </div>
                  {!isAi && <Avatar fallback="US" className="bg-accent text-accent-foreground" />}
                </div>
              );
            })}
            
            {/* Typing Indicator */}
            {isTyping && (
              <div className="flex gap-4 justify-start animate-pulse">
                <Avatar fallback="AI" className="bg-primary text-primary-foreground" />
                <div className="bg-card border border-border p-4 rounded-2xl flex items-center gap-1">
                  <span className="w-2 h-2 bg-accent rounded-full animate-bounce"></span>
                  <span className="w-2 h-2 bg-accent rounded-full animate-bounce [animation-delay:0.2s]"></span>
                  <span className="w-2 h-2 bg-accent rounded-full animate-bounce [animation-delay:0.4s]"></span>
                </div>
              </div>
            )}

            {/* Qualified Lead summary card */}
            {isComplete && (
              <Card className="p-6 border-accent bg-accent/5 max-w-2xl mx-auto space-y-4 animate-in fade-in zoom-in duration-300">
                <h3 className="font-extrabold text-sm text-accent">🎉 Consultation Qualified</h3>
                <p className="text-xs text-muted leading-relaxed">{summary || "Lead successfully graded and synced to Google Sheets CRM."}</p>
                {emailDraft && (
                  <div className="bg-card border border-border p-4 rounded-lg text-[11px] font-semibold text-primary overflow-x-auto max-h-40 overflow-y-auto mb-2">
                    <pre className="whitespace-pre-wrap">{emailDraft}</pre>
                  </div>
                )}
                {leadId && (
                  <Button 
                    onClick={() => api.exportPDFTranscript(leadId)} 
                    className="w-full py-3.5 text-xs font-bold tracking-wide flex items-center justify-center gap-1.5"
                  >
                    <Download className="w-4 h-4" /> Export Advisory Report (PDF)
                  </Button>
                )}
              </Card>
            )}
          </div>
        </div>

        {/* Input box section */}
        <div className="p-6 border-t border-border bg-card/85 backdrop-blur-md shrink-0">
          <div className="max-w-3xl mx-auto flex flex-col gap-4">
            {/* Suggested Prompts */}
            <div className="flex flex-wrap gap-2 justify-center">
              {suggestedPrompts.map((prompt) => (
                <button
                  key={prompt}
                  onClick={() => setInputVal(prompt)}
                  className="px-3.5 py-1.5 bg-muted/40 border border-border rounded-full text-xs font-semibold text-muted hover:bg-muted/80 transition-all cursor-pointer"
                >
                  💡 {prompt}
                </button>
              ))}
            </div>
            
            <form onSubmit={handleSubmit} className="relative flex items-center">
              <input
                type="text"
                value={inputVal}
                onChange={(e) => setInputVal(e.target.value)}
                placeholder="Ask about properties, yields, or Golden Visa regulations..."
                className="w-full pl-6 pr-14 py-4 bg-background border border-border rounded-2xl text-sm focus:outline-none focus:ring-1 focus:ring-accent shadow-sm"
              />
              <button
                type="submit"
                className="absolute right-4 p-2 bg-primary text-primary-foreground rounded-xl hover:opacity-90 transition-opacity cursor-pointer"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>
          </div>
        </div>
      </main>

      {/* 3. Right Sidebar: BANT & Lead Profile */}
      <aside className="w-80 border-l border-border bg-card flex flex-col h-full shrink-0 p-6 overflow-y-auto space-y-6">
        <div>
          <h3 className="font-extrabold text-sm text-primary mb-3">Lead Qualification Progress</h3>
          <ProgressBar value={getProgress()} className="mb-2" />
          <span className="text-[10px] text-muted block text-right font-semibold">{getProgress()}% Completed</span>
        </div>

        <div className="space-y-4">
          <div className="text-[10px] font-bold text-muted uppercase tracking-wider">Captured Attributes</div>
          <div className="space-y-3 bg-muted/15 p-4 rounded-xl border border-border/30">
            {qualificationFields.map((field, idx) => (
              <div key={idx} className="flex justify-between items-center text-xs pb-1.5 border-b border-border/30 last:border-0 last:pb-0">
                <span className="text-muted">{field.name}</span>
                <span className={`font-extrabold ${field.value === "Waiting..." ? "text-muted" : "text-primary"}`}>{field.value}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="p-5 bg-accent/15 border border-accent/20 rounded-xl text-center space-y-1">
          <span className="text-[9px] text-accent font-extrabold uppercase tracking-wider block">BANT Grading</span>
          <span className="text-4xl font-extrabold text-accent block">Grade {grade}</span>
        </div>

        {/* Grade A Payment Schedule Breakdown */}
        {grade === "A" && (() => {
          const budgetVal = (() => {
            const digits = currentLead.budget.replace(/[^0-9]/g, "");
            return digits ? parseFloat(digits) : 0;
          })();
          const bookingVal = budgetVal * 0.20;
          const remainingVal = budgetVal * 0.80;
          
          if (budgetVal > 0) {
            return (
              <Card className="p-4 border-accent bg-accent/5 space-y-3 text-xs animate-in fade-in duration-300">
                <h4 className="font-extrabold text-accent text-[11px] uppercase tracking-wide flex items-center gap-1.5">
                  💰 Instalment Schedule
                </h4>
                <div className="space-y-2 font-semibold">
                  <div className="flex justify-between border-b border-border/40 pb-1.5 text-[10px]">
                    <span className="text-muted">Total Budget</span>
                    <span className="text-primary">AED {budgetVal.toLocaleString()} (${Math.round(budgetVal/3.6725).toLocaleString()})</span>
                  </div>
                  <div className="flex justify-between border-b border-border/40 pb-1.5 text-[10px] text-accent">
                    <span>20% Booking</span>
                    <span>AED {bookingVal.toLocaleString()} (${Math.round(bookingVal/3.6725).toLocaleString()})</span>
                  </div>
                  <div className="flex justify-between text-[10px] text-muted">
                    <span>80% Balance</span>
                    <span>AED {remainingVal.toLocaleString()} (${Math.round(remainingVal/3.6725).toLocaleString()})</span>
                  </div>
                </div>
              </Card>
            );
          }
          return null;
        })()}

        {/* Property & Yield Details */}
        <Card className="p-5 border-border bg-card space-y-4">
          <div>
            <span className="text-[9px] text-accent font-extrabold uppercase tracking-wider block mb-1">Target Yields</span>
            <h4 className="font-extrabold text-sm text-primary">Dubai Hills Estate</h4>
          </div>
          <div className="grid grid-cols-2 gap-3 text-xs">
            <div className="bg-muted/10 p-2.5 rounded-lg">
              <span className="text-[9px] text-muted block">Projected ROI</span>
              <span className="font-bold text-primary">7.8% Annually</span>
            </div>
            <div className="bg-muted/10 p-2.5 rounded-lg">
              <span className="text-[9px] text-muted block">DLD Fee Split</span>
              <span className="font-bold text-primary">4% Land Registry</span>
            </div>
          </div>
        </Card>
      </aside>
    </div>
  );
}
