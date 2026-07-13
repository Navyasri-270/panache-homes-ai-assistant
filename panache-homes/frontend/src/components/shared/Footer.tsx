import React from "react";
import Link from "next/link";

export default function Footer() {
  return (
    <footer className="bg-primary text-primary-foreground border-t border-border mt-auto">
      <div className="max-w-7xl mx-auto px-4 py-12 grid grid-cols-1 md:grid-cols-4 gap-8">
        <div>
          <h3 className="font-extrabold text-lg tracking-wider mb-4">🏢 PANACHE HOMES</h3>
          <p className="text-sm text-muted mb-4">
            Boutique real estate brokerage combining top-tier human advisory with advanced AI integrations.
          </p>
        </div>
        <div>
          <h4 className="font-bold mb-4">Quick Links</h4>
          <div className="flex flex-col gap-2 text-sm text-muted">
            <Link href="#home">Home</Link>
            <Link href="#about">About</Link>
            <Link href="#services">Services</Link>
            <Link href="/chat">AI Consultation</Link>
          </div>
        </div>
        <div>
          <h4 className="font-bold mb-4">Dubai Office</h4>
          <p className="text-sm text-muted">
            Marina Plaza, Office 402,<br />Dubai Marina, Dubai, UAE
          </p>
        </div>
        <div>
          <h4 className="font-bold mb-4">Contact Desk</h4>
          <p className="text-sm text-muted">
            Phone: +971 4 999 8888<br />
            Email: contact@panachehomes.ae
          </p>
        </div>
      </div>
      <div className="border-t border-border/10 py-6 text-center text-xs text-muted flex flex-col md:flex-row justify-between items-center max-w-7xl mx-auto px-4">
        <p>© 2026 Panache Homes Real Estate. All rights reserved.</p>
        <div className="flex gap-4 mt-2 md:mt-0">
          <Link href="/privacy">Privacy Policy</Link>
          <Link href="/terms">Terms of Service</Link>
        </div>
      </div>
    </footer>
  );
}
