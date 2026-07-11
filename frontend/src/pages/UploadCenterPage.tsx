import * as React from "react"
import { UploadCloud, File, CheckCircle2, Activity, Database, AlertCircle, X, Network } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { cn } from "@/lib/utils"

import { ApiService } from "../services/api"

export function UploadCenterPage() {
  const [activeFile, setActiveFile] = React.useState<File | null>(null)
  const [uploadStatus, setUploadStatus] = React.useState<'idle'|'uploading'|'processing'|'done'|'error'>('idle')
  const [progress, setProgress] = React.useState(0)
  const [pipelineStep, setPipelineStep] = React.useState<string>('none')
  const fileInputRef = React.useRef<HTMLInputElement>(null)

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0]
      setActiveFile(file)
      await startUploadProcess(file)
    }
  }

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault()
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0]
      setActiveFile(file)
      await startUploadProcess(file)
    }
  }

  const startUploadProcess = async (file: File) => {
    try {
      setUploadStatus('uploading')
      setProgress(25)
      const docId = await ApiService.uploadDocument(file)
      
      setUploadStatus('processing')
      setProgress(50)
      
      await ApiService.processDocumentPipeline(docId, (step) => {
        setPipelineStep(step)
        if (step === 'extract') setProgress(60)
        if (step === 'knowledge') setProgress(75)
        if (step === 'graph') setProgress(85)
        if (step === 'embeddings') setProgress(95)
        if (step === 'done') {
          setProgress(100)
          setUploadStatus('done')
        }
      })
    } catch (err) {
      console.error(err)
      setUploadStatus('error')
    }
  }

  return (
    <div className="space-y-6 max-w-6xl animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Document Upload Center</h1>

      <div className="grid gap-6 lg:grid-cols-3">
        
        {/* Left Column: Upload Area & Queue */}
        <div className="space-y-6 lg:col-span-2">
          
          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={handleFileChange} 
            className="hidden" 
            accept=".pdf,.docx,.txt,.csv"
          />
          <Card 
            className="border-dashed border-2 border-primary/20 bg-primary/5 shadow-none transition-colors hover:bg-primary/10 hover:border-primary/40 cursor-pointer"
            onClick={() => fileInputRef.current?.click()}
            onDragOver={(e) => e.preventDefault()}
            onDrop={handleDrop}
          >
            <CardContent className="flex flex-col items-center justify-center py-16 text-center">
              <div className="bg-primary/10 p-4 rounded-full mb-4">
                <UploadCloud className="w-8 h-8 text-primary" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Drag & Drop files here</h3>
              <p className="text-sm text-muted-foreground max-w-sm mb-6">
                Supported formats: PDF, CSV, DOCX, TXT. Maximum file size: 100MB.
              </p>
              <Button onClick={(e) => { e.stopPropagation(); fileInputRef.current?.click() }}>Select Files</Button>
            </CardContent>
          </Card>

          <Card className="shadow-sm">
            <CardHeader className="pb-3 border-b">
              <CardTitle className="text-lg">Active Uploads & Processing</CardTitle>
            </CardHeader>
            <CardContent className="pt-4 space-y-4">
              {activeFile && (
                <ActiveUploadItem 
                  filename={activeFile.name}
                  size={`${(activeFile.size / (1024*1024)).toFixed(2)} MB`}
                  progress={progress}
                  status={uploadStatus === 'error' ? 'failed' : uploadStatus === 'done' ? 'processing' : 'uploading'}
                />
              )}
              {!activeFile && <p className="text-sm text-muted-foreground">No active uploads.</p>}
            </CardContent>
          </Card>
        </div>

        {/* Right Column: Timeline & Extraction Preview */}
        <div className="space-y-6 lg:col-span-1">
          <Card className="shadow-sm">
            <CardHeader className="pb-3 border-b">
              <CardTitle className="text-base flex items-center">
                <Activity className="w-4 h-4 mr-2 text-primary" />
                Processing Pipeline
              </CardTitle>
              <CardDescription className="text-xs">
                Compressor_M7_Maintenance_Manual_2023.pdf
              </CardDescription>
            </CardHeader>
            <CardContent className="pt-6 pl-2">
              <div className="space-y-6 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-border before:to-transparent">
                
                <PipelineStep 
                  title="Upload Complete" 
                  description="File stored in secure bucket." 
                  status={uploadStatus !== 'idle' ? 'done' : 'pending'}
                  icon={CheckCircle2} 
                />
                <PipelineStep 
                  title="OCR & Text Extraction" 
                  description="Extracting text and tables." 
                  status={['knowledge', 'graph', 'embeddings', 'done'].includes(pipelineStep) ? 'done' : pipelineStep === 'extract' ? 'active' : 'pending'} 
                  icon={File} 
                />
                <PipelineStep 
                  title="Entity Recognition" 
                  description="Identifying assets and parameters." 
                  status={['graph', 'embeddings', 'done'].includes(pipelineStep) ? 'done' : pipelineStep === 'knowledge' ? 'active' : 'pending'} 
                  icon={Network} 
                />
                <PipelineStep 
                  title="Vector Indexing" 
                  description="Embedding to Chroma DB." 
                  status={pipelineStep === 'done' ? 'done' : pipelineStep === 'embeddings' ? 'active' : 'pending'} 
                  icon={Database} 
                />
                
              </div>
            </CardContent>
          </Card>

          <Card className="shadow-sm border-primary/20 bg-primary/5">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm">Live Extraction Preview</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="text-xs text-muted-foreground italic mb-2">Finding relationships...</div>
                <div className="flex flex-wrap gap-2">
                  <Badge variant="secondary" className="bg-background">Asset: Compressor M7</Badge>
                  <Badge variant="secondary" className="bg-background">Part: Rotor Shaft</Badge>
                  <Badge variant="secondary" className="bg-background">Metric: Oil Pressure</Badge>
                  <Badge variant="secondary" className="bg-background border-warning text-warning-foreground">Threshold: &lt; 40 psi</Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

function ActiveUploadItem({ filename, size, progress, status }: { filename: string, size: string, progress: number, status: 'uploading' | 'processing' | 'failed' }) {
  return (
    <div className="flex items-start space-x-4 p-3 rounded-lg border bg-surface/50">
      <div className="bg-background p-2 rounded border shadow-sm flex-shrink-0">
        <File className="w-5 h-5 text-muted-foreground" />
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex justify-between items-start mb-1">
          <p className="text-sm font-medium truncate pr-2">{filename}</p>
          <Button variant="ghost" size="icon" className="h-6 w-6 text-muted-foreground flex-shrink-0 -mr-2 -mt-1">
            <X className="w-3 h-3" />
          </Button>
        </div>
        <div className="flex justify-between items-center text-xs text-muted-foreground mb-2">
          <span>{size}</span>
          <span>{status === 'uploading' ? `${progress}%` : 'Processing with AI...'}</span>
        </div>
        <Progress 
          value={progress} 
          className="h-1.5" 
          indicatorClassName={cn(
            status === 'processing' && "bg-primary animate-pulse",
            status === 'failed' && "bg-destructive"
          )} 
        />
      </div>
    </div>
  )
}

function PipelineStep({ title, description, status, icon: Icon }: { title: string, description: string, status: 'done' | 'active' | 'pending', icon: any }) {
  return (
    <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
      {/* Marker */}
      <div className={cn(
        "flex items-center justify-center w-8 h-8 rounded-full border-2 bg-background z-10 shrink-0 relative md:mx-auto",
        status === 'done' ? "border-success text-success" : 
        status === 'active' ? "border-primary text-primary shadow-[0_0_10px_rgba(var(--primary),0.2)]" : 
        "border-border text-muted-foreground"
      )}>
        {status === 'active' ? (
          <Activity className="w-4 h-4 animate-pulse" />
        ) : (
          <Icon className="w-4 h-4" />
        )}
      </div>
      
      {/* Content */}
      <div className="w-[calc(100%-3rem)] md:w-[calc(50%-2rem)] p-4 rounded border shadow-sm bg-card ml-4 md:ml-0 md:odd:mr-4 md:even:ml-4">
        <h4 className={cn("text-sm font-semibold", status === 'active' && "text-primary")}>{title}</h4>
        <p className="text-xs text-muted-foreground mt-1">{description}</p>
      </div>
    </div>
  )
}
