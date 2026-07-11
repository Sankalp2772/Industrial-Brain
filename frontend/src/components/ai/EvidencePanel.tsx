import * as React from "react"
import { FileText, ExternalLink } from "lucide-react"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

export interface EvidenceSource {
  id: string
  title: string
  type: string
  url?: string
  snippet: string
}

export interface EvidencePanelProps {
  sources: EvidenceSource[]
}

export function EvidencePanel({ sources }: EvidencePanelProps) {
  return (
    <div className="space-y-4">
      <h4 className="text-sm font-semibold tracking-tight">Supporting Evidence</h4>
      <div className="grid gap-3">
        {sources.map((source) => (
          <Card key={source.id} className="bg-surface border-muted shadow-sm overflow-hidden">
            <CardHeader className="p-3 pb-0">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <FileText className="w-4 h-4 text-muted-foreground" />
                  <CardTitle className="text-sm font-medium leading-none">{source.title}</CardTitle>
                </div>
                <Badge variant="secondary" className="text-[10px] uppercase tracking-wider">{source.type}</Badge>
              </div>
            </CardHeader>
            <CardContent className="p-3 pt-2">
              <p className="text-xs text-muted-foreground line-clamp-2 italic border-l-2 border-primary/20 pl-2">
                "{source.snippet}"
              </p>
              {source.url && (
                <a href={source.url} className="inline-flex items-center text-[10px] text-primary hover:underline mt-2 font-medium">
                  View Source <ExternalLink className="w-3 h-3 ml-1" />
                </a>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
