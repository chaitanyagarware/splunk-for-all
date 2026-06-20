# Time Reference

Time is a filter, grouping key, display value, and source of subtle bugs.

## Core Fields

| Field | Meaning |
|---|---|
| `_time` | Parsed event time, stored as epoch seconds |
| `_indextime` | Time Splunk indexed the event |
| `date_*` | Search-time components when available; do not assume universal presence |

## Relative Modifiers

| Modifier | Intent |
|---|---|
| `earliest=-15m` | Last 15 minutes from dispatch time |
| `earliest=-24h` | Last 24 hours |
| `earliest=@d` | From the start of today |
| `earliest=-1d@d latest=@d` | Previous calendar day |
| `earliest=-7d@d latest=@d` | Previous seven complete calendar days |
| `earliest=-1mon@mon latest=@mon` | Previous complete calendar month |

Calendar boundaries use configured time context and can cross daylight-saving changes.

## Parse And Display

```spl
| eval parsed=strptime(timestamp,"%Y-%m-%dT%H:%M:%S.%3NZ")
| eval displayed=strftime(_time,"%Y-%m-%d %H:%M:%S %Z")
```

Confirm format directives supported by your version. Parsing a timestamp with no zone requires an explicit source-time-zone policy.

## Bucketing

```spl
| bin _time span=5m
| stats count BY _time host
```

```spl
| timechart span=1h fixedrange=true count
```

Choose span from decision cadence and event volume, not simply what produces a smooth chart.

## Ingestion Lag

```spl
| eval ingest_lag_seconds=_indextime-_time
| stats p50(ingest_lag_seconds) AS p50 p95(ingest_lag_seconds) AS p95
        max(ingest_lag_seconds) AS max BY sourcetype
```

Interpret negative lag as a possible clock/future-time issue. Positive lag may be normal for batch sources or backfills.

## Compare Periods Carefully

Match complete periods, time zones, business calendars, and population changes. A week-over-week comparison that includes half of today on only one side is biased.

## Common Time Bugs

- Event timestamp parsed in the wrong zone.
- Search uses relative time but dashboard label implies calendar time.
- Scheduled alert window ignores ingestion delay.
- Overlapping scheduled windows produce duplicate actions.
- Missing buckets are converted to zero without checking source health.
- Sorting text-formatted time instead of epoch time.
- Comparing current partial period with prior complete period.

