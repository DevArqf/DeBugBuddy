"use client"

import { useRef } from "react"
import { Bug, Zap, Shield, BarChart3, Terminal, GitBranch, Search, Settings, History, Cpu } from "lucide-react"
import { cn } from "@/lib/utils"

const features = [
  {
    icon: Bug,
    title: "Explain Errors Instantly",
    description: "Get plain-English explanations with fixes and examples. No more deciphering cryptic stack traces or searching through endless forum posts.",
    color: "from-emerald-500 to-green-600",
    details: [
      "Automatic language detection",
      "Context-aware explanations",
      "Code fix suggestions",
      "Example solutions included"
    ]
  },
  {
    icon: Zap,
    title: "Predict Issues",
    description: "Static checks, pattern scans, and optional ML prediction catch bugs before they crash your program. Write better code proactively.",
    color: "from-green-500 to-teal-600",
    details: [
      "150+ error patterns",
      "ML-powered predictions",
      "Multi-file scanning",
      "Watch mode for real-time feedback"
    ]
  },
  {
    icon: Shield,
    title: "Local-First Privacy",
    description: "Everything stays on your machine unless you explicitly opt into AI mode. Your code, your errors, your privacy.",
    color: "from-teal-500 to-cyan-600",
    details: [
      "No data collection",
      "Offline-first design",
      "Optional AI enhancement",
      "Local history storage"
    ]
  },
  {
    icon: BarChart3,
    title: "History Analytics",
    description: "Track frequent errors and languages over time. Identify patterns in your debugging workflow and improve your coding habits.",
    color: "from-cyan-500 to-emerald-600",
    details: [
      "Error frequency tracking",
      "Language statistics",
      "Time-based analytics",
      "Searchable history"
    ]
  },
  {
    icon: Terminal,
    title: "Powerful CLI",
    description: "Full-featured command-line interface with intuitive commands for explaining, predicting, watching, and searching.",
    color: "from-emerald-400 to-green-500",
    details: [
      "dbug explain",
      "dbug predict",
      "dbug watch",
      "dbug search"
    ]
  },
  {
    icon: GitBranch,
    title: "GitHub Integration",
    description: "Search GitHub issues for similar errors, with repo scoping and exact matching for precision.",
    color: "from-green-400 to-teal-500",
    details: [
      "Issue search",
      "Repo scoping",
      "Exact matching",
      "Closed issues support"
    ]
  },
]

function FeatureCard({ feature, index }: { feature: typeof features[0]; index: number }) {
  return (
    <div 
      className="group relative p-6 rounded-2xl bg-card border border-border hover:border-primary/30 transition-all duration-500 hover:shadow-[0_0_40px_var(--glow)] overflow-hidden"
      style={{ animationDelay: `${index * 100}ms` }}
    >
      {/* Background Gradient */}
      <div className={cn(
        "absolute inset-0 opacity-0 group-hover:opacity-10 transition-opacity duration-500 bg-gradient-to-br",
        feature.color
      )} />
      
      {/* Icon */}
      <div className="relative mb-4">
        <div className="w-14 h-14 rounded-xl bg-primary/10 flex items-center justify-center border border-primary/20 group-hover:border-primary/40 transition-all duration-300 group-hover:shadow-[0_0_20px_var(--glow)]">
          <feature.icon className="w-7 h-7 text-primary group-hover:scale-110 transition-transform duration-300" />
        </div>
      </div>

      {/* Content */}
      <h3 className="text-xl font-bold text-foreground mb-2 group-hover:text-primary transition-colors duration-300">
        {feature.title}
      </h3>
      <p className="text-muted-foreground mb-4 leading-relaxed">
        {feature.description}
      </p>

      {/* Details */}
      <ul className="space-y-2">
        {feature.details.map((detail, i) => (
          <li key={i} className="flex items-center gap-2 text-sm">
            <div className="w-1.5 h-1.5 rounded-full bg-primary" />
            <span className="text-muted-foreground group-hover:text-foreground transition-colors duration-300">
              {detail}
            </span>
          </li>
        ))}
      </ul>

      {/* Hover Line */}
      <div className="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-primary to-accent group-hover:w-full transition-all duration-500" />
    </div>
  )
}

export function FeaturesSection() {
  return (
    <section id="features" className="relative py-32 overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-background via-card/20 to-background" />
      
      {/* Grid Pattern */}
      <div className="absolute inset-0 opacity-5" style={{
        backgroundImage: `linear-gradient(var(--primary) 1px, transparent 1px), linear-gradient(90deg, var(--primary) 1px, transparent 1px)`,
        backgroundSize: "60px 60px"
      }} />

      <div className="relative container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-6">
            <Cpu className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium text-primary">Core Features</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
            Everything you need to{" "}
            <span className="text-primary glow-text">debug smarter</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            A comprehensive toolkit for understanding, predicting, and learning from your errors.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <FeatureCard key={feature.title} feature={feature} index={index} />
          ))}
        </div>

        {/* Stats */}
        <div className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-6">
          {[
            { value: "150+", label: "Error Patterns" },
            { value: "7+", label: "Languages" },
            { value: "3", label: "AI Providers" },
            { value: "100%", label: "Open Source" },
          ].map((stat, index) => (
            <div 
              key={stat.label}
              className="text-center p-6 rounded-xl bg-card/50 border border-border"
            >
              <div className="text-4xl md:text-5xl font-bold text-primary glow-text mb-2">
                {stat.value}
              </div>
              <div className="text-muted-foreground">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
