"use client";
import React, { useEffect } from "react";
import { AlertCircle, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/Button";

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function ErrorPage({ error, reset }: ErrorProps) {
  useEffect(() => {
    console.error("Critical server rendering boundary error:", error);
  }, [error]);

  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center p-6 text-center space-y-6">
      <div className="space-y-2 flex flex-col items-center">
        <div className="p-4 bg-rose-50 rounded-full text-rose-500 mb-2">
          <AlertCircle className="w-10 h-10 animate-bounce" />
        </div>
        <h1 className="text-3xl font-extrabold text-primary">System Disruption</h1>
        <p className="text-muted text-xs max-w-sm mx-auto leading-relaxed">
          An unexpected error occurred during page compilation or API queries.
        </p>
      </div>

      <Button onClick={() => reset()} className="flex items-center gap-2 py-5 font-bold tracking-wide">
        <RefreshCw className="w-4 h-4" /> Attempt Reconnect
      </Button>
    </div>
  );
}
