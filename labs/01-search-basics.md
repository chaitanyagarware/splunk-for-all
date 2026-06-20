# Lab 01: Search Flight School

## Scenario

You have received a synthetic web source. Before anyone builds a dashboard, you must establish what the data contains and answer basic traffic questions.

## Objectives

- Inspect metadata and field coverage.
- Filter with Boolean logic.
- Derive fields with `eval`.
- Produce ranked tables with `stats` and `sort`.

## Tasks

### 1. Verify The Source

Find the event count, earliest time, latest time, hosts, and percentage of events containing `status` and `response_time`. Expected total: 36.

### 2. Inspect Evidence

Return the five most recent events that are not health checks. Display time, request ID, client IP, method, URI, status, response time, and host.

### 3. Classify Status

Create `status_family` with values `2xx`, `4xx`, `5xx`, and `other`. Count requests by family and calculate percentage of all requests.

### 4. Rank Endpoints

For each URI, calculate requests, errors (`status>=500`), average response time, and p95 response time. Rank by errors, then p95 response time.

### 5. Explain The Result

Answer:

- Which endpoint produces every server error?
- Which host serves those errors?
- Does the dataset prove that host is the root cause? Why not?

## Constraints

- Use an explicit index and sourcetype.
- Do not use `transaction`, `join`, or a subsearch.
- Round displayed percentages and durations to two decimals.

## Stretch

Create a `latency_band` and compare error rate by band. State whether the relationship implies causation.

Solution: [Lab 01 solution](solutions/01-search-basics.md)

