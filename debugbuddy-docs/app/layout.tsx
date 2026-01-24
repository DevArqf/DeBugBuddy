import React from "react"
import type { Metadata, Viewport } from 'next'
import { Inter, JetBrains_Mono } from 'next/font/google'
import { Analytics } from '@vercel/analytics/next'
import './globals.css'

const inter = Inter({ 
  subsets: ["latin"],
  variable: "--font-inter"
});

const jetbrainsMono = JetBrains_Mono({ 
  subsets: ["latin"],
  variable: "--font-jetbrains"
});

export const metadata: Metadata = {
  title: 'DeBugBuddy Documentation | Your Terminal Debugging Companion',
  description: 'DeBugBuddy is an open-source CLI + TUI that explains errors in plain English, predicts issues before they break, and keeps a searchable local history. Stop Googling. Understand your errors.',
  keywords: ['debugging', 'python', 'cli', 'tui', 'error-explanation', 'developer-tools', 'stack-trace'],
  authors: [{ name: 'DevArqf' }],
  openGraph: {
    title: 'DeBugBuddy - Stop Googling. Understand Your Errors.',
    description: 'Your terminal debugging companion - instant error explanations, no StackOverflow required.',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'DeBugBuddy Documentation',
    description: 'Your terminal debugging companion - instant error explanations, no StackOverflow required.',
  },
}

export const viewport: Viewport = {
  themeColor: '#22c55e',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.variable} ${jetbrainsMono.variable} font-sans antialiased`}>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
