import React from "react";
import { cn } from "@/lib/utils";
import { X } from "lucide-react";

export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  className?: string;
}

export function Modal({ isOpen, onClose, title, children, className }: ModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Overlay */}
      <div className="absolute inset-0 bg-primary/40 backdrop-blur-sm" onClick={onClose} />
      
      {/* Dialog container */}
      <div className={cn("relative z-10 w-full max-w-lg rounded-xl border border-border bg-card p-6 shadow-lg animate-in fade-in zoom-in duration-200", className)}>
        <div className="flex items-center justify-between border-b border-border pb-3 mb-4">
          {title && <h3 className="text-lg font-bold text-primary">{title}</h3>}
          <button onClick={onClose} className="rounded-md p-1 hover:bg-muted text-muted transition-colors cursor-pointer">
            <X className="w-5 h-5" />
          </button>
        </div>
        <div>{children}</div>
      </div>
    </div>
  );
}
