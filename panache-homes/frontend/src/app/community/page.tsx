import React from "react";
import Navbar from "@/components/shared/Navbar";
import Footer from "@/components/shared/Footer";
import ExploreMap from "@/components/landing/ExploreMap";

export default function CommunityPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-grow pt-24 bg-background">
        <ExploreMap />
      </main>
      <Footer />
    </div>
  );
}
