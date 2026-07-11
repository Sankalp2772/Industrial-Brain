import * as React from "react"
import { ArrowRight } from "lucide-react"
import { Link } from "react-router-dom"
import { Hero } from "@/components/landing/Hero"
import { Features } from "@/components/landing/Features"
import { Impact } from "@/components/landing/Impact"
import { Button } from "@/components/ui/button"

export function LandingPage() {
  return (
    <div className="bg-background min-h-screen">
      {/* Simple Header */}
      <header className="absolute inset-x-0 top-0 z-50">
        <nav className="flex items-center justify-between p-6 lg:px-8" aria-label="Global">
          <div className="flex lg:flex-1">
            <Link to="/" className="-m-1.5 p-1.5 flex items-center gap-2">
              <div className="bg-primary text-primary-foreground p-1 rounded-sm">
                <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="14" x2="23" y2="14"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="14" x2="4" y2="14"></line></svg>
              </div>
              <span className="font-bold text-lg">Industrial Brain</span>
            </Link>
          </div>
          <div className="flex flex-1 justify-end items-center gap-4">
            <Link to="/login" className="text-sm font-semibold leading-6 text-foreground hover:text-primary transition-colors">
              Log in
            </Link>
            <Button asChild>
              <Link to="/login">Get Started</Link>
            </Button>
          </div>
        </nav>
      </header>

      <main>
        <Hero />
        <Impact />
        <Features />

        {/* CTA Section */}
        <div className="bg-primary">
          <div className="px-6 py-24 sm:px-6 sm:py-32 lg:px-8">
            <div className="mx-auto max-w-2xl text-center">
              <h2 className="text-3xl font-bold tracking-tight text-primary-foreground sm:text-4xl">
                Ready to transform your plant operations?
              </h2>
              <p className="mx-auto mt-6 max-w-xl text-lg leading-8 text-primary-foreground/80">
                Join the industrial leaders who are already leveraging AI to prevent downtime and increase efficiency.
              </p>
              <div className="mt-10 flex items-center justify-center gap-x-6">
                <Button variant="secondary" size="lg" asChild>
                  <Link to="/login">Get started <ArrowRight className="ml-2 w-4 h-4" /></Link>
                </Button>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Landing Footer */}
      <footer className="bg-surface py-12 border-t">
        <div className="mx-auto max-w-7xl px-6 lg:px-8 text-center text-sm text-muted-foreground">
          &copy; {new Date().getFullYear()} Industrial Brain Inc. All rights reserved.
        </div>
      </footer>
    </div>
  )
}
