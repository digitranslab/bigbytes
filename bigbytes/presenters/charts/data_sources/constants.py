from bigbytes.shared.enum import StrEnum

DEFAULT_LIMIT = 10000


class ChartDataSourceType(StrEnum):
    BLOCK = 'block'
    BLOCK_RUNS = 'block_runs'
    CHART_CODE = 'chart_code'
    PIPELINES = 'pipelines'
    PIPELINE_RUNS = 'pipeline_runs'
    PIPELINE_SCHEDULES = 'pipeline_schedules'
    SYSTEM_METRICS = 'system_metrics'
