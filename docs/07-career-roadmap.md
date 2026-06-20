# Certification And Career Roadmap

## Learning Objectives

- Build a role-based portfolio rather than memorize isolated commands.
- Use official certification blueprints as the current authority.
- Turn the repository curriculum into demonstrable projects.

## Choose A Role Outcome

| Role direction | Practice emphasis | Portfolio evidence |
|---|---|---|
| Search analyst | SPL, dashboards, data quality | Reproducible analysis with decision narrative |
| Platform admin | Data onboarding, config, RBAC, health | Tested app/config change with rollback and monitoring |
| Detection engineer | Threat hypotheses, CIM, tuning | Detection package with tests, triage, and limitations |
| Observability engineer | SLIs, correlation, cardinality | Service dashboard with explicit population and drilldowns |
| Content developer | Knowledge objects, packaging, automation | Versioned app structure, documentation, CI, release notes |

## Twelve-Week Plan

| Weeks | Focus | Deliverable |
|---|---|---|
| 1-2 | Architecture, data, first searches | Data-flow diagram and field-quality report |
| 3-4 | Filtering, eval, stats, time | SPL notebook solving 15 questions |
| 5-6 | Correlation, regex, JSON, multivalue | Web and auth lab write-ups |
| 7-8 | Dashboards, alerts, knowledge objects | Decision-focused dashboard plus runbook |
| 9-10 | Data models, performance, admin | Query benchmark and configuration change plan |
| 11 | Applied specialization | Security, observability, or IT capstone |
| 12 | Review and explain | Portfolio README and recorded walkthrough |

## Certification

Certification names, prerequisites, exam versions, delivery policies, and blueprints change. Use [Splunk's official certification site](https://www.splunk.com/en_us/training/certification-track.html) as the only current authority. Do not use or share exam dumps.

Prepare by mapping every blueprint objective to:

1. A concept you can explain without product jargon.
2. A task you can perform in a lab.
3. A failure mode you can diagnose.
4. An official documentation page you can find quickly.

## Portfolio Standard

A strong project includes synthetic data, question, assumptions, field contract, annotated SPL, validation evidence, performance notes, screenshots without secrets, limitations, and next steps. It should be reproducible by another learner.

## Interview Drills

- Explain why early filtering changes distributed-search cost.
- Compare `stats`, `eventstats`, and `streamstats` with one scenario each.
- Diagnose a sourcetype whose timestamps are one day in the future.
- Design a failed-login alert and explain at least five false positives.
- Explain why indexer replication is not the same as backup.
- Review a slow search containing `join`, `transaction`, global sort, and all-time scope.
- Describe how you would prove an accelerated data model is complete enough.

## Final Checkpoint

Can you take an unfamiliar source from data contract through ingestion validation, normalization, analysis, performance review, dashboard/alert design, access control, runbook, and lifecycle ownership? That end-to-end reasoning is more durable than memorizing every command.

## Official Resources

- [Splunk Education](https://www.splunk.com/en_us/training.html)
- [Splunk Certification](https://www.splunk.com/en_us/training/certification-track.html)
- [Splunk Community](https://community.splunk.com/)

Previous: [IT operations](06-use-cases/03-it-operations.md) · Next: [Hands-on labs](../labs/README.md)

