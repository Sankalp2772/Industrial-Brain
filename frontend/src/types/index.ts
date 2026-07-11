export interface User {
  id: string
  name: string
  email: string
  role: string
  avatarInitials: string
}

export interface Document {
  id: string
  title: string
  type: string
  asset: string
  status: 'Indexed' | 'Processing' | 'Failed' | 'Uploaded'
  date: string
}

export interface DashboardMetrics {
  totalDocuments: number
  registeredAssets: number
  knowledgeCoverage: number
  criticalAssets: number
  avgQueryTime: string
}

export interface Incident {
  id: string
  asset: string
  issue: string
  time: string
  severity: 'critical' | 'warning'
}

export interface SystemStatus {
  name: string
  status: 'healthy' | 'degraded' | 'down'
  latency: string
}

export interface AnalyticsData {
  knowledgeGrowth: { name: string, nodes: number, edges: number }[]
  fleetHealth: { name: string, value: number }[]
  failureTrends: { name: string, count: number }[]
  mostQueriedAssets: { id: string, name: string, queries: number, topic: string }[]
}
