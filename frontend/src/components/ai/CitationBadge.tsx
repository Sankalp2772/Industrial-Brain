import * as React from "react"
import { cn } from "@/lib/utils"

export interface CitationBadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  index: number
  source?: string
}

export function CitationBadge({ index, source, className, ...props }: CitationBadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center justify-center rounded-sm bg-primary/10 px-1.5 py-0.5 text-xs font-semibold text-primary hover:bg-primary/20 cursor-pointer transition-colors ml-1 align-super",
        className
      )}
      title={source}
      {...props}
    >
      [{index}]
    </span>
  )
}
