# Hands-On Labs

The labs use the synthetic data in [`datasets/`](../datasets/README.md). Load it into `index=tutorial`, validate the expected event counts, and use **All time** only for this fixed historical dataset. In real work, always choose a bounded operational window.

## Lab Path

| Lab | Approx. time | Main skills |
|---|---:|---|
| [01: Search flight school](01-search-basics.md) | 30 min | Inspect, filter, calculate, present |
| [02: Web reliability](02-web-analytics.md) | 45 min | Rates, percentiles, time, service analysis |
| [03: Authentication hunt](03-security-investigation.md) | 60 min | Hypothesis, correlation, tuning, evidence |
| [04: Performance clinic](04-performance-clinic.md) | 45 min | Search shape, cardinality, Job Inspector |
| [05: Capstone](05-capstone.md) | 2-4 hr | Requirements through operational handoff |

## Lab Method

1. Write your expected result before running SPL.
2. Build the search one pipe at a time.
3. Keep a note of row count and fields after each transformation.
4. Answer the plain-language question, not only the query task.
5. Read the solution after you have a working attempt.

The included data is intentionally small. A query that runs instantly here may still be unsuitable at production scale.

## Completion Standard

You have completed a lab when you can explain:

- The event population and time range.
- The analytical unit and denominator.
- What every command changes.
- One data-quality risk.
- One scale risk.
- What the result does and does not prove.

Solutions: [solution guide](solutions/README.md)

