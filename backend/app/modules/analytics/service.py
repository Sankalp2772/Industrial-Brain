from app.modules.analytics.aggregator import AnalyticsAggregator
import time

# Simple in-memory cache
_cache = {}
CACHE_TTL = 60 # seconds

class AnalyticsService:
    def __init__(self):
        self.aggregator = AnalyticsAggregator()

    def _get_cached(self, key: str, builder_func):
        now = time.time()
        if key in _cache:
            data, timestamp = _cache[key]
            if now - timestamp < CACHE_TTL:
                return data
                
        data = builder_func()
        _cache[key] = (data, now)
        return data

    def get_dashboard(self) -> dict:
        return self._get_cached("dashboard", self.aggregator.build_dashboard_kpis)
        
    def get_documents(self) -> dict:
        return self._get_cached("documents", self.aggregator.build_document_analytics)

    # Placeholders for other endpoints
    def get_assets(self) -> dict:
        return {}
    def get_incidents(self) -> dict:
        return {}
    def get_maintenance(self) -> dict:
        return {}
    def get_copilot(self) -> dict:
        return {}
    def get_performance(self) -> dict:
        return {}
