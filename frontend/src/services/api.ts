import axios from 'axios'
import { Document, DashboardMetrics, Incident, SystemStatus, AnalyticsData } from '../types'
import { useAuthStore } from '../store/useAuthStore'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

const apiClient = axios.create({
  baseURL: API_BASE,
})

// Request interceptor to attach JWT
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('auth-storage') 
    ? JSON.parse(localStorage.getItem('auth-storage') || '{}')?.state?.token 
    : null;
  
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor to handle 401s
apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
    }
    return Promise.reject(error)
  }
)

export const ApiService = {
  // Auth methods
  async login(credentials: any): Promise<any> {
    const res = await apiClient.post('/auth/login', credentials)
    return res.data.data
  },
  
  async register(data: any): Promise<any> {
    const res = await apiClient.post('/auth/register', data)
    return res.data.data
  },

  async logout(): Promise<any> {
    try {
      const res = await apiClient.post('/auth/logout')
      return res.data
    } catch(e) {
      return null;
    }
  },

  async getDocuments(): Promise<Document[]> {
    try {
      const res = await apiClient.get(`/documents`)
      const data = res.data.data
      return data.documents.map((d: any) => ({
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
      const res = await apiClient.get(`/analytics/dashboard`)
      const data = res.data.data
      
      return {
        metrics: {
          totalDocuments: parseInt(data.kpis.find((k: any) => k.title === 'Total Documents')?.value || '0'),
          registeredAssets: parseInt(data.kpis.find((k: any) => k.title === 'Total Assets')?.value || '0'),
          knowledgeCoverage: 92, 
          criticalAssets: parseInt(data.riskDistribution.series[0].data[3] || '0'),
          avgQueryTime: '1.2s' 
        },
        incidents: [], 
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
      const res = await apiClient.get(`/analytics/dashboard`)
      const data = res.data.data
      
      const fleetHealth = data.healthDistribution.labels.map((lbl: string, i: number) => ({
        name: lbl,
        value: data.healthDistribution.series[0].data[i] || 0
      }))
      
      return {
        knowledgeGrowth: [], 
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
    
    const res = await apiClient.post(`/documents/upload`, formData)
    return res.data.data.id
  },

  async processDocumentPipeline(docId: string, onProgress: (step: string) => void): Promise<void> {
    try {
      onProgress('extract')
      await apiClient.post(`/documents/${docId}/extract`)
      
      onProgress('knowledge')
      await apiClient.post(`/documents/${docId}/knowledge`)
      
      onProgress('graph')
      await apiClient.post(`/graph/documents/${docId}/graph`)
      
      onProgress('embeddings')
      await apiClient.post(`/embeddings/documents/${docId}/embed`)
      
      onProgress('done')
    } catch (e) {
      console.error(e)
      throw e
    }
  },

  async queryCopilot(question: string): Promise<any> {
    const res = await apiClient.post(`/copilot/query`, { question })
    return res.data.data
  },

  async getCopilotHistory(): Promise<any[]> {
    try {
      const res = await apiClient.get('/copilot/history')
      return res.data.data
    } catch (e) {
      console.error(e)
      return []
    }
  },
  
  client: apiClient
}
