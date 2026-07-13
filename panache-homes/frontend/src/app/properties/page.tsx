import React from "react";
import Navbar from "@/components/shared/Navbar";
import Footer from "@/components/shared/Footer";
import PropertyGallery from "@/components/landing/PropertyGallery";

export default function PropertiesPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-grow pt-24 bg-background">
        <PropertyGallery />
      </main>
      <Footer />
    </div>
  );
}
