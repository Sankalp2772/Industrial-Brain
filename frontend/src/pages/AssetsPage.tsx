import * as React from "react"
import { ApiService } from "@/services/api"
import { AlertTriangle, CheckCircle2, Clock, FileText, Settings, ShieldAlert, Sparkles, TrendingDown, TrendingUp, Activity, PenTool, Bot, Loader2 } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { CitationBadge } from "@/components/ai/CitationBadge"
import { SuggestedQuestions } from "@/components/ai/SuggestedQuestions"
import { cn } from "@/lib/utils"

export function AssetsPage() {
  const [loading, setLoading] = React.useState(true)
  const [profile, setProfile] = React.useState<any>(null)
  const [timeline, setTimeline] = React.useState<any[]>([])
  const [summary, setSummary] = React.useState<string>("")
  const [docs, setDocs] = React.useState<any[]>([])

  React.useEffect(() => {
    async function loadAsset() {
      try {
        const assetsRes = await ApiService.client.get(`/assets`);
        const assetsJson = assetsRes.data;
        let targetAssetId = "P-101";
        if (assetsJson.success && assetsJson.data.assets.length > 0) {
          targetAssetId = assetsJson.data.assets[0].id;
        }

        const ASSET_ID = targetAssetId;
        const [profRes, timeRes, sumRes, docsRes] = await Promise.all([
          ApiService.client.get(`/assets/${ASSET_ID}`),
          ApiService.client.get(`/assets/${ASSET_ID}/timeline`),
          ApiService.client.get(`/assets/${ASSET_ID}/summary`),
          ApiService.client.get(`/assets/${ASSET_ID}/documents`)
        ])
        
        const p = profRes.data
        const t = timeRes.data
        const s = sumRes.data
        const d = docsRes.data
        
        if (p.success) setProfile(p.data)
        if (t.success) setTimeline(t.data)
        if (s.success) setSummary(s.data.summary)
        if (d.success) setDocs(d.data)
      } catch (e) {
        console.error(e)
      } finally {
        setLoading(false)
      }
    }
    loadAsset()
  }, [])

  if (loading) {
    return <div className="flex items-center justify-center h-full"><Loader2 className="w-8 h-8 animate-spin text-primary" /></div>
  }

  if (!profile) {
    return <div className="p-8 text-center text-muted-foreground">Asset not found or backend unavailable. Make sure to run Graph Builder first.</div>
  }

  return (
    <div className="space-y-6 max-w-7xl animate-in fade-in duration-500">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div className="flex items-center gap-4">
           <div className="bg-primary/10 p-3 rounded-lg border border-primary/20">
             <Settings className="w-8 h-8 text-primary" />
           </div>
           <div>
             <div className="flex items-center gap-2">
               <h1 className="text-3xl font-bold tracking-tight">{profile.asset_id}</h1>
               <Badge className={profile.health.classification === 'Healthy' ? "bg-success text-success-foreground" : "bg-warning text-warning-foreground"}>
                 {profile.health.classification}
               </Badge>
             </div>
             <p className="text-muted-foreground mt-1 flex items-center text-sm">
               {profile.type} &bull; {profile.properties?.location || "Unknown Location"} 
             </p>
           </div>
        </div>
        <div className="flex gap-2">
           <Button variant="outline">View Knowledge Graph</Button>
           <Button>Create Work Order</Button>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        <div className="space-y-6 col-span-1">
          <Card className="shadow-sm border-primary/20 bg-primary/5 relative overflow-hidden">
             <div className="absolute top-0 right-0 p-4 opacity-10">
               <Activity className="w-24 h-24" />
             </div>
             <CardHeader className="pb-2">
               <CardTitle className="text-base flex items-center">
                 <Sparkles className="w-4 h-4 mr-2 text-primary" />
                 Health Score
               </CardTitle>
             </CardHeader>
             <CardContent>
               <div className="flex items-end gap-2">
                 <span className="text-5xl font-bold text-primary">{profile.health.score}</span>
                 <span className="text-muted-foreground mb-1">/ 100</span>
               </div>
               <div className="mt-4 space-y-2 text-xs">
                 {profile.health.reasons.map((r: string, i: number) => (
                   <div key={i} className="text-muted-foreground">- {r}</div>
                 ))}
               </div>
             </CardContent>
          </Card>

          <Card className="shadow-sm">
             <CardHeader className="pb-3 border-b">
               <CardTitle className="text-base">Connected Graph Nodes</CardTitle>
             </CardHeader>
             <CardContent className="pt-4 space-y-4">
               <div>
                 <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Metrics</h4>
                 <div className="flex flex-wrap gap-2">
                   <Badge variant="secondary">Incidents: {profile.connected_incidents}</Badge>
                   <Badge variant="secondary">Maintenance: {profile.connected_maintenance}</Badge>
                   <Badge variant="secondary">Docs: {profile.connected_documents}</Badge>
                 </div>
               </div>
               <div>
                 <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Documentation</h4>
                 <div className="space-y-2">
                   {docs.map((d: any, i: number) => (
                      <div key={i} className="flex items-center text-sm">
                        <FileText className="w-4 h-4 mr-2 text-muted-foreground"/> {d.type || 'Document'} {d.id}
                      </div>
                   ))}
                 </div>
               </div>
             </CardContent>
          </Card>
        </div>

        <div className="space-y-6 col-span-1 md:col-span-2">
          <Card className="shadow-sm border-primary/30">
            <CardHeader className="bg-primary/5 border-b pb-4">
              <CardTitle className="text-lg flex items-center justify-between">
                <div className="flex items-center">
                  <Bot className="w-5 h-5 mr-2 text-primary" />
                  AI Intelligence Summary
                </div>
                <Badge variant="outline" className="font-normal bg-background">Live from Gemini</Badge>
              </CardTitle>
            </CardHeader>
            <CardContent className="pt-6">
              <div className="text-sm leading-relaxed text-foreground/90 space-y-4">
                <p>{summary}</p>
              </div>
            </CardContent>
          </Card>

          <Card className="shadow-sm">
            <CardHeader className="pb-3 border-b">
              <CardTitle className="text-lg">Operational Timeline</CardTitle>
              <CardDescription>Chronological history merged from Neo4j</CardDescription>
            </CardHeader>
            <CardContent className="pt-6 pl-2 max-h-[400px] overflow-y-auto">
              <div className="space-y-6 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-border before:via-border before:to-transparent">
                {timeline.map((event: any, i: number) => (
                  <TimelineEvent 
                    key={i}
                    date={event.date} 
                    title={event.type} 
                    description={event.description} 
                    type={event.type.toLowerCase() === 'incident' ? 'incident' : event.type.toLowerCase() === 'maintenance' ? 'maintenance' : 'inspection'} 
                  />
                ))}
                {timeline.length === 0 && <div className="text-center text-muted-foreground text-sm">No timeline events found in graph.</div>}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

function TimelineEvent({ date, title, description, type }: { date: string, title: string, description: string, type: string }) {
  const typeConfig: any = {
    incident: { icon: ShieldAlert, color: "text-destructive", border: "border-destructive", bg: "bg-destructive/10" },
    maintenance: { icon: PenTool, color: "text-primary", border: "border-primary", bg: "bg-primary/10" },
    inspection: { icon: CheckCircle2, color: "text-success", border: "border-success", bg: "bg-success/10" },
  }
  const config = typeConfig[type] || typeConfig.maintenance
  const Icon = config.icon

  return (
    <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
      <div className={cn("flex items-center justify-center w-10 h-10 rounded-full border-2 bg-background z-10 shrink-0 relative md:mx-auto", config.border, config.color)}>
        <Icon className="w-5 h-5" />
      </div>
      <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded-xl border shadow-sm bg-card ml-4 md:ml-0 md:odd:mr-4 md:even:ml-4 transition-shadow hover:shadow-md">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-1">
          <h4 className={cn("text-sm font-semibold tracking-tight", config.color)}>{title}</h4>
          <span className="text-[10px] text-muted-foreground whitespace-nowrap mt-1 sm:mt-0 font-medium uppercase tracking-wider">{date}</span>
        </div>
        <p className="text-xs text-muted-foreground mt-2 leading-relaxed">{description}</p>
      </div>
    </div>
  )
}
