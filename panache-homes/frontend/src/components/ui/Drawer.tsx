import React from "react";
import { cn } from "@/lib/utils";
import { X } from "lucide-react";

export interface DrawerProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  side?: "left" | "right";
  className?: string;
}

export function Drawer({ isOpen, onClose, title, children, side = "right", className }: DrawerProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex">
      {/* Overlay */}
      <div className="absolute inset-0 bg-primary/40 backdrop-blur-sm" onClick={onClose} />
      
      {/* Drawer content */}
      <div
        className={cn(
          "relative z-10 w-80 h-full bg-card p-6 shadow-lg flex flex-col border-border transition-transform duration-300 ease-out",
          {
            "left-0 border-r animate-in slide-in-from-left": side === "left",
            "ml-auto border-l animate-in slide-in-from-right": side === "right",
          },
          className
        )}
      >
        <div className="flex items-center justify-between border-b border-border pb-3 mb-4">
          {title && <h3 className="font-bold text-lg text-primary">{title}</h3>}
          <button onClick={onClose} className="rounded-md p-1 hover:bg-muted text-muted transition-colors cursor-pointer">
            <X className="w-5 h-5" />
          </button>
        </div>
        <div className="flex-1 overflow-y-auto">{children}</div>
      </div>
    </div>
  );
}
