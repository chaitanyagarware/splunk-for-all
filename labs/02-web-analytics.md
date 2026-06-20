# Lab 02: Web Reliability

## Scenario

The storefront team reports intermittent checkout failures. Build a small reliability analysis from the 36 web events.

## Objectives

- Define eligible requests and correct denominators.
- Compare counts, rates, and latency percentiles.
- Build an investigation table and an operational recommendation.

## Tasks

### 1. Define The Population

Exclude `/health`. Report total eligible requests and field coverage for status and response time.

### 2. Service Indicators

Calculate:

- Request count.
- Server-error count.
- Server-error rate.
- Median and p95 response time.
- “Good” request percentage, where good means `status<500 AND response_time<1`.

Write down why that good-event definition may not represent a real user outcome.

### 3. Find The Concentration

Break the same indicators down by URI and host. Apply a minimum-volume condition so that one tiny group cannot dominate the ranking.

### 4. Create A Timeline

Build a one-minute time chart of requests and errors. Because the sample is small, inspect empty buckets and decide whether filling them with zero would be honest.

### 5. Build The Drilldown

Return raw evidence for the worst endpoint with request ID and client IP. Limit displayed fields, but preserve `_raw` while investigating.

## Deliverable

Write a five-sentence incident note: observed symptom, affected scope, evidence, uncertainty, and next test. Do not claim root cause from this dataset.

## Stretch

Compare p95 latency for successful versus server-error requests. Explain why the sample size makes the percentile unstable.

Solution: [Lab 02 solution](solutions/02-web-analytics.md)

