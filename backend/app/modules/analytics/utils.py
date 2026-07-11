def format_chart_data(labels: list, data: list, series_name: str = "Series 1") -> dict:
    """Format simple label/value data into frontend ChartData shape"""
    return {
        "labels": labels,
        "series": [
            {
                "name": series_name,
                "data": data
            }
        ]
    }

def format_multi_series_chart(labels: list, series_list: list) -> dict:
    """Format multi-series data into frontend ChartData shape"""
    return {
        "labels": labels,
        "series": series_list
    }
