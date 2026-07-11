import * as React from "react"

export function Footer() {
  return (
    <footer className="w-full border-t bg-surface py-4 px-6 mt-auto">
      <div className="flex flex-col md:flex-row justify-between items-center text-xs text-muted-foreground">
        <p>&copy; {new Date().getFullYear()} Industrial Brain Platform. All rights reserved.</p>
        <div className="flex space-x-4 mt-2 md:mt-0">
          <span className="hover:text-primary cursor-pointer transition-colors">Privacy Policy</span>
          <span className="hover:text-primary cursor-pointer transition-colors">Terms of Service</span>
          <span>Version 1.0.0</span>
        </div>
      </div>
    </footer>
  )
}
