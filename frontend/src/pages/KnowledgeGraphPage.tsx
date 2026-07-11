import * as React from "react"
import { Search, Filter, Network, Database, FileText, ChevronRight, Share2, Maximize, ZoomIn, ZoomOut, Loader2 } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"

export function KnowledgeGraphPage() {
  const [selectedNode, setSelectedNode] = React.useState<string | null>(null)
  const [nodeData, setNodeData] = React.useState<any>(null)
  const [loading, setLoading] = React.useState(true)
  const [defaultAsset, setDefaultAsset] = React.useState<string>("P-101")

  React.useEffect(() => {
    async function loadInitial() {
      try {
        const assetsRes = await fetch(`http://localhost:8001/api/v1/assets`);
        const assetsJson = await assetsRes.json();
        if (assetsJson.success && assetsJson.data.assets.length > 0) {
          const targetAssetId = assetsJson.data.assets[0].id;
          setDefaultAsset(targetAssetId)
          setSelectedNode(targetAssetId)
        } else {
          setSelectedNode("P-101")
        }
      } catch (e) {
        console.error(e)
      }
    }
    loadInitial()
  }, [])

  React.useEffect(() => {
    if (!selectedNode) return;
    async function loadRelationships() {
      try {
        setLoading(true)
        const res = await fetch(`http://localhost:8001/api/v1/assets/${selectedNode}/relationships`)
        const json = await res.json()
        if (json.success) {
          setNodeData(json.data)
        }
      } catch (e) {
        console.error(e)
      } finally {
        setLoading(false)
      }
    }
    loadRelationships()
  }, [selectedNode])

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] animate-in fade-in duration-500">
      <div className="mb-4">
        <h1 className="text-3xl font-bold tracking-tight">Knowledge Graph Explorer</h1>
        <p className="text-muted-foreground mt-1">Visualize relationships between assets, maintenance logs, and documents.</p>
      </div>

      <div className="flex-1 flex gap-4 overflow-hidden">
        <Card className="w-80 flex-shrink-0 flex flex-col shadow-sm h-full overflow-hidden">
          <CardHeader className="pb-3 border-b bg-surface">
            <CardTitle className="text-lg">Filters</CardTitle>
          </CardHeader>
          <CardContent className="flex-1 overflow-y-auto p-4 space-y-6">
            <div className="space-y-3">
              <Label>Search Graph</Label>
              <div className="relative">
                <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input placeholder="Find nodes..." className="pl-9" />
              </div>
            </div>
            <Button className="w-full">Apply Filters</Button>
          </CardContent>
        </Card>

        <Card className="flex-1 flex flex-col shadow-sm overflow-hidden relative bg-slate-50 dark:bg-slate-900/50">
          <div className="absolute top-4 right-4 flex space-x-2 z-10">
             <Button variant="outline" size="icon" className="bg-background/80 backdrop-blur"><ZoomIn className="w-4 h-4" /></Button>
             <Button variant="outline" size="icon" className="bg-background/80 backdrop-blur"><ZoomOut className="w-4 h-4" /></Button>
             <Button variant="outline" size="icon" className="bg-background/80 backdrop-blur"><Maximize className="w-4 h-4" /></Button>
          </div>
          <div className="flex-1 relative overflow-hidden flex items-center justify-center p-8">
             <svg width="100%" height="100%" viewBox="0 0 800 600" className="absolute inset-0 w-full h-full">
                <g className="cursor-pointer" onClick={() => setSelectedNode(defaultAsset)}>
                  <circle cx="400" cy="300" r="40" fill="hsl(var(--primary))" opacity={selectedNode === defaultAsset ? "0.3" : "0.1"} stroke="hsl(var(--primary))" strokeWidth="2" />
                  <circle cx="400" cy="300" r="25" fill="hsl(var(--primary))" />
                  <text x="400" y="355" fontSize="14" fill="currentColor" textAnchor="middle" className="font-bold">{defaultAsset}</text>
                </g>
                <text x="400" y="380" fontSize="12" fill="currentColor" textAnchor="middle" className="text-muted-foreground">Click to load live graph relationships</text>
             </svg>
          </div>
        </Card>

        <Card className="w-80 flex-shrink-0 flex flex-col shadow-sm h-full overflow-hidden">
          <CardHeader className="pb-3 border-b bg-surface flex flex-row items-center justify-between">
            <CardTitle className="text-lg">Node Details</CardTitle>
            <Share2 className="w-4 h-4 text-muted-foreground cursor-pointer hover:text-foreground" />
          </CardHeader>
          {loading ? (
            <div className="flex-1 flex items-center justify-center"><Loader2 className="w-6 h-6 animate-spin text-primary" /></div>
          ) : nodeData && nodeData.asset ? (
            <CardContent className="flex-1 overflow-y-auto p-0">
              <div className="p-4 border-b">
                 <div className="flex items-center gap-2 mb-2">
                   <Badge variant="outline" className="bg-primary/10 text-primary border-primary/20">Asset</Badge>
                 </div>
                 <h2 className="text-2xl font-bold tracking-tight">{nodeData.asset.id}</h2>
                 <p className="text-sm text-muted-foreground mt-1">{nodeData.asset.name}</p>
              </div>

              <div className="p-4 border-b">
                <h3 className="text-sm font-semibold mb-3 flex items-center">
                  <Network className="w-4 h-4 mr-2" /> Relationships ({nodeData.relationships?.length || 0})
                </h3>
                <div className="space-y-2">
                  {nodeData.relationships?.map((r: any, i: number) => (
                    <RelItem key={i} type={r.type} target={r.target || r.source} />
                  ))}
                </div>
              </div>
              <div className="p-4 border-b">
                <h3 className="text-sm font-semibold mb-3 flex items-center">
                  <Database className="w-4 h-4 mr-2" /> Connected Nodes
                </h3>
                <div className="space-y-2">
                  {nodeData.connected_nodes?.map((n: any, i: number) => (
                    <div key={i} className="text-xs text-muted-foreground">- {n.id || n.name || n.action || n.finding || 'Node'}</div>
                  ))}
                </div>
              </div>
            </CardContent>
          ) : (
            <div className="flex-1 flex items-center justify-center text-muted-foreground text-sm p-6 text-center">
              Select a node in the graph.
            </div>
          )}
        </Card>
      </div>
    </div>
  )
}

function RelItem({ type, target }: { type: string, target: string }) {
  return (
    <div className="flex items-center text-xs justify-between group cursor-pointer hover:bg-muted p-1 -mx-1 rounded">
      <span className="font-mono text-[10px] text-muted-foreground bg-surface px-1.5 py-0.5 rounded border">{type}</span>
      <span className="font-medium flex items-center truncate max-w-[150px]">{target} <ChevronRight className="w-3 h-3 ml-1 opacity-0 group-hover:opacity-100 transition-opacity" /></span>
    </div>
  )
}
