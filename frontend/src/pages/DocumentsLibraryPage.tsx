import * as React from "react"
import { Search, Filter, LayoutGrid, List, MoreVertical, FileText, Bot, Trash2, ExternalLink, Loader2 } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ApiService } from "@/services/api"
import { Document } from "@/types"
import { cn } from "@/lib/utils"

export function DocumentsLibraryPage() {
  const [view, setView] = React.useState<'table' | 'grid'>('table')
  const [documents, setDocuments] = React.useState<Document[]>([])
  const [loading, setLoading] = React.useState(true)

  React.useEffect(() => {
    async function loadData() {
      try {
        const docs = await ApiService.getDocuments()
        setDocuments(docs)
      } catch (e) {
        console.error(e)
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [])

  return (
    <div className="space-y-6 h-full flex flex-col animate-in fade-in duration-500">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Documents Library</h1>
          <p className="text-muted-foreground mt-1">Manage and search your ingested industrial intelligence.</p>
        </div>
        <Button asChild>
           <a href="/app/documents/upload">Upload Document</a>
        </Button>
      </div>

      <div className="flex flex-col sm:flex-row justify-between items-center gap-4 bg-surface p-2 rounded-lg border shadow-sm">
        <div className="relative w-full sm:max-w-md">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input placeholder="Search document titles or contents..." className="w-full pl-9 bg-background" />
        </div>
        <div className="flex items-center space-x-2 w-full sm:w-auto">
          <Button variant="outline" className="flex-1 sm:flex-none">
            <Filter className="w-4 h-4 mr-2" /> Filters
          </Button>
          <div className="border-l pl-2 flex items-center space-x-1">
            <Button variant={view === 'table' ? 'secondary' : 'ghost'} size="icon" onClick={() => setView('table')}>
              <List className="w-4 h-4" />
            </Button>
            <Button variant={view === 'grid' ? 'secondary' : 'ghost'} size="icon" onClick={() => setView('grid')}>
              <LayoutGrid className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-auto">
        {loading ? (
          <div className="flex items-center justify-center h-full">
            <Loader2 className="w-8 h-8 text-primary animate-spin" />
          </div>
        ) : view === 'table' ? (
          <div className="rounded-md border bg-card shadow-sm">
            <Table>
              <TableHeader className="bg-surface sticky top-0">
                <TableRow>
                  <TableHead className="w-[300px]">Document Title</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Asset Association</TableHead>
                  <TableHead>Upload Date</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {documents.map((doc) => (
                  <TableRow key={doc.id} className="hover:bg-muted/50">
                    <TableCell className="font-medium flex items-center">
                      <FileText className="w-4 h-4 mr-2 text-muted-foreground" />
                      <span className="truncate max-w-[250px]" title={doc.title}>{doc.title}</span>
                    </TableCell>
                    <TableCell className="text-muted-foreground">{doc.type}</TableCell>
                    <TableCell>
                      <Badge variant="secondary" className="font-normal">{doc.asset}</Badge>
                    </TableCell>
                    <TableCell className="text-muted-foreground">{doc.date}</TableCell>
                    <TableCell>
                      <StatusBadge status={doc.status} />
                    </TableCell>
                    <TableCell className="text-right">
                      <DocActions />
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {documents.map((doc) => (
              <Card key={doc.id} className="group hover:shadow-md transition-shadow">
                <CardHeader className="p-4 pb-2 flex flex-row items-start justify-between space-y-0">
                  <div className="bg-primary/10 p-2 rounded">
                    <FileText className="w-6 h-6 text-primary" />
                  </div>
                  <DocActions />
                </CardHeader>
                <CardContent className="p-4 pt-2">
                  <h3 className="font-semibold text-sm line-clamp-2 mb-2 group-hover:text-primary transition-colors">{doc.title}</h3>
                  <div className="space-y-1.5 mt-4 text-xs">
                    <div className="flex justify-between items-center border-b pb-1">
                      <span className="text-muted-foreground">Type</span>
                      <span className="font-medium">{doc.type}</span>
                    </div>
                    <div className="flex justify-between items-center border-b pb-1">
                      <span className="text-muted-foreground">Asset</span>
                      <Badge variant="secondary" className="text-[10px] px-1 py-0">{doc.asset}</Badge>
                    </div>
                    <div className="flex justify-between items-center pt-1">
                      <span className="text-muted-foreground">Status</span>
                      <StatusBadge status={doc.status} />
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

function StatusBadge({ status }: { status: string }) {
  const colors: Record<string, string> = {
    "Indexed": "bg-success/15 text-success hover:bg-success/25 border-success/30",
    "Processing": "bg-primary/15 text-primary hover:bg-primary/25 border-primary/30",
    "Failed": "bg-destructive/15 text-destructive hover:bg-destructive/25 border-destructive/30"
  }
  
  return (
    <Badge variant="outline" className={cn("text-[10px] uppercase tracking-wider font-semibold", colors[status] || "")}>
      {status}
    </Badge>
  )
}

function DocActions() {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="h-8 w-8 p-0">
          <span className="sr-only">Open menu</span>
          <MoreVertical className="h-4 w-4" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-[160px]">
        <DropdownMenuLabel>Actions</DropdownMenuLabel>
        <DropdownMenuItem>
          <ExternalLink className="mr-2 h-4 w-4" /> View Original
        </DropdownMenuItem>
        <DropdownMenuItem className="text-primary font-medium focus:text-primary focus:bg-primary/10">
          <Bot className="mr-2 h-4 w-4" /> Open in Copilot
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem className="text-destructive focus:text-destructive focus:bg-destructive/10">
          <Trash2 className="mr-2 h-4 w-4" /> Delete
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
