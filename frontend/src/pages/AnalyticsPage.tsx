import * as React from "react"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area, PieChart, Pie, Cell } from "recharts"
import { Download, Calendar, Activity, Database, TrendingUp, Loader2 } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ApiService } from "@/services/api"
import { AnalyticsData } from "@/types"

const COLORS = ['hsl(var(--success))', 'hsl(var(--warning))', 'hsl(var(--destructive))', 'hsl(var(--muted))']

export function AnalyticsPage() {
  const [loading, setLoading] = React.useState(true)
  const [data, setData] = React.useState<AnalyticsData | null>(null)

  React.useEffect(() => {
    async function loadData() {
      try {
        const result = await ApiService.getAnalytics()
        setData(result)
      } catch (e) {
        console.error(e)
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

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Business Analytics</h1>
          <p className="text-muted-foreground mt-1">Platform utilization, knowledge growth, and asset intelligence trends.</p>
        </div>
        <div className="flex gap-2">
           <Button variant="outline" className="bg-background"><Calendar className="w-4 h-4 mr-2" /> Last 6 Months</Button>
           <Button><Download className="w-4 h-4 mr-2" /> Export Report</Button>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        
        {/* Knowledge Growth */}
        <Card className="col-span-1 md:col-span-2 shadow-sm">
          <CardHeader>
            <CardTitle className="text-lg flex items-center">
              <TrendingUp className="w-5 h-5 mr-2 text-primary" />
              Knowledge Graph Growth
            </CardTitle>
            <CardDescription>Total nodes (entities) and edges (relationships) ingested over time.</CardDescription>
          </CardHeader>
          <CardContent className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data.knowledgeGrowth} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorNodes" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="hsl(var(--border))" />
                <XAxis dataKey="name" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `${value / 1000}k`} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '8px' }}
                  itemStyle={{ color: 'hsl(var(--foreground))' }}
                />
                <Area type="monotone" dataKey="nodes" stroke="hsl(var(--primary))" fillOpacity={1} fill="url(#colorNodes)" strokeWidth={2} name="Total Nodes" />
                <Area type="monotone" dataKey="edges" stroke="hsl(var(--secondary))" fillOpacity={0.1} strokeWidth={2} strokeDasharray="5 5" name="Total Relationships" />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Asset Health Distribution */}
        <Card className="col-span-1 shadow-sm">
          <CardHeader>
            <CardTitle className="text-lg flex items-center">
              <Activity className="w-5 h-5 mr-2 text-primary" />
              Fleet Health Status
            </CardTitle>
            <CardDescription>Current status of all registered assets.</CardDescription>
          </CardHeader>
          <CardContent className="h-80 flex flex-col items-center justify-center relative">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={data.fleetHealth}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                  stroke="none"
                >
                  {data.fleetHealth.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '8px' }}
                />
              </PieChart>
            </ResponsiveContainer>
            
            <div className="w-full mt-4 grid grid-cols-2 gap-4">
              {data.fleetHealth.map((item, index) => (
                 <div key={item.name} className="flex items-center text-sm">
                   <div className="w-3 h-3 rounded-full mr-2" style={{ backgroundColor: COLORS[index] }} />
                   <span className="text-muted-foreground mr-auto">{item.name}</span>
                   <span className="font-semibold">{item.value}</span>
                 </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Failure Root Causes */}
        <Card className="col-span-1 shadow-sm">
          <CardHeader>
            <CardTitle className="text-lg">Predictive Anomaly Trends</CardTitle>
            <CardDescription>Most common telemetry alerts triggering AI analysis.</CardDescription>
          </CardHeader>
          <CardContent className="h-64">
             <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data.failureTrends} layout="vertical" margin={{ top: 0, right: 0, left: 30, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="hsl(var(--border))" />
                  <XAxis type="number" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis type="category" dataKey="name" stroke="hsl(var(--foreground))" fontSize={12} tickLine={false} axisLine={false} width={80} />
                  <Tooltip cursor={{ fill: 'hsl(var(--muted))' }} contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '8px' }} />
                  <Bar dataKey="count" fill="hsl(var(--primary))" radius={[0, 4, 4, 0]} barSize={20} />
                </BarChart>
             </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Most Queried Assets Table */}
        <Card className="col-span-1 md:col-span-2 shadow-sm">
          <CardHeader>
            <CardTitle className="text-lg flex items-center">
              <Database className="w-5 h-5 mr-2 text-primary" />
              Most Queried Assets
            </CardTitle>
            <CardDescription>Assets frequently investigated using the AI Copilot.</CardDescription>
          </CardHeader>
          <CardContent>
             <div className="space-y-4">
               <div className="grid grid-cols-12 text-xs font-semibold text-muted-foreground uppercase tracking-wider pb-2 border-b">
                 <div className="col-span-5">Asset</div>
                 <div className="col-span-3">Queries (30d)</div>
                 <div className="col-span-4">Primary Topic</div>
               </div>
               
               {data.mostQueriedAssets.map(asset => (
                 <AssetRow key={asset.id} name={asset.name} queries={asset.queries.toString()} topic={asset.topic} />
               ))}
               
             </div>
          </CardContent>
        </Card>

      </div>
    </div>
  )
}

function AssetRow({ name, queries, topic }: { name: string, queries: string, topic: string }) {
  return (
    <div className="grid grid-cols-12 text-sm py-2 border-b last:border-0 hover:bg-muted/50 rounded transition-colors -mx-2 px-2">
      <div className="col-span-5 font-medium flex items-center">{name}</div>
      <div className="col-span-3 text-muted-foreground flex items-center">{queries}</div>
      <div className="col-span-4 text-muted-foreground truncate pr-2 flex items-center">{topic}</div>
    </div>
  )
}
