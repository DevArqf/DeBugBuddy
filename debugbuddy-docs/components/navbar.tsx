"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { Bug, Menu, X, Github, Terminal, BookOpen, Shield, Command, Sparkles, ChevronDown } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

const navItems = [
  { name: "Home", href: "#home" },
  { name: "Features", href: "#features" },
  { name: "Installation", href: "#installation" },
  { name: "CLI", href: "#cli" },
  { name: "TUI", href: "#tui" },
  { name: "AI Providers", href: "#ai" },
  { name: "Languages", href: "#languages" },
  { name: "Roadmap", href: "#roadmap" },
]

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)
  const [activeSection, setActiveSection] = useState("home")

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20)
      
      // Update active section based on scroll position
      const sections = navItems.map(item => item.href.slice(1))
      for (const section of sections.reverse()) {
        const element = document.getElementById(section)
        if (element) {
          const rect = element.getBoundingClientRect()
          if (rect.top <= 100) {
            setActiveSection(section)
            break
          }
        }
      }
    }

    window.addEventListener("scroll", handleScroll)
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  return (
    <header
      className={cn(
        "fixed top-0 left-0 right-0 z-50 transition-all duration-500 ease-out",
        scrolled 
          ? "glass py-3" 
          : "bg-transparent py-5"
      )}
    >
      <div className="container mx-auto px-4">
        <nav className="flex items-center justify-between">
          {/* Logo */}
          <Link 
            href="#home" 
            className="flex items-center gap-3 group"
          >
            <div className="relative">
              <div className="w-10 h-10 rounded-xl bg-primary/20 flex items-center justify-center border border-primary/30 group-hover:border-primary/60 transition-all duration-300 group-hover:shadow-[0_0_20px_var(--glow)]">
                <Bug className="w-5 h-5 text-primary" />
              </div>
              <div className="absolute -inset-1 bg-primary/20 rounded-xl blur-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            </div>
            <div className="flex flex-col">
              <span className="text-lg font-bold text-foreground tracking-tight">
                DeBugBuddy
              </span>
              <span className="text-xs text-muted-foreground -mt-0.5">
                Documentation
              </span>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden lg:flex items-center gap-1">
            {navItems.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  "px-3 py-2 text-sm font-medium rounded-lg transition-all duration-300",
                  activeSection === item.href.slice(1)
                    ? "text-primary bg-primary/10"
                    : "text-muted-foreground hover:text-foreground hover:bg-muted"
                )}
              >
                {item.name}
              </Link>
            ))}
          </div>

          {/* Actions */}
          <div className="flex items-center gap-3">
            <Link 
              href="https://github.com/DevArqf/DeBugBuddy" 
              target="_blank"
              className="hidden md:flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              <Github className="w-4 h-4" />
              <span>GitHub</span>
            </Link>
            
            <Button
              size="sm"
              asChild
              className="hidden md:flex bg-primary hover:bg-primary/90 text-primary-foreground gap-2 shadow-[0_0_20px_var(--glow)] hover:shadow-[0_0_30px_var(--glow)] transition-all duration-300"
            >
              <Link
                href="https://pypi.org/project/debugbuddy-cli/0.4.7/"
                target="_blank"
                rel="noreferrer"
              >
                <Terminal className="w-4 h-4" />
                pip install
              </Link>
            </Button>

            {/* Mobile Menu Toggle */}
            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden"
              onClick={() => setIsOpen(!isOpen)}
            >
              {isOpen ? (
                <X className="w-5 h-5" />
              ) : (
                <Menu className="w-5 h-5" />
              )}
            </Button>
          </div>
        </nav>

        {/* Mobile Navigation */}
        <div
          className={cn(
            "lg:hidden overflow-hidden transition-all duration-500 ease-out",
            isOpen ? "max-h-[500px] opacity-100 mt-4" : "max-h-0 opacity-0"
          )}
        >
          <div className="flex flex-col gap-2 p-4 rounded-xl bg-card border border-border">
            {navItems.map((item, index) => (
              <Link
                key={item.name}
                href={item.href}
                onClick={() => setIsOpen(false)}
                className={cn(
                  "px-4 py-3 text-sm font-medium rounded-lg transition-all duration-300",
                  activeSection === item.href.slice(1)
                    ? "text-primary bg-primary/10"
                    : "text-muted-foreground hover:text-foreground hover:bg-muted"
                )}
                style={{ animationDelay: `${index * 50}ms` }}
              >
                {item.name}
              </Link>
            ))}
            <div className="pt-4 mt-2 border-t border-border flex flex-col gap-2">
              <Link 
                href="https://github.com/DevArqf/DeBugBuddy" 
                target="_blank"
                className="flex items-center gap-2 px-4 py-3 text-sm text-muted-foreground hover:text-foreground transition-colors rounded-lg hover:bg-muted"
              >
                <Github className="w-4 h-4" />
                <span>View on GitHub</span>
              </Link>
              <Button 
                className="w-full bg-primary hover:bg-primary/90 text-primary-foreground gap-2"
              >
                <Terminal className="w-4 h-4" />
                pip install debugbuddy-cli
              </Button>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}
