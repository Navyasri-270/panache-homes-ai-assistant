import React from "react";

export default function BantSidebar() {
  const fields = [
    { name: "Name", value: "Michael (USA)", status: "qualified" },
    { name: "Country", value: "United States", status: "qualified" },
    { name: "Budget", value: "AED 2,500,000", status: "qualified" },
    { name: "Payment Method", value: "Cash", status: "qualified" },
    { name: "Timeline", value: "1-3 Months", status: "qualified" },
    { name: "Purpose", value: "Investment", status: "qualified" },
  ];

  return (
    <div className="w-80 border-l border-border bg-card p-6 flex flex-col h-full gap-6">
      <div>
        <h3 className="font-bold text-lg mb-2">BANT Qualification Profile</h3>
        <div className="w-full bg-muted h-2 rounded-full overflow-hidden">
          <div className="bg-accent h-full w-[100%] transition-all duration-500"></div>
        </div>
      </div>
      <div className="space-y-4">
        {fields.map((field, idx) => (
          <div key={idx} className="flex justify-between items-center text-sm pb-2 border-b border-border/50">
            <span className="text-muted">{field.name}</span>
            <span className="font-bold text-primary">{field.value}</span>
          </div>
        ))}
      </div>
      <div className="mt-auto p-4 bg-accent/10 border border-accent/20 rounded-lg text-center">
        <span className="text-xs text-accent font-bold uppercase tracking-wider block mb-1">Lead Grade</span>
        <span className="text-4xl font-extrabold text-accent">Grade A</span>
      </div>
    </div>
  );
}
