"use client"

import Link from "next/link"
import { Bug, Github, Heart, ExternalLink } from "lucide-react"

const footerLinks = {
  Documentation: [
    { name: "Getting Started", href: "#installation" },
    { name: "CLI Reference", href: "#cli" },
    { name: "TUI Guide", href: "#tui" },
    { name: "AI Providers", href: "#ai" },
  ],
  Resources: [
    { name: "GitHub", href: "https://github.com/DevArqf/DeBugBuddy", external: true },
    { name: "PyPI", href: "https://pypi.org/project/debugbuddy-cli/", external: true },
    { name: "Changelog", href: "https://github.com/DevArqf/DeBugBuddy/releases", external: true },
    { name: "Contributing", href: "https://github.com/DevArqf/DeBugBuddy/blob/main/CONTRIBUTING.md", external: true },
  ],
  Community: [
    { name: "Report a Bug", href: "https://github.com/DevArqf/DeBugBuddy/issues/new", external: true },
    { name: "Feature Request", href: "https://github.com/DevArqf/DeBugBuddy/issues/new", external: true },
    { name: "Discussions", href: "https://github.com/DevArqf/DeBugBuddy/discussions", external: true },
  ],
}

export function Footer() {
  return (
    <footer className="relative border-t border-border bg-card/30">
      {/* Main Footer */}
      <div className="container mx-auto px-4 py-16">
        <div className="grid md:grid-cols-2 lg:grid-cols-5 gap-12">
          {/* Brand */}
          <div className="lg:col-span-2">
            <Link href="#home" className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-xl bg-primary/20 flex items-center justify-center border border-primary/30">
                <Bug className="w-5 h-5 text-primary" />
              </div>
              <div>
                <span className="text-xl font-bold text-foreground">DeBugBuddy</span>
              </div>
            </Link>
            <p className="text-muted-foreground mb-6 max-w-sm">
              Your terminal{"'"}s debugging companion. Instant error explanations, 
              no StackOverflow required. Open source and privacy-first.
            </p>
            <div className="flex items-center gap-4">
              <a
                href="https://github.com/DevArqf/DeBugBuddy"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors"
              >
                <Github className="w-5 h-5" />
                <span className="text-sm">Star on GitHub</span>
              </a>
            </div>
          </div>

          {/* Links */}
          {Object.entries(footerLinks).map(([category, links]) => (
            <div key={category}>
              <h4 className="font-semibold text-foreground mb-4">{category}</h4>
              <ul className="space-y-3">
                {links.map((link) => (
                  <li key={link.name}>
                    {link.external ? (
                      <a
                        href={link.href}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-1 text-muted-foreground hover:text-primary transition-colors text-sm"
                      >
                        {link.name}
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    ) : (
                      <Link
                        href={link.href}
                        className="text-muted-foreground hover:text-primary transition-colors text-sm"
                      >
                        {link.name}
                      </Link>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-border">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-1 text-sm text-muted-foreground">
              <span>Made with</span>
              <Heart className="w-4 h-4 text-red-500 fill-red-500" />
              <span>by</span>
              <a 
                href="https://github.com/DevArqf" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-foreground hover:text-primary transition-colors"
              >
                DevArqf
              </a>
            </div>
            <div className="flex items-center gap-6 text-sm text-muted-foreground">
              <span>MIT License</span>
              <span>v0.4.7</span>
            </div>
          </div>
        </div>
      </div>

      {/* Glow Effect */}
      <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-1/2 h-px bg-gradient-to-r from-transparent via-primary/50 to-transparent" />
    </footer>
  )
}
