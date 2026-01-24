"use client"

import { useEffect, useRef, useState } from "react"
import Image from "next/image"
import { Button } from "@/components/ui/button"
import { Terminal, Github, Copy, Check, Sparkles, ArrowRight, Bug, Zap, Shield, BarChart3 } from "lucide-react"
import Link from "next/link"

const matrixChars = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789"

function MatrixRain() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext("2d")
    if (!ctx) return

    const resizeCanvas = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }
    resizeCanvas()
    window.addEventListener("resize", resizeCanvas)

    const fontSize = 14
    const columns = Math.floor(canvas.width / fontSize)
    const drops: number[] = Array(columns).fill(1)

    const draw = () => {
      ctx.fillStyle = "rgba(12, 18, 15, 0.05)"
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      ctx.fillStyle = "#22c55e"
      ctx.font = `${fontSize}px monospace`

      for (let i = 0; i < drops.length; i++) {
        const char = matrixChars[Math.floor(Math.random() * matrixChars.length)]
        const x = i * fontSize
        const y = drops[i] * fontSize

        ctx.globalAlpha = Math.random() * 0.5 + 0.1
        ctx.fillText(char, x, y)

        if (y > canvas.height && Math.random() > 0.98) {
          drops[i] = 0
        }
        drops[i]++
      }
    }

    const interval = setInterval(draw, 50)

    return () => {
      clearInterval(interval)
      window.removeEventListener("resize", resizeCanvas)
    }
  }, [])

  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0 pointer-events-none opacity-30"
    />
  )
}

function TypewriterText({ text, delay = 50 }: { text: string; delay?: number }) {
  const [displayText, setDisplayText] = useState("")
  const [currentIndex, setCurrentIndex] = useState(0)

  useEffect(() => {
    if (currentIndex < text.length) {
      const timeout = setTimeout(() => {
        setDisplayText(prev => prev + text[currentIndex])
        setCurrentIndex(prev => prev + 1)
      }, delay)
      return () => clearTimeout(timeout)
    }
  }, [currentIndex, text, delay])

  return (
    <span>
      {displayText}
      <span className="animate-terminal-blink text-primary">|</span>
    </span>
  )
}

export function HeroSection() {
  const [copied, setCopied] = useState(false)

  const copyCommand = () => {
    navigator.clipboard.writeText("pip install debugbuddy-cli")
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <section id="home" className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background Effects */}
      <MatrixRain />
      
      {/* Gradient Overlay */}
      <div className="absolute inset-0 bg-gradient-to-b from-background via-background/90 to-background" />
      
      {/* Glow Effects */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-[120px] animate-pulse" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent/20 rounded-full blur-[120px] animate-pulse delay-1000" />

      {/* Content */}
      <div className="relative z-10 container mx-auto px-4 py-32">
        <div className="max-w-5xl mx-auto text-center">
          {/* Banner Logo */}
          <div className="mb-8 animate-fade-up">
            <Image
              src="/debugbuddy-branding/DeBugBuddy Banner.png"
              alt="DeBugBuddy Banner"
              width={400}
              height={100}
              className="mx-auto h-auto w-auto max-w-[280px] md:max-w-[400px] drop-shadow-[0_0_30px_var(--glow)]"
              priority
            />
          </div>

          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-8 animate-fade-up" style={{ animationDelay: "50ms" }}>
            <Sparkles className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium text-primary">v0.4.7 — Now with Grok AI Support</span>
          </div>

          {/* Main Headline */}
          <h1 className="text-5xl md:text-7xl lg:text-8xl font-bold tracking-tight mb-6 animate-fade-up" style={{ animationDelay: "100ms" }}>
            <span className="text-foreground">Stop Googling.</span>
            <br />
            <span className="text-primary glow-text">Understand</span>
            <span className="text-foreground"> your errors.</span>
          </h1>

          {/* Subtitle */}
          <p className="text-xl md:text-2xl text-muted-foreground max-w-3xl mx-auto mb-10 leading-relaxed animate-fade-up" style={{ animationDelay: "200ms" }}>
            DeBugBuddy is a local-first CLI + TUI that explains errors in{" "}
            <span className="text-foreground font-medium">plain English</span>, predicts issues before they break, 
            and keeps your debugging history <span className="text-primary">private</span>.
          </p>

          {/* Install Command */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12 animate-fade-up" style={{ animationDelay: "300ms" }}>
            <div className="flex items-center gap-3 px-5 py-3 rounded-xl bg-card border border-border font-mono text-sm group hover:border-primary/50 transition-all duration-300 hover:shadow-[0_0_30px_var(--glow)]">
              <Terminal className="w-4 h-4 text-primary" />
              <span className="text-muted-foreground">$</span>
              <span className="text-foreground">pip install debugbuddy-cli</span>
              <button
                onClick={copyCommand}
                className="ml-2 p-1.5 rounded-md hover:bg-muted transition-colors"
                aria-label="Copy command"
              >
                {copied ? (
                  <Check className="w-4 h-4 text-primary" />
                ) : (
                  <Copy className="w-4 h-4 text-muted-foreground group-hover:text-foreground" />
                )}
              </button>
            </div>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 animate-fade-up" style={{ animationDelay: "400ms" }}>
            <Button 
              size="lg" 
              className="bg-primary hover:bg-primary/90 text-primary-foreground gap-2 px-8 shadow-[0_0_30px_var(--glow)] hover:shadow-[0_0_50px_var(--glow)] transition-all duration-300"
              asChild
            >
              <Link href="#installation">
                Get Started
                <ArrowRight className="w-4 h-4" />
              </Link>
            </Button>
            <Button 
              size="lg" 
              variant="outline" 
              className="gap-2 px-8 border-border hover:border-primary/50 hover:bg-primary/5 transition-all duration-300 bg-transparent"
              asChild
            >
              <Link href="https://github.com/DevArqf/DeBugBuddy" target="_blank">
                <Github className="w-4 h-4" />
                View on GitHub
              </Link>
            </Button>
          </div>

          {/* Quick Features */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-20 animate-fade-up" style={{ animationDelay: "500ms" }}>
            {[
              { icon: Bug, label: "Explain Fast", desc: "Plain-English fixes" },
              { icon: Zap, label: "Predict Issues", desc: "Before they break" },
              { icon: Shield, label: "Local-First", desc: "Privacy by default" },
              { icon: BarChart3, label: "Analytics", desc: "Track patterns" },
            ].map((feature, index) => (
              <div
                key={feature.label}
                className="group p-4 rounded-xl bg-card/50 border border-border hover:border-primary/30 transition-all duration-300 hover:shadow-[0_0_20px_var(--glow)]"
              >
                <feature.icon className="w-8 h-8 text-primary mb-3 group-hover:scale-110 transition-transform duration-300" />
                <h3 className="font-semibold text-foreground mb-1">{feature.label}</h3>
                <p className="text-sm text-muted-foreground">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 text-muted-foreground animate-bounce">
        <span className="text-xs font-medium">Scroll to explore</span>
        <div className="w-6 h-10 rounded-full border-2 border-muted-foreground/30 flex items-start justify-center p-2">
          <div className="w-1 h-2 bg-primary rounded-full animate-pulse" />
        </div>
      </div>
    </section>
  )
}
