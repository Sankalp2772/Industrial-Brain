import * as React from "react"
import { Send, Bot, User, History, MessageSquare, Plus, Network, FileText, Settings, Database, Activity, Cpu } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { CitationBadge } from "@/components/ai/CitationBadge"
import { ConfidenceScore } from "@/components/ai/ConfidenceScore"
import { EvidencePanel } from "@/components/ai/EvidencePanel"
import { SuggestedQuestions } from "@/components/ai/SuggestedQuestions"

export function CopilotPage() {
  const [inputValue, setInputValue] = React.useState("")

  return (
    <div className="flex h-[calc(100vh-8rem)] animate-in fade-in duration-500 overflow-hidden bg-background">
      
      {/* Left Column: Chat History */}
      <div className="w-64 border-r bg-surface flex-shrink-0 flex flex-col hidden md:flex">
        <div className="p-4 border-b">
          <Button className="w-full justify-start" variant="outline">
            <Plus className="w-4 h-4 mr-2" /> New Chat
          </Button>
        </div>
        <div className="flex-1 overflow-y-auto p-3 space-y-2">
          <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2 mt-2 px-2">Today</div>
          <HistoryItem title="Pump A-42 Vibration Analysis" active />
          <HistoryItem title="Maintenance Schedule Q4" />
          <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2 mt-6 px-2">Yesterday</div>
          <HistoryItem title="Compressor M7 Failure Root Cause" />
          <HistoryItem title="Safety Protocol Updates" />
        </div>
      </div>

      {/* Center Column: Chat Area */}
      <div className="flex-1 flex flex-col relative">
        {/* Header */}
        <div className="h-14 border-b bg-surface flex items-center px-6 justify-between flex-shrink-0">
          <div className="flex items-center">
            <Cpu className="w-5 h-5 text-primary mr-2" />
            <h2 className="font-semibold">Pump A-42 Vibration Analysis</h2>
          </div>
          <Badge variant="outline" className="bg-primary/5 text-primary text-xs">Model: Gemini 1.5 Pro</Badge>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-8 pb-32">
          
          <UserMessage content="Why is Pump A-42 showing high vibration today? Does it need immediate maintenance?" />
          
          <div className="flex gap-4">
            <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
              <Bot className="w-5 h-5 text-primary-foreground" />
            </div>
            <div className="flex-1 space-y-4">
              <div className="text-sm font-medium">Industrial AI Copilot</div>
              <div className="text-sm leading-relaxed text-foreground/90 space-y-4">
                <p>
                  Pump A-42 is currently experiencing a <span className="font-semibold text-warning text-amber-600">12% increase in vibration</span> on the primary bearing assembly, crossing the 4.2g threshold at 08:14 AM today<CitationBadge index={1} />.
                </p>
                <p>
                  According to the <span className="font-medium text-primary">Centrifugal Pump Operating Manual v4</span><CitationBadge index={2} />, sustained vibration above 4.0g indicates potential bearing wear or misalignment. Looking at the maintenance history, the bearings were last replaced on Jan 10, 2023, following a critical failure<CitationBadge index={3} />.
                </p>
                <p>
                  <span className="font-semibold text-foreground">Recommendation:</span> Immediate maintenance is not required to prevent catastrophic failure today, but I strongly suggest scheduling a proactive inspection of the bearing housing during the upcoming weekend window to prevent an unplanned outage next week.
                </p>
              </div>
              <div className="flex flex-wrap gap-2 pt-2">
                <SuggestedQuestions questions={[
                  "Create a work order for a bearing inspection.",
                  "Show me the telemetry graph for the last 24 hours.",
                  "What is the part number for the replacement bearing?"
                ]} />
              </div>
            </div>
          </div>

        </div>

        {/* Input Area */}
        <div className="absolute bottom-0 inset-x-0 p-4 bg-gradient-to-t from-background via-background to-transparent pt-10">
          <div className="max-w-3xl mx-auto relative">
            <Input 
              placeholder="Ask the Industrial Brain about assets, manuals, or telemetry..." 
              className="pr-12 h-14 bg-surface shadow-lg border-primary/20 focus-visible:ring-primary/30"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
            />
            <Button size="icon" className="absolute right-2 top-2 h-10 w-10">
              <Send className="w-4 h-4" />
            </Button>
          </div>
          <div className="text-center text-[10px] text-muted-foreground mt-2">
            AI can make mistakes. Verify critical operational insights with original documentation.
          </div>
        </div>
      </div>

      {/* Right Column: Evidence & Context */}
      <div className="w-80 border-l bg-surface flex-shrink-0 hidden lg:flex flex-col overflow-y-auto">
        <div className="p-4 border-b">
          <h3 className="font-semibold flex items-center">
            <Activity className="w-4 h-4 mr-2 text-primary" />
            Intelligence Context
          </h3>
        </div>
        
        <div className="p-4 space-y-6">
          <div className="space-y-2">
             <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Overall Confidence</div>
             <ConfidenceScore score={92} />
          </div>

          <div className="space-y-3">
            <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Source Documents</div>
            <EvidencePanel 
              sources={[
                {
                  id: "1",
                  title: "Centrifugal Pump Manual v4",
                  type: "manual",
                  snippet: "Section 4.2: Sustained vibration above 4.0g on the primary bearing assembly indicates severe wear requiring immediate inspection to prevent housing damage."
                },
                {
                  id: "2",
                  title: "Pump A-42 Maintenance Log",
                  type: "log",
                  snippet: "2023-01-10: Replaced seized bearing assembly after critical failure. Pump was offline for 14 hours."
                }
              ]}
            />
          </div>

          <div className="space-y-3">
            <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Related Assets</div>
            <div className="grid grid-cols-2 gap-2">
              <Button variant="outline" className="h-auto py-2 px-3 justify-start bg-background text-xs">
                <Database className="w-3 h-3 mr-2 text-primary flex-shrink-0" /> Pump A-42
              </Button>
              <Button variant="outline" className="h-auto py-2 px-3 justify-start bg-background text-xs">
                <Settings className="w-3 h-3 mr-2 text-muted-foreground flex-shrink-0" /> Bearing Assy
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function HistoryItem({ title, active }: { title: string, active?: boolean }) {
  return (
    <Button 
      variant={active ? "secondary" : "ghost"} 
      className="w-full justify-start font-normal px-2 h-9 text-xs truncate"
    >
      <MessageSquare className="w-3 h-3 mr-2 opacity-50 flex-shrink-0" />
      <span className="truncate">{title}</span>
    </Button>
  )
}

function UserMessage({ content }: { content: string }) {
  return (
    <div className="flex gap-4">
      <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center flex-shrink-0">
        <User className="w-5 h-5 text-secondary-foreground" />
      </div>
      <div className="flex-1 space-y-1 mt-1">
        <div className="text-sm font-medium">You</div>
        <div className="text-sm text-foreground/80">{content}</div>
      </div>
    </div>
  )
}
