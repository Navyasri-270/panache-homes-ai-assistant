import React from "react";
import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="fixed top-0 left-0 w-full z-50 bg-background/80 backdrop-blur-md border-b border-border">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        <Link href="/" className="font-extrabold text-lg tracking-wider text-primary">
          🏢 PANACHE <span className="text-accent">HOMES</span>
        </Link>
        <div className="flex items-center gap-6 text-sm font-medium">
          <Link href="#home" className="hover:text-accent transition-colors">Home</Link>
          <Link href="#about" className="hover:text-accent transition-colors">About</Link>
          <Link href="#services" className="hover:text-accent transition-colors">Services</Link>
          <Link href="#contact" className="hover:text-accent transition-colors">Contact</Link>
          <Link href="/admin" className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90 transition-opacity">
            Admin Login
          </Link>
        </div>
      </div>
    </nav>
  );
}
