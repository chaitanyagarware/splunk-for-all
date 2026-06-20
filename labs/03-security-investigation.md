# Lab 03: Authentication Investigation

## Scenario

Identity monitoring has produced two hypotheses: password spraying from one source, and repeated failures followed by success for one account/source pair.

## Objectives

- Translate hypotheses into SPL.
- Separate unordered aggregation from sequence.
- Add context and identify false-positive paths.

## Tasks

### 1. Validate The Data

Confirm 30 events. Report action and reason distributions, distinct users, distinct source IPs, and timestamp range.

### 2. Password Spray

Find sources with at least eight failures against at least five distinct users. Return failure count, targeted user count, users, first time, and last time.

### 3. Failure Then Success

Find user/source pairs with at least five failures and at least one success. Include first failure, last failure, first success, and application.

Add a condition that the first success occurs after the first failure. Then explain why this still may not fully describe an uninterrupted failure-then-success sequence.

### 4. Triage

For each result, inspect raw events in time order. Identify the most likely benign explanation in this synthetic dataset and the result that deserves deeper investigation.

### 5. Detection Specification

Write:

- Threat hypothesis.
- Required fields and coverage check.
- Search window and schedule.
- Thresholds and rationale.
- Five expected false-positive sources.
- Triage fields, owner, and runbook entry.
- One data-silence monitor.

## Safety Note

This is educational logic, not a production-ready detection. Real authentication fields, source addressing, retries, MFA flows, service identities, and baselines require environment-specific validation.

Solution: [Lab 03 solution](solutions/03-security-investigation.md)

