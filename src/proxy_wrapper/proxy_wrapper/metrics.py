from prometheus_client import Counter, Histogram, Gauge


metric_request_internal_errors = Counter(
    'request_internal_errors',
    'Number of server errors when calling a Job',
    labelnames=['endpoint'],
)
metric_request_duration = Histogram(
    'request_duration',
    'Duration of model call',
    buckets=(.001, .0025, .005, .01, .025, .05, .075, .1, .25, .5, .75, 1.0, 2.5, 5.0, 7.5,
             10.0, 25.0, 50.0, 75.0, 100.0, 250.0, 500.0, 750.0, 1000.0, float("inf")),
    labelnames=['endpoint'],
)
metric_requests_started = Counter(
    'requests_started',
    'Total number of started requests calling Job (may be not finished yet)',
)
metric_requests_done = Counter(
    'requests_done',
    'Total number of finished requests calling Job (processed and done)',
)
metric_endpoint_requests_started = Counter(
    'endpoint_requests_started',
    'Total number of started requests calling Job (may be not finished yet)',
    labelnames=['endpoint'],
)
metric_last_call_timestamp = Gauge(
    'last_call_timestamp',
    'Timestamp (in seconds) of the last request calling Job',
)
