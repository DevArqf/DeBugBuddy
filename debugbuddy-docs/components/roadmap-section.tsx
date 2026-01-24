"use client"

import { Check, Circle, Clock, Rocket, Calendar, Code2, Bot, Globe, MessageSquare } from "lucide-react"
import { cn } from "@/lib/utils"

const roadmap = [
  {
    version: "v0.2.0",
    status: "completed",
    quarter: "Released",
    title: "Language Expansion & AI",
    features: [
      "TypeScript, C, and PHP support",
      "AI provider integration",
      "Enhanced pattern matching",
    ],
  },
  {
    version: "v0.3.0",
    status: "completed",
    quarter: "Released",
    title: "Prediction & GitHub",
    features: [
      "Error prediction engine",
      "Custom pattern training",
      "GitHub issue integration",
    ],
  },
  {
    version: "v0.4.0",
    status: "completed",
    quarter: "Q1 2026",
    title: "Java, Ruby & Grok",
    features: [
      "Java and Ruby language support",
      "ML prediction optimization",
      "Basic error analytics in CLI",
      "Grok as AI provider",
    ],
    isCurrent: true,
  },
  {
    version: "v0.5.0",
    status: "upcoming",
    quarter: "Q2 2026",
    title: "Go, Rust & IDE Integration",
    features: [
      "Go and Rust language support",
      "VS Code extension",
      "Multi-file project scanning",
      "Mistral AI provider",
    ],
  },
  {
    version: "v0.6.0",
    status: "upcoming",
    quarter: "Q3 2026",
    title: "Analytics Dashboard",
    features: [
      "Web-based analytics dashboard",
      "Swift language support",
      "Export/import patterns",
      "Performance benchmarks",
    ],
  },
  {
    version: "v0.7.0",
    status: "upcoming",
    quarter: "Q3 2026",
    title: "Team Collaboration",
    features: [
      "Kotlin and C# support",
      "Slack bot integration",
      "Interactive charts",
      "Shareable reports",
    ],
  },
  {
    version: "v0.8.0",
    status: "upcoming",
    quarter: "Q4 2026",
    title: "Discord & Cloud",
    features: [
      "Discord bot integration",
      "Cloud sync (opt-in)",
      "Auto-suggest fixes from history",
      "User authentication for dashboard",
    ],
  },
  {
    version: "v0.9.0",
    status: "upcoming",
    quarter: "Q4 2026",
    title: "Scale & Polish",
    features: [
      "Scala and Elixir support",
      "Full integration testing",
      "Sub-1s startup time",
      "User feedback system",
    ],
  },
  {
    version: "v1.0.0",
    status: "upcoming",
    quarter: "Q1 2027",
    title: "Production Ready",
    features: [
      "12+ language support",
      "Full-featured dashboard",
      "Slack & Discord bots",
      "Enterprise features",
    ],
    isMilestone: true,
  },
]

function RoadmapItem({ item, index }: { item: typeof roadmap[0]; index: number }) {
  const isCompleted = item.status === "completed"
  const isCurrent = item.isCurrent
  const isMilestone = item.isMilestone

  return (
    <div className="relative flex gap-6">
      {/* Timeline Line */}
      {index < roadmap.length - 1 && (
        <div className={cn(
          "absolute left-6 top-14 w-0.5 h-full -translate-x-1/2",
          isCompleted ? "bg-primary" : "bg-border"
        )} />
      )}

      {/* Status Icon */}
      <div className="relative flex-shrink-0">
        <div className={cn(
          "w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-300",
          isCompleted 
            ? "bg-primary/20 border border-primary/30" 
            : isCurrent
              ? "bg-primary/10 border border-primary/20 animate-pulse"
              : isMilestone
                ? "bg-accent/10 border border-accent/20"
                : "bg-muted border border-border"
        )}>
          {isCompleted ? (
            <Check className="w-5 h-5 text-primary" />
          ) : isCurrent ? (
            <Clock className="w-5 h-5 text-primary" />
          ) : isMilestone ? (
            <Rocket className="w-5 h-5 text-accent" />
          ) : (
            <Circle className="w-5 h-5 text-muted-foreground" />
          )}
        </div>
      </div>

      {/* Content */}
      <div className={cn(
        "flex-1 pb-12 group",
        index === roadmap.length - 1 && "pb-0"
      )}>
        <div className={cn(
          "p-6 rounded-2xl border transition-all duration-300",
          isCompleted
            ? "bg-card/50 border-primary/20"
            : isCurrent
              ? "bg-primary/5 border-primary/30 shadow-[0_0_30px_var(--glow)]"
              : isMilestone
                ? "bg-accent/5 border-accent/20"
                : "bg-card/30 border-border hover:border-primary/20"
        )}>
          <div className="flex flex-wrap items-center gap-3 mb-3">
            <span className={cn(
              "text-lg font-bold font-mono",
              isCompleted || isCurrent ? "text-primary" : isMilestone ? "text-accent" : "text-foreground"
            )}>
              {item.version}
            </span>
            <span className={cn(
              "text-xs px-2 py-1 rounded-full",
              isCompleted
                ? "bg-primary/10 text-primary"
                : isCurrent
                  ? "bg-primary/20 text-primary"
                  : "bg-muted text-muted-foreground"
            )}>
              {item.quarter}
            </span>
            {isCurrent && (
              <span className="text-xs px-2 py-1 rounded-full bg-primary text-primary-foreground animate-pulse">
                Current
              </span>
            )}
            {isMilestone && (
              <span className="text-xs px-2 py-1 rounded-full bg-accent/20 text-accent">
                Milestone
              </span>
            )}
          </div>

          <h3 className={cn(
            "text-xl font-bold mb-3",
            isCompleted || isCurrent ? "text-foreground" : "text-muted-foreground"
          )}>
            {item.title}
          </h3>

          <ul className="space-y-2">
            {item.features.map((feature, i) => (
              <li key={i} className="flex items-start gap-2">
                <div className={cn(
                  "w-1.5 h-1.5 rounded-full mt-2",
                  isCompleted ? "bg-primary" : "bg-muted-foreground"
                )} />
                <span className={cn(
                  "text-sm",
                  isCompleted || isCurrent ? "text-muted-foreground" : "text-muted-foreground/70"
                )}>
                  {feature}
                </span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  )
}

export function RoadmapSection() {
  return (
    <section id="roadmap" className="relative py-32 overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-background via-card/10 to-background" />

      <div className="relative container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-6">
            <Calendar className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium text-primary">Roadmap</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
            Building the{" "}
            <span className="text-primary glow-text">future</span>{" "}
            of debugging
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Our journey to v1.0.0 — with new languages, integrations, and features every release.
          </p>
        </div>

        {/* Legend */}
        <div className="flex flex-wrap justify-center gap-6 mb-12">
          {[
            { icon: Check, label: "Completed", color: "text-primary" },
            { icon: Clock, label: "In Progress", color: "text-primary" },
            { icon: Circle, label: "Planned", color: "text-muted-foreground" },
            { icon: Rocket, label: "Milestone", color: "text-accent" },
          ].map((item) => (
            <div key={item.label} className="flex items-center gap-2 text-sm">
              <item.icon className={cn("w-4 h-4", item.color)} />
              <span className="text-muted-foreground">{item.label}</span>
            </div>
          ))}
        </div>

        {/* Timeline */}
        <div className="max-w-3xl mx-auto">
          {roadmap.map((item, index) => (
            <RoadmapItem key={item.version} item={item} index={index} />
          ))}
        </div>

        {/* Note */}
        <div className="mt-12 text-center">
          <p className="text-sm text-muted-foreground">
            <strong>Q</strong> stands for quarter: Q1 (Jan-Mar), Q2 (Apr-Jun), Q3 (Jul-Sep), Q4 (Oct-Dec)
          </p>
        </div>
      </div>
    </section>
  )
}
