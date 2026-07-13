"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Users, FileSpreadsheet, Settings, BarChart3, ArrowLeft, RefreshCw, CheckCircle, Shield, Download, Mail, Copy, Search, ArrowUpDown, ChevronLeft, ChevronRight, Activity, Database, Key, MessageCircle, CheckCircle2, XCircle, MessageSquare } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Input } from "@/components/ui/Input";
import { Textarea } from "@/components/ui/Textarea";
import { Drawer } from "@/components/ui/Drawer";
import { api } from "@/lib/api";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from "recharts";

export default function DashboardPage() {
  const router = useRouter();
  const [adminUser, setAdminUser] = useState("");
  const [activeTab, setActiveTab] = useState<"leads" | "analytics" | "settings">("leads");
  const [sheetsUrl, setSheetsUrl] = useState("");
  const [sheetsCreds, setSheetsCreds] = useState('{\n  "type": "service_account",\n  "project_id": "panache-homes-crm"\n}');
  const [leads, setLeads] = useState<any[]>([]);
  const [sheetsConfigured, setSheetsConfigured] = useState(false);
  const [isEditingConfig, setIsEditingConfig] = useState(false);
  const [loading, setLoading] = useState(true);

  // Search & Filter & Sort state
  const [searchQuery, setSearchQuery] = useState("");
  const [gradeFilter, setGradeFilter] = useState("All");
  const [statusFilter, setStatusFilter] = useState("All");
  const [sortField, setSortField] = useState("created_at");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");

  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  // Selected lead drawer details
  const [selectedLead, setSelectedLead] = useState<any | null>(null);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  const loadData = async () => {
    try {
      setLoading(true);
      const leadsList = await api.getLeads();
      setLeads(leadsList);
      
      const sheetsStatus = await api.getSheetsStatus();
      setSheetsConfigured(sheetsStatus.configured);
      if (sheetsStatus.url) {
        setSheetsUrl(sheetsStatus.url);
      }
      setIsEditingConfig(!sheetsStatus.configured);
      setLoading(false);
    } catch (err) {
      setLoading(false);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem("admin_token");
    const user = localStorage.getItem("admin_user");
    if (!token) {
      router.push("/login");
    } else {
      setAdminUser(user || "admin@panachehomes.ae");
      loadData();
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("admin_token");
    localStorage.removeItem("admin_user");
    // Clear cookie to trigger Next.js Middleware redirect
    document.cookie = "admin_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
  };

  const handleSaveSettings = async () => {
    try {
      await api.updateSettings({
        google_sheets_url: sheetsUrl,
        google_sheets_creds: sheetsCreds
      });
      alert("Google Sheets settings saved successfully!");
      loadData();
    } catch (err) {
      alert("Failed to save settings");
    }
  };

  const handleUpdateStatus = async (id: number, status: string) => {
    try {
      await api.updateLeadStatus(id, status);
      loadData();
      if (selectedLead && selectedLead.id === id) {
        setSelectedLead((prev: any) => ({ ...prev, status }));
      }
    } catch (err) {
      alert("Failed to update status");
    }
  };

  const handleCopyEmail = (text: string) => {
    navigator.clipboard.writeText(text);
    alert("Outreach email copied to clipboard!");
  };

  const handleCopyWhatsApp = (lead: any) => {
    const msg = `Hello ${lead.first_name}, thank you for consulting with Panache Homes. I have prepared your Dubai Property Consultation Report. We have identified excellent options matching your budget of ${lead.budget} AED. Let's schedule a call to discuss the project allocation.`;
    navigator.clipboard.writeText(msg);
    alert("WhatsApp outreach message copied to clipboard!");
  };

  const getGradeCount = (g: string) => {
    return leads.filter(l => l.grade === g).length;
  };

  // Check if lead was created today
  const isToday = (dateStr: string) => {
    if (!dateStr) return false;
    const date = new Date(dateStr);
    const today = new Date();
    return date.getDate() === today.getDate() &&
           date.getMonth() === today.getMonth() &&
           date.getFullYear() === today.getFullYear();
  };

  const todaysLeadsCount = leads.filter(l => isToday(l.created_at)).length;

  // Sorting helper
  const handleSort = (field: string) => {
    if (sortField === field) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortOrder("asc");
    }
  };

  // Filter & Sort leads list
  const filteredLeads = leads
    .filter((lead) => {
      const matchesSearch = 
        `${lead.first_name} ${lead.last_name}`.toLowerCase().includes(searchQuery.toLowerCase()) ||
        lead.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (lead.country && lead.country.toLowerCase().includes(searchQuery.toLowerCase()));
      
      const matchesGrade = gradeFilter === "All" || lead.grade === gradeFilter;
      const matchesStatus = statusFilter === "All" || lead.status === statusFilter;

      return matchesSearch && matchesGrade && matchesStatus;
    })
    .sort((a, b) => {
      let valA = a[sortField] || "";
      let valB = b[sortField] || "";
      
      if (typeof valA === "string") valA = valA.toLowerCase();
      if (typeof valB === "string") valB = valB.toLowerCase();

      if (valA < valB) return sortOrder === "asc" ? -1 : 1;
      if (valA > valB) return sortOrder === "asc" ? 1 : -1;
      return 0;
    });

  // Pagination calculation
  const totalPages = Math.ceil(filteredLeads.length / itemsPerPage);
  const paginatedLeads = filteredLeads.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  // Recharts Analytics Datasets
  const gradeDistributionData = [
    { name: "Grade A", value: getGradeCount("A"), color: "#C9A227" },
    { name: "Grade B", value: getGradeCount("B"), color: "#0F172A" },
    { name: "Grade C", value: getGradeCount("C"), color: "#64748B" },
    { name: "Grade D", value: getGradeCount("D"), color: "#CBD5E1" }
  ].filter(item => item.value > 0);

  const syncStatusData = [
    { name: "Synced", count: leads.filter(l => l.synced_to_sheets).length },
    { name: "Local Only", count: leads.filter(l => !l.synced_to_sheets).length }
  ];

  const cleanBudgetNumericForFront = (budgetStr: string) => {
    const cleaned = budgetStr.replace(/[^\d\.]/g, "");
    if (!cleaned) return 0;
    const val = parseFloat(cleaned);
    if (val < 100) return val * 1000000;
    return val;
  };

  const getDailyLeadsData = () => {
    const counts: Record<string, number> = {};
    leads.forEach(l => {
      if (l.created_at) {
        try {
          const date = new Date(l.created_at).toLocaleDateString(undefined, { month: "short", day: "numeric" });
          counts[date] = (counts[date] || 0) + 1;
        } catch (e) {}
      }
    });
    return Object.entries(counts).map(([name, count]) => ({ name, count }));
  };

  const getMonthlyLeadsData = () => {
    const counts: Record<string, number> = {};
    leads.forEach(l => {
      if (l.created_at) {
        try {
          const month = new Date(l.created_at).toLocaleString(undefined, { month: "short", year: "2-digit" });
          counts[month] = (counts[month] || 0) + 1;
        } catch (e) {}
      }
    });
    return Object.entries(counts).map(([name, count]) => ({ name, count }));
  };

  const getCountryData = () => {
    const counts: Record<string, number> = {};
    leads.forEach(l => {
      const country = l.country || "Unknown";
      counts[country] = (counts[country] || 0) + 1;
    });
    return Object.entries(counts).map(([name, count]) => ({ name, count })).sort((a,b) => b.count - a.count);
  };

  const getBudgetData = () => {
    const counts = { "Below 2M": 0, "2M - 5M": 0, "Above 5M": 0, "Unconfirmed": 0 };
    leads.forEach(l => {
      const raw = l.budget || "";
      if (raw.toLowerCase().includes("unconfirmed")) {
        counts["Unconfirmed"]++;
      } else {
        const val = cleanBudgetNumericForFront(raw);
        if (val === 0) {
          counts["Unconfirmed"]++;
        } else if (val < 2000000) {
          counts["Below 2M"]++;
        } else if (val <= 5000000) {
          counts["2M - 5M"]++;
        } else {
          counts["Above 5M"]++;
        }
      }
    });
    return Object.entries(counts).map(([name, count]) => ({ name, count }));
  };

  const getPaymentData = () => {
    const counts: Record<string, number> = {};
    leads.forEach(l => {
      const method = l.payment_method || "Flexible";
      counts[method] = (counts[method] || 0) + 1;
    });
    return Object.entries(counts).map(([name, count]) => ({ name, count }));
  };

  const getPurposeData = () => {
    const counts: Record<string, number> = {};
    leads.forEach(l => {
      const purpose = l.purpose || "Flexible";
      counts[purpose] = (counts[purpose] || 0) + 1;
    });
    return Object.entries(counts).map(([name, count]) => ({ name, count }));
  };

  return (
    <div className="min-h-screen bg-background flex flex-col text-foreground">
      {/* Sticky Header */}
      <header className="h-16 border-b border-border bg-card/85 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <Link href="/" className="p-1.5 rounded hover:bg-muted text-muted transition-colors">
            <ArrowLeft className="w-4 h-4" />
          </Link>
          <div>
            <h2 className="font-extrabold text-sm tracking-wide text-primary">PANACHE HOMES</h2>
            <span className="text-[10px] text-muted flex items-center gap-1.5 font-bold uppercase tracking-wider">
              <Shield className="w-3 h-3 text-accent" /> Portal: {adminUser}
            </span>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <Badge variant="secondary" className="px-3 py-1 flex items-center gap-1.5 text-[10px] font-bold">
            {sheetsConfigured ? (
              <>
                <CheckCircle className="w-3 h-3 text-emerald-500" /> Active Sync
              </>
            ) : (
              <>
                <span className="w-1.5 h-1.5 rounded-full bg-amber-500"></span> Local Offline
              </>
            )}
          </Badge>
          <Link href="/login">
            <Button variant="outline" size="sm" onClick={handleLogout} className="text-xs">Log Out</Button>
          </Link>
        </div>
      </header>

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-6 py-8 space-y-8">
        {/* Analytics summary cards */}
        <section className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <Card className="p-6">
            <div className="text-xs text-muted mb-2 font-bold uppercase tracking-wider flex justify-between items-center">
              Total Leads <Users className="w-4 h-4 text-accent" />
            </div>
            <div className="text-3xl font-extrabold text-primary">{leads.length}</div>
          </Card>
          <Card className="p-6">
            <div className="text-xs text-muted mb-2 font-bold uppercase tracking-wider flex justify-between items-center">
              Today's Leads <Activity className="w-4 h-4 text-accent animate-pulse" />
            </div>
            <div className="text-3xl font-extrabold text-primary">{todaysLeadsCount}</div>
          </Card>
          <Card className="p-6">
            <div className="text-xs text-muted mb-2 font-bold uppercase tracking-wider flex justify-between items-center">
              Grade A Profiles <Shield className="w-4 h-4 text-accent" />
            </div>
            <div className="text-3xl font-extrabold text-primary">{getGradeCount("A")}</div>
          </Card>
          <Card className="p-6">
            <div className="text-xs text-muted mb-2 font-bold uppercase tracking-wider flex justify-between items-center">
              Google Sheets <FileSpreadsheet className="w-4 h-4 text-accent" />
            </div>
            <div className={`text-3xl font-extrabold ${sheetsConfigured ? "text-green-500" : "text-rose-500"}`}>
              {sheetsConfigured ? "🟢 Connected" : "🔴 Not Linked"}
            </div>
          </Card>
        </section>

        {/* Tab Controls */}
        <div className="flex border-b border-border gap-6">
          <button
            onClick={() => setActiveTab("leads")}
            className={`pb-3 text-sm font-bold flex items-center gap-2 border-b-2 transition-all cursor-pointer ${
              activeTab === "leads" ? "border-accent text-accent" : "border-transparent text-muted hover:text-primary"
            }`}
          >
            <Users className="w-4 h-4" /> Leads Pipeline
          </button>
          <button
            onClick={() => setActiveTab("analytics")}
            className={`pb-3 text-sm font-bold flex items-center gap-2 border-b-2 transition-all cursor-pointer ${
              activeTab === "analytics" ? "border-accent text-accent" : "border-transparent text-muted hover:text-primary"
            }`}
          >
            <BarChart3 className="w-4 h-4" /> CRM Analytics
          </button>
          <button
            onClick={() => setActiveTab("settings")}
            className={`pb-3 text-sm font-bold flex items-center gap-2 border-b-2 transition-all cursor-pointer ${
              activeTab === "settings" ? "border-accent text-accent" : "border-transparent text-muted hover:text-primary"
            }`}
          >
            <Settings className="w-4 h-4" /> Integrations & Settings
          </button>
        </div>

        {/* Tab Contents */}
        <section className="min-h-[400px]">
          {activeTab === "leads" && (
            <Card className="border border-border shadow-sm overflow-hidden space-y-4">
              <div className="p-6 border-b border-border flex justify-between items-center flex-wrap gap-4 bg-muted/10">
                <h3 className="font-extrabold text-base text-primary">Qualified Client Profiles</h3>
                <Button variant="outline" size="sm" className="text-xs flex items-center gap-1.5" onClick={loadData}>
                  <RefreshCw className="w-3.5 h-3.5" /> Refresh List
                </Button>
              </div>

              {/* Filters Panel */}
              <div className="px-6 py-2 grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted" />
                  <Input 
                    placeholder="Search name, country..."
                    value={searchQuery}
                    onChange={(e) => { setSearchQuery(e.target.value); setCurrentPage(1); }}
                    className="pl-9 text-xs"
                  />
                </div>
                
                <select 
                  value={gradeFilter}
                  onChange={(e) => { setGradeFilter(e.target.value); setCurrentPage(1); }}
                  className="bg-card border border-border text-xs p-2 rounded-lg font-semibold cursor-pointer focus:outline-none focus:ring-1 focus:ring-accent"
                >
                  <option value="All">All Grades</option>
                  <option value="A">Grade A</option>
                  <option value="B">Grade B</option>
                  <option value="C">Grade C</option>
                  <option value="D">Grade D</option>
                </select>

                <select 
                  value={statusFilter}
                  onChange={(e) => { setStatusFilter(e.target.value); setCurrentPage(1); }}
                  className="bg-card border border-border text-xs p-2 rounded-lg font-semibold cursor-pointer focus:outline-none focus:ring-1 focus:ring-accent"
                >
                  <option value="All">All Statuses</option>
                  <option value="New">New</option>
                  <option value="Contacted">Contacted</option>
                  <option value="Qualified">Qualified</option>
                </select>
              </div>

              {loading ? (
                <div className="p-12 text-center text-xs text-muted font-bold">Loading CRM Leads...</div>
              ) : filteredLeads.length === 0 ? (
                <div className="p-12 text-center text-xs text-muted font-bold">No leads matched filters.</div>
              ) : (
                <div className="space-y-4">
                  <div className="overflow-x-auto">
                    <table className="w-full text-left text-xs border-collapse">
                      <thead>
                        <tr className="bg-muted/30 border-b border-border/80 text-muted font-bold">
                          <th className="p-4 cursor-pointer hover:text-primary transition-colors" onClick={() => handleSort("first_name")}>
                            Name <ArrowUpDown className="inline w-3 h-3 ml-1" />
                          </th>
                          <th className="p-4 cursor-pointer hover:text-primary transition-colors" onClick={() => handleSort("country")}>
                            Country <ArrowUpDown className="inline w-3 h-3 ml-1" />
                          </th>
                          <th className="p-4 cursor-pointer hover:text-primary transition-colors" onClick={() => handleSort("budget")}>
                            Budget <ArrowUpDown className="inline w-3 h-3 ml-1" />
                          </th>
                          <th className="p-4">Payment</th>
                          <th className="p-4">Timeline</th>
                          <th className="p-4">Purpose</th>
                          <th className="p-4 text-center cursor-pointer hover:text-primary transition-colors" onClick={() => handleSort("grade")}>
                            Grade <ArrowUpDown className="inline w-3 h-3 ml-1" />
                          </th>
                          <th className="p-4 text-center">Sync Status</th>
                          <th className="p-4 text-right">Actions</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-border/50 font-semibold">
                        {paginatedLeads.map((lead) => (
                          <tr 
                            key={lead.id} 
                            onClick={() => { setSelectedLead(lead); setIsDrawerOpen(true); }}
                            className="hover:bg-muted/10 transition-colors cursor-pointer"
                          >
                            <td className="p-4">
                              <div className="font-bold text-primary">{lead.first_name} {lead.last_name}</div>
                              <span className="text-[10px] text-muted block">{lead.email}</span>
                            </td>
                            <td className="p-4">{lead.country}</td>
                            <td className="p-4 text-accent">{lead.budget}</td>
                            <td className="p-4">{lead.payment_method}</td>
                            <td className="p-4">{lead.timeline}</td>
                            <td className="p-4">{lead.purpose}</td>
                            <td className="p-4 text-center">
                              <Badge variant={lead.grade === "A" ? "secondary" : "outline"} className="px-2 py-0.5 text-[10px]">
                                Grade {lead.grade}
                              </Badge>
                            </td>
                            <td className="p-4 text-center">
                              <span className={lead.synced_to_sheets ? "text-emerald-500" : "text-amber-500"}>
                                {lead.synced_to_sheets ? "Synced" : "Local"}
                              </span>
                            </td>
                            <td className="p-4 text-right space-x-2" onClick={(e) => e.stopPropagation()}>
                              <select 
                                value={lead.status} 
                                onChange={(e) => handleUpdateStatus(lead.id, e.target.value)}
                                className="bg-card border border-border text-[10px] p-1 rounded font-bold cursor-pointer"
                              >
                                <option value="New">New</option>
                                <option value="Contacted">Contacted</option>
                                <option value="Qualified">Qualified</option>
                              </select>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>

                  {/* Pagination Actions */}
                  {totalPages > 1 && (
                    <div className="flex justify-between items-center p-4 border-t border-border bg-muted/5">
                      <span className="text-[10px] text-muted font-bold">Showing Page {currentPage} of {totalPages}</span>
                      <div className="flex gap-2">
                        <Button 
                          variant="outline" 
                          size="sm" 
                          disabled={currentPage === 1}
                          onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                          className="p-2"
                        >
                          <ChevronLeft className="w-4 h-4" />
                        </Button>
                        <Button 
                          variant="outline" 
                          size="sm" 
                          disabled={currentPage === totalPages}
                          onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                          className="p-2"
                        >
                          <ChevronRight className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </Card>
          )}

          {activeTab === "analytics" && (
            <div className="space-y-8 animate-in fade-in duration-300">
              {leads.length === 0 ? (
                <div className="p-16 text-center border border-dashed border-border rounded-2xl bg-card space-y-3">
                  <Activity className="w-8 h-8 text-accent mx-auto animate-pulse" />
                  <h4 className="font-extrabold text-sm text-primary">No Analytics Records Found</h4>
                  <p className="text-xs text-muted max-w-sm mx-auto font-semibold">
                    No lead records found in the database. When consultations are completed, client analytics will populate here.
                  </p>
                </div>
              ) : (
                <>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {/* 1. Grade Distribution PieChart */}
                    <Card className="p-6 space-y-4">
                      <h3 className="font-bold text-sm text-primary">BANT Grade Distribution</h3>
                      <div className="h-64 flex justify-center items-center">
                        <ResponsiveContainer width="100%" height="100%">
                          <PieChart>
                            <Pie
                              data={gradeDistributionData}
                              cx="50%"
                              cy="50%"
                              innerRadius={60}
                              outerRadius={80}
                              paddingAngle={5}
                              dataKey="value"
                            >
                              {gradeDistributionData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.color} />
                              ))}
                            </Pie>
                            <Tooltip formatter={(value) => [`${value} Leads`]} />
                            <Legend verticalAlign="bottom" height={36} />
                          </PieChart>
                        </ResponsiveContainer>
                      </div>
                    </Card>

                    {/* 2. Synced Status BarChart */}
                    <Card className="p-6 space-y-4">
                      <h3 className="font-bold text-sm text-primary">Google Sheets Integration Volume</h3>
                      <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart data={syncStatusData}>
                            <CartesianGrid strokeDasharray="3 3" vertical={false} />
                            <XAxis dataKey="name" stroke="#64748B" fontSize={10} tickLine={false} />
                            <YAxis stroke="#64748B" fontSize={10} tickLine={false} />
                            <Tooltip />
                            <Bar dataKey="count" fill="#C9A227" radius={[4, 4, 0, 0]} barSize={40} name="Total Leads" />
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                    </Card>

                    {/* 3. Daily Leads Trend LineChart */}
                    <Card className="p-6 space-y-4">
                      <h3 className="font-bold text-sm text-primary">Daily Leads Trend</h3>
                      <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                          <LineChart data={getDailyLeadsData()}>
                            <CartesianGrid strokeDasharray="3 3" vertical={false} />
                            <XAxis dataKey="name" stroke="#64748B" fontSize={10} tickLine={false} />
                            <YAxis stroke="#64748B" fontSize={10} tickLine={false} />
                            <Tooltip />
                            <Line type="monotone" dataKey="count" stroke="#C9A227" strokeWidth={2.5} dot={{ r: 4 }} name="Leads Captured" />
                          </LineChart>
                        </ResponsiveContainer>
                      </div>
                    </Card>

                    {/* 4. Monthly Leads Trend BarChart */}
                    <Card className="p-6 space-y-4">
                      <h3 className="font-bold text-sm text-primary">Monthly Leads Trend</h3>
                      <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart data={getMonthlyLeadsData()}>
                            <CartesianGrid strokeDasharray="3 3" vertical={false} />
                            <XAxis dataKey="name" stroke="#64748B" fontSize={10} tickLine={false} />
                            <YAxis stroke="#64748B" fontSize={10} tickLine={false} />
                            <Tooltip />
                            <Bar dataKey="count" fill="#0F172A" radius={[4, 4, 0, 0]} barSize={40} name="Leads Count" />
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                    </Card>

                    {/* 5. Country Distribution BarChart */}
                    <Card className="p-6 space-y-4">
                      <h3 className="font-bold text-sm text-primary">Country Distribution</h3>
                      <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart data={getCountryData()} layout="vertical">
                            <CartesianGrid strokeDasharray="3 3" horizontal={false} />
                            <XAxis type="number" stroke="#64748B" fontSize={10} tickLine={false} />
                            <YAxis type="category" dataKey="name" stroke="#64748B" fontSize={10} tickLine={false} />
                            <Tooltip />
                            <Bar dataKey="count" fill="#64748B" radius={[0, 4, 4, 0]} name="Leads Count" />
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                    </Card>

                    {/* 6. Budget Distribution BarChart */}
                    <Card className="p-6 space-y-4">
                      <h3 className="font-bold text-sm text-primary">Budget Distribution</h3>
                      <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart data={getBudgetData()}>
                            <CartesianGrid strokeDasharray="3 3" vertical={false} />
                            <XAxis dataKey="name" stroke="#64748B" fontSize={10} tickLine={false} />
                            <YAxis stroke="#64748B" fontSize={10} tickLine={false} />
                            <Tooltip />
                            <Bar dataKey="count" fill="#C9A227" radius={[4, 4, 0, 0]} name="Leads Count" />
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                    </Card>

                    {/* 7. Payment Method Distribution BarChart */}
                    <Card className="p-6 space-y-4">
                      <h3 className="font-bold text-sm text-primary">Payment Method Distribution</h3>
                      <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart data={getPaymentData()}>
                            <CartesianGrid strokeDasharray="3 3" vertical={false} />
                            <XAxis dataKey="name" stroke="#64748B" fontSize={10} tickLine={false} />
                            <YAxis stroke="#64748B" fontSize={10} tickLine={false} />
                            <Tooltip />
                            <Bar dataKey="count" fill="#0F172A" radius={[4, 4, 0, 0]} name="Leads Count" />
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                    </Card>

                    {/* 8. Purpose Distribution BarChart */}
                    <Card className="p-6 space-y-4">
                      <h3 className="font-bold text-sm text-primary">Purpose Distribution</h3>
                      <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart data={getPurposeData()}>
                            <CartesianGrid strokeDasharray="3 3" vertical={false} />
                            <XAxis dataKey="name" stroke="#64748B" fontSize={10} tickLine={false} />
                            <YAxis stroke="#64748B" fontSize={10} tickLine={false} />
                            <Tooltip />
                            <Bar dataKey="count" fill="#64748B" radius={[4, 4, 0, 0]} name="Leads Count" />
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                    </Card>
                  </div>

                  {/* 9. System Status & Health */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <Card className="p-5 flex items-center gap-4 border-border bg-card">
                      <div className="p-3 bg-emerald-50 rounded-xl text-emerald-500">
                        <Database className="w-5 h-5" />
                      </div>
                      <div>
                        <span className="text-[10px] text-muted block font-bold uppercase tracking-wider">SQLite DB Status</span>
                        <span className="font-extrabold text-xs text-primary">Operational (panache_leads.db)</span>
                      </div>
                    </Card>
                    <Card className="p-5 flex items-center gap-4 border-border bg-card">
                      <div className={`p-3 rounded-xl ${sheetsConfigured ? "bg-emerald-50 text-emerald-500" : "bg-rose-50 text-rose-500"}`}>
                        <CheckCircle className="w-5 h-5" />
                      </div>
                      <div>
                        <span className="text-[10px] text-muted block font-bold uppercase tracking-wider">Sheets Link status</span>
                        <span className="font-extrabold text-xs text-primary">
                          {sheetsConfigured ? "Connected (CRM Active)" : "Not Configured"}
                        </span>
                      </div>
                    </Card>
                    <Card className="p-5 flex items-center gap-4 border-border bg-card">
                      <div className="p-3 bg-emerald-50 rounded-xl text-emerald-500">
                        <Key className="w-5 h-5" />
                      </div>
                      <div>
                        <span className="text-[10px] text-muted block font-bold uppercase tracking-wider">Gemini API status</span>
                        <span className="font-extrabold text-xs text-primary">Online (1.5 Flash Model)</span>
                      </div>
                    </Card>
                  </div>
                </>
              )}
            </div>
          )}

          {activeTab === "settings" && (
            <Card className="p-8 max-w-2xl mx-auto space-y-6">
              <div className="flex justify-between items-center border-b border-border pb-3">
                <h3 className="font-extrabold text-base text-primary">Google Sheets Configuration</h3>
                <div className="flex items-center gap-2">
                  {sheetsConfigured ? (
                    <Badge className="bg-emerald-500 text-white font-bold px-2.5 py-1">🟢 Connected</Badge>
                  ) : (
                    <Badge className="bg-rose-500 text-white font-bold px-2.5 py-1">🔴 Not Linked</Badge>
                  )}
                </div>
              </div>
              <div className="space-y-4">
                {sheetsConfigured && !isEditingConfig && (
                  <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold rounded-lg">
                    ✅ Configuration Loaded
                  </div>
                )}
                <div className="flex flex-col gap-2">
                  <label className="text-xs font-bold text-muted">Google Sheets Spreadsheet URL</label>
                  <Input 
                    value={sheetsUrl} 
                    disabled={!isEditingConfig}
                    onChange={(e) => setSheetsUrl(e.target.value)} 
                    placeholder="https://docs.google.com/spreadsheets/..." 
                  />
                </div>
                <div className="flex flex-col gap-2">
                  <label className="text-xs font-bold text-muted">Service Account Credentials JSON</label>
                  <Textarea 
                    value={isEditingConfig ? sheetsCreds : "•••••••••••••••••••••••••••••••• (Credentials Configured)"} 
                    disabled={!isEditingConfig}
                    onChange={(e) => setSheetsCreds(e.target.value)} 
                    rows={6}
                  />
                </div>
                <div className="pt-4 flex gap-4">
                  {isEditingConfig ? (
                    <>
                      <Button className="flex-1" onClick={handleSaveSettings}>Save Configuration</Button>
                      {sheetsConfigured && (
                        <Button variant="outline" onClick={() => setIsEditingConfig(false)}>Cancel</Button>
                      )}
                    </>
                  ) : (
                    <Button className="flex-1" onClick={() => setIsEditingConfig(true)}>Edit Configuration</Button>
                  )}
                  <Button variant="outline" onClick={loadData}>Refresh Connection Status</Button>
                </div>
              </div>
            </Card>
          )}
        </section>
      </main>

      {/* Slide-out Client Profile Details Drawer */}
      <Drawer
        isOpen={isDrawerOpen}
        onClose={() => setIsDrawerOpen(false)}
        title="Client Advisory Dossier"
        className="w-96 md:w-[500px]"
      >
        {selectedLead && (
          <div className="space-y-6 text-xs text-foreground pb-8 max-h-[85vh] overflow-y-auto pr-2">
            {/* Summary block */}
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <h4 className="text-sm font-extrabold text-primary">{selectedLead.first_name} {selectedLead.last_name}</h4>
                <Badge variant={selectedLead.grade === "A" ? "secondary" : "outline"}>
                  Grade {selectedLead.grade}
                </Badge>
              </div>
              <div className="text-[10px] text-muted font-semibold">Registered: {new Date(selectedLead.created_at).toLocaleString()}</div>
            </div>

            {/* BANT Attributes Grid */}
            <div className="space-y-3 bg-muted/20 p-4 rounded-xl border border-border/40">
              <h5 className="font-bold text-[10px] text-muted uppercase tracking-wider">Qualifying Criteria</h5>
              <div className="space-y-2">
                <div className="flex justify-between border-b border-border/30 pb-1.5">
                  <span className="text-muted font-bold">Country</span>
                  <span className="font-extrabold text-primary">{selectedLead.country}</span>
                </div>
                <div className="flex justify-between border-b border-border/30 pb-1.5">
                  <span className="text-muted font-bold">Budget (AED)</span>
                  <span className="font-extrabold text-accent">{selectedLead.budget}</span>
                </div>
                <div className="flex justify-between border-b border-border/30 pb-1.5">
                  <span className="text-muted font-bold">Payment Method</span>
                  <span className="font-extrabold text-primary">{selectedLead.payment_method}</span>
                </div>
                <div className="flex justify-between border-b border-border/30 pb-1.5">
                  <span className="text-muted font-bold">Timeline</span>
                  <span className="font-extrabold text-primary">{selectedLead.timeline}</span>
                </div>
                <div className="flex justify-between border-b border-border/30 pb-1.5">
                  <span className="text-muted font-bold">Purpose</span>
                  <span className="font-extrabold text-primary">{selectedLead.purpose}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted font-bold">Google Sheets Sync</span>
                  <span className={`font-extrabold ${selectedLead.synced_to_sheets ? "text-emerald-500" : "text-amber-500"}`}>
                    {selectedLead.synced_to_sheets ? "🟢 Synced" : "🟡 Pending Sync (Local)"}
                  </span>
                </div>
              </div>
            </div>

            {/* Grade Explanation */}
            <div className="space-y-2 bg-accent/5 p-4 rounded-xl border border-accent/20">
              <h5 className="font-bold text-[10px] text-accent uppercase tracking-wider">Grade Explanation</h5>
              <div className="space-y-1 text-[11px] leading-relaxed">
                <div className="font-bold text-primary">Grade {selectedLead.grade} Classification</div>
                {selectedLead.grade === "A" && (
                  <ul className="list-disc pl-4 space-y-0.5 text-muted">
                    <li>Budget above AED 1.5M</li>
                    <li>Timeline within 3 months</li>
                    <li>Cash / ready payment strategy</li>
                    <li>High-yielding investment potential</li>
                  </ul>
                )}
                {selectedLead.grade === "B" && (
                  <ul className="list-disc pl-4 space-y-0.5 text-muted">
                    <li>Budget above AED 1.5M</li>
                    <li>Timeline 3-6 months or mortgage payment</li>
                  </ul>
                )}
                {selectedLead.grade === "C" && (
                  <ul className="list-disc pl-4 space-y-0.5 text-muted">
                    <li>Entry-level budget or flexible timeline</li>
                    <li>Standard investment matching profile</li>
                  </ul>
                )}
                {selectedLead.grade === "D" && (
                  <ul className="list-disc pl-4 space-y-0.5 text-muted">
                    <li>Budget or timeline remained unconfirmed</li>
                    <li>Requires cold lead nurturing</li>
                  </ul>
                )}
              </div>
            </div>

            {/* Investment Breakdown (Grade A only) */}
            {selectedLead.grade === "A" && (() => {
              const budgetVal = (() => {
                const digits = selectedLead.budget.replace(/[^0-9]/g, "");
                return digits ? parseFloat(digits) : 0;
              })();
              const usdVal = budgetVal / 3.6725;
              const bookingAed = budgetVal * 0.20;
              const bookingUsd = usdVal * 0.20;
              const balanceAed = budgetVal * 0.80;
              const balanceUsd = usdVal * 0.80;
              return (
                <div className="space-y-3 bg-primary/5 p-4 rounded-xl border border-primary/10">
                  <h5 className="font-bold text-[10px] text-primary uppercase tracking-wider">Grade A Exclusive 20/80 Payment Schedule</h5>
                  <div className="space-y-2">
                    <div className="flex justify-between border-b border-border/30 pb-1.5">
                      <span className="text-muted">Total Budget</span>
                      <span className="font-extrabold text-primary">AED {budgetVal.toLocaleString()} (${Math.round(usdVal).toLocaleString()} USD)</span>
                    </div>
                    <div className="flex justify-between border-b border-border/30 pb-1.5 text-accent">
                      <span className="font-bold">20% Booking</span>
                      <span className="font-extrabold">AED {bookingAed.toLocaleString()} (${Math.round(bookingUsd).toLocaleString()} USD)</span>
                    </div>
                    <div className="flex justify-between text-muted">
                      <span>80% Balance</span>
                      <span className="font-bold">AED {balanceAed.toLocaleString()} (${Math.round(balanceUsd).toLocaleString()} USD)</span>
                    </div>
                  </div>
                </div>
              );
            })()}

            {/* AI Summary Section */}
            {selectedLead.ai_summary && (
              <div className="space-y-2">
                <h5 className="font-bold text-[10px] text-muted uppercase tracking-wider">AI Conversation Summary</h5>
                <p className="p-3.5 bg-muted/15 border border-border/40 rounded-xl leading-relaxed font-semibold text-muted text-[11px]">
                  {selectedLead.ai_summary}
                </p>
              </div>
            )}

            {/* Complete Conversation Transcript with timestamps */}
            {(() => {
              let transcript: any[] = [];
              if (selectedLead.chat_transcript) {
                try {
                  transcript = typeof selectedLead.chat_transcript === "string" 
                    ? JSON.parse(selectedLead.chat_transcript) 
                    : selectedLead.chat_transcript;
                } catch (e) {
                  console.error(e);
                }
              }
              if (transcript && transcript.length > 0) {
                return (
                  <div className="space-y-2">
                    <h5 className="font-bold text-[10px] text-muted uppercase tracking-wider flex items-center gap-1">
                      <MessageSquare className="w-3.5 h-3.5 text-accent" /> Consultation Transcript
                    </h5>
                    <div className="bg-card border border-border rounded-xl divide-y divide-border/30 max-h-48 overflow-y-auto p-2 space-y-2">
                      {transcript.map((msg: any, idx: number) => {
                        const isAi = msg.role !== "user";
                        return (
                          <div key={idx} className="p-2 text-[10px] leading-relaxed space-y-0.5">
                            <div className="flex justify-between items-center text-[9px] font-bold text-muted">
                              <span className={isAi ? "text-accent" : "text-primary"}>
                                {isAi ? "Panache AI Assistant" : "Client"}
                              </span>
                              {msg.timestamp && <span>{msg.timestamp}</span>}
                            </div>
                            <div className="text-muted font-semibold">{msg.content}</div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                );
              }
              return null;
            })()}

            {/* Personalized Email Draft */}
            {selectedLead.generated_email && (
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <h5 className="font-bold text-[10px] text-muted uppercase tracking-wider flex items-center gap-1.5">
                    <Mail className="w-3.5 h-3.5 text-accent" /> Advisory Correspondence
                  </h5>
                  <button 
                    onClick={() => handleCopyEmail(selectedLead.generated_email)}
                    className="p-1 hover:bg-muted rounded text-muted hover:text-primary transition-colors cursor-pointer flex items-center gap-1 text-[10px] font-bold"
                  >
                    <Copy className="w-3 h-3" /> Copy Draft
                  </button>
                </div>
                <div className="bg-card border border-border p-4 rounded-xl text-[10px] font-semibold text-primary max-h-40 overflow-y-auto">
                  <pre className="whitespace-pre-wrap">{selectedLead.generated_email}</pre>
                </div>
              </div>
            )}

            {/* Actions Panel */}
            <div className="space-y-3 pt-4 border-t border-border">
              <Button 
                onClick={() => api.exportPDFTranscript(selectedLead.id)} 
                className="w-full py-4 text-xs font-bold tracking-wide flex items-center justify-center gap-1.5"
              >
                <Download className="w-3.5 h-3.5" /> Export Advisory Report (PDF)
              </Button>
              <div className="grid grid-cols-2 gap-2">
                <Button 
                  variant="outline" 
                  onClick={() => handleCopyWhatsApp(selectedLead)}
                  className="text-[10px] font-bold py-2.5 flex items-center justify-center gap-1"
                >
                  <MessageCircle className="w-3.5 h-3.5 text-emerald-500" /> WhatsApp Msg
                </Button>
                <select 
                  value={selectedLead.status} 
                  onChange={(e) => handleUpdateStatus(selectedLead.id, e.target.value)}
                  className="bg-card border border-border text-[10px] p-2 rounded font-bold cursor-pointer w-full text-center"
                >
                  <option value="New">New</option>
                  <option value="Contacted">Contacted</option>
                  <option value="Qualified">Qualified</option>
                  <option value="Closed">Closed</option>
                </select>
              </div>
              <div className="flex gap-2">
                <Button 
                  className="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white text-[10px] font-bold py-2 flex items-center justify-center gap-1"
                  onClick={() => handleUpdateStatus(selectedLead.id, "Contacted")}
                >
                  <CheckCircle2 className="w-3.5 h-3.5" /> Mark Contacted
                </Button>
                <Button 
                  className="flex-1 bg-rose-600 hover:bg-rose-700 text-white text-[10px] font-bold py-2 flex items-center justify-center gap-1"
                  onClick={() => handleUpdateStatus(selectedLead.id, "Closed")}
                >
                  <XCircle className="w-3.5 h-3.5" /> Mark Closed
                </Button>
              </div>
            </div>
          </div>
        )}
      </Drawer>
    </div>
  );
}
