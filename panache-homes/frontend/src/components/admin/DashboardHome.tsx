import React from "react";

export default function DashboardHome() {
  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-extrabold text-primary">CRM Admin Dashboard</h1>
          <p className="text-sm text-muted">Manage qualified client portfolios and synced pipelines.</p>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="p-6 bg-card border border-border rounded-lg shadow-sm">
          <div className="text-xs text-muted mb-2 font-bold uppercase tracking-wider">Today's Leads</div>
          <div className="text-3xl font-extrabold text-primary">12</div>
        </div>
        <div className="p-6 bg-card border border-border rounded-lg shadow-sm">
          <div className="text-xs text-muted mb-2 font-bold uppercase tracking-wider">Qualified Leads</div>
          <div className="text-3xl font-extrabold text-primary">84</div>
        </div>
        <div className="p-6 bg-card border border-border rounded-lg shadow-sm">
          <div className="text-xs text-muted mb-2 font-bold uppercase tracking-wider">Grade A Profiles</div>
          <div className="text-3xl font-extrabold text-primary">28</div>
        </div>
        <div className="p-6 bg-card border border-border rounded-lg shadow-sm">
          <div className="text-xs text-muted mb-2 font-bold uppercase tracking-wider">Sheets Sync Status</div>
          <div className="text-3xl font-extrabold text-green-500">Connected</div>
        </div>
      </div>
    </div>
  );
}
