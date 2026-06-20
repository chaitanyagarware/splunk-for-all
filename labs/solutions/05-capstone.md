# Solution 05: Capstone Review Guide

The capstone has no single query answer. Use this review guide to test whether the work is operationally defensible.

## Data

- Counts match 36 web, 30 auth, and 20 order events.
- Time, numeric types, field coverage, and allowed categorical values are tested.
- Synthetic identity and IP assumptions remain documented.
- Data freshness is separated from event activity.

## Semantics

- Server-error rates use requests with valid status as their stated denominator.
- Revenue excludes or separately represents canceled, pending, and refunded orders.
- Authentication logic distinguishes password spray from one-user guessing.
- Normalized fields preserve source fields and report conflicts.

Example revenue analysis:

```spl
index=tutorial sourcetype="splunk_for_all:orders"
| eval gross_value=quantity*unit_price
| stats sum(eval(if(status="completed",gross_value,0))) AS completed_value
        sum(gross_value) AS submitted_value count AS orders BY region product
| eval completed_value=round(completed_value,2),
       submitted_value=round(submitted_value,2)
```

## Dashboard

Each panel names a decision and exposes time range, population, field coverage, units, and drilldown. Panels do not silently compare unrelated time windows. High-cardinality tokens are bounded and escaped.

## Alerts

Each analytic has positive, negative, boundary, late-data, missing-field, and duplicate-event test cases. Suppression is tied to the entity that represents repeated risk. The response destination has an owner and a tested runbook.

## Operations

The package documents app context, ownership, minimum permissions, deployment path, rollback trigger, source silence, search health, dependency inventory, and review cadence. No personal owner is a single point of failure.

## Final Presentation

Explain the project in this order: question, evidence contract, method, result, limitations, decision, operational ownership. If the walkthrough begins with visualization colors, return to the user outcome.

