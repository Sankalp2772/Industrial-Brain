import * as React from "react"

export function TypingAnimation() {
  return (
    <div className="flex items-center space-x-1 p-4 bg-muted/30 rounded-lg max-w-[100px]">
      <div className="w-2 h-2 bg-primary/60 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
      <div className="w-2 h-2 bg-primary/60 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
      <div className="w-2 h-2 bg-primary/60 rounded-full animate-bounce"></div>
    </div>
  )
}

export function ProcessingIndicator() {
  return (
    <div className="flex items-center space-x-3 text-sm text-muted-foreground">
      <div className="w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin"></div>
      <span>Analyzing industrial data...</span>
    </div>
  )
}
