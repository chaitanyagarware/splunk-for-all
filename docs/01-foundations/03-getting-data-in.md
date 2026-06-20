# Getting Data In

## Learning Objectives

- Design a data onboarding contract.
- Choose a collection method and sourcetype strategy.
- Validate event boundaries, timestamps, metadata, and data quality.

## Begin With A Data Contract

Before touching an input, record:

| Decision | Example |
|---|---|
| Owner and consumers | Payments team; SRE and fraud analysts |
| Questions to answer | Error rate, latency, suspicious refund behavior |
| Source and transport | JSON file via forwarder; TLS enabled |
| Expected volume | 30 GB/day, peak 2 MB/s |
| Schema | Timestamp, service, operation, status, duration, trace ID |
| Classification | Internal; no passwords or payment data |
| Retention | Searchable 30 days, archive per policy |
| Validation | Event count, lag, parse failures, missing critical fields |

## Metadata That Matters

- `index` controls storage policy and commonly access.
- `sourcetype` identifies the format and parsing rules, not the sending host or team.
- `source` identifies the input origin, often a file path or input name.
- `host` identifies the event-producing host when that concept is meaningful.
- `_time` is the parsed event time; `_indextime` is when Splunk indexed the event.

Avoid sourcetypes named after one server or one date. Stable source typing enables reusable fields and knowledge objects.

## Collection Options

| Method | Good fit | Watch for |
|---|---|---|
| Forwarder file monitor | Host logs and durable files | Rotation, permissions, duplicate paths, multiline rules |
| HTTP Event Collector | Application and service events | Token scope, TLS, acknowledgment, retries, load balancing |
| Add-on/API input | SaaS or platform APIs | Checkpoints, rate limits, pagination, credentials |
| Syslog architecture | Network and appliance logs | Durable intermediary, transport security, source identity |
| Upload | Small lab data | Manual, not continuous or production-grade |

## Parsing Checklist

Preview representative data, including failures and edge cases:

1. One logical event becomes one event.
2. `_time` matches the event timestamp, format, zone, and precision.
3. `host`, `source`, and `sourcetype` are intentional.
4. Character encoding is correct.
5. Sensitive fields are excluded or handled under policy.
6. Very long or malformed events have an explicit strategy.
7. Search-time fields are typed and named consistently.

Inspect newly indexed data:

```spl
index=tutorial sourcetype="splunk_for_all:*" earliest=-24h
| eval ingest_lag_seconds=_indextime-_time
| stats count min(_time) AS first_event max(_time) AS last_event
        p50(ingest_lag_seconds) AS p50_lag p95(ingest_lag_seconds) AS p95_lag
        BY sourcetype host
| convert ctime(first_event) ctime(last_event)
```

Negative lag can indicate clock skew or future timestamps. Large positive lag can indicate collection delay, backfill, or parsing errors. Interpret it in context.

## Configuration Principle

Inputs describe collection. Parsing configuration describes how raw streams become events. Output configuration describes forwarding. Search-time knowledge describes how fields and meaning are derived. Keep changes in apps rather than editing default files, and test with supported inspection tools before deployment.

## Production Notes

- Test with a representative sample and a rollback plan.
- Estimate license/ingest impact before enabling a high-volume source.
- Route only with a documented requirement; avoid duplicating data accidentally.
- Monitor source silence as well as malformed events.
- Never send the same file through overlapping monitor stanzas.
- Use official add-ons where appropriate, but review their field and permission behavior.

## Checkpoint

What is wrong with using `sourcetype=linux_server_42`? It binds format to one asset, reduces reuse, invites sourcetype sprawl, and does not explain the event structure.

## Official Resources

- [Getting Data In](https://help.splunk.com/en/splunk-enterprise/get-data-in/get-started-with-getting-data-in)
- [Splunk Add-ons](https://splunkbase.splunk.com/)

Previous: [Architecture](02-architecture.md) · Next: [Search fundamentals](../02-spl/01-search-fundamentals.md)

