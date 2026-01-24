"use client"

import { useState } from "react"
import { Bot, Sparkles, Shield, Zap, Copy, Check, ArrowRight, Lock } from "lucide-react"
import { cn } from "@/lib/utils"

const providers = [
  {
    id: "openai",
    name: "OpenAI",
    description: "GPT-4 and GPT-3.5 for powerful error analysis and suggestions.",
    configKey: "openai_api_key",
    color: "from-green-500 to-emerald-600",
    features: ["GPT-4 Turbo support", "Fast inference", "Detailed explanations"],
  },
  {
    id: "anthropic",
    name: "Anthropic",
    description: "Claude models for nuanced understanding and safer outputs.",
    configKey: "anthropic_api_key",
    color: "from-orange-500 to-amber-600",
    features: ["Claude 3 support", "Long context windows", "Thoughtful analysis"],
  },
  {
    id: "grok",
    name: "Grok (xAI)",
    description: "xAI's Grok model for fast, witty, and accurate debugging help.",
    configKey: "grok_api_key",
    color: "from-blue-500 to-indigo-600",
    features: ["Real-time knowledge", "Fast responses", "New in v0.4.0"],
    isNew: true,
  },
]

function ProviderCard({ 
  provider, 
  isActive, 
  onClick 
}: { 
  provider: typeof providers[0]
  isActive: boolean
  onClick: () => void
}) {
  return (
    <button
      onClick={onClick}
      className={cn(
        "relative w-full p-6 rounded-2xl text-left transition-all duration-500",
        "border overflow-hidden",
        isActive
          ? "bg-card border-primary/30 shadow-[0_0_40px_var(--glow)]"
          : "bg-card/50 border-border hover:border-primary/20"
      )}
    >
      {/* Background Gradient on Active */}
      {isActive && (
        <div className={cn(
          "absolute inset-0 opacity-10 bg-gradient-to-br",
          provider.color
        )} />
      )}

      <div className="relative">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className={cn(
              "w-12 h-12 rounded-xl flex items-center justify-center transition-all",
              isActive ? "bg-primary/20 border border-primary/30" : "bg-muted"
            )}>
              <Bot className={cn(
                "w-6 h-6 transition-colors",
                isActive ? "text-primary" : "text-muted-foreground"
              )} />
            </div>
            <div>
              <h3 className={cn(
                "font-bold text-lg transition-colors",
                isActive ? "text-primary" : "text-foreground"
              )}>
                {provider.name}
              </h3>
              {provider.isNew && (
                <span className="inline-flex items-center gap-1 text-xs text-primary bg-primary/10 px-2 py-0.5 rounded-full">
                  <Sparkles className="w-3 h-3" />
                  New
                </span>
              )}
            </div>
          </div>
          <div className={cn(
            "w-4 h-4 rounded-full border-2 transition-all",
            isActive ? "bg-primary border-primary" : "border-muted-foreground"
          )} />
        </div>

        <p className="text-muted-foreground text-sm mb-4">{provider.description}</p>

        <div className="flex flex-wrap gap-2">
          {provider.features.map((feature) => (
            <span 
              key={feature}
              className="text-xs px-2 py-1 rounded-md bg-muted/50 text-muted-foreground"
            >
              {feature}
            </span>
          ))}
        </div>
      </div>
    </button>
  )
}

export function AISection() {
  const [activeProvider, setActiveProvider] = useState(providers[0])
  const [copied, setCopied] = useState(false)

  const configCommand = `dbug config ai_provider ${activeProvider.id}\ndbug config ${activeProvider.configKey} YOUR_API_KEY`

  const copyConfig = () => {
    navigator.clipboard.writeText(configCommand)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <section id="ai" className="relative py-32 overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-background via-card/10 to-background" />

      <div className="relative container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-6">
            <Bot className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium text-primary">AI Integration</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
            <span className="text-primary glow-text">Optional</span>{" "}
            AI-powered explanations
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Enhance your debugging with AI providers. Completely optional — everything works locally by default.
          </p>
        </div>

        {/* Privacy Notice */}
        <div className="max-w-3xl mx-auto mb-12">
          <div className="flex items-start gap-4 p-6 rounded-2xl bg-primary/5 border border-primary/20">
            <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center flex-shrink-0">
              <Shield className="w-5 h-5 text-primary" />
            </div>
            <div>
              <h3 className="font-bold text-foreground mb-1">Privacy First</h3>
              <p className="text-muted-foreground text-sm">
                AI is <strong className="text-foreground">opt-in only</strong>. Without configuration, DeBugBuddy uses 
                local pattern matching with 150+ built-in patterns. Your code never leaves your machine unless you 
                explicitly enable AI mode.
              </p>
            </div>
          </div>
        </div>

        {/* Provider Selection */}
        <div className="grid lg:grid-cols-2 gap-8 max-w-6xl mx-auto">
          {/* Providers List */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-foreground mb-4">Choose a Provider</h3>
            {providers.map((provider) => (
              <ProviderCard
                key={provider.id}
                provider={provider}
                isActive={activeProvider.id === provider.id}
                onClick={() => setActiveProvider(provider)}
              />
            ))}
          </div>

          {/* Configuration */}
          <div className="lg:sticky lg:top-24 h-fit">
            <div className="p-6 md:p-8 rounded-2xl bg-card border border-border">
              <h3 className="text-xl font-bold text-foreground mb-6">
                Configure {activeProvider.name}
              </h3>

              {/* Steps */}
              <div className="space-y-6 mb-8">
                <div className="flex gap-4">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center">
                    <span className="text-sm font-bold text-primary">1</span>
                  </div>
                  <div>
                    <h4 className="font-medium text-foreground mb-1">Get an API Key</h4>
                    <p className="text-sm text-muted-foreground">
                      Visit the {activeProvider.name} website and create an API key from your account dashboard.
                    </p>
                  </div>
                </div>

                <div className="flex gap-4">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center">
                    <span className="text-sm font-bold text-primary">2</span>
                  </div>
                  <div>
                    <h4 className="font-medium text-foreground mb-1">Configure DeBugBuddy</h4>
                    <p className="text-sm text-muted-foreground mb-3">
                      Run these commands to set up your provider:
                    </p>
                    <div className="relative group">
                      <div className="p-4 rounded-xl bg-muted/50 border border-border font-mono text-sm">
                        <div className="text-primary mb-1">$ dbug config ai_provider {activeProvider.id}</div>
                        <div className="text-primary">$ dbug config {activeProvider.configKey} YOUR_KEY</div>
                      </div>
                      <button
                        onClick={copyConfig}
                        className="absolute top-3 right-3 p-2 rounded-lg bg-card hover:bg-muted transition-colors opacity-0 group-hover:opacity-100"
                      >
                        {copied ? <Check className="w-4 h-4 text-primary" /> : <Copy className="w-4 h-4 text-muted-foreground" />}
                      </button>
                    </div>
                  </div>
                </div>

                <div className="flex gap-4">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center">
                    <span className="text-sm font-bold text-primary">3</span>
                  </div>
                  <div>
                    <h4 className="font-medium text-foreground mb-1">Use AI-Enhanced Explanations</h4>
                    <p className="text-sm text-muted-foreground">
                      Add the <code className="px-1.5 py-0.5 rounded bg-muted text-primary">--ai</code> flag to any explain command:
                    </p>
                    <div className="mt-3 p-4 rounded-xl bg-muted/50 border border-border font-mono text-sm">
                      <span className="text-primary">$</span> dbug explain --ai
                    </div>
                  </div>
                </div>
              </div>

              {/* Security Note */}
              <div className="flex items-start gap-3 p-4 rounded-xl bg-muted/30 border border-border">
                <Lock className="w-4 h-4 text-primary mt-0.5" />
                <p className="text-xs text-muted-foreground">
                  API keys are stored locally in <code className="text-foreground">~/.debugbuddy/config.json</code>. 
                  They are never shared or transmitted except to your chosen AI provider.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
