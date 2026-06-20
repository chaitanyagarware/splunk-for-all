# Monitoring And Troubleshooting

## Learning Objectives

- Troubleshoot from symptom to layer without random changes.
- Monitor data, search, resource, and cluster health.
- Use internal logs and supported tools with clear evidence.

## Troubleshooting Loop

1. Define the symptom, impact, start time, and affected scope.
2. Establish what changed and what still works.
3. Trace the path across producer, collection, parsing, storage, search, and presentation.
4. Gather evidence before restarting or editing.
5. Form one falsifiable hypothesis.
6. Make the smallest reversible test.
7. Verify recovery and monitor recurrence.
8. Record cause, contributing conditions, and preventive action.

## Data Health

Check event freshness by source:

```spl
| metadata type=sourcetypes index=tutorial
| eval age_seconds=now()-recentTime
| convert ctime(recentTime)
| sort - age_seconds
```

`metadata` is efficient but has scope and behavior to understand. For critical feeds, create source-specific freshness rules that account for expected schedules and quiet periods.

Ingestion lag:

```spl
index=tutorial earliest=-2h
| eval lag=_indextime-_time
| stats count p50(lag) AS p50_lag p95(lag) AS p95_lag max(lag) AS max_lag
        BY sourcetype
```

Backfills, clock skew, future timestamps, and batch sources require contextual thresholds.

## Internal Logs

On authorized deployments, `_internal` contains platform diagnostics. Start narrow:

```spl
index=_internal sourcetype=splunkd log_level IN (WARN,ERROR) earliest=-15m
| stats count values(component) AS components values(message) AS examples
        BY host
| sort - count
```

Field availability and log formats vary. Broad `_internal` scans can be noisy and expensive. The Monitoring Console provides supported health views and topology-aware checks.

## Search Health

Monitor runtime, concurrency, skipped searches, auto-finalization, result limits, and scheduler delay. A search completing successfully can still be incomplete because of truncation or a stale acceleration summary.

## Common Symptom Map

| Symptom | Evidence to gather first |
|---|---|
| No new events | Producer output, forwarder/input state, transport, receiving, index routing |
| Wrong timestamps | Raw sample, `_time`, `_indextime`, parsing provenance, time zone |
| Search slow | Exact SPL/time, Job Inspector, concurrency, cardinality, peer health |
| Alert missing | Schedule, window, ingestion delay, owner, permissions, dispatch status |
| Dashboard partial | Token values, base search, panel job messages, role access, limits |
| Cluster unhealthy | Supported health command/views, peer status, fix-up, disk/network events |

## Restart Is Not Diagnosis

A restart may clear a symptom while destroying evidence and creating availability risk. Know whether a setting requires reload or restart, follow topology order, and capture state first.

## Practice

Write a runbook for “authentication events are 30 minutes late.” Include five hypotheses, one test per hypothesis, escalation criteria, and success metrics after recovery.

## Official Resources

- [Monitoring Splunk Enterprise](https://help.splunk.com/en/splunk-enterprise/administer/monitor)
- [Troubleshooting Manual](https://help.splunk.com/en/splunk-enterprise/administer/troubleshoot)

Previous: [Security and RBAC](03-security-and-rbac.md) · Next: [Security analytics](../06-use-cases/01-security.md)

