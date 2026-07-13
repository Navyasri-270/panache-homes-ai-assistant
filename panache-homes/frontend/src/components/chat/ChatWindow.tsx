import React from "react";

export default function ChatWindow() {
  return (
    <div className="flex-1 flex flex-col h-full bg-card rounded-lg border border-border">
      <div className="p-4 border-b border-border flex items-center justify-between">
        <div>
          <h2 className="font-bold">Panache AI Property Assistant</h2>
          <span className="text-xs text-green-500 flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-green-500 inline-block animate-pulse"></span>
            AI Online
          </span>
        </div>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* Messages layout placeholder */}
        <div className="flex gap-3 max-w-[80%]">
          <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-xs text-primary-foreground">
            AI
          </div>
          <div className="bg-muted p-3 rounded-lg text-sm">
            Hello! I can help you explore premium off-plan projects in Dubai. What budget range are you looking at?
          </div>
        </div>
      </div>
      <div className="p-4 border-t border-border bg-background">
        <form className="flex gap-2">
          <input
            type="text"
            placeholder="Type your message..."
            className="flex-1 px-4 py-2 bg-card border border-border rounded-lg text-sm focus:outline-none"
          />
          <button type="submit" className="px-4 py-2 bg-primary text-primary-foreground text-sm font-bold rounded-lg">
            Send
          </button>
        </form>
      </div>
    </div>
  );
}
