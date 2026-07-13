import React from "react";

export default function Stats() {
  const stats = [
    { value: "500+", label: "Investors Supported", icon: "🚀" },
    { value: "40+", label: "Countries Reached", icon: "🌍" },
    { value: "10+", label: "Years Experience", icon: "🏆" },
    { value: "AI", label: "Powered Matching", icon: "🤖" },
  ];

  return (
    <section className="py-12 bg-card border-y border-border">
      <div className="max-w-7xl mx-auto px-4 grid grid-cols-2 md:grid-cols-4 gap-8">
        {stats.map((stat, idx) => (
          <div key={idx} className="text-center">
            <span className="text-2xl mb-2 block">{stat.icon}</span>
            <div className="text-3xl font-extrabold text-primary mb-1">{stat.value}</div>
            <div className="text-sm text-muted">{stat.label}</div>
          </div>
        ))}
      </div>
    </section>
  );
}
