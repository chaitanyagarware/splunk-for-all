# Lab 04: SPL Performance Clinic

## Scenario

A dashboard search is slow in production. The sample data is too small to benchmark meaningfully, so this lab focuses on search shape and a measurement plan.

## Problem Search

```spl
index=* earliest=0
| rex field=_raw "status=(?<status>\d+)"
| transaction client_ip maxspan=30m
| search status>=500
| sort 0 - duration
| table client_ip host uri status duration _raw
```

## Tasks

### 1. Challenge The Requirement

List at least five questions you must answer before optimizing. Include the intended analytical unit and why events are being grouped by client IP.

### 2. Identify Cost Drivers

Annotate every stage: retrieval scope, regex work, transaction state, late filtering, global sort, and result width. Explain possible semantic errors as well as cost.

### 3. Rewrite

Assume the real requirement is: “For the last 15 minutes, show each host's server-error count, distinct affected client IPs, and p95 response time.” Write a selective search without `rex`, `transaction`, or global raw-event sort.

### 4. Measurement Plan

Describe an A/B comparison using Job Inspector. Hold the time range and data population constant. Record runtime, scanned events, result count, command durations, warnings, and concurrency context.

### 5. Scale Review

Name three fields that may have high cardinality in the web source and what you would do before using each as a dashboard split.

## Stretch

Describe conditions under which a data model and `tstats` could serve the rewritten search. Include required fields, semantic validation, acceleration coverage, and freshness.

Solution: [Lab 04 solution](solutions/04-performance-clinic.md)

