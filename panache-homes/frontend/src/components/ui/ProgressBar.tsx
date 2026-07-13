import React from "react";
import { cn } from "@/lib/utils";

export interface ProgressBarProps {
  value: number; // 0 to 100
  className?: string;
}

export function ProgressBar({ value, className }: ProgressBarProps) {
  const percent = Math.min(Math.max(value, 0), 100);

  return (
    <div className={cn("w-full bg-muted h-2.5 rounded-full overflow-hidden", className)}>
      <div
        className="bg-accent h-full transition-all duration-500 ease-out"
        style={{ width: `${percent}%` }}
      />
    </div>
  );
}
