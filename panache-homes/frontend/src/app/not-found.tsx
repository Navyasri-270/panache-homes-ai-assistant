"use client";
import React from "react";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/Button";

export default function NotFound() {
  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center p-6 text-center space-y-6">
      <div className="space-y-2">
        <span className="text-accent text-5xl font-extrabold tracking-widest block">404</span>
        <h1 className="text-3xl font-extrabold text-primary">Luxury Page Not Found</h1>
        <p className="text-muted text-xs max-w-sm mx-auto leading-relaxed">
          The property residence page or resource you are looking for has been relocated or is temporarily unavailable.
        </p>
      </div>
      
      <Link href="/">
        <Button className="flex items-center gap-2 py-5 font-bold tracking-wide">
          <ArrowLeft className="w-4 h-4" /> Return to Residences
        </Button>
      </Link>
    </div>
  );
}
