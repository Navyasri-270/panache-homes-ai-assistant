"use client";
import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { Badge } from "@/components/ui/Badge";

interface Community {
  name: string;
  desc: string;
  roi: string;
  highlights: string;
  img: string;
}

export default function ExploreMap() {
  const router = useRouter();
  const [communities, setCommunities] = useState<Community[]>([]);
  const [selected, setSelected] = useState<string>("Downtown Dubai");
  const [loading, setLoading] = useState(true);

  // Fetch communities from FastAPI backend
  useEffect(() => {
    const fetchComms = async () => {
      try {
        const comms = await api.getCommunities();
        setCommunities(comms);
        if (comms.length > 0) {
          setSelected(comms[0].name);
        }
        setLoading(false);
      } catch (err) {
        setLoading(false);
      }
    };
    fetchComms();
  }, []);

  const activeCommunity = communities.find((c) => c.name === selected) || communities[0];

  const handleTalkToAI = () => {
    if (!activeCommunity) return;
    // Set selected community details in session storage for Chat page consumption
    sessionStorage.setItem("selected_community", activeCommunity.name);
    // Navigate automatically to Chat console
    router.push("/chat");
  };

  const getPinStyle = (name: string) => {
    const pinStyles: Record<string, string> = {
      "Downtown Dubai": "top-[20%] left-[55%]",
      "Palm Jumeirah": "top-1/4 left-1/4",
      "Dubai Marina": "top-[40%] left-[30%]",
      "Dubai Hills Estate": "top-2/3 left-[45%]",
      "Business Bay": "top-[35%] left-[50%]",
      "Arabian Ranches": "top-3/4 left-[75%]"
    };
    return pinStyles[name] || "top-1/2 left-1/2";
  };

  if (loading) {
    return (
      <div className="py-20 text-center text-xs text-muted font-bold">
        Loading Dubai Communities...
      </div>
    );
  }

  if (communities.length === 0) {
    return null;
  }

  return (
    <section id="map" className="py-20 bg-muted/20 border-y border-border">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-extrabold text-primary mb-4">Explore Dubai Communities</h2>
          <p className="text-muted max-w-2xl mx-auto">
            Interact with the map of Dubai and review investment metrics for key property development hubs.
          </p>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-stretch">
          {/* Stylized Map with pins */}
          <div 
            style={{ backgroundImage: "url('/images/dubai_skyline.jpg')" }}
            className="relative rounded-2xl overflow-hidden border border-border h-[400px] bg-cover bg-center shadow-lg"
          >
            <div className="absolute inset-0 bg-primary/70 backdrop-blur-[1px]" />
            
            {/* Interactive Pins */}
            {communities.map((comm) => {
              const isActive = selected === comm.name;
              return (
                <button
                  key={comm.name}
                  onClick={() => setSelected(comm.name)}
                  className={`absolute ${getPinStyle(comm.name)} -translate-x-1/2 -translate-y-1/2 flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold border transition-all duration-300 shadow-md cursor-pointer hover:scale-105 ${
                    isActive 
                      ? "bg-accent border-accent text-accent-foreground scale-110 z-10" 
                      : "bg-primary border-white text-primary-foreground"
                  }`}
                >
                  📍 {comm.name}
                </button>
              );
            })}
          </div>

          {/* Details Card */}
          {activeCommunity && (
            <div className="bg-card rounded-2xl border border-border overflow-hidden flex flex-col justify-between shadow-sm hover:shadow-md transition-shadow">
              <div className="h-[200px] bg-cover bg-center animate-in fade-in duration-300" style={{ backgroundImage: `url('${activeCommunity.img}')` }} />
              <div className="p-8 flex-1 flex flex-col justify-between">
                <div>
                  <div className="flex justify-between items-center mb-3">
                    <span className="text-xs text-accent font-bold uppercase tracking-wider block">Community Profile</span>
                    <Badge variant="secondary" className="font-bold text-[10px]">{activeCommunity.roi}</Badge>
                  </div>
                  <h3 className="text-2xl font-extrabold text-primary mb-2">{activeCommunity.name}</h3>
                  <p className="text-muted text-xs leading-relaxed mb-4">{activeCommunity.desc}</p>
                  
                  <div className="bg-muted/30 p-3 rounded-lg border border-border/40 mb-6">
                    <span className="text-[10px] text-muted font-bold uppercase tracking-wider block mb-1">Investment Highlights</span>
                    <p className="text-primary text-xs font-semibold leading-relaxed">{activeCommunity.highlights}</p>
                  </div>
                </div>
                <button 
                  onClick={handleTalkToAI}
                  className="w-full py-3 bg-primary text-primary-foreground font-bold rounded-lg hover:opacity-95 transition-opacity cursor-pointer text-xs uppercase tracking-wider"
                >
                  Talk to AI About {activeCommunity.name}
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
