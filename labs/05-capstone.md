# Lab 05: Operational Analytics Capstone

## Mission

Build a reviewable “Storefront Health and Risk” content package using all three datasets. The goal is not the prettiest dashboard; it is a defensible chain from data contract to action.

## Required Deliverables

### 1. Data Readiness Report

For each sourcetype, document owner, purpose, event count, time range, critical fields, field coverage, type checks, sensitive-data classification, and one freshness monitor.

### 2. Reusable Search Layer

Create and document:

- A normalized endpoint field.
- A calculated revenue field: `quantity*unit_price`.
- A lookup design for host owner and criticality.
- Naming and permissions for the shared objects.

### 3. Dashboard Design

Create a wireframe or dashboard with four sections:

1. Storefront request health.
2. Checkout errors and latency.
3. Completed order value by region/product.
4. Authentication risk and telemetry confidence.

Every panel must list audience, decision, base population, time range, SPL, limitations, and drilldown.

### 4. Alert Specification

Design one checkout reliability alert and one authentication analytic. Include schedule, window, ingestion delay, threshold rationale, suppression, severity, owner, response, and test cases.

### 5. Performance Review

Use Job Inspector where available. Identify broad retrieval, high-cardinality grouping, duplicated bases, centralized commands, and acceleration opportunities. Record evidence before and after changes.

### 6. Operational Handoff

Write a runbook with dashboard meaning, alert triage, dependencies, data-silence behavior, permissions, deployment/rollback, monitoring, and quarterly review owner.

## Acceptance Criteria

- SPL is syntactically clear and uses explicit indexes/sourcetypes.
- Rates state their denominator and field coverage.
- Detection claims include false positives and bypasses.
- Dashboard panels lead to decisions and preserve drilldown context.
- Shared objects have team ownership and minimum permissions.
- No secrets, personal data, proprietary content, or destructive commands appear.
- Limitations are visible, not hidden in implementation notes.

## Self-Review Rubric

Score each 0-3: data correctness, SPL clarity, statistical reasoning, performance, security, usability, operational readiness, and documentation. A strong project has no zero and explains every score below three.

Guidance: [Capstone review guide](solutions/05-capstone.md)

