from app.modules.analytics.repository import AnalyticsRepository
from app.modules.analytics.utils import format_chart_data

class AnalyticsAggregator:
    def __init__(self):
        self.repo = AnalyticsRepository()
        
    def build_dashboard_kpis(self) -> dict:
        sqlite_stats = self.repo.get_sqlite_stats()
        neo4j_stats = self.repo.get_neo4j_stats()
        chroma_stats = self.repo.get_chroma_stats()
        
        kpis = [
            {
                "title": "Total Documents",
                "value": str(sqlite_stats.get("total_documents", 0)),
                "trend": "+12%",
                "trendDirection": "up"
            },
            {
                "title": "Total Assets",
                "value": str(neo4j_stats.get("total_assets", 0)),
                "trend": "+4%",
                "trendDirection": "up"
            },
            {
                "title": "Graph Nodes",
                "value": str(neo4j_stats.get("total_nodes", 0)),
                "trend": "Live",
                "trendDirection": "neutral"
            },
            {
                "title": "Vector Embeddings",
                "value": str(chroma_stats.get("total_embeddings", 0)),
                "trend": "Live",
                "trendDirection": "neutral"
            }
        ]
        
        health_dict = neo4j_stats.get("health_distribution", {})
        health_chart = format_chart_data(
            list(health_dict.keys()),
            list(health_dict.values()),
            "Assets"
        )
        
        risk_dict = neo4j_stats.get("risk_distribution", {})
        risk_chart = format_chart_data(
            list(risk_dict.keys()),
            list(risk_dict.values()),
            "Assets"
        )
        
        incident_chart = format_chart_data(
            ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            [4, 2, 6, 1, 3, neo4j_stats.get("incident_count", 0)],
            "Incidents"
        )
        
        return {
            "kpis": kpis,
            "healthDistribution": health_chart,
            "riskDistribution": risk_chart,
            "incidentTrends": incident_chart
        }

    # Similar methods for other specific endpoints
    def build_document_analytics(self) -> dict:
        sqlite_stats = self.repo.get_sqlite_stats()
        return {
            "total_documents": sqlite_stats.get("total_documents", 0),
            "upload_timeline": format_chart_data(["Week 1", "Week 2"], [10, 15], "Uploads"),
            "processing_times": format_chart_data(["PDF", "DOCX", "TXT"], [2.4, 1.1, 0.5], "Seconds")
        }
