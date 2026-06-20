# Statistics And Time

## Learning Objectives

- Aggregate events with `stats`, `eventstats`, and `streamstats`.
- Build correct time series.
- Calculate rates, percentiles, and baselines without common denominator errors.

## Three Statistical Shapes

### `stats`: Events Become A Table

```spl
index=tutorial sourcetype="splunk_for_all:web"
| stats count AS requests
        count(eval(status>=500)) AS errors
        avg(response_time) AS avg_seconds
        perc95(response_time) AS p95_seconds
        BY host
| eval error_rate=round(100*errors/requests, 2)
```

After `stats`, fields not used in an aggregation or `BY` clause are gone.

### `eventstats`: Add Group Statistics To Events

```spl
index=tutorial sourcetype="splunk_for_all:web"
| eventstats avg(response_time) AS host_avg stdev(response_time) AS host_sd BY host
| eval z_score=if(host_sd>0, (response_time-host_avg)/host_sd, null())
| where z_score>=3
```

The original events remain, enriched with group-level values.

### `streamstats`: Running Or Windowed State

```spl
index=tutorial sourcetype="splunk_for_all:web"
| sort 0 host _time
| streamstats window=5 avg(response_time) AS rolling_5 BY host
```

Order is part of the calculation. `sort 0` requests an untruncated sort but can be expensive at scale; constrain the input and understand memory limits.

## Time Series

```spl
index=tutorial sourcetype="splunk_for_all:web" earliest=-24h
| timechart span=15m count AS requests
        count(eval(status>=500)) AS errors
| eval error_rate=round(100*errors/requests, 2)
```

Use a span appropriate to the question and volume. Tiny spans produce noise and sparse buckets; huge spans hide incidents. Empty buckets, missing data, and true zero are not interchangeable.

To split by one dimension:

```spl
index=tutorial sourcetype="splunk_for_all:web" earliest=-24h
| timechart span=15m count BY host limit=10 useother=true
```

High-cardinality splits create wide, expensive, unreadable results. Rank or aggregate dimensions intentionally.

## Percentiles And Averages

Latency distributions are usually skewed. An average describes the arithmetic center but can conceal a painful tail; percentiles describe thresholds within the observed sample. State the unit, population, window, and aggregation level.

Do not average precomputed averages without their weights. Combine totals:

```spl
| stats sum(total_duration) AS duration sum(request_count) AS requests
| eval weighted_average=duration/requests
```

## Denominators

Detection and reliability errors often begin with a wrong denominator:

```spl
index=tutorial sourcetype="splunk_for_all:web"
| stats count AS all_events
        count(eval(isnotnull(status))) AS requests_with_status
        count(eval(status>=500)) AS errors
| eval observed_error_rate=100*errors/requests_with_status,
       field_coverage=100*requests_with_status/all_events
```

Report coverage beside the rate when missing fields can bias the result.

## Production Notes

- Align time zones and business calendars before comparing periods.
- Use `bin _time span=...` plus `stats` when you need grouping that `timechart` does not express clearly.
- Baselines should account for seasonality, deployments, and missing data.
- Statistical anomaly does not automatically mean operational incident.

## Practice

For each host, calculate requests, errors, error rate, median latency, p95 latency, and field coverage. Filter to hosts with at least 10 requests, then rank by error rate and p95 latency.

## Official Resources

- [`stats` command](https://help.splunk.com/en/splunk-enterprise/search/spl-search-reference/9.4/search-commands/stats)
- [Time modifiers](https://help.splunk.com/en/splunk-enterprise/search/spl2-search-manual/dates-and-time/time-modifiers)

Previous: [Fields and filtering](02-fields-and-filtering.md) · Next: [Enrichment and correlation](04-enrichment-and-correlation.md)

