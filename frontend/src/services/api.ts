import { Document, DashboardMetrics, Incident, SystemStatus, AnalyticsData } from '../types'

const API_BASE = 'http://localhost:8001/api/v1'

export const ApiService = {
  async getDocuments(): Promise<Document[]> {
    try {
      const res = await fetch(`${API_BASE}/documents`)
      const json = await res.json()
      if (!json.success) throw new Error(json.message)
      return json.data.documents.map((d: any) => ({
        id: d.id,
        title: d.filename,
        type: d.content_type.includes('pdf') ? 'PDF' : 'Word',
        asset: 'General',
        status: d.processing_status === 'Completed' ? 'Indexed' : d.processing_status,
        date: d.upload_time
      }))
    } catch (e) {
      console.error(e)
      return []
    }
  },

  async getDashboardData(): Promise<{
    metrics: DashboardMetrics
    incidents: Incident[]
    systemStatus: SystemStatus[]
  }> {
    try {
      const res = await fetch(`${API_BASE}/analytics/dashboard`)
      const json = await res.json()
      if (!json.success) throw new Error(json.message)
      const data = json.data
      
      return {
        metrics: {
          totalDocuments: parseInt(data.kpis.find((k: any) => k.title === 'Total Documents')?.value || '0'),
          registeredAssets: parseInt(data.kpis.find((k: any) => k.title === 'Total Assets')?.value || '0'),
          knowledgeCoverage: 92, // Mocked until computed
          criticalAssets: parseInt(data.riskDistribution.series[0].data[3] || '0'),
          avgQueryTime: '1.2s' // Mocked until computed
        },
        incidents: [], // Fetch from /analytics/incidents if created
        systemStatus: [
          { name: 'Neo4j Graph', status: 'healthy', latency: '45ms' },
          { name: 'ChromaDB', status: 'healthy', latency: '12ms' },
          { name: 'Gemini LLM', status: 'healthy', latency: '850ms' }
        ]
      }
    } catch (e) {
      console.error(e)
      return {
        metrics: { totalDocuments: 0, registeredAssets: 0, knowledgeCoverage: 0, criticalAssets: 0, avgQueryTime: '0s' },
        incidents: [],
        systemStatus: []
      }
    }
  },

  async getAnalytics(): Promise<AnalyticsData> {
    try {
      const res = await fetch(`${API_BASE}/analytics/dashboard`)
      const json = await res.json()
      if (!json.success) throw new Error(json.message)
      const data = json.data
      
      const fleetHealth = data.healthDistribution.labels.map((lbl: string, i: number) => ({
        name: lbl,
        value: data.healthDistribution.series[0].data[i] || 0
      }))
      
      return {
        knowledgeGrowth: [], // Fill from backend
        fleetHealth: fleetHealth,
        failureTrends: [],
        mostQueriedAssets: []
      }
    } catch(e) {
      console.error(e)
      return { knowledgeGrowth: [], fleetHealth: [], failureTrends: [], mostQueriedAssets: [] }
    }
  },

  async uploadDocument(file: File): Promise<string> {
    const formData = new FormData()
    formData.append('file', file)
    
    const res = await fetch(`${API_BASE}/documents/upload`, {
      method: 'POST',
      body: formData
    })
    const json = await res.json()
    if (!json.success) throw new Error(json.message)
    return json.data.id
  },

  async processDocumentPipeline(docId: string, onProgress: (step: string) => void): Promise<void> {
    try {
      onProgress('extract')
      await fetch(`${API_BASE}/extraction/document/${docId}/extract`, { method: 'POST' })
      
      onProgress('knowledge')
      await fetch(`${API_BASE}/extraction/document/${docId}/knowledge`, { method: 'POST' })
      
      onProgress('graph')
      await fetch(`${API_BASE}/graph/documents/${docId}/graph`, { method: 'POST' })
      
      onProgress('embeddings')
      await fetch(`${API_BASE}/embeddings/documents/${docId}/embeddings`, { method: 'POST' })
      
      onProgress('done')
    } catch (e) {
      console.error(e)
      throw e
    }
  },

  async queryCopilot(question: string): Promise<any> {
    const res = await fetch(`${API_BASE}/copilot/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ question })
    })
    const json = await res.json()
    if (!json.success) throw new Error(json.message)
    return json.data
  }
}
