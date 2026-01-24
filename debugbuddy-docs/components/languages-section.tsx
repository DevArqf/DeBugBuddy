"use client"

import { Check, Plus, Code2, FileCode, Braces, Hash, Coffee, Gem, FileType } from "lucide-react"
import { cn } from "@/lib/utils"

const languages = [
  { name: "Python", patterns: 45, status: "stable", abbr: "PY" },
  { name: "JavaScript", patterns: 32, status: "stable", abbr: "JS" },
  { name: "TypeScript", patterns: 28, status: "stable", abbr: "TS" },
  { name: "C/C++", patterns: 18, status: "stable", abbr: "C++" },
  { name: "PHP", patterns: 15, status: "stable", abbr: "PHP" },
  { name: "Java", patterns: 12, status: "new", abbr: "JV" },
  { name: "Ruby", patterns: 10, status: "new", abbr: "RB" },
]

const upcoming = [
  { name: "Go", version: "v0.5.0", quarter: "Q2 2026" },
  { name: "Rust", version: "v0.5.0", quarter: "Q2 2026" },
  { name: "Swift", version: "v0.6.0", quarter: "Q3 2026" },
  { name: "Kotlin", version: "v0.7.0", quarter: "Q3 2026" },
  { name: "C#", version: "v0.7.0", quarter: "Q3 2026" },
  { name: "Scala", version: "v0.9.0", quarter: "Q4 2026" },
  { name: "Elixir", version: "v0.9.0", quarter: "Q4 2026" },
]

function LanguageCard({ language }: { language: typeof languages[0] }) {
  return (
    <div className="group p-6 rounded-2xl bg-card border border-border hover:border-primary/30 transition-all duration-300 hover:shadow-[0_0_30px_var(--glow)]">
      <div className="flex items-start justify-between mb-4">
        <div className="w-14 h-14 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center group-hover:bg-primary/20 group-hover:border-primary/40 transition-all duration-300">
          <span className="text-lg font-bold font-mono text-primary">{language.abbr}</span>
        </div>
        {language.status === "new" && (
          <span className="text-xs font-medium px-2 py-1 rounded-full bg-primary/10 text-primary">
            New
          </span>
        )}
      </div>
      <h3 className="text-xl font-bold text-foreground mb-2 group-hover:text-primary transition-colors">
        {language.name}
      </h3>
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <Check className="w-4 h-4 text-primary" />
        <span>{language.patterns} error patterns</span>
      </div>
    </div>
  )
}

function UpcomingLanguage({ language }: { language: typeof upcoming[0] }) {
  return (
    <div className="flex items-center justify-between p-4 rounded-xl bg-muted/30 border border-border">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-muted flex items-center justify-center">
          <Plus className="w-4 h-4 text-muted-foreground" />
        </div>
        <span className="font-medium text-foreground">{language.name}</span>
      </div>
      <div className="flex items-center gap-3 text-sm">
        <span className="text-muted-foreground">{language.version}</span>
        <span className="px-2 py-0.5 rounded bg-muted text-muted-foreground text-xs">
          {language.quarter}
        </span>
      </div>
    </div>
  )
}

export function LanguagesSection() {
  const totalPatterns = languages.reduce((sum, lang) => sum + lang.patterns, 0)

  return (
    <section id="languages" className="relative py-32 overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-card/20 via-background to-card/20" />

      <div className="relative container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-6">
            <Code2 className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium text-primary">Language Support</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
            <span className="text-primary glow-text">{languages.length}</span>{" "}
            languages supported
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            With <strong className="text-foreground">{totalPatterns}+</strong> error patterns 
            and growing. More languages coming every release.
          </p>
        </div>

        {/* Current Languages */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          {languages.map((language) => (
            <LanguageCard key={language.name} language={language} />
          ))}
        </div>

        {/* Upcoming Languages */}
        <div className="max-w-3xl mx-auto">
          <h3 className="text-xl font-bold text-foreground mb-6 text-center">
            Coming Soon
          </h3>
          <div className="grid sm:grid-cols-2 gap-4">
            {upcoming.map((language) => (
              <UpcomingLanguage key={language.name} language={language} />
            ))}
          </div>
        </div>

        {/* Contribute CTA */}
        <div className="mt-16 text-center">
          <div className="inline-flex flex-col items-center p-8 rounded-2xl bg-card border border-border">
            <h3 className="text-xl font-bold text-foreground mb-2">
              Want to add a language?
            </h3>
            <p className="text-muted-foreground mb-4 max-w-md">
              DeBugBuddy is open source. Contribute new patterns or add support for your favorite language.
            </p>
            <a
              href="https://github.com/DevArqf/DeBugBuddy/blob/main/CONTRIBUTING.md"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-primary text-primary-foreground font-medium hover:bg-primary/90 transition-colors shadow-[0_0_20px_var(--glow)] hover:shadow-[0_0_30px_var(--glow)]"
            >
              Contribute on GitHub
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}
