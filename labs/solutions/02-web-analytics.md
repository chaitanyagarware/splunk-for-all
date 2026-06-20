# Solution 02: Web Reliability

## Population And Indicators

```spl
index=tutorial sourcetype="splunk_for_all:web" uri!="/health"
| stats count AS eligible count(status) AS with_status
        count(response_time) AS with_latency
        count(eval(status>=500)) AS server_errors
        count(eval(status<500 AND response_time<1)) AS good
        median(response_time) AS median_seconds
        perc95(response_time) AS p95_seconds
| eval status_coverage=round(100*with_status/eligible,2),
       latency_coverage=round(100*with_latency/eligible,2),
       server_error_rate=round(100*server_errors/with_status,2),
       good_percentage=round(100*good/eligible,2),
       median_seconds=round(median_seconds,3),
       p95_seconds=round(p95_seconds,3)
```

The “good” definition treats every non-5xx response under one second as good. That may count 404s and 429s as successful user outcomes and ignores endpoint-specific expectations.

## Concentration

```spl
index=tutorial sourcetype="splunk_for_all:web" uri!="/health"
| stats count AS requests count(eval(status>=500)) AS errors
        perc95(response_time) AS p95 BY uri host
| where requests>=3
| eval error_rate=round(100*errors/requests,2), p95=round(p95,3)
| sort 0 - error_rate - p95
```

The minimum of three is pedagogical, not statistically justified.

## Timeline

```spl
index=tutorial sourcetype="splunk_for_all:web" uri!="/health"
| timechart span=1m count AS requests count(eval(status>=500)) AS errors
```

An empty time bucket may mean zero eligible events because the complete fixed source has been loaded. In live data it could also mean collection failure, so filling it requires a telemetry-health assumption.

## Drilldown

```spl
index=tutorial sourcetype="splunk_for_all:web" uri="/api/checkout"
| sort 0 _time
| table _time request_id client_ip host status response_time _raw
```

Example incident note: Checkout returned repeated 5xx responses during the sample window. All observed server errors affected `/api/checkout` and were recorded on `web-03`. Error events also had high response times relative to other endpoints. The sample does not include application, dependency, deployment, or infrastructure evidence, so it does not establish root cause. Next, correlate request IDs and timestamps with checkout application and dependency logs.

