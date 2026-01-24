import { Navbar } from "@/components/navbar"
import { HeroSection } from "@/components/hero-section"
import { FeaturesSection } from "@/components/features-section"
import { InstallationSection } from "@/components/installation-section"
import { CLISection } from "@/components/cli-section"
import { TUISection } from "@/components/tui-section"
import { AISection } from "@/components/ai-section"
import { LanguagesSection } from "@/components/languages-section"
import { RoadmapSection } from "@/components/roadmap-section"
import { FAQSection } from "@/components/faq-section"
import { Footer } from "@/components/footer"

export default function DocsPage() {
  return (
    <main className="min-h-screen bg-background">
      <Navbar />
      <HeroSection />
      <FeaturesSection />
      <InstallationSection />
      <CLISection />
      <TUISection />
      <AISection />
      <LanguagesSection />
      <RoadmapSection />
      <FAQSection />
      <Footer />
    </main>
  )
}
