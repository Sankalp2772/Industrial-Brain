import * as React from "react"
import { 
  FileText, Database, Network, AlertTriangle, 
  Clock, Upload, Bot, Search, Activity, 
  CheckCircle2, Server, Globe, Loader2 
} from "lucide-react"
import { Link } from "react-router-dom"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ApiService } from "@/services/api"
import { DashboardMetrics, Incident, SystemStatus } from "@/types"
import { cn } from "@/lib/utils"

export function DashboardPage() {
  const [loading, setLoading] = React.useState(true)
  const [data, setData] = React.useState<{
    metrics: DashboardMetrics
    incidents: Incident[]
    systemStatus: SystemStatus[]
  } | null>(null)

  React.useEffect(() => {
    async function loadData() {
      try {
        const result = await ApiService.getDashboardData()
        setData(result)
      } catch (e) {
        console.error("Failed to fetch dashboard data", e)
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [])

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center h-full">
        <Loader2 className="w-8 h-8 text-primary animate-spin" />
      </div>
    )
  }

  const { metrics, incidents, systemStatus } = data

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Plant Operations Dashboard</h1>
        <p className="text-muted-foreground mt-1">Real-time overview of AI intelligence and asset health.</p>
      </div>

      {/* Top KPI Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-5">
        <KpiCard title="Total Documents" value={metrics.totalDocuments.toLocaleString()} icon={FileText} trend="+2.5%" />
        <KpiCard title="Registered Assets" value={metrics.registeredAssets.toLocaleString()} icon={Database} trend="+0.8%" />
        <KpiCard title="Knowledge Coverage" value={`${metrics.knowledgeCoverage}%`} icon={Network} trend="+5.2%" />
        <KpiCard title="Critical Assets" value={metrics.criticalAssets.toString()} icon={AlertTriangle} trend="-2" alert />
        <KpiCard title="Avg Query Time" value={metrics.avgQueryTime} icon={Clock} trend="-0.1s" />
      </div>

      {/* Quick Actions */}
      <div className="grid gap-4 md:grid-cols-4">
        <QuickActionCard title="Upload Document" description="Ingest new manuals or logs" icon={Upload} href="/app/documents/upload" />
        <QuickActionCard title="Open AI Copilot" description="Troubleshoot with Industrial AI" icon={Bot} href="/app/copilot" />
        <QuickActionCard title="Search Assets" description="Find equipment by ID or tag" icon={Search} href="/app/assets" />
        <QuickActionCard title="Knowledge Graph" description="Explore operational relationships" icon={Network} href="/app/knowledge-graph" />
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Recent Incidents */}
        <Card className="col-span-1 border-destructive/20 shadow-sm">
          <CardHeader className="bg-destructive/5 border-b pb-4">
            <CardTitle className="text-lg flex items-center">
              <AlertTriangle className="w-5 h-5 mr-2 text-destructive" />
              Recent Incidents
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-4 space-y-4">
             {incidents.map(inc => (
               <IncidentRow key={inc.id} asset={inc.asset} issue={inc.issue} time={inc.time} severity={inc.severity} />
             ))}
          </CardContent>
        </Card>

        {/* Recent AI Queries (static for now, could be moved to API) */}
        <Card className="col-span-1 shadow-sm">
          <CardHeader className="bg-primary/5 border-b pb-4">
            <CardTitle className="text-lg flex items-center">
              <Bot className="w-5 h-5 mr-2 text-primary" />
              Recent AI Queries
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-4 space-y-4">
             <QueryRow query="What is the standard operating pressure for Pump A-42?" user="Engineer J." />
             <QueryRow query="Show maintenance history for Conveyor B motor." user="Tech M." />
             <QueryRow query="Locate replacement part for Valve C-12 actuator." user="Manager S." />
             <QueryRow query="Why did Compressor 4 trip yesterday?" user="Engineer J." />
          </CardContent>
        </Card>

        {/* Recent Uploads */}
        <Card className="col-span-1 shadow-sm">
          <CardHeader className="border-b pb-4">
            <CardTitle className="text-lg flex items-center">
              <FileText className="w-5 h-5 mr-2 text-muted-foreground" />
              Recent Uploads
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-4 space-y-4">
             <UploadRow filename="Pump_A42_Manual_v2.pdf" status="indexed" />
             <UploadRow filename="Q3_Maintenance_Logs.csv" status="processing" />
             <UploadRow filename="Sensor_Telemetry_Week40.json" status="uploaded" />
             <UploadRow filename="Old_Valve_Specs.pdf" status="failed" />
          </CardContent>
        </Card>
      </div>

      {/* System Status Module */}
      <Card className="shadow-sm">
        <CardHeader className="bg-surface border-b pb-4">
          <CardTitle className="text-lg flex items-center">
            <Server className="w-5 h-5 mr-2 text-muted-foreground" />
            Core Infrastructure Status
          </CardTitle>
          <CardDescription>Real-time health of the Industrial Brain AI stack.</CardDescription>
        </CardHeader>
        <CardContent className="pt-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
             {systemStatus.map(sys => (
               <StatusIndicator key={sys.name} name={sys.name} status={sys.status} latency={sys.latency} />
             ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

function KpiCard({ title, value, icon: Icon, trend, alert }: { title: string, value: string, icon: any, trend: string, alert?: boolean }) {
  return (
    <Card className={cn("shadow-sm", alert && "border-destructive/50")}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <Icon className={cn("h-4 w-4", alert ? "text-destructive" : "text-muted-foreground")} />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        <p className={cn("text-xs flex items-center mt-1 font-medium", trend.startsWith('+') ? "text-success" : alert ? "text-destructive" : "text-muted-foreground")}>
          {trend} from last week
        </p>
      </CardContent>
    </Card>
  )
}

function QuickActionCard({ title, description, icon: Icon, href }: { title: string, description: string, icon: any, href: string }) {
  return (
    <Card className="hover:border-primary/50 transition-colors shadow-sm group">
      <Link to={href} className="block h-full">
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <div className="bg-primary/10 p-2 rounded-md group-hover:bg-primary/20 transition-colors">
              <Icon className="h-5 w-5 text-primary" />
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <CardTitle className="text-base mb-1 group-hover:text-primary transition-colors">{title}</CardTitle>
          <p className="text-xs text-muted-foreground">{description}</p>
        </CardContent>
      </Link>
    </Card>
  )
}

function IncidentRow({ asset, issue, time, severity }: { asset: string, issue: string, time: string, severity: 'critical' | 'warning' }) {
  return (
    <div className="flex items-start justify-between text-sm border-b last:border-0 pb-3 last:pb-0">
      <div>
        <div className="font-semibold">{asset}</div>
        <div className={cn("text-xs font-medium mt-0.5", severity === 'critical' ? "text-destructive" : "text-amber-600 dark:text-amber-400")}>
          {issue}
        </div>
      </div>
      <div className="text-xs text-muted-foreground whitespace-nowrap">{time}</div>
    </div>
  )
}

function QueryRow({ query, user }: { query: string, user: string }) {
  return (
    <div className="text-sm border-b last:border-0 pb-3 last:pb-0">
      <div className="font-medium line-clamp-2 leading-relaxed">"{query}"</div>
      <div className="text-xs text-muted-foreground mt-1.5 flex items-center">
        <div className="w-4 h-4 bg-muted rounded-full flex items-center justify-center mr-1.5 text-[8px] font-bold">
          {user.charAt(0)}
        </div>
        {user}
      </div>
    </div>
  )
}

function UploadRow({ filename, status }: { filename: string, status: 'uploaded' | 'processing' | 'indexed' | 'failed' }) {
  const statusColors = {
    uploaded: "bg-secondary text-secondary-foreground",
    processing: "bg-primary/20 text-primary border-primary/30",
    indexed: "bg-success/20 text-success border-success/30",
    failed: "bg-destructive/20 text-destructive border-destructive/30"
  }
  
  return (
    <div className="flex flex-col gap-2 text-sm border-b last:border-0 pb-3 last:pb-0">
      <div className="font-medium truncate" title={filename}>{filename}</div>
      <div className="flex items-center justify-between">
        <Badge variant="outline" className={cn("text-[10px] uppercase tracking-wider px-2 py-0", statusColors[status])}>
          {status}
        </Badge>
        {status === 'processing' && <Activity className="w-3 h-3 text-primary animate-pulse" />}
      </div>
    </div>
  )
}

function StatusIndicator({ name, status, latency }: { name: string, status: 'healthy' | 'degraded' | 'down', latency: string }) {
  return (
    <div className="flex flex-col">
      <div className="flex items-center text-sm font-medium mb-2">
        <div className={cn("w-2 h-2 rounded-full mr-2", status === 'healthy' ? "bg-success" : status === 'degraded' ? "bg-warning" : "bg-destructive")} />
        {name}
      </div>
      <div className="text-xs text-muted-foreground flex items-center justify-between">
        <span>Latency:</span>
        <span className="font-mono">{latency}</span>
      </div>
    </div>
  )
}
