import React from "react";
import { cn } from "@/lib/utils";

export interface SectionProps extends React.HTMLAttributes<HTMLDivElement> {
  background?: "default" | "muted" | "card";
  padding?: "none" | "sm" | "md" | "lg";
}

export function Section({ className, background = "default", padding = "md", ...props }: SectionProps) {
  return (
    <section
      className={cn(
        "w-full border-b border-border/10",
        {
          "bg-background": background === "default",
          "bg-muted/30": background === "muted",
          "bg-card": background === "card",
        },
        {
          "py-0": padding === "none",
          "py-10 md:py-12": padding === "sm",
          "py-16 md:py-20": padding === "md",
          "py-24 md:py-32": padding === "lg",
        },
        className
      )}
      {...props}
    />
  );
}
