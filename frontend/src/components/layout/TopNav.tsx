import * as React from "react"
import { Bell, Search, User, LogOut, Settings as SettingsIcon } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"
import { useLocation, Link, useNavigate } from "react-router-dom"
import { useAuthStore } from "@/store/useAuthStore"
import { ApiService } from "@/services/api"

export function TopNav() {
  const location = useLocation()
  const navigate = useNavigate()
  const { user, logout } = useAuthStore()
  
  // Basic logic to generate breadcrumbs from pathname for the shell
  const paths = location.pathname.split('/').filter(Boolean)
  
  const handleLogout = async () => {
    try {
      await ApiService.logout();
    } finally {
      logout()
      navigate('/login')
    }
  }
  
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 shadow-sm">
      <div className="container flex h-14 items-center max-w-full px-4 justify-between">
        <div className="flex items-center gap-4">
          <div className="md:hidden flex items-center">
             {/* Mobile menu toggle would go here */}
          </div>
          
          <Breadcrumb className="hidden sm:flex">
            <BreadcrumbList>
              <BreadcrumbItem>
                <BreadcrumbLink asChild>
                  <Link to="/">Home</Link>
                </BreadcrumbLink>
              </BreadcrumbItem>
              {paths.length > 0 && <BreadcrumbSeparator />}
              {paths.map((path, index) => {
                const href = `/${paths.slice(0, index + 1).join('/')}`
                const isLast = index === paths.length - 1
                const title = path.charAt(0).toUpperCase() + path.slice(1).replace(/-/g, ' ')
                
                return (
                  <React.Fragment key={path}>
                    <BreadcrumbItem>
                      {isLast ? (
                        <BreadcrumbPage>{title}</BreadcrumbPage>
                      ) : (
                        <BreadcrumbLink asChild>
                          <Link to={href}>{title}</Link>
                        </BreadcrumbLink>
                      )}
                    </BreadcrumbItem>
                    {!isLast && <BreadcrumbSeparator />}
                  </React.Fragment>
                )
              })}
            </BreadcrumbList>
          </Breadcrumb>
        </div>

        <div className="flex items-center space-x-4">
          <div className="hidden md:flex relative">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              type="search"
              placeholder="Search assets, documents..."
              className="w-full rounded-lg bg-surface pl-9 md:w-[250px] lg:w-[300px] h-9"
            />
          </div>
          
          <nav className="flex items-center space-x-2">
            <Button variant="ghost" size="icon" className="relative h-9 w-9">
              <Bell className="h-5 w-5 text-muted-foreground" />
              <span className="absolute top-2 right-2 h-2 w-2 rounded-full bg-destructive border border-background"></span>
            </Button>
            
            {user && (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="relative h-9 w-9 rounded-full ml-2">
                    <Avatar className="h-9 w-9 border">
                      <AvatarFallback className="bg-primary/10 text-primary text-xs font-semibold">{user.avatarInitials}</AvatarFallback>
                    </Avatar>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent className="w-56" align="end" forceMount>
                  <DropdownMenuLabel className="font-normal">
                    <div className="flex flex-col space-y-1">
                      <p className="text-sm font-medium leading-none">{user.name}</p>
                      <p className="text-xs leading-none text-muted-foreground">
                        {user.email}
                      </p>
                    </div>
                  </DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem asChild>
                    <Link to="/app/settings">
                      <User className="mr-2 h-4 w-4" />
                      <span>Profile</span>
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem asChild>
                    <Link to="/app/settings">
                      <SettingsIcon className="mr-2 h-4 w-4" />
                      <span>Preferences</span>
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem className="text-destructive focus:bg-destructive/10 focus:text-destructive" onClick={handleLogout}>
                    <LogOut className="mr-2 h-4 w-4" />
                    <span>Log out</span>
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            )}
          </nav>
        </div>
      </div>
    </header>
  )
}
