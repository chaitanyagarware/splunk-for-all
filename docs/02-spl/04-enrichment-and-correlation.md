# Enrichment And Correlation

## Learning Objectives

- Enrich events with lookups.
- Correlate related behavior with `stats` before reaching for `join` or `transaction`.
- Understand subsearch limits and semantic tradeoffs.

## Lookups

Lookups map event fields to maintained context such as asset owner, business unit, approved service, or risk tier.

```spl
index=web sourcetype=access_combined
| lookup asset_inventory host OUTPUT owner environment criticality
| fillnull value="unknown" owner environment criticality
| stats count AS requests count(eval(status>=500)) AS errors
        BY owner environment criticality
```

`OUTPUTNEW` avoids overwriting an existing field. Define who maintains the lookup, how freshness is measured, and how unmatched values are handled. A lookup is a small data product, not merely a CSV.

## Correlate With `stats`

Many multi-event questions can become conditional aggregation:

```spl
index=auth sourcetype=auth_events earliest=-1h
| stats count(eval(action="failure")) AS failures
        count(eval(action="success")) AS successes
        min(_time) AS first_seen max(_time) AS last_seen
        values(src_ip) AS source_ips
        BY user
| where failures>=5 AND successes>=1
```

This asks for users with both failures and success in the window. It is scalable and explicit, but it does not prove the success occurred after the failures. Add ordered logic when sequence matters.

## `transaction`

`transaction` groups events using fields and time/sequence constraints. It can be readable for bounded investigation, but is memory-intensive and subject to limits.

```spl
index=app (action=start OR action=end) earliest=-15m
| transaction request_id startswith="action=start" endswith="action=end" maxspan=2m
| where eventcount>=2
```

Before using it, ask whether `stats min(_time) max(_time) values(...) BY request_id` answers the question. `transaction` is appropriate only when its event grouping semantics are actually needed.

## Subsearches

A bracketed search runs first and formats its result into the outer search:

```spl
index=web sourcetype=access_combined
[ search index=auth action=blocked earliest=-15m
  | fields src_ip
  | rename src_ip AS client_ip
  | format ]
```

Subsearches have execution and result limits. Always run the inner search independently and inspect `| format`. For repeated or large correlation, consider a lookup, summary, data model, or a combined search with `stats`.

## `join`

`join` feels familiar to SQL users but is often a poor default in SPL because one side is a limited subsearch and centralized processing can be expensive. Use it when the required semantics truly match and the right-side dataset is small and controlled.

Alternative combined search:

```spl
(index=web sourcetype=access_combined) OR (index=auth sourcetype=auth_events)
| eval correlation_key=coalesce(client_ip, src_ip)
| stats values(uri) AS uris values(action) AS auth_actions
        count AS events BY correlation_key
| where isnotnull(mvfind(auth_actions, "blocked")) AND mvcount(uris)>0
```

Validate field semantics: two datasets using the name `src_ip` may describe different network positions.

## Production Notes

- Correlation windows encode a hypothesis. Tune them with known examples.
- Many-to-many joins can multiply rows and distort counts.
- `values()` is not ordered and can be limited; do not treat it as an event timeline.
- Record lookup match rate to expose enrichment gaps.

## Practice

Identify authentication users with at least three failures and a later success from one of the same source IPs. Build it first with `stats`, then explain which part of the sequence claim your first version cannot guarantee.

## Official Resources

- [`lookup` command](https://help.splunk.com/en/splunk-enterprise/search/spl-search-reference/9.4/search-commands/lookup)
- [`transaction` command](https://help.splunk.com/en/splunk-enterprise/search/spl-search-reference/9.4/search-commands/transaction)

Previous: [Statistics and time](03-statistics-and-time.md) · Next: [Advanced data shaping](05-advanced-data-shaping.md)

