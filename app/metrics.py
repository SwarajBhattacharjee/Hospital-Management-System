"""
metrics.py
Prometheus metrics instrumentation for Hospital Management System.
Exposes request counts (Counter), latency (Histogram), and patient gauge (Gauge).
"""

import time
from flask import request, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

# ---------------------------------------------------------------------------
# PROMETHEUS METRIC DEFINITIONS
# ---------------------------------------------------------------------------
HTTP_REQUESTS_TOTAL = Counter(
    'http_requests_total',
    'Total HTTP requests processed by endpoint, HTTP method, and status code',
    ['method', 'endpoint', 'status']
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds by endpoint and HTTP method',
    ['method', 'endpoint'],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

PATIENTS_TOTAL_GAUGE = Gauge(
    'hms_patients_total',
    'Total count of patient records currently in the database'
)


def init_metrics(app):
    """
    Hooks request timers and metric updates to the Flask application instance,
    and registers the public /metrics endpoint.
    """

    @app.before_request
    def before_request_metric_timer():
        request._prometheus_start_time = time.time()

    @app.after_request
    def after_request_metric_collector(response):
        if hasattr(request, '_prometheus_start_time'):
            latency = time.time() - request._prometheus_start_time
            endpoint = request.endpoint or 'unmatched'
            method = request.method
            status = str(response.status_code)
            HTTP_REQUESTS_TOTAL.labels(method=method, endpoint=endpoint, status=status).inc()
            HTTP_REQUEST_DURATION_SECONDS.labels(method=method, endpoint=endpoint).observe(latency)
        return response

    @app.route('/metrics', methods=['GET'])
    def metrics():
        """
        Public Prometheus metrics endpoint.
        Dynamically refreshes the active patient count gauge from the database
        and returns metrics formatted for Prometheus scrapers.
        """
        try:
            from app.models import Patient
            count = Patient.query.count()
            PATIENTS_TOTAL_GAUGE.set(count)
        except Exception as e:
            app.logger.warning(f"Failed to query patient count for Prometheus gauge: {e}")

        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
