import * as React from "react"
import { NavLink } from "react-router-dom"
import { 
  LayoutDashboard, 
  FileText, 
  Network, 
  Database, 
  Bot, 
  BarChart3, 
  Settings,
  Cpu
} from "lucide-react"
import { cn } from "@/lib/utils"

const navItems = [
  { name: "Dashboard", href: "/app/dashboard", icon: LayoutDashboard },
  { name: "Documents", href: "/app/documents", icon: FileText },
  { name: "Knowledge Graph", href: "/app/knowledge-graph", icon: Network },
  { name: "Assets", href: "/app/assets", icon: Database },
  { name: "AI Copilot", href: "/app/copilot", icon: Bot },
  { name: "Analytics", href: "/app/analytics", icon: BarChart3 },
  { name: "Settings", href: "/app/settings", icon: Settings },
]

export function Sidebar({ className }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn("pb-12 border-r bg-surface h-full w-64 flex-shrink-0 hidden md:flex flex-col shadow-enterprise z-10", className)}>
      <div className="space-y-4 py-4 flex-1">
        <div className="px-3 py-2">
          <h2 className="mb-2 px-4 text-lg font-semibold tracking-tight flex items-center text-primary">
            <Cpu className="mr-2 w-5 h-5" />
            Industrial Brain
          </h2>
          <div className="space-y-1 mt-6">
            {navItems.map((item) => (
              <NavLink
                key={item.href}
                to={item.href}
                className={({ isActive }) =>
                  cn(
                    "w-full flex items-center px-4 py-2 text-sm font-medium rounded-md transition-colors",
                    isActive
                      ? "bg-primary/10 text-primary"
                      : "text-muted-foreground hover:bg-muted hover:text-foreground"
                  )
                }
              >
                {({ isActive }) => (
                  <>
                    <item.icon className={cn("mr-3 h-4 w-4", isActive ? "text-primary" : "text-muted-foreground")} />
                    {item.name}
                  </>
                )}
              </NavLink>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
