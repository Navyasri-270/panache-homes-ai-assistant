"use client";
import React from "react";
import Link from "next/link";

export default function Hero() {
  const handleScrollToMap = () => {
    const mapElement = document.getElementById("map");
    if (mapElement) {
      mapElement.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <section 
      style={{ backgroundImage: "url('https://images.unsplash.com/photo-1582672060674-bc2bd8022eb0?auto=format&fit=crop&w=1920&q=80')" }}
      className="relative h-[85vh] flex items-center justify-center bg-cover bg-center"
    >
      <div className="absolute inset-0 bg-primary/75" />
      <div className="relative z-10 text-center px-4 max-w-4xl">
        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight text-primary-foreground mb-6">
          AI-Powered Dubai Property Investment Assistant
        </h1>
        <p className="text-lg md:text-xl text-primary-foreground/80 mb-8 max-w-2xl mx-auto">
          Qualify your budget, compute dynamic payment splits, and match with premium luxury off-plan properties instantly.
        </p>
        <div className="flex flex-wrap justify-center gap-4">
          <Link href="/chat">
            <button className="px-6 py-3 bg-accent text-accent-foreground font-bold rounded-lg hover:opacity-90 transition-opacity cursor-pointer">
              Start AI Consultation
            </button>
          </Link>
          <button 
            onClick={handleScrollToMap}
            className="px-6 py-3 bg-background text-foreground font-bold rounded-lg border border-border hover:bg-muted transition-colors cursor-pointer"
          >
            Explore Communities
          </button>
        </div>
      </div>
    </section>
  );
}
