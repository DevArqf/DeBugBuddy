"use client"

import { useState } from "react"
import { Monitor, Terminal, Code2, Search, History, Settings, GitBranch, Eye, Brain, ChevronRight, Sparkles } from "lucide-react"
import { cn } from "@/lib/utils"

const tuiScreens = [
  {
    id: "dashboard",
    name: "Dashboard",
    icon: Monitor,
    description: "Central hub showing recent errors, quick actions, and system status.",
    features: ["Recent error list", "Quick action buttons", "System health indicator", "Keyboard shortcuts"],
  },
  {
    id: "explain",
    name: "Explain",
    icon: Code2,
    description: "Detailed error explanations with syntax highlighting and suggested fixes.",
    features: ["Syntax-highlighted output", "Step-by-step fixes", "Related examples", "AI enhancement toggle"],
  },
  {
    id: "predict",
    name: "Predict",
    icon: Brain,
    description: "Scan files for potential issues with real-time results and severity levels.",
    features: ["File browser", "Real-time scanning", "Severity indicators", "One-click fixes"],
  },
  {
    id: "history",
    name: "History",
    icon: History,
    description: "Browse and search your debugging history with analytics.",
    features: ["Searchable list", "Filter by language", "Statistics view", "Export options"],
  },
  {
    id: "search",
    name: "Search",
    icon: Search,
    description: "Search through patterns and history with powerful filters.",
    features: ["Fuzzy search", "Pattern matching", "Filter options", "Quick navigation"],
  },
  {
    id: "github",
    name: "GitHub",
    icon: GitBranch,
    description: "Search GitHub issues directly from the TUI interface.",
    features: ["Issue search", "Repo filtering", "Preview pane", "Open in browser"],
  },
  {
    id: "watch",
    name: "Watch",
    icon: Eye,
    description: "Monitor files for changes with live error prediction.",
    features: ["File watchers", "Live updates", "Notification log", "Auto-fix suggestions"],
  },
  {
    id: "config",
    name: "Config",
    icon: Settings,
    description: "Manage all settings with an intuitive interface.",
    features: ["Visual editor", "API key management", "Theme options", "Export/Import"],
  },
]

function TUIPreview({ activeScreen }: { activeScreen: typeof tuiScreens[0] }) {
  return (
    <div className="relative overflow-hidden rounded-2xl border border-border bg-card shadow-2xl">
      {/* Window Chrome */}
      <div className="flex items-center gap-2 px-4 py-3 bg-muted/50 border-b border-border">
        <div className="w-3 h-3 rounded-full bg-red-500/60" />
        <div className="w-3 h-3 rounded-full bg-yellow-500/60" />
        <div className="w-3 h-3 rounded-full bg-green-500/60" />
        <span className="ml-4 text-sm text-muted-foreground font-mono">DeBugBuddy TUI</span>
      </div>

      {/* TUI Interface */}
      <div className="flex h-[450px]">
        {/* Sidebar */}
        <div className="w-48 border-r border-border bg-muted/30 p-2 space-y-1">
          {tuiScreens.map((screen) => (
            <div
              key={screen.id}
              className={cn(
                "flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all",
                activeScreen.id === screen.id
                  ? "bg-primary/20 text-primary"
                  : "text-muted-foreground hover:text-foreground hover:bg-muted"
              )}
            >
              <screen.icon className="w-4 h-4" />
              <span>{screen.name}</span>
            </div>
          ))}
        </div>

        {/* Main Content */}
        <div className="flex-1 p-6 overflow-hidden">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-lg bg-primary/10 border border-primary/20 flex items-center justify-center">
              <activeScreen.icon className="w-5 h-5 text-primary" />
            </div>
            <div>
              <h4 className="font-bold text-foreground">{activeScreen.name}</h4>
              <p className="text-xs text-muted-foreground">{activeScreen.description}</p>
            </div>
          </div>

          {/* Mock Content based on screen */}
          {activeScreen.id === "explain" && (
            <div className="space-y-4">
              <div className="p-4 rounded-lg bg-destructive/10 border border-destructive/20">
                <div className="text-sm font-mono text-destructive">
                  NameError: name {"'undefined_var'"} is not defined
                </div>
              </div>
              <div className="p-4 rounded-lg bg-muted/50 border border-border">
                <div className="text-sm text-foreground mb-2 font-medium">Explanation:</div>
                <div className="text-sm text-muted-foreground">
                  {"You're trying to use a variable that hasn't been defined..."}
                </div>
              </div>
              <div className="p-4 rounded-lg bg-primary/5 border border-primary/20">
                <div className="text-sm text-primary mb-2 font-medium">Suggested Fix:</div>
                <div className="text-sm font-mono text-foreground">
                  undefined_var = {"''"} # Define the variable first
                </div>
              </div>
            </div>
          )}

          {activeScreen.id === "predict" && (
            <div className="space-y-3">
              {[
                { line: 15, type: "warning", msg: "Potential IndexError" },
                { line: 23, type: "warning", msg: "Possible TypeError" },
                { line: 31, type: "success", msg: "Good practice detected" },
              ].map((item, i) => (
                <div key={i} className={cn(
                  "flex items-center gap-3 p-3 rounded-lg border",
                  item.type === "warning" 
                    ? "bg-yellow-500/5 border-yellow-500/20" 
                    : "bg-primary/5 border-primary/20"
                )}>
                  <span className={cn(
                    "text-xs font-mono px-2 py-1 rounded",
                    item.type === "warning" ? "bg-yellow-500/10 text-yellow-500" : "bg-primary/10 text-primary"
                  )}>
                    Line {item.line}
                  </span>
                  <span className="text-sm text-foreground">{item.msg}</span>
                </div>
              ))}
            </div>
          )}

          {activeScreen.id === "history" && (
            <div className="space-y-3">
              {[
                { error: "TypeError", lang: "Python", time: "2 min ago" },
                { error: "ReferenceError", lang: "JavaScript", time: "15 min ago" },
                { error: "NameError", lang: "Python", time: "1 hour ago" },
              ].map((item, i) => (
                <div key={i} className="flex items-center justify-between p-3 rounded-lg bg-muted/30 border border-border">
                  <div className="flex items-center gap-3">
                    <span className="text-sm font-medium text-foreground">{item.error}</span>
                    <span className="text-xs px-2 py-0.5 rounded bg-primary/10 text-primary">{item.lang}</span>
                  </div>
                  <span className="text-xs text-muted-foreground">{item.time}</span>
                </div>
              ))}
            </div>
          )}

          {activeScreen.id === "dashboard" && (
            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 rounded-lg bg-muted/30 border border-border">
                <div className="text-2xl font-bold text-primary mb-1">47</div>
                <div className="text-xs text-muted-foreground">Total Errors</div>
              </div>
              <div className="p-4 rounded-lg bg-muted/30 border border-border">
                <div className="text-2xl font-bold text-foreground mb-1">3</div>
                <div className="text-xs text-muted-foreground">Languages</div>
              </div>
              <div className="col-span-2 p-4 rounded-lg bg-muted/30 border border-border">
                <div className="text-sm font-medium text-foreground mb-2">Recent</div>
                <div className="text-xs text-muted-foreground">TypeError: Cannot read property...</div>
              </div>
            </div>
          )}

          {(activeScreen.id === "search" || activeScreen.id === "github" || activeScreen.id === "watch" || activeScreen.id === "config") && (
            <div className="space-y-4">
              <div className="flex items-center gap-2 p-3 rounded-lg bg-muted/50 border border-border">
                <Search className="w-4 h-4 text-muted-foreground" />
                <span className="text-sm text-muted-foreground">Search or type a command...</span>
              </div>
              <div className="grid grid-cols-2 gap-3">
                {activeScreen.features.map((feature, i) => (
                  <div key={i} className="flex items-center gap-2 p-3 rounded-lg bg-muted/30 border border-border">
                    <div className="w-1.5 h-1.5 rounded-full bg-primary" />
                    <span className="text-sm text-muted-foreground">{feature}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Status Bar */}
      <div className="flex items-center justify-between px-4 py-2 bg-muted/30 border-t border-border text-xs text-muted-foreground font-mono">
        <span>Press ? for help</span>
        <span>q: quit | Tab: navigate | Enter: select</span>
      </div>
    </div>
  )
}

export function TUISection() {
  const [activeScreen, setActiveScreen] = useState(tuiScreens[0])

  return (
    <section id="tui" className="relative py-32 overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-card/20 via-background to-card/20" />

      <div className="relative container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-6">
            <Monitor className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium text-primary">Textual GUI</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
            A beautiful{" "}
            <span className="text-primary glow-text">terminal UI</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Full-screen interface powered by Textual. Navigate between views without leaving your terminal.
          </p>
        </div>

        {/* Launch Command */}
        <div className="flex justify-center mb-12">
          <div className="inline-flex items-center gap-3 px-6 py-3 rounded-xl bg-card border border-border font-mono">
            <Terminal className="w-5 h-5 text-primary" />
            <span className="text-muted-foreground">$</span>
            <span className="text-foreground font-medium">debugbuddy</span>
            <span className="text-muted-foreground ml-2">← Launch the TUI</span>
          </div>
        </div>

        {/* Screen Selector */}
        <div className="flex flex-wrap justify-center gap-3 mb-10">
          {tuiScreens.map((screen) => (
            <button
              key={screen.id}
              onClick={() => setActiveScreen(screen)}
              className={cn(
                "flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300",
                activeScreen.id === screen.id
                  ? "bg-primary/20 text-primary border border-primary/30"
                  : "bg-card/50 text-muted-foreground border border-border hover:border-primary/20 hover:text-foreground"
              )}
            >
              <screen.icon className="w-4 h-4" />
              {screen.name}
            </button>
          ))}
        </div>

        {/* TUI Preview */}
        <div className="max-w-5xl mx-auto">
          <TUIPreview activeScreen={activeScreen} />
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mt-16">
          {[
            { icon: Sparkles, title: "Keyboard-First", desc: "Navigate entirely with keyboard shortcuts" },
            { icon: Monitor, title: "Split Panels", desc: "View multiple sections simultaneously" },
            { icon: Terminal, title: "Integrated", desc: "No context switching needed" },
            { icon: Code2, title: "Syntax Highlighting", desc: "Beautiful code display built-in" },
          ].map((feature) => (
            <div key={feature.title} className="p-6 rounded-xl bg-card/50 border border-border">
              <feature.icon className="w-8 h-8 text-primary mb-3" />
              <h4 className="font-bold text-foreground mb-1">{feature.title}</h4>
              <p className="text-sm text-muted-foreground">{feature.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
