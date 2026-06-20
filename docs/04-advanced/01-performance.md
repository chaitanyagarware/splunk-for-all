# Search Performance Engineering

## Learning Objectives

- Diagnose slow searches with Job Inspector and search logs.
- Reduce retrieved events, transferred fields, cardinality, and centralized work.
- Choose acceleration only after measuring the workload.

## A Cost Model

Search cost is shaped by:

```text
events scanned x work per event + result movement + centralized state + concurrency
```

This is not a billing formula; it is a reasoning tool. The same SPL can behave very differently across time ranges, field cardinality, cluster topology, and concurrent workloads.

## Optimization Order

### 1. Clarify The Question

Define the smallest event population and output needed. An unclear question tends to become `index=* earliest=0`.

### 2. Restrict Time And Indexed Scope

```spl
index=web sourcetype=access_combined status>=500 earliest=-15m
```

Use specific indexes, sourcetypes, hosts, and selective terms. Avoid leading wildcards and broad `NOT` logic as the primary selector.

### 3. Filter Before Expensive Work

Weak:

```spl
index=web
| rex field=_raw "status=(?<status>\d+)"
| where status>=500
```

Better when `status` is already a reliable extracted field:

```spl
index=web sourcetype=access_combined status>=500
| fields _time host uri status response_time
```

### 4. Reduce Fields And Rows

Carry only needed fields and transform early enough to reduce the stream. Do not place `table` in the middle merely to select fields; use `fields`.

### 5. Control Cardinality

Grouping by `request_id`, raw URL including query strings, user agent, or unrestricted IP can create enormous result sets. Normalize or rank before splitting.

### 6. Replace Costly Shapes

- Prefer conditional `stats` over many subsearches.
- Prefer `stats` over `transaction` when sequence semantics are unnecessary.
- Prefer lookups over repeated small joins.
- Use `tstats` only when fields and data models support the question.

## Job Inspector

Use Job Inspector to compare, not guess. Record:

- Search text, exact time range, result count, and runtime.
- Event scan and command-level durations.
- Remote versus local work and result transfer.
- Warnings, truncation, auto-finalization, and limits.
- The same measures after one deliberate change.

One fast run does not establish a performance claim. Consider cache, concurrency, and data distribution.

## Scheduled Search Load

Searches that all start on the minute create concurrency spikes. Review schedule windows, priorities, runtime, skipped searches, and whether summaries can serve repeated work. Do not randomly stagger compliance or detection searches without understanding timeliness requirements.

## Anti-Patterns

| Pattern | Risk | Better question |
|---|---|---|
| All indexes, all time | Massive ambiguous scan | Which source and window answer this? |
| `dedup` on huge raw stream | Centralized state | Can `stats latest(...) BY key` work? |
| Unlimited `values()` | Memory and truncated sets | Do I need examples, count, or full set? |
| Early global sort | Expensive ordering | Can aggregation reduce first? |
| Dashboard with many independent bases | Concurrency and duplication | Can panels share a selective base or summary? |

## Practice

Take one working search and produce three versions. Change only one variable per version. Capture Job Inspector evidence and explain whether performance improved without changing meaning.

## Official Resources

- [Search optimization](https://help.splunk.com/en/splunk-enterprise/search/search-manual/9.4/optimizing-searches)
- [Search Job Inspector](https://help.splunk.com/en/splunk-enterprise/search/search-manual/9.4/manage-jobs/view-search-job-properties)

Previous: [Data models and tstats](../03-knowledge/03-data-models-and-tstats.md) · Next: [Advanced patterns](02-advanced-patterns.md)

