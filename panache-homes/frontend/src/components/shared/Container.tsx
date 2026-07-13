import React from "react";
import { cn } from "@/lib/utils";

export interface ContainerProps extends React.HTMLAttributes<HTMLDivElement> {
  size?: "sm" | "md" | "lg" | "xl" | "full";
}

export function Container({ className, size = "xl", ...props }: ContainerProps) {
  return (
    <div
      className={cn(
        "mx-auto px-4 w-full",
        {
          "max-w-3xl": size === "sm",
          "max-w-5xl": size === "md",
          "max-w-7xl": size === "lg",
          "max-w-8xl": size === "xl",
          "max-w-full": size === "full",
        },
        className
      )}
      {...props}
    />
  );
}
