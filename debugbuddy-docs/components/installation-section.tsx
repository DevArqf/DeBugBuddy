"use client"

import { useState } from "react"
import { Terminal, Copy, Check, Package, Rocket, Settings, CheckCircle2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

const steps = [
  {
    number: "01",
    title: "Install the Package",
    description: "Install DeBugBuddy using pip. It works with Python 3.8+ and has minimal dependencies.",
    command: "pip install debugbuddy-cli",
    icon: Package,
  },
  {
    number: "02",
    title: "Run Your First Command",
    description: "After your Python script encounters an error, simply run dbug explain to get instant explanations.",
    command: "python script.py && dbug explain",
    icon: Terminal,
  },
  {
    number: "03",
    title: "Launch the TUI",
    description: "For a full-screen interactive experience, launch the Textual-based GUI with a single command.",
    command: "debugbuddy",
    icon: Rocket,
  },
  {
    number: "04",
    title: "Configure (Optional)",
    description: "Customize your experience with AI providers, history settings, and more.",
    command: "dbug config ai_provider grok",
    icon: Settings,
  },
]

function CodeBlock({ code, language = "bash" }: { code: string; language?: string }) {
  const [copied, setCopied] = useState(false)

  const copyCode = () => {
    navigator.clipboard.writeText(code)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="relative group">
      <div className="absolute -inset-0.5 bg-gradient-to-r from-primary/50 to-accent/50 rounded-xl blur opacity-0 group-hover:opacity-30 transition-opacity duration-500" />
      <div className="relative bg-card border border-border rounded-xl overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-2 bg-muted/50 border-b border-border">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500/60" />
            <div className="w-3 h-3 rounded-full bg-yellow-500/60" />
            <div className="w-3 h-3 rounded-full bg-green-500/60" />
          </div>
          <span className="text-xs text-muted-foreground font-mono">{language}</span>
        </div>
        {/* Code */}
        <div className="p-4 font-mono text-sm overflow-x-auto">
          <div className="flex items-center gap-3">
            <span className="text-primary select-none">$</span>
            <code className="text-foreground">{code}</code>
          </div>
        </div>
        {/* Copy Button */}
        <button
          onClick={copyCode}
          className="absolute top-12 right-4 p-2 rounded-lg bg-muted/50 hover:bg-muted transition-colors opacity-0 group-hover:opacity-100"
          aria-label="Copy code"
        >
          {copied ? (
            <Check className="w-4 h-4 text-primary" />
          ) : (
            <Copy className="w-4 h-4 text-muted-foreground" />
          )}
        </button>
      </div>
    </div>
  )
}

export function InstallationSection() {
  return (
    <section id="installation" className="relative py-32 overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-card/20 via-background to-card/20" />

      <div className="relative container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-6">
            <Package className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium text-primary">Installation</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
            Get started in{" "}
            <span className="text-primary glow-text">seconds</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            A simple pip install is all you need to start debugging smarter.
          </p>
        </div>

        {/* Steps */}
        <div className="max-w-4xl mx-auto space-y-8">
          {steps.map((step, index) => (
            <div 
              key={step.number}
              className="group relative"
            >
              {/* Connection Line */}
              {index < steps.length - 1 && (
                <div className="absolute left-7 top-20 w-0.5 h-16 bg-gradient-to-b from-primary/50 to-transparent" />
              )}

              <div className="flex gap-6">
                {/* Step Number */}
                <div className="flex-shrink-0">
                  <div className="w-14 h-14 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center group-hover:border-primary/50 group-hover:shadow-[0_0_20px_var(--glow)] transition-all duration-300">
                    <span className="text-lg font-bold text-primary font-mono">{step.number}</span>
                  </div>
                </div>

                {/* Content */}
                <div className="flex-1 pb-8">
                  <div className="flex items-center gap-3 mb-2">
                    <step.icon className="w-5 h-5 text-primary" />
                    <h3 className="text-xl font-bold text-foreground">{step.title}</h3>
                  </div>
                  <p className="text-muted-foreground mb-4 leading-relaxed">
                    {step.description}
                  </p>
                  <CodeBlock code={step.command} />
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Quick Start Example */}
        <div className="mt-20 max-w-4xl mx-auto">
          <div className="p-6 md:p-8 rounded-2xl bg-card border border-border">
            <div className="flex items-center gap-3 mb-6">
              <CheckCircle2 className="w-6 h-6 text-primary" />
              <h3 className="text-xl font-bold text-foreground">Quick Start Example</h3>
            </div>
            
            <div className="space-y-6">
              <div>
                <p className="text-sm text-muted-foreground mb-2">1. Create a test file with an error:</p>
                <CodeBlock code="echo 'print(undefined_var)' > test.py" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground mb-2">2. Run it and explain the error:</p>
                <CodeBlock code="python test.py; dbug explain" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground mb-2">3. Or predict errors before running:</p>
                <CodeBlock code="dbug predict test.py" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
