"use client";
import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Shield, Mail, Lock, ArrowLeft } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { api } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      const res = await api.login({ username: email, password });
      // Set secure cookie for Next.js Middleware route protection
      document.cookie = `admin_token=${res.access_token}; path=/; max-age=86400; SameSite=Strict; Secure`;
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Invalid administrator credentials.");
    }
  };

  return (
    <div 
      style={{ backgroundImage: "url('https://images.unsplash.com/photo-1582672060674-bc2bd8022eb0?auto=format&fit=crop&w=1920&q=80')" }}
      className="min-h-screen bg-cover bg-center flex items-center justify-center p-4"
    >
      <div className="absolute inset-0 bg-primary/80 backdrop-blur-sm" />
      
      <Card className="relative z-10 w-full max-w-md bg-card/90 border-border p-8 shadow-2xl rounded-2xl space-y-6">
        <Link href="/" className="inline-flex items-center gap-1.5 text-xs text-muted hover:text-primary transition-colors mb-4">
          <ArrowLeft className="w-3.5 h-3.5" /> Back to Home
        </Link>
        
        <div className="text-center space-y-2">
          <h2 className="font-extrabold text-lg tracking-wider text-primary">🏢 PANACHE HOMES</h2>
          <h3 className="text-2xl font-extrabold text-primary flex items-center justify-center gap-2">
            <Shield className="w-5 h-5 text-accent animate-pulse" /> Administrator Portal
          </h3>
          <p className="text-xs text-muted tracking-wide uppercase font-bold">Authorized Personnel Only</p>
        </div>

        {error && (
          <div className="p-3 bg-rose-50 border border-rose-200 text-rose-800 text-xs font-semibold rounded-lg">
            {error}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-4">
          <div className="space-y-1.5">
            <label className="text-xs font-bold text-muted flex items-center gap-1.5">
              <Mail className="w-3.5 h-3.5 text-accent" /> Email Address
            </label>
            <Input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="admin@panachehomes.ae"
              required
            />
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-bold text-muted flex items-center gap-1.5">
              <Lock className="w-3.5 h-3.5 text-accent" /> Password
            </label>
            <Input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>

          <Button type="submit" className="w-full py-6 font-bold tracking-wide mt-2">
            Log In to Console
          </Button>
        </form>
      </Card>
    </div>
  );
}
