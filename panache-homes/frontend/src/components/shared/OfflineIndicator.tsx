"use client";
import React, { useState, useEffect } from "react";
import { WifiOff } from "lucide-react";

export default function OfflineIndicator() {
  const [isOffline, setIsOffline] = useState(false);

  useEffect(() => {
    if (typeof window !== "undefined") {
      setIsOffline(!navigator.onLine);
      
      const handleOnline = () => setIsOffline(false);
      const handleOffline = () => setIsOffline(true);

      window.addEventListener("online", handleOnline);
      window.addEventListener("offline", handleOffline);

      return () => {
        window.removeEventListener("online", handleOnline);
        window.removeEventListener("offline", handleOffline);
      };
    }
  }, []);

  if (!isOffline) return null;

  return (
    <div className="bg-rose-500 text-white text-xs font-bold text-center py-2 px-4 flex items-center justify-center gap-1.5 z-[9999] relative animate-in slide-in-from-top duration-300">
      <WifiOff className="w-4 h-4 animate-pulse" />
      <span>You are currently offline. CRM operations and AI chat consultation states are cached locally.</span>
    </div>
  );
}
