"use client";
import React, { useState } from "react";
import { useRouter } from "next/navigation";
import Navbar from "@/components/shared/Navbar";
import Hero from "@/components/landing/Hero";
import Stats from "@/components/landing/Stats";
import PropertyGallery from "@/components/landing/PropertyGallery";
import ExploreMap from "@/components/landing/ExploreMap";
import Footer from "@/components/shared/Footer";
import { Section } from "@/components/shared/Section";
import { Container } from "@/components/shared/Container";
import { Card } from "@/components/ui/Card";

export default function Home() {
  const router = useRouter();
  const [openFaq, setOpenFaq] = useState<number | null>(null);

  const communities = [
    { title: "Palm Jumeirah", desc: "Beachfront signature villas and luxury waterfront penthouses.", img: "/images/luxury_villa.jpg" },
    { title: "Dubai Marina", desc: "Modern sky apartments overlooking the world's largest man-made marina.", img: "/images/dubai_skyline.jpg" },
    { title: "Downtown Dubai", desc: "Prestige residences in the home of Burj Khalifa and Dubai Mall.", img: "/images/luxury_apartment.jpg" },
    { title: "Business Bay", desc: "Canal-front suites offering high occupancies and fast development.", img: "/images/luxury_apartment.jpg" },
    { title: "Dubai Hills Estate", desc: "Private gated golf villas and premium green parkland communities.", img: "/images/luxury_villa.jpg" },
    { title: "Arabian Ranches", desc: "Tranquil desert-themed villas designed for quiet family neighborhoods.", img: "/images/luxury_villa.jpg" }
  ];

  const services = [
    { title: "Luxury Apartments", desc: "Exclusive listings of high-end penthouses and canal suites.", icon: "🏢" },
    { title: "Luxury Villas", desc: "Waterfront mansions and private gated golf course residences.", icon: "🏡" },
    { title: "Off-Plan Developments", desc: "Direct pre-launch access to premium off-plan layouts and payment plans.", icon: "✨" },
    { title: "Investment Advisory", desc: "Intelligent data-driven yield assessment and currency pegging reviews.", icon: "📈" },
    { title: "Property Management", desc: "End-to-end lease management, RERA coordination, and maintenance.", icon: "🔑" },
    { title: "Golden Visa Consulting", desc: "Bespoke legal assistance matching purchases to the AED 2M+ residency.", icon: "🛂" }
  ];

  const benefits = [
    { title: "High Rental Yield", desc: "Dubai yields average 6-9%, outperforming major global capitals.", icon: "💰" },
    { title: "Golden Visa", desc: "Secure 10-year residency visa for purchases of AED 2M or more.", icon: "🛂" },
    { title: "Tax-Free Income", desc: "Zero income tax on rental earnings or capital gains.", icon: "🪙" },
    { title: "Stable AED Currency", desc: "Pegged stably to the US Dollar (3.6725 AED/USD).", icon: "💵" },
    { title: "Remote Purchase", desc: "Complete property acquisition legally from anywhere globally.", icon: "🌍" },
    { title: "Growing Economy", desc: "Backed by world-class infrastructure and pro-business policies.", icon: "🏢" }
  ];

  const timelineSteps = [
    { step: "01", title: "Ask AI", desc: "Voice your goals and constraints naturally to our assistant." },
    { step: "02", title: "Instant Qualification", desc: "Get dynamically qualified according to budget and timelines." },
    { step: "03", title: "Property Recommendations", desc: "Instantly matches premium residential projects matching criteria." },
    { step: "04", title: "Advisor Contact", desc: "Confirm allocations with RERA registered professionals." },
    { step: "05", title: "Purchase", desc: "Secure booking, sign DLD paperwork, own property." }
  ];

  const faqs = [
    { q: "How does the AI Property Assistant help me?", a: "Our AI assistant guides you through real-time capital growth assessments, ROI estimates, down-payment thresholds, and Golden Visa eligibility parameters instantly." },
    { q: "What is the RERA and DLD registration fee?", a: "Standard DLD (Dubai Land Department) registration fees are 4% of the property value, typically paid at the time of purchase." },
    { q: "Am I eligible for a Golden Visa through real estate investment?", a: "Yes, investing in properties valued at AED 2,000,000 (approx. USD 545,000) or more qualifies you for the 10-year residency Golden Visa." }
  ];

  const handleLearnMore = (serviceTitle: string) => {
    sessionStorage.setItem("selected_property", `our ${serviceTitle} service`);
    router.push("/chat");
  };

  const handleCommunityClick = (commTitle: string) => {
    sessionStorage.setItem("selected_community", commTitle);
    router.push("/chat");
  };

  return (
    <div className="flex flex-col min-h-screen bg-background text-foreground">
      <Navbar />
      
      <main className="flex-1 pt-16">
        {/* Luxury Hero */}
        <Hero />
        
        {/* Statistics Bar */}
        <Stats />
        
        {/* Premium Communities Grid */}
        <Section id="communities" background="default">
          <Container>
            <div className="text-center mb-12">
              <h2 className="text-3xl font-extrabold text-primary mb-4 animate-fade-in">Premium Communities</h2>
              <p className="text-muted max-w-2xl mx-auto text-xs font-semibold">
                Explore prime neighborhoods offering world-class capital appreciation.
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {communities.map((comm, idx) => (
                <div 
                  key={idx} 
                  onClick={() => handleCommunityClick(comm.title)}
                  className="group relative h-64 rounded-2xl overflow-hidden shadow-sm hover:shadow-lg transition-all duration-300 cursor-pointer"
                >
                  <div 
                    className="absolute inset-0 bg-cover bg-center transition-transform duration-500 group-hover:scale-105" 
                    style={{ backgroundImage: `url('${comm.img}')` }} 
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-primary/90 via-primary/45 to-transparent" />
                  <div className="absolute bottom-0 left-0 w-full p-6 text-primary-foreground">
                    <h3 className="text-xl font-bold mb-2">{comm.title}</h3>
                    <p className="text-xs text-primary-foreground/80 leading-relaxed">{comm.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </Container>
        </Section>
        
        {/* Why Invest in Dubai */}
        <Section id="why-invest" background="muted">
          <Container>
            <div className="text-center mb-12">
              <h2 className="text-3xl font-extrabold text-primary mb-4">Why Invest in Dubai?</h2>
              <p className="text-muted max-w-2xl mx-auto text-xs font-semibold">
                Tax-free yields, long-term visas, and stable growth metrics make Dubai a premium choice.
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {benefits.map((benefit, idx) => (
                <Card key={idx} className="p-6 hover:shadow-md transition-shadow">
                  <span className="text-3xl mb-4 block">{benefit.icon}</span>
                  <h3 className="font-bold text-lg text-primary mb-2">{benefit.title}</h3>
                  <p className="text-xs text-muted leading-relaxed">{benefit.desc}</p>
                </Card>
              ))}
            </div>
          </Container>
        </Section>
        
        {/* Property Gallery */}
        <PropertyGallery />
        
        {/* Explore Dubai Communities Map */}
        <ExploreMap />
        
        {/* How It Works Timeline */}
        <Section id="how-it-works" background="default">
          <Container>
            <div className="text-center mb-12">
              <h2 className="text-3xl font-extrabold text-primary mb-4">How It Works</h2>
              <p className="text-muted max-w-2xl mx-auto text-xs font-semibold">
                Our dynamic pipeline takes you from raw inquiry to property ownership smoothly.
              </p>
            </div>
            <div className="flex flex-col md:flex-row justify-between gap-8 max-w-5xl mx-auto relative">
              {timelineSteps.map((step, idx) => (
                <div key={idx} className="flex-1 text-center relative z-10">
                  <div className="w-12 h-12 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-extrabold text-lg mx-auto mb-4 border-2 border-accent">
                    {step.step}
                  </div>
                  <h3 className="font-bold text-primary mb-2">{step.title}</h3>
                  <p className="text-xs text-muted leading-relaxed">{step.desc}</p>
                </div>
              ))}
            </div>
          </Container>
        </Section>
        
        {/* Panache AI Advantage */}
        <Section id="advantage" background="muted">
          <Container>
            <div className="text-center mb-12">
              <h2 className="text-3xl font-extrabold text-primary mb-4">The Panache AI Advantage</h2>
              <p className="text-muted max-w-2xl mx-auto text-xs font-semibold">
                How our intelligent assistant simplifies property investment compared to traditional searching.
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-12 max-w-4xl mx-auto">
              <Card className="p-8 border-border bg-card">
                <h3 className="font-bold text-lg text-primary mb-6 flex items-center gap-2">🛑 Traditional Search</h3>
                <ul className="space-y-4 text-xs text-muted font-semibold">
                  <li className="flex items-center gap-3">❌ Searching manually through listings</li>
                  <li className="flex items-center gap-3">❌ Confusing pricing structures</li>
                  <li className="flex items-center gap-3">❌ Delayed responses from brokerages</li>
                </ul>
              </Card>
              <Card className="p-8 border-accent bg-primary text-primary-foreground">
                <h3 className="font-bold text-lg text-accent mb-6 flex items-center gap-2">✨ Panache AI</h3>
                <ul className="space-y-4 text-xs text-primary-foreground/80 font-semibold">
                  <li className="flex items-center gap-3">✔ Simple natural language matching</li>
                  <li className="flex items-center gap-3">✔ Dynamic payment split breakdowns</li>
                  <li className="flex items-center gap-3">✔ Instant RERA qualified advice</li>
                </ul>
              </Card>
            </div>
          </Container>
        </Section>
        
        {/* Services */}
        <Section id="services" background="default">
          <Container>
            <div className="text-center mb-12">
              <h2 className="text-3xl font-extrabold text-primary mb-4">Premium Broker Services</h2>
              <p className="text-muted max-w-2xl mx-auto text-xs font-semibold">
                Bespoke property brokerage and intelligent advisory services to guide you at every stage.
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {services.map((service, idx) => (
                <Card key={idx} className="p-6 flex flex-col justify-between hover:shadow-md transition-shadow">
                  <div>
                    <span className="text-3xl mb-4 block">{service.icon}</span>
                    <h3 className="font-bold text-lg text-primary mb-2">{service.title}</h3>
                    <p className="text-xs text-muted leading-relaxed mb-6">{service.desc}</p>
                  </div>
                  <button 
                    onClick={() => handleLearnMore(service.title)}
                    className="w-full py-2 bg-muted text-primary text-xs font-bold rounded hover:bg-border transition-colors cursor-pointer uppercase tracking-wider"
                  >
                    Learn More
                  </button>
                </Card>
              ))}
            </div>
          </Container>
        </Section>
        
        {/* Testimonials */}
        <Section id="testimonials" background="muted">
          <Container>
            <div className="text-center mb-12">
              <h2 className="text-3xl font-extrabold text-primary mb-4">Client Testimonials</h2>
              <p className="text-muted max-w-2xl mx-auto text-xs font-semibold">
                Trusted by international property investors and family buyers worldwide.
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {Array.from({ length: 3 }).map((_, idx) => (
                <Card key={idx} className="p-6">
                  <div className="flex items-center gap-1 mb-4 text-accent">★★★★★</div>
                  <p className="text-xs text-muted leading-relaxed mb-6 font-semibold">
                    &ldquo;The AI Assistant matched my budget parameters instantly, generating a clean 20/80 breakdown and connecting me to a qualified Dubai Hills broker.&rdquo;
                  </p>
                  <div className="flex items-center gap-3 border-t border-border pt-4">
                    <div className="w-8 h-8 rounded-full bg-primary text-primary-foreground font-bold flex items-center justify-center text-xs">
                      M
                    </div>
                    <div>
                      <h4 className="font-bold text-sm text-primary">Michael S.</h4>
                      <span className="text-[10px] text-muted block font-semibold">USA Investor</span>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </Container>
        </Section>
        
        {/* FAQ Accordion */}
        <Section id="faq" background="default">
          <Container className="max-w-4xl">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-extrabold text-primary mb-4">Frequently Asked Questions</h2>
              <p className="text-muted max-w-2xl mx-auto text-xs font-semibold">
                Quick answers regarding properties, visa applications, and payment cycles.
              </p>
            </div>
            <div className="space-y-4">
              {faqs.map((faq, idx) => {
                const isOpen = openFaq === idx;
                return (
                  <div key={idx} className="border-b border-border pb-4">
                    <h3 
                      onClick={() => setOpenFaq(isOpen ? null : idx)}
                      className="font-bold text-primary mb-2 flex justify-between items-center text-sm cursor-pointer hover:text-accent transition-colors"
                    >
                      {faq.q}
                      <span className="text-xs font-bold text-muted">{isOpen ? "▲" : "▼"}</span>
                    </h3>
                    <div className={`grid transition-all duration-300 ease-in-out ${
                      isOpen ? "grid-rows-[1fr] opacity-100 mt-2" : "grid-rows-[0fr] opacity-0 overflow-hidden"
                    }`}>
                      <p className="text-xs text-muted leading-relaxed overflow-hidden">
                        {faq.a}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          </Container>
        </Section>
      </main>
      
      <Footer />
    </div>
  );
}
