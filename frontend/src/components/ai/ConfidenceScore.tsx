import * as React from "react"
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"

export interface ConfidenceScoreProps {
  score: number // 0 to 100
  className?: string
}

export function ConfidenceScore({ score, className }: ConfidenceScoreProps) {
  let variant: "default" | "secondary" | "destructive" | "outline" = "default"
  let colorClass = ""

  if (score >= 90) {
    colorClass = "bg-success/15 text-success hover:bg-success/25 border-success/30"
  } else if (score >= 70) {
    colorClass = "bg-warning/15 text-warning-foreground hover:bg-warning/25 border-warning/30 text-amber-700 dark:text-amber-400"
  } else {
    colorClass = "bg-destructive/15 text-destructive hover:bg-destructive/25 border-destructive/30"
  }

  return (
    <Badge variant="outline" className={cn("font-medium", colorClass, className)}>
      {score}% Confidence
    </Badge>
  )
}
