"use client"

import { useState } from "react"
import { Terminal, Copy, Check, ChevronRight, Code2, Search, Eye, History, Settings, GitBranch, Brain, FileSearch } from "lucide-react"
import { cn } from "@/lib/utils"

const commands = [
  {
    name: "explain",
    syntax: "dbug explain [options]",
    description: "Explain the most recent error message in plain English with fixes and examples.",
    icon: Code2,
    options: [
      { flag: "--ai", description: "Use AI provider for enhanced explanations" },
      { flag: "--verbose", description: "Show detailed stack trace analysis" },
      { flag: "--lang <language>", description: "Override detected language" },
    ],
    example: "dbug explain --ai",
    output: `╔══════════════════════════════════════════════════════════════╗
║  DeBugBuddy - Error Explanation                               ║
╠══════════════════════════════════════════════════════════════╣
║  Error: NameError: name 'undefined_var' is not defined       ║
║                                                               ║
║  Explanation:                                                 ║
║  You're trying to use a variable 'undefined_var' that        ║
║  hasn't been defined yet in your code.                       ║
║                                                               ║
║  Fix:                                                         ║
║  • Define the variable before using it                       ║
║  • Check for typos in the variable name                      ║
║  • Ensure the variable is in scope                           ║
╚══════════════════════════════════════════════════════════════╝`
  },
  {
    name: "predict",
    syntax: "dbug predict <file> [options]",
    description: "Scan a file for potential errors before running. Uses pattern matching and optional ML.",
    icon: Brain,
    options: [
      { flag: "--ml", description: "Enable ML-powered prediction" },
      { flag: "--strict", description: "Report all potential issues" },
      { flag: "--json", description: "Output results as JSON" },
    ],
    example: "dbug predict app.py --ml",
    output: `Scanning: app.py
───────────────────────────────────────
⚠  Line 15: Potential IndexError - array access without bounds check
⚠  Line 23: Possible TypeError - mixing str and int operations
✓  Line 31: Pattern match: null check before use (good practice)
───────────────────────────────────────
Found 2 potential issues, 1 good practice`
  },
  {
    name: "watch",
    syntax: "dbug watch <file|directory> [options]",
    description: "Watch files for changes and automatically predict errors in real-time.",
    icon: Eye,
    options: [
      { flag: "--recursive", description: "Watch directories recursively" },
      { flag: "--pattern <glob>", description: "File pattern to watch (e.g., '*.py')" },
      { flag: "--notify", description: "Show desktop notifications" },
    ],
    example: "dbug watch ./src --recursive --pattern '*.py'",
    output: `👁  Watching: ./src/**/*.py
───────────────────────────────────────
[14:32:15] Change detected: src/utils.py
           ⚠ 1 potential issue found
[14:32:47] Change detected: src/main.py  
           ✓ No issues detected`
  },
  {
    name: "history",
    syntax: "dbug history [options]",
    description: "View your error history with statistics and analytics.",
    icon: History,
    options: [
      { flag: "--stats", description: "Show error statistics" },
      { flag: "--limit <n>", description: "Limit results to n entries" },
      { flag: "--lang <language>", description: "Filter by language" },
      { flag: "--export <file>", description: "Export history to JSON" },
    ],
    example: "dbug history --stats",
    output: `╔══════════════════════════════════════════════════════════════╗
║  Error History Statistics                                     ║
╠══════════════════════════════════════════════════════════════╣
║  Total Errors: 47                                             ║
║                                                               ║
║  By Language:                                                 ║
║  ████████████████████░░░░░  Python      68%                  ║
║  ███████░░░░░░░░░░░░░░░░░░  JavaScript  22%                  ║
║  ███░░░░░░░░░░░░░░░░░░░░░░  TypeScript  10%                  ║
║                                                               ║
║  Most Common:                                                 ║
║  1. TypeError (12)  2. NameError (8)  3. SyntaxError (6)     ║
╚══════════════════════════════════════════════════════════════╝`
  },
  {
    name: "search",
    syntax: "dbug search <query> [options]",
    description: "Search through error patterns and your history for similar issues.",
    icon: Search,
    options: [
      { flag: "--patterns", description: "Search built-in patterns only" },
      { flag: "--history", description: "Search history only" },
      { flag: "--exact", description: "Exact match only" },
    ],
    example: "dbug search 'TypeError' --patterns",
    output: `Found 23 matching patterns:
───────────────────────────────────────
[PY001] TypeError: unsupported operand type(s)
[PY002] TypeError: 'NoneType' object is not subscriptable
[PY003] TypeError: can only concatenate str to str
[JS001] TypeError: Cannot read property of undefined
[JS002] TypeError: X is not a function
...`
  },
  {
    name: "github",
    syntax: "dbug github search <query> [options]",
    description: "Search GitHub issues for similar errors with repo scoping.",
    icon: GitBranch,
    options: [
      { flag: "--repo <owner/repo>", description: "Scope to specific repository" },
      { flag: "--exact", description: "Use exact matching" },
      { flag: "--include-closed", description: "Include closed issues" },
      { flag: "-l <language>", description: "Filter by language" },
    ],
    example: 'dbug github search "TypeError" -l python --repo django/django',
    output: `GitHub Issues Search Results
───────────────────────────────────────
#12345 - TypeError when using async views (closed)
        django/django • 23 comments • ✓ resolved
        
#12280 - TypeError in template rendering (open)
        django/django • 8 comments
        
#12198 - TypeError with custom middleware (closed)
        django/django • 15 comments • ✓ resolved`
  },
  {
    name: "config",
    syntax: "dbug config <key> [value]",
    description: "View and manage DeBugBuddy configuration settings.",
    icon: Settings,
    options: [
      { flag: "--list", description: "List all settings" },
      { flag: "--reset", description: "Reset to defaults" },
    ],
    example: "dbug config ai_provider grok",
    output: `Configuration updated:
───────────────────────────────────────
ai_provider: grok ✓

Current settings:
• ai_provider: grok
• use_ml_prediction: true
• max_history: 1000
• grok_api_key: ********...`
  },
  {
    name: "train",
    syntax: "dbug train [options]",
    description: "Train custom patterns or ML models with your own error data.",
    icon: FileSearch,
    options: [
      { flag: "--patterns <file>", description: "Load custom patterns from JSON" },
      { flag: "--ml", description: "Train ML model on history" },
      { flag: "--export <file>", description: "Export trained model" },
    ],
    example: "dbug train --patterns custom_patterns.json",
    output: `Training custom patterns...
───────────────────────────────────────
Loaded: 15 custom patterns
Validated: ✓ All patterns valid
Merged: ✓ Added to pattern library

Total patterns available: 165`
  },
]

function CommandCard({ command, isActive, onClick }: { 
  command: typeof commands[0]
  isActive: boolean
  onClick: () => void 
}) {
  return (
    <button
      onClick={onClick}
      className={cn(
        "w-full flex items-center gap-3 p-4 rounded-xl text-left transition-all duration-300",
        isActive 
          ? "bg-primary/10 border border-primary/30 shadow-[0_0_20px_var(--glow)]" 
          : "bg-card/50 border border-border hover:border-primary/20 hover:bg-card"
      )}
    >
      <div className={cn(
        "w-10 h-10 rounded-lg flex items-center justify-center transition-colors",
        isActive ? "bg-primary/20" : "bg-muted"
      )}>
        <command.icon className={cn(
          "w-5 h-5 transition-colors",
          isActive ? "text-primary" : "text-muted-foreground"
        )} />
      </div>
      <div className="flex-1">
        <div className="flex items-center gap-2">
          <span className={cn(
            "font-mono font-bold transition-colors",
            isActive ? "text-primary" : "text-foreground"
          )}>
            {command.name}
          </span>
        </div>
        <p className="text-sm text-muted-foreground line-clamp-1">{command.description}</p>
      </div>
      <ChevronRight className={cn(
        "w-4 h-4 transition-all",
        isActive ? "text-primary rotate-90" : "text-muted-foreground"
      )} />
    </button>
  )
}

function CommandDetail({ command }: { command: typeof commands[0] }) {
  const [copied, setCopied] = useState(false)

  const copyExample = () => {
    navigator.clipboard.writeText(command.example)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="space-y-6">
      {/* Syntax */}
      <div>
        <h4 className="text-sm font-medium text-muted-foreground mb-2">Syntax</h4>
        <div className="p-4 rounded-xl bg-muted/50 border border-border font-mono text-sm">
          <span className="text-primary">$</span> {command.syntax}
        </div>
      </div>

      {/* Description */}
      <div>
        <h4 className="text-sm font-medium text-muted-foreground mb-2">Description</h4>
        <p className="text-foreground leading-relaxed">{command.description}</p>
      </div>

      {/* Options */}
      <div>
        <h4 className="text-sm font-medium text-muted-foreground mb-2">Options</h4>
        <div className="space-y-2">
          {command.options.map((option) => (
            <div key={option.flag} className="flex gap-4 p-3 rounded-lg bg-muted/30 border border-border/50">
              <code className="text-primary font-mono text-sm whitespace-nowrap">{option.flag}</code>
              <span className="text-muted-foreground text-sm">{option.description}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Example */}
      <div>
        <h4 className="text-sm font-medium text-muted-foreground mb-2">Example</h4>
        <div className="relative group">
          <div className="p-4 rounded-xl bg-card border border-border font-mono text-sm">
            <span className="text-primary">$</span> {command.example}
          </div>
          <button
            onClick={copyExample}
            className="absolute top-3 right-3 p-2 rounded-lg bg-muted/50 hover:bg-muted transition-colors opacity-0 group-hover:opacity-100"
          >
            {copied ? <Check className="w-4 h-4 text-primary" /> : <Copy className="w-4 h-4 text-muted-foreground" />}
          </button>
        </div>
      </div>

      {/* Output */}
      <div>
        <h4 className="text-sm font-medium text-muted-foreground mb-2">Sample Output</h4>
        <div className="relative overflow-hidden rounded-xl border border-border">
          <div className="flex items-center gap-2 px-4 py-2 bg-muted/50 border-b border-border">
            <div className="w-3 h-3 rounded-full bg-red-500/60" />
            <div className="w-3 h-3 rounded-full bg-yellow-500/60" />
            <div className="w-3 h-3 rounded-full bg-green-500/60" />
            <span className="ml-2 text-xs text-muted-foreground font-mono">Terminal</span>
          </div>
          <pre className="p-4 bg-card font-mono text-xs text-foreground overflow-x-auto whitespace-pre">
            {command.output}
          </pre>
        </div>
      </div>
    </div>
  )
}

export function CLISection() {
  const [activeCommand, setActiveCommand] = useState(commands[0])

  return (
    <section id="cli" className="relative py-32 overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-background via-card/10 to-background" />

      <div className="relative container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-6">
            <Terminal className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium text-primary">CLI Reference</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
            Powerful{" "}
            <span className="text-primary glow-text">command-line</span>{" "}
            interface
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Every command you need to debug, predict, and learn from your errors.
          </p>
        </div>

        {/* Commands Grid */}
        <div className="grid lg:grid-cols-12 gap-8 max-w-7xl mx-auto">
          {/* Command List */}
          <div className="lg:col-span-4 space-y-3">
            {commands.map((command) => (
              <CommandCard
                key={command.name}
                command={command}
                isActive={activeCommand.name === command.name}
                onClick={() => setActiveCommand(command)}
              />
            ))}
          </div>

          {/* Command Detail */}
          <div className="lg:col-span-8">
            <div className="sticky top-24 p-6 md:p-8 rounded-2xl bg-card border border-border">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-12 h-12 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center">
                  <activeCommand.icon className="w-6 h-6 text-primary" />
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-foreground font-mono">
                    dbug {activeCommand.name}
                  </h3>
                </div>
              </div>
              <CommandDetail command={activeCommand} />
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
