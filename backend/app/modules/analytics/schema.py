from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ChartSeries(BaseModel):
    name: Optional[str] = None
    data: List[float]

class ChartData(BaseModel):
    labels: List[str]
    series: List[ChartSeries]

class KPIData(BaseModel):
    title: str
    value: str
    trend: Optional[str] = None
    trendDirection: Optional[str] = None

class DashboardAnalyticsResponse(BaseModel):
    kpis: List[KPIData]
    healthDistribution: ChartData
    riskDistribution: ChartData
    incidentTrends: ChartData

class DocumentAnalyticsResponse(BaseModel):
    total_documents: int
    upload_timeline: ChartData
    processing_times: ChartData

class AssetAnalyticsResponse(BaseModel):
    total_assets: int
    type_distribution: ChartData
    health_distribution: ChartData
    risk_distribution: ChartData

class MaintenanceAnalyticsResponse(BaseModel):
    total_incidents: int
    incident_types: ChartData
    open_work_orders: int
    maintenance_timeline: ChartData

class CopilotAnalyticsResponse(BaseModel):
    total_queries: int
    query_timeline: ChartData
    average_query_time: str

class PerformanceAnalyticsResponse(BaseModel):
    avg_extraction_time: str
    avg_knowledge_time: str
    avg_graph_time: str
    avg_embedding_time: str
