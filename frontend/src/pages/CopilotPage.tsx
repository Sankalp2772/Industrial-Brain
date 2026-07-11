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

import { ApiService } from "../services/api"

export function CopilotPage() {
  const [inputValue, setInputValue] = React.useState("")
  const [messages, setMessages] = React.useState<{role: string, content: string, sources?: any[]}[]>([
    {
      role: 'assistant',
      content: 'Hello! I am the Industrial AI Copilot. Ask me questions about your uploaded manuals, schematics, and assets.'
    }
  ])
  const [isTyping, setIsTyping] = React.useState(false)

  const handleSend = async () => {
    if (!inputValue.trim()) return
    const userMessage = inputValue
    setInputValue("")
    setMessages(prev => [...prev, { role: 'user', content: userMessage }])
    setIsTyping(true)

    try {
      const aiResponse = await ApiService.queryCopilot(userMessage)
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: aiResponse.answer,
        sources: aiResponse.sources
      }])
    } catch (e) {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Error: Could not reach the backend copilot API.' 
      }])
    } finally {
      setIsTyping(false)
    }
  }

  const latestSources = messages.filter(m => m.role === 'assistant' && m.sources && m.sources.length > 0).pop()?.sources || []

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
          
          {messages.map((msg, i) => (
            msg.role === 'user' ? (
              <UserMessage key={i} content={msg.content} />
            ) : (
              <div key={i} className="flex gap-4">
                <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
                  <Bot className="w-5 h-5 text-primary-foreground" />
                </div>
                <div className="flex-1 space-y-4">
                  <div className="text-sm font-medium">Industrial AI Copilot</div>
                  <div className="text-sm leading-relaxed text-foreground/90 space-y-4">
                    <p>{msg.content}</p>
                  </div>
                </div>
              </div>
            )
          ))}

          {isTyping && (
             <div className="flex gap-4">
               <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
                 <Bot className="w-5 h-5 text-primary-foreground" />
               </div>
               <div className="flex-1 space-y-4">
                 <div className="text-sm font-medium">Industrial AI Copilot</div>
                 <div className="text-sm text-muted-foreground animate-pulse">Thinking...</div>
               </div>
             </div>
          )}

        </div>

        {/* Input Area */}
        <div className="absolute bottom-0 inset-x-0 p-4 bg-gradient-to-t from-background via-background to-transparent pt-10">
          <div className="max-w-3xl mx-auto relative">
            <Input 
              placeholder="Ask the Industrial Brain about assets, manuals, or telemetry..." 
              className="pr-12 h-14 bg-surface shadow-lg border-primary/20 focus-visible:ring-primary/30"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') handleSend()
              }}
            />
            <Button size="icon" className="absolute right-2 top-2 h-10 w-10" onClick={handleSend} disabled={isTyping}>
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
            {latestSources.length > 0 ? (
              <EvidencePanel 
                sources={latestSources.map((s, idx) => ({
                  id: String(idx+1),
                  title: s.document,
                  type: "document",
                  snippet: s.text
                }))}
              />
            ) : (
              <div className="text-sm text-muted-foreground">No sources required for this query.</div>
            )}
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
