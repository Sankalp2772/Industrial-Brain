import * as React from "react"
import { Button } from "@/components/ui/button"
import { Sparkles } from "lucide-react"

export interface SuggestedQuestionsProps {
  questions: string[]
  onSelect?: (question: string) => void
}

export function SuggestedQuestions({ questions, onSelect }: SuggestedQuestionsProps) {
  if (!questions || questions.length === 0) return null

  return (
    <div className="space-y-3 mt-4">
      <div className="flex items-center text-sm font-medium text-muted-foreground">
        <Sparkles className="w-4 h-4 mr-2 text-primary" />
        Suggested Questions
      </div>
      <div className="flex flex-wrap gap-2">
        {questions.map((q, idx) => (
          <Button
            key={idx}
            variant="outline"
            size="sm"
            className="rounded-full bg-surface text-foreground hover:bg-muted hover:text-primary transition-colors text-xs py-1 h-auto"
            onClick={() => onSelect?.(q)}
          >
            {q}
          </Button>
        ))}
      </div>
    </div>
  )
}
