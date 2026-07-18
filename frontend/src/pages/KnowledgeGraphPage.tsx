import * as React from "react"
import ForceGraph2D from 'react-force-graph-2d'
import { ApiService } from "@/services/api"
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

  const containerRef = React.useRef<HTMLDivElement>(null)
  const [dimensions, setDimensions] = React.useState({ width: 800, height: 600 })

  React.useEffect(() => {
    if (!containerRef.current) return
    const resizeObserver = new ResizeObserver((entries) => {
      for (let entry of entries) {
        setDimensions({
          width: entry.contentRect.width,
          height: entry.contentRect.height
        })
      }
    })
    resizeObserver.observe(containerRef.current)
    return () => resizeObserver.disconnect()
  }, [])

  const graphData = React.useMemo(() => {
    if (!nodeData || !nodeData.asset) return { nodes: [], links: [] }
    
    const nodes = []
    const links = []
    
    nodes.push({
      id: nodeData.asset.id,
      name: nodeData.asset.name,
      label: nodeData.asset.type || 'Asset',
      val: 20,
      color: 'hsl(221, 83%, 53%)'
    })
    
    nodeData.connected_nodes?.forEach((n: any) => {
      const isDoc = n._labels?.includes('Document')
      nodes.push({
        id: n.id || n.name,
        name: n.name || n.id,
        label: isDoc ? 'Document' : (n.type || 'Node'),
        val: isDoc ? 10 : 15,
        color: isDoc ? '#10b981' : '#f59e0b'
      })
    })
    
    nodeData.relationships?.forEach((r: any) => {
      links.push({
        source: r.source,
        target: r.target,
        name: r.type,
        color: '#94a3b8'
      })
    })
    
    return { nodes, links }
  }, [nodeData])

  React.useEffect(() => {
    async function loadInitial() {
      try {
        const assetsRes = await ApiService.client.get(`/assets`);
        const assetsJson = assetsRes.data;
        if (assetsJson.success && assetsJson.data.assets.length > 0) {
          const targetAssetId = assetsJson.data.assets[0].id;
          setSelectedNode(targetAssetId)
        }
      } catch (e) {
        console.error(e)
      }
    }
    loadInitial()
  }, [])

  React.useEffect(() => {
    async function loadRelationships() {
      try {
        setLoading(true)
        const res = await ApiService.client.get(`/assets/${selectedNode}/relationships`)
        const json = res.data
        if (json.success) {
          setNodeData(json.data)
        }
      } catch (e) {
        console.error(e)
      } finally {
        setLoading(false)
      }
    }
    if (selectedNode) {
      loadRelationships()
    }
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
          <div ref={containerRef} className="flex-1 relative overflow-hidden flex items-center justify-center">
             {graphData.nodes.length > 0 ? (
               <ForceGraph2D
                 graphData={graphData}
                 width={dimensions.width}
                 height={dimensions.height}
                 nodeLabel="name"
                 nodeColor="color"
                 nodeRelSize={1}
                 linkColor="color"
                 linkWidth={2}
                 linkDirectionalArrowLength={3.5}
                 linkDirectionalArrowRelPos={1}
                 onNodeClick={(node: any) => setSelectedNode(node.id)}
                 nodeCanvasObject={(node: any, ctx, globalScale) => {
                   const label = node.name || node.id;
                   const fontSize = 12/globalScale;
                   ctx.font = `${fontSize}px Sans-Serif`;
                   ctx.beginPath();
                   ctx.arc(node.x, node.y, node.val, 0, 2 * Math.PI, false);
                   ctx.fillStyle = node.color;
                   ctx.fill();
                   
                   ctx.textAlign = 'center';
                   ctx.textBaseline = 'middle';
                   ctx.fillStyle = '#1e293b'; // dark slate for contrast
                   ctx.fillText(label, node.x, node.y + node.val + fontSize);
                 }}
               />
             ) : (
               <div className="text-muted-foreground flex items-center"><Loader2 className="w-4 h-4 mr-2 animate-spin" /> Loading Graph...</div>
             )}
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
