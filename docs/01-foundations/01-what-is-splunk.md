# What Is Splunk?

## Learning Objectives

- Explain the path from machine data to action.
- Distinguish events, metrics, traces, and knowledge objects.
- Recognize where data quality and governance enter the system.

## Mental Model

Splunk is a family of products and services for collecting, indexing, searching, analyzing, and acting on machine data. This course focuses on durable concepts shared by common Splunk Platform workflows while calling out that Cloud and Enterprise operations differ.

Think in layers:

| Layer | Question | Examples |
|---|---|---|
| Collection | How does data arrive? | Files, forwarders, HEC, APIs, network inputs |
| Parsing | How are events and time identified? | Line breaking, timestamp recognition, source typing |
| Storage | Where and how long is data retained? | Indexes, buckets, retention policies |
| Search | Which events answer the question? | SPL base searches and pipelines |
| Knowledge | How is meaning reused? | Field extractions, lookups, tags, event types, data models |
| Action | What happens next? | Dashboard, alert, ticket, automation, investigation |

An attractive dashboard cannot repair missing data, incorrect timestamps, or inconsistent semantics. Observability begins before ingestion.

## Data Shapes

### Events

Discrete records such as a login attempt, HTTP request, or process start. Events usually retain raw context and work well for investigation.

### Metrics

Numeric measurements identified by dimensions, such as CPU utilization by host. Metrics are optimized for time-series analysis; cardinality design matters.

### Traces

Connected spans representing a request across services. Trace and span identifiers allow causality and latency to be followed across boundaries.

### Knowledge Objects

Reusable interpretations layered over data: fields, lookups, reports, alerts, tags, event types, workflow actions, and data models. Their permissions, naming, and ownership determine whether a deployment stays understandable.

## Search-Time Versus Index-Time

Index-time work occurs as data is parsed and stored. Search-time work occurs when a search runs. Index-time configuration has a large blast radius: mistakes can affect all future events and often cannot be retroactively repaired without reingestion. Prefer search-time enrichment unless storage, routing, privacy, or performance requirements justify earlier transformation.

## A Question Becomes SPL

Business question: *Which web endpoints have both elevated errors and material traffic?*

```spl
index=web sourcetype=access_combined earliest=-24h
| stats count AS requests count(eval(status>=500)) AS errors BY uri_path
| eval error_rate=round(100*errors/requests, 2)
| where requests>=100 AND error_rate>=2
| sort - error_rate
```

This is stronger than counting errors alone because one failure out of one request is not the same operational signal as 500 failures out of 10,000 requests.

## Production Notes

- Treat data onboarding as a contract: owner, purpose, schema, volume, access, retention, and validation.
- Keep sensitive fields out when they are not required. Masking after broad ingestion is not equivalent to data minimization.
- Use stable naming conventions for indexes, sourcetypes, fields, apps, and knowledge objects.
- Measure completeness, timeliness, parsing correctness, and semantic consistency.

## Checkpoint

For an authentication source, identify one risk at each layer. Example: collection outage, incorrect timestamp zone, insufficient retention, broad search role, conflicting field aliases, and an alert with no owner.

## Official Resources

- [Splunk Platform product documentation](https://help.splunk.com/en/splunk-enterprise)
- [Splunk Lantern](https://lantern.splunk.com/)

Previous: [Start here](../00-start-here.md) · Next: [Architecture](02-architecture.md)

