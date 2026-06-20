# Splunk For Security Analytics

## Learning Objectives

- Turn a threat hypothesis into measurable SPL.
- Separate detection, triage, investigation, and response.
- Tune logic using environment context and validation evidence.

## Detection Engineering Loop

```text
threat hypothesis -> data requirements -> analytic -> test -> tune
                  -> deploy -> triage -> feedback -> measure
```

Start with behavior and required evidence, not a clever query. Document log sources, fields, evasion opportunities, expected benign causes, severity, and response.

## Example: Password Spraying Hypothesis

Hypothesis: one source attempts a small number of common passwords across many users.

```spl
index=auth sourcetype=auth_events action=failure earliest=-10m@m latest=@m
| stats count AS failures dc(user) AS targeted_users values(user) AS users
        BY src_ip
| where failures>=10 AND targeted_users>=5
| eval failures_per_user=round(failures/targeted_users, 2)
| sort - targeted_users
```

Required tuning includes NAT/proxy behavior, vulnerability scanners, identity provider retries, service accounts, trusted infrastructure, field normalization, ingestion delay, and source IP semantics. Counts alone do not establish malicious intent.

## Example: Failure Then Success

```spl
index=auth sourcetype=auth_events earliest=-30m
| stats count(eval(action="failure")) AS failures
        count(eval(action="success")) AS successes
        min(eval(if(action="failure",_time,null()))) AS first_failure
        max(eval(if(action="success",_time,null()))) AS last_success
        BY user src_ip
| where failures>=5 AND successes>=1 AND last_success>=first_failure
```

This still does not prove strict event sequence. A later maximum success plus an earlier minimum failure can coexist with other ordering. Use the advanced sequence pattern when strict order is essential.

## Triage Output

A detection result should carry useful context without exposing unnecessary sensitive data:

- Stable entity and analytic identifiers.
- First/last time and search window.
- Counts and threshold evidence.
- Source, destination, user, asset, and identity context.
- Data source and field coverage.
- Links to a bounded investigation, not an unrestricted all-time search.
- Analytic version and suppression/tuning applied.

## Risk-Based Thinking

Multiple weak signals can become meaningful around the same entity. Risk aggregation must control duplicate signals, entity resolution, score inflation, time decay, and explainability. A risk score prioritizes investigation; it is not proof.

## Detection Quality

Measure data availability, alert volume, distinct entities, analyst disposition, time to triage, true/false-positive evidence, and coverage gaps. “No alerts” can mean no activity, broken telemetry, overly strict logic, or effective prevention.

## Practice

Complete [the authentication hunt](../../labs/03-security-investigation.md). Then add one bypass hypothesis and one data-health alert for the same source.

## Official Resources

- [Splunk Security Content](https://research.splunk.com/)
- [Common Information Model](https://help.splunk.com/en/data-management/common-information-model)

Previous: [Monitoring](../05-admin/04-monitoring-and-troubleshooting.md) · Next: [Observability](02-observability.md)

