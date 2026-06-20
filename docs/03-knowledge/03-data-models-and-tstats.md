# Data Models, CIM, And `tstats`

## Learning Objectives

- Explain data models and the Common Information Model (CIM).
- Use `tstats` with clear field and acceleration assumptions.
- Validate semantic mapping before optimizing queries.

## Data Models

A data model defines structured datasets and fields for a domain. It can power Pivot, standardized content, and accelerated searches. Constraints determine which events belong; fields provide consistent meaning.

The CIM is a collection of shared semantic conventions used by many Splunk apps and security use cases. Mapping data to CIM is not merely renaming fields. Event constraints, tags, field meanings, allowed values, and data quality must agree.

## Why `tstats` Is Fast

`tstats` calculates statistics from indexed fields and, when used with accelerated data models, their summaries. It does not provide arbitrary access to every search-time field. Speed comes from a different data access path, not magic syntax.

Against indexed metadata:

```spl
| tstats count WHERE index=web BY sourcetype host
| sort - count
```

Against an illustrative accelerated data model:

```spl
| tstats summariesonly=true count AS events
    FROM datamodel=Authentication.Authentication
    WHERE Authentication.action=failure
    BY _time span=15m Authentication.src Authentication.user
| rename Authentication.* AS *
```

The exact model, dataset, constraints, and fields depend on installed content and your mapping. `summariesonly=true` intentionally excludes non-summary data; understand coverage before using it.

## Validate Before Accelerating

1. Define the business meaning of each normalized field.
2. Measure source field coverage and allowed values.
3. Validate dataset constraints against raw-event searches.
4. Test representative searches without acceleration.
5. Estimate summary storage and build cost.
6. Enable acceleration where justified.
7. Monitor summary freshness, size, search behavior, and permissions.

Compare populations, not only totals:

```spl
index=auth sourcetype=auth_events earliest=-24h
| stats count AS raw_events dc(user) AS raw_users
```

Then compare the equivalent model query over the same exact time range and document expected exclusions.

## Acceleration Tradeoffs

Acceleration exchanges storage and build work for faster eligible searches. Wide time ranges, high-cardinality fields, frequent model changes, and overlapping accelerated content can increase cost. Summary retention and late-arriving data affect completeness.

## Common Failure Modes

- A tag exists but the event-type constraint is too broad.
- The same field name has different semantics across sources.
- Required fields are sparse or typed inconsistently.
- Searches use fields not included in accelerated summaries.
- Summary lag is interpreted as a real drop in activity.
- Analysts compare `tstats` and raw searches over different time boundaries.

## Practice

Design a minimal authentication model contract: dataset constraint, required fields, optional fields, allowed actions, and three quality tests. Then write one raw SPL query and one conceptual `tstats` query that should agree.

## Official Resources

- [Common Information Model Add-on Manual](https://help.splunk.com/en/data-management/common-information-model)
- [`tstats` command](https://help.splunk.com/en/splunk-enterprise/search/spl-search-reference/9.4/search-commands/tstats)

Previous: [Knowledge objects](02-knowledge-objects.md) · Next: [Performance](../04-advanced/01-performance.md)

