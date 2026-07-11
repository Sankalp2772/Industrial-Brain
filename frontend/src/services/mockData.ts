import { Document, DashboardMetrics, Incident, SystemStatus, AnalyticsData } from '../types'

export const mockDocuments: Document[] = [
  { id: "1", title: "Centrifugal Pump Operating Manual v4", type: "Manual", asset: "Pump A-42", status: "Indexed", date: "2023-10-24" },
  { id: "2", title: "Turbine Shaft Maintenance Log - Oct", type: "Maintenance Log", asset: "Turbine T-1", status: "Indexed", date: "2023-10-22" },
  { id: "3", title: "Sensor Telemetry Extract Q3", type: "Telemetry CSV", asset: "Multiple", status: "Processing", date: "2023-10-26" },
  { id: "4", title: "Safety Protocol Guidelines 2023", type: "Policy", asset: "General", status: "Indexed", date: "2023-09-15" },
  { id: "5", title: "HVAC System Schematics", type: "Diagram", asset: "HVAC-Main", status: "Failed", date: "2023-10-25" },
]

export const mockDashboardMetrics: DashboardMetrics = {
  totalDocuments: 14203,
  registeredAssets: 2845,
  knowledgeCoverage: 84,
  criticalAssets: 14,
  avgQueryTime: "1.2s"
}

export const mockIncidents: Incident[] = [
  { id: "1", asset: "Pump A-42", issue: "Vibration Anomaly Detected", time: "10m ago", severity: "critical" },
  { id: "2", asset: "Conveyor B", issue: "Motor Temp > 85°C", time: "1h ago", severity: "warning" },
  { id: "3", asset: "Valve C-12", issue: "Pressure Drop", time: "3h ago", severity: "warning" },
]

export const mockSystemStatus: SystemStatus[] = [
  { name: "Gemini (LLM)", status: "healthy", latency: "120ms" },
  { name: "Neo4j (Graph DB)", status: "healthy", latency: "45ms" },
  { name: "Chroma (Vector DB)", status: "healthy", latency: "8ms" },
  { name: "Backend API", status: "healthy", latency: "32ms" },
]

export const mockAnalyticsData: AnalyticsData = {
  knowledgeGrowth: [
    { name: 'Jan', nodes: 4000, edges: 2400 },
    { name: 'Feb', nodes: 5000, edges: 3908 },
    { name: 'Mar', nodes: 6000, edges: 4800 },
    { name: 'Apr', nodes: 8780, edges: 7908 },
    { name: 'May', nodes: 11900, edges: 11800 },
    { name: 'Jun', nodes: 14203, edges: 16500 },
  ],
  fleetHealth: [
    { name: 'Operational', value: 2400 },
    { name: 'Warning', value: 300 },
    { name: 'Critical', value: 14 },
    { name: 'Offline', value: 131 },
  ],
  failureTrends: [
    { name: 'Vibration', count: 120 },
    { name: 'Temperature', count: 85 },
    { name: 'Pressure', count: 65 },
    { name: 'Flow Rate', count: 40 },
    { name: 'Electrical', count: 35 },
  ],
  mostQueriedAssets: [
    { id: "1", name: "Pump A-42", queries: 142, topic: "Vibration Anomalies" },
    { id: "2", name: "Compressor M7", queries: 98, topic: "Maintenance Procedures" },
    { id: "3", name: "Conveyor Belt B", queries: 65, topic: "Motor Temperatures" },
    { id: "4", name: "HVAC Main Chiller", queries: 42, topic: "Pressure Drops" },
  ]
}
