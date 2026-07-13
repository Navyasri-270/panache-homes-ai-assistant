"use client";
import React from "react";
import { useRouter } from "next/navigation";

export interface Property {
  title: string;
  community: string;
  price: string;
  roi: string;
  desc: string;
  img: string;
}

export default function PropertyGallery() {
  const router = useRouter();

  const properties: Property[] = [
    {
      title: "Burj Khalifa Sky Residence",
      community: "Downtown Dubai",
      price: "Starting AED 4.5M",
      roi: "ROI 7.8%",
      desc: "Ultra-high-end sky apartments with panoramic fountain views and private concierge.",
      img: "/images/luxury_apartment.jpg"
    },
    {
      title: "Palm Jumeirah Signature Villa",
      community: "Palm Jumeirah",
      price: "Starting AED 18.0M",
      roi: "ROI 6.5%",
      desc: "Stunning custom beachfront mansion with private pool, direct sea access, and luxury gardens.",
      img: "/images/luxury_villa.jpg"
    },
    {
      title: "Marina Gate Premium Apartment",
      community: "Dubai Marina",
      price: "Starting AED 2.8M",
      roi: "ROI 8.2%",
      desc: "Modern luxury high-rise apartment with panoramic marina views, rooftop pool, and health club.",
      img: "/images/dubai_skyline.jpg"
    },
    {
      title: "Dubai Hills Estate Gated Mansion",
      community: "Dubai Hills Estate",
      price: "Starting AED 12.5M",
      roi: "ROI 7.2%",
      desc: "Luxury estate villa built directly on the championship golf course with infinity pool.",
      img: "/images/luxury_villa.jpg"
    },
    {
      title: "Burj Al Arab Sunset Duplex",
      community: "Jumeirah",
      price: "Starting AED 9.2M",
      roi: "ROI 6.8%",
      desc: "Exclusive duplex residence offering unmatched sunset views over the Arabian Gulf.",
      img: "/images/dubai_skyline.jpg"
    },
    {
      title: "One Canal Private Penthouses",
      community: "Dubai Water Canal",
      price: "Starting AED 15.0M",
      roi: "ROI 7.0%",
      desc: "Ultra-luxury full-floor penthouse with private terrace pool and custom automated design.",
      img: "/images/luxury_apartment.jpg"
    },
    {
      title: "Arabian Ranches Family Villa",
      community: "Arabian Ranches III",
      price: "Starting AED 3.8M",
      roi: "ROI 7.5%",
      desc: "Tranquil family villa with expansive landscaped garden, family parks, and community pools.",
      img: "/images/luxury_villa.jpg"
    },
    {
      title: "Business Bay Canal Suite",
      community: "Business Bay",
      price: "Starting AED 1.8M",
      roi: "ROI 8.5%",
      desc: "Elegant modern executive apartment with water views and premium workspace facilities.",
      img: "/images/luxury_apartment.jpg"
    }
  ];

  const handleAskAI = (title: string) => {
    sessionStorage.setItem("selected_property", title);
    router.push("/chat");
  };

  return (
    <section id="gallery" className="py-20 bg-background">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-extrabold text-primary mb-4">Featured Luxury Developments</h2>
          <p className="text-muted max-w-2xl mx-auto">
            Explore investment-ready residential projects in prime Dubai communities.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {properties.map((prop, idx) => (
            <div key={idx} className="bg-card rounded-2xl overflow-hidden border border-border shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300 flex flex-col justify-between h-[420px]">
              <div>
                <div 
                  className="h-44 bg-cover bg-center relative" 
                  style={{ backgroundImage: `url('${prop.img}')` }}
                >
                  <span className="absolute top-3 left-3 bg-primary/80 backdrop-blur-sm text-primary-foreground text-xs font-bold px-2.5 py-1 rounded">
                    {prop.community}
                  </span>
                </div>
                <div className="p-5">
                  <h3 className="font-extrabold text-lg text-primary mb-2 line-clamp-1">{prop.title}</h3>
                  <p className="text-xs text-muted leading-relaxed line-clamp-3 mb-4">{prop.desc}</p>
                </div>
              </div>
              <div className="p-5 pt-0">
                <div className="flex justify-between items-center text-xs font-bold border-t border-border/50 pt-4 mb-4">
                  <span className="text-accent">{prop.price}</span>
                  <span className="text-primary">{prop.roi}</span>
                </div>
                <button 
                  onClick={() => handleAskAI(prop.title)}
                  className="w-full py-2.5 bg-primary text-primary-foreground font-bold text-xs rounded-lg hover:opacity-90 transition-opacity cursor-pointer uppercase tracking-wider"
                >
                  Ask AI About This Property
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
