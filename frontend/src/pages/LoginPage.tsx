import * as React from "react"
import { Cpu, Lock, Mail, ArrowRight } from "lucide-react"
import { Link, useNavigate } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { useAuthStore } from "@/store/useAuthStore"

import { ApiService } from "@/services/api"
import { useState } from "react"

export function LoginPage() {
  const navigate = useNavigate()
  const login = useAuthStore((state) => state.login)
  const [error, setError] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setIsLoading(true)
    
    const formData = new FormData(e.target as HTMLFormElement)
    const email = formData.get("email") as string
    const password = formData.get("password") as string

    try {
      const data = await ApiService.login({ email, password })
      // Initialize initials
      const initials = data.user.name.split(" ").map((n: string) => n[0]).join("").toUpperCase().substring(0,2) || "U"
      
      login({
        ...data.user,
        avatarInitials: initials
      }, data.access_token)
      
      navigate("/app/dashboard")
    } catch (err: any) {
      setError(err.response?.data?.message || "Login failed. Please check your credentials.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen w-full flex bg-background">
      {/* Left Panel: Auth Form */}
      <div className="flex-1 flex flex-col justify-center px-4 sm:px-6 lg:flex-none lg:w-[500px] lg:px-20 xl:px-24 bg-surface z-10 shadow-xl relative">
        <div className="mx-auto w-full max-w-sm lg:w-96">
          <div className="flex items-center space-x-2">
            <div className="bg-primary text-primary-foreground p-1.5 rounded-md">
              <Cpu className="h-6 w-6" />
            </div>
            <span className="text-xl font-bold tracking-tight text-foreground">Industrial Brain</span>
          </div>
          
          <h2 className="mt-8 text-2xl font-bold leading-9 tracking-tight text-foreground">
            Sign in to your account
          </h2>
          <p className="mt-2 text-sm leading-6 text-muted-foreground">
            Enterprise AI for industrial intelligence.
          </p>

          <div className="mt-10">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <Label htmlFor="email" className="text-sm font-medium leading-6">
                  Email address
                </Label>
                <div className="mt-2 relative rounded-md shadow-sm">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Mail className="h-4 w-4 text-muted-foreground" />
                  </div>
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    autoComplete="email"
                    required
                    className="pl-10"
                    placeholder="engineer@company.com"
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="password" className="text-sm font-medium leading-6">
                  Password
                </Label>
                <div className="mt-2 relative rounded-md shadow-sm">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Lock className="h-4 w-4 text-muted-foreground" />
                  </div>
                  <Input
                    id="password"
                    name="password"
                    type="password"
                    autoComplete="current-password"
                    required
                    className="pl-10"
                    placeholder="••••••••"
                  />
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Checkbox id="remember-me" />
                  <Label htmlFor="remember-me" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                    Remember me
                  </Label>
                </div>

                <div className="text-sm leading-6 flex gap-3">
                  <Link to="/register" className="font-semibold text-primary hover:text-primary/80 transition-colors">
                    Sign up
                  </Link>
                  <a href="#" className="font-semibold text-primary hover:text-primary/80 transition-colors">
                    Forgot password?
                  </a>
                </div>
              </div>

              {error && (
                <div className="text-red-500 text-sm font-medium text-center">
                  {error}
                </div>
              )}

              <div>
                <Button type="submit" disabled={isLoading} className="w-full flex items-center justify-center">
                  {isLoading ? "Signing in..." : "Sign in"} <ArrowRight className="ml-2 w-4 h-4" />
                </Button>
              </div>
            </form>
          </div>
        </div>
      </div>

      {/* Right Panel: Branding / Graphic */}
      <div className="hidden lg:flex flex-1 relative bg-primary items-center justify-center overflow-hidden">
        {/* Subtle grid pattern */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#ffffff1a_1px,transparent_1px),linear-gradient(to_bottom,#ffffff1a_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] opacity-30"></div>
        
        <div className="relative z-10 flex flex-col items-center text-primary-foreground max-w-lg text-center">
           <Cpu className="w-24 h-24 mb-8 opacity-90" />
           <h1 className="text-4xl font-extrabold tracking-tight mb-4">
             Intelligence for the Industrial Enterprise.
           </h1>
           <p className="text-lg opacity-80 mb-8 leading-relaxed">
             Secure, reliable, and scalable AI infrastructure built to optimize your plant operations and eliminate unplanned downtime.
           </p>
           
           <div className="grid grid-cols-2 gap-8 text-left mt-8 w-full border-t border-primary-foreground/20 pt-8">
             <div>
               <div className="text-3xl font-bold">99.9%</div>
               <div className="text-sm opacity-80 mt-1">Uptime SLA</div>
             </div>
             <div>
               <div className="text-3xl font-bold">SOC 2</div>
               <div className="text-sm opacity-80 mt-1">Type II Certified</div>
             </div>
           </div>
        </div>
      </div>
    </div>
  )
}
