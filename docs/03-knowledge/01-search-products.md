# Reports, Dashboards, And Alerts

## Learning Objectives

- Turn an exploratory search into a reliable saved search.
- Choose between reports, dashboards, and alerts.
- Design content around decisions rather than visual novelty.

## From Question To Product

An exploratory search answers a question once. A search product answers a recurring question for a defined audience with ownership, permissions, schedule, performance expectations, and a response.

| Product | Best for | Required design work |
|---|---|---|
| Report | Reusable search and table/chart | Time range, permissions, schedule, result contract |
| Dashboard | Shared situational view | Audience, hierarchy, tokens, load, drilldowns |
| Alert | Condition that requires action | Signal logic, suppression, routing, runbook, owner |

## Dashboard Design

Start with decisions:

1. What decision should this page support?
2. Who makes it and how often?
3. What is normal, what changed, and where can they investigate?
4. What data-quality caveat must remain visible?

A useful operational hierarchy is summary indicators, trends, breakdowns, and then event evidence. Prefer a few meaningful panels over a wall of single values.

### Base Search Pattern

A shared base can avoid repeated retrieval, but overly broad bases create large result sets and coupling. Keep the base selective and transformations compatible with downstream panels.

```spl
index=web sourcetype=access_combined earliest=-24h
| fields _time host uri status response_time
```

Then one panel can calculate service health:

```spl
| stats count AS requests count(eval(status>=500)) AS errors
        perc95(response_time) AS p95 BY host
| eval error_rate=round(100*errors/requests, 2)
```

## Alert Design

Good alert logic separates signal, context, and response.

```spl
index=auth action=failure earliest=-10m@m latest=@m
| stats count AS failures dc(src_ip) AS source_count values(src_ip) AS sources BY user
| where failures>=10 AND source_count>=3
```

Before enabling it, define:

- Search schedule and time window, including ingestion delay.
- Threshold rationale and minimum data volume.
- Entity key, severity, suppression field, and suppression duration.
- Expected false positives and tuning dimensions.
- Owner, destination, investigation steps, and closure feedback.
- Behavior when the data source is late or silent.

Never claim that example logic is a universally valid detection. Validate against your data and threat model.

## Scheduling

Schedules should account for runtime and ingestion delay. A five-minute search scheduled every five minutes may use a slightly wider window, but overlapping windows can duplicate actions. Use stable alert identifiers or throttling to manage repeats, and monitor skipped searches.

## Permissions And Ownership

Saved objects have app context, owner, and sharing. Avoid personal ownership for operational content. Use roles and apps that represent the team, review dependencies such as macros and lookups, and document handoff.

## Practice

Design a three-panel web-health dashboard and one alert. For every panel, write the decision it supports. For the alert, write a five-step runbook before choosing a threshold.

## Official Resources

- [Create dashboards](https://help.splunk.com/en/splunk-enterprise/create-dashboards-and-reports)
- [Alerting Manual](https://help.splunk.com/en/splunk-enterprise/alert-and-respond/alerting-manual)

Previous: [Advanced data shaping](../02-spl/05-advanced-data-shaping.md) · Next: [Knowledge objects](02-knowledge-objects.md)

