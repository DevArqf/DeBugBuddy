"use client"

import { useState } from "react"
import { HelpCircle, ChevronDown, Shield, Code2, Zap, Settings } from "lucide-react"
import { cn } from "@/lib/utils"

const faqs = [
  {
    question: "Is my code private?",
    answer: "Yes, absolutely. DeBugBuddy runs locally by default. Your code, error messages, and debugging history never leave your machine unless you explicitly opt into AI mode. Even with AI enabled, only the specific error context is sent to your chosen provider.",
    icon: Shield,
  },
  {
    question: "Does it replace StackOverflow?",
    answer: "For debugging, yes! Instead of copying error messages, searching, reading through multiple answers, and adapting solutions — you get instant, context-aware explanations right in your terminal. It's like having a debugging expert on call.",
    icon: Code2,
  },
  {
    question: "Can I add custom error patterns?",
    answer: "Absolutely. You can create custom JSON pattern files and load them with `dbug train --patterns custom.json`. These are merged with the built-in patterns. You can also train ML models on your error history for personalized predictions.",
    icon: Settings,
  },
  {
    question: "How accurate is the error prediction?",
    answer: "DeBugBuddy uses 150+ hand-crafted patterns plus optional ML prediction. Pattern matching catches common issues with high accuracy. ML prediction learns from your coding patterns over time. Accuracy improves as you use it more.",
    icon: Zap,
  },
  {
    question: "Which Python version is required?",
    answer: "DeBugBuddy requires Python 3.8 or higher. It's tested on Python 3.8, 3.9, 3.10, 3.11, and 3.12. The TUI interface uses Textual, which has excellent cross-platform support.",
    icon: Code2,
  },
  {
    question: "Can I use it without an internet connection?",
    answer: "Yes! The core functionality works completely offline. Pattern matching, error explanations, prediction, and history all work without internet. Only AI-enhanced explanations and GitHub search require connectivity.",
    icon: Shield,
  },
  {
    question: "How do I contribute a new language?",
    answer: "We'd love contributions! Check out the patterns/ directory in our GitHub repo for examples. Each language has a JSON file with error patterns. Submit a PR with your patterns, and we'll review and merge. See CONTRIBUTING.md for guidelines.",
    icon: Code2,
  },
  {
    question: "Is there an IDE/editor extension?",
    answer: "Not yet, but it's on our roadmap for v0.5.0! We're planning a VS Code extension first, with other editors to follow. In the meantime, the TUI provides a great integrated experience.",
    icon: Settings,
  },
]

function FAQItem({ faq, isOpen, onClick }: { 
  faq: typeof faqs[0]
  isOpen: boolean
  onClick: () => void
}) {
  return (
    <div className={cn(
      "border border-border rounded-xl overflow-hidden transition-all duration-300",
      isOpen ? "bg-card shadow-[0_0_20px_var(--glow)]" : "bg-card/50 hover:bg-card"
    )}>
      <button
        onClick={onClick}
        className="w-full flex items-center gap-4 p-6 text-left"
      >
        <div className={cn(
          "flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center transition-colors",
          isOpen ? "bg-primary/20" : "bg-muted"
        )}>
          <faq.icon className={cn(
            "w-5 h-5 transition-colors",
            isOpen ? "text-primary" : "text-muted-foreground"
          )} />
        </div>
        <span className={cn(
          "flex-1 font-semibold transition-colors",
          isOpen ? "text-primary" : "text-foreground"
        )}>
          {faq.question}
        </span>
        <ChevronDown className={cn(
          "w-5 h-5 transition-all duration-300",
          isOpen ? "text-primary rotate-180" : "text-muted-foreground"
        )} />
      </button>
      <div className={cn(
        "overflow-hidden transition-all duration-300",
        isOpen ? "max-h-96" : "max-h-0"
      )}>
        <div className="px-6 pb-6 pl-20">
          <p className="text-muted-foreground leading-relaxed">
            {faq.answer}
          </p>
        </div>
      </div>
    </div>
  )
}

export function FAQSection() {
  const [openIndex, setOpenIndex] = useState<number | null>(0)

  return (
    <section id="faq" className="relative py-32 overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-card/20 via-background to-card/20" />

      <div className="relative container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-6">
            <HelpCircle className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium text-primary">FAQ</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
            Frequently asked{" "}
            <span className="text-primary glow-text">questions</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Everything you need to know about DeBugBuddy.
          </p>
        </div>

        {/* FAQ List */}
        <div className="max-w-3xl mx-auto space-y-4">
          {faqs.map((faq, index) => (
            <FAQItem
              key={faq.question}
              faq={faq}
              isOpen={openIndex === index}
              onClick={() => setOpenIndex(openIndex === index ? null : index)}
            />
          ))}
        </div>

        {/* Still have questions */}
        <div className="mt-16 text-center">
          <p className="text-muted-foreground mb-4">
            Still have questions?
          </p>
          <a
            href="https://github.com/DevArqf/DeBugBuddy/discussions"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-card border border-border hover:border-primary/30 text-foreground font-medium transition-all duration-300 hover:shadow-[0_0_20px_var(--glow)]"
          >
            <HelpCircle className="w-4 h-4" />
            Ask in Discussions
          </a>
        </div>
      </div>
    </section>
  )
}
