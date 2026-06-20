# Splunk For Observability

## Learning Objectives

- Connect logs, metrics, and traces around service questions.
- Build service-level indicators with correct units and populations.
- Use high-cardinality context without creating unbounded analytics.

## Signals And Questions

| Signal | Strength | Typical question |
|---|---|---|
| Logs | Rich discrete context | What happened and why? |
| Metrics | Efficient numeric trends | Is the service outside normal bounds? |
| Traces | Request path and causality | Where did latency or error originate? |

The goal is not to collect everything. It is to preserve enough context to explain user-impacting behavior with sustainable cost and access controls.

## RED Method

For request-driven services, start with rate, errors, and duration:

```spl
index=web sourcetype=access_combined earliest=-1h
| bin _time span=5m
| stats count AS requests count(eval(status>=500)) AS errors
        perc50(response_time) AS p50 perc95(response_time) AS p95
        BY _time host
| eval error_rate=round(100*errors/requests, 2)
```

Define what counts as a request and error. Health checks, retries, canceled requests, and client errors may need separate treatment.

## Service-Level Indicators

Availability-style SLI:

```spl
index=web sourcetype=access_combined earliest=-30d@d latest=@d
| eval good=if(status<500 AND response_time<1.0,1,0)
| stats sum(good) AS good_events count AS valid_events
| eval sli=100*good_events/valid_events
```

This example needs a real contract: eligibility filters, missing latency behavior, maintenance, synthetic traffic, aggregation window, target, and late data. “Good” must reflect a user outcome.

## Correlation Context

Propagate stable identifiers such as service, environment, trace ID, span ID, version, region, and deployment ID. Never place unbounded identifiers such as raw user ID into metric dimensions without cardinality and privacy review.

Use logs to pivot from a trace:

```spl
index=app trace_id="<trace-id>" earliest=-15m latest=+15m
| sort 0 _time
| table _time service host level message trace_id span_id
```

Treat values pasted into searches as untrusted input and quote/escape through supported UI token handling.

## Change Correlation

Overlay deployments or feature changes on service signals. Temporal proximity helps prioritize a hypothesis but does not prove causation. Confirm with affected versions, rollback behavior, traces, and control populations.

## Practice

Use the web dataset to define one availability and one latency SLI. Write the exact eligible-event population and what missing `response_time` means. Then create a drilldown that preserves the original time and host scope.

## Official Resources

- [Splunk Observability documentation](https://help.splunk.com/en/splunk-observability-cloud)
- [Splunk Lantern observability use cases](https://lantern.splunk.com/Observability)

Previous: [Security analytics](01-security.md) · Next: [IT operations](03-it-operations.md)

