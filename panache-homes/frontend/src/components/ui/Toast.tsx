import React from "react";
import { cn } from "@/lib/utils";
import { X, CheckCircle, AlertCircle } from "lucide-react";

export interface ToastProps {
  message: string;
  type?: "success" | "error" | "info";
  onClose: () => void;
}

export function Toast({ message, type = "info", onClose }: ToastProps) {
  return (
    <div
      className={cn(
        "fixed bottom-4 right-4 z-50 flex items-center gap-3 w-80 max-w-sm p-4 rounded-lg border shadow-lg animate-in slide-in-from-bottom duration-300",
        {
          "bg-emerald-50 border-emerald-200 text-emerald-800 dark:bg-emerald-950/30 dark:border-emerald-800 dark:text-emerald-300": type === "success",
          "bg-rose-50 border-rose-200 text-rose-800 dark:bg-rose-950/30 dark:border-rose-800 dark:text-rose-300": type === "error",
          "bg-card border-border text-foreground": type === "info",
        }
      )}
    >
      {type === "success" && <CheckCircle className="w-5 h-5 text-emerald-500 shrink-0" />}
      {type === "error" && <AlertCircle className="w-5 h-5 text-rose-500 shrink-0" />}
      
      <p className="text-sm font-medium flex-1">{message}</p>
      
      <button onClick={onClose} className="p-1 rounded hover:bg-muted text-muted transition-colors cursor-pointer">
        <X className="w-4 h-4" />
      </button>
    </div>
  );
}
