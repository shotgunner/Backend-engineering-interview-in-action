Prometheus uses a pull-based approach to collect metrics from targets. It periodically scrapes metrics endpoints (typically every 15-30 seconds) to gather data while avoiding excessive load on monitored servers.

We run a prometheus_client server endpoint on our application servers that exposes Prometheus metrics, including:
- Counters (monotonically increasing values)
- Gauges (values that can go up and down) 
- Histograms (for measuring distributions)
- Summaries (similar to histograms but with client-side quantiles)

The Prometheus server discovers and scrapes these endpoints to collect the metrics data.

For querying the collected metrics, Prometheus provides PromQL (Prometheus Query Language).
Helpful PromQL resources:
- Cheat sheet: https://promlabs.com/promql-cheat-sheet/
- Official docs: https://prometheus.io/docs/prometheus/latest/querying/basics/
