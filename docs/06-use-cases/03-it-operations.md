# Splunk For IT Operations

## Learning Objectives

- Build service-centric operational views.
- Detect data and infrastructure health issues without alert storms.
- Connect symptoms, changes, ownership, and runbooks.

## Entity And Service Context

Operational data often names the same entity differently. Establish identity rules for hostnames, cloud instance IDs, containers, services, and clusters. Enrich with owner, environment, criticality, region, and lifecycle status.

```spl
index=os sourcetype=system_metrics earliest=-30m
| lookup asset_inventory host OUTPUT owner environment criticality
| stats latest(cpu_pct) AS cpu latest(memory_pct) AS memory
        latest(_time) AS last_seen BY host owner environment criticality
| eval age=now()-last_seen
```

Do not page solely because a host disappeared if ephemeral lifecycle data says it was terminated normally.

## Symptom Versus Cause

High CPU, queue depth, errors, and slow response are symptoms. Combine them with dependency, change, and saturation context. Avoid one alert per metric when several describe the same service incident.

## Data Silence

```spl
| metadata type=hosts index=os
| eval minutes_silent=round((now()-recentTime)/60,1)
| where minutes_silent>15
| convert ctime(recentTime)
| sort - minutes_silent
```

Production silence detection needs an expected-entity inventory. `metadata` can tell you what was seen, not what should exist but never reported.

## Change-Aware Investigation

```spl
(index=web sourcetype=access_combined) OR (index=changes sourcetype=deployment)
| eval service=coalesce(service, app)
| bin _time span=5m
| stats count(eval(sourcetype="access_combined" AND status>=500)) AS errors
        values(eval(if(sourcetype="deployment",version,null()))) AS deployments
        BY _time service
```

This places signals together but does not show the error denominator. Add request totals before drawing rate conclusions.

## Operational Content Checklist

- A named audience and decision.
- Entity and service ownership.
- Normalization and enrichment coverage.
- Threshold rationale or baseline behavior.
- Deduplication and incident grouping.
- Maintenance and ephemeral-asset handling.
- A tested runbook and escalation path.
- Service and data-source health indicators.

## Practice

Design a “service readiness” dashboard with exactly four panels. Each must answer a distinct question: user impact, dependency health, recent changes, and telemetry confidence. Add drilldowns that keep time and entity context.

## Official Resources

- [Splunk Lantern IT use cases](https://lantern.splunk.com/IT_Use_Cases)
- [Monitoring Splunk Enterprise](https://help.splunk.com/en/splunk-enterprise/administer/monitor)

Previous: [Observability](02-observability.md) · Next: [Career roadmap](../07-career-roadmap.md)

