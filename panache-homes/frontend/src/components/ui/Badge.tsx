import React from "react";
import { cn } from "@/lib/utils";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "primary" | "secondary" | "outline" | "destructive";
}

export function Badge({ className, variant = "primary", ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none",
        {
          "bg-primary text-primary-foreground": variant === "primary",
          "bg-accent text-accent-foreground": variant === "secondary",
          "border border-border text-foreground": variant === "outline",
          "bg-red-500 text-white": variant === "destructive",
        },
        className
      )}
      {...props}
    />
  );
}
