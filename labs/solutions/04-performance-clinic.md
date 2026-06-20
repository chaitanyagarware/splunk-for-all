# Solution 04: SPL Performance Clinic

## Requirement Questions

- Which indexes and sourcetypes contain eligible web events?
- What exact time range and freshness are needed?
- Is the unit an event, request, client, session, or host?
- Why group all traffic from one client IP into a transaction?
- Is `status` already extracted and numeric?
- Which output fields support a decision?
- What volume, cardinality, concurrency, and runtime target apply?

## Cost And Meaning

`index=* earliest=0` retrieves an unbounded mixed population. `rex` repeats extraction over every event. `transaction client_ip` centralizes state and treats unrelated requests behind NAT as one group. Filtering after transaction does unnecessary work and can change field semantics. `sort 0` globally orders an unbounded result. Carrying `_raw` increases result width and may expose unnecessary content.

## Rewrite

```spl
index=web sourcetype=access_combined status>=500 earliest=-15m
| stats count AS server_errors dc(client_ip) AS affected_clients
        perc95(response_time) AS p95_seconds BY host
| sort 0 - server_errors
```

Use your real index and sourcetype. This query assumes `status`, `client_ip`, and `response_time` are reliable search-time fields and that one event represents one request.

## Measurement

Run old and new versions over the same authorized population in a representative non-peak and peak context. Record normalized runtime, event scan, command time, peer/local distribution, result count, transfer, warnings, truncation, and concurrent workload. Confirm semantic equivalence against known test cases before accepting speed improvements.

## Cardinality

- `request_id`: nearly unique; use for bounded drilldown, not dashboard splits.
- `client_ip`: potentially large and privacy-sensitive; aggregate, restrict, or rank.
- `uri`: query strings can make it unbounded; normalize to path or route template.

`tstats` could help only if required fields have suitable indexed/data-model representation, the normalized model population is validated, acceleration summaries cover the time range, and summary freshness meets the use case.

