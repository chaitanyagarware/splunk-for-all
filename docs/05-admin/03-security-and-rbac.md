# Security, RBAC, And Hardening

## Learning Objectives

- Apply least privilege across users, services, data, and knowledge objects.
- Identify trust boundaries and secret-handling risks.
- Build a reviewable hardening and audit process.

## Security Model

Protect four things:

1. **Management plane:** administrative endpoints, CLI, configuration, deployment systems.
2. **Data plane:** collection endpoints, forwarders, receiving, indexes, exports.
3. **Search plane:** capabilities, index access, risky commands, workload use.
4. **Content plane:** apps, macros, scripts, lookups, dashboards, alerts, tokens.

Security is not complete when login works. Authorization, transport, audit, data minimization, workload abuse, and content supply chain all matter.

## RBAC

Design roles around job functions. Review:

- Allowed and default indexes.
- Capabilities and inheriting roles.
- Search filters where supported and suitable.
- App and knowledge-object permissions.
- Workload/resource limits.
- Authentication method, session policy, and service-account lifecycle.

Do not use a broad default index as a substitute for explicit access. Test effective permissions with a representative account, not only by reading configuration.

## Least-Privilege Search Content

Macros and saved searches execute within permission contexts that deserve review. A user who can edit a widely used macro can alter many downstream searches. Scheduled searches may outlive their owner or run with elevated access.

Inventory shared scheduled searches:

```spl
| rest /services/saved/searches splunk_server=local
| search is_scheduled=1
| table title eai:acl.app eai:acl.owner eai:acl.sharing disabled cron_schedule
```

Endpoint fields vary. Use this as a starting pattern and verify in your environment.

## Hardening Checklist

- Use supported versions and track security advisories.
- Restrict management interfaces by network and identity.
- Require TLS with validated certificates for sensitive transport.
- Integrate strong enterprise authentication and protect emergency access.
- Disable or constrain unused inputs, apps, accounts, and capabilities.
- Keep secrets in supported stores; rotate and audit them.
- Review third-party apps, custom commands, scripts, and dependencies.
- Forward audit and platform logs to protected monitoring.
- Test backup and recovery, including configuration and identity dependencies.

## Data Protection

Ingest only what is needed. Classify fields, define retention, restrict export, and understand that hashed identifiers can remain personal or linkable data. Redaction at dashboard display does not remove values from indexed raw events or other search paths.

## Audit Questions

```spl
index=_audit earliest=-24h
| stats count BY action user info
| sort - count
```

Internal index access is privileged and fields vary. Build focused audit use cases: administrative changes, authentication anomalies, saved-search changes, export activity, and disabled monitoring. Protect audit data from the identities it observes where feasible.

## Practice

Design roles for three personas: dashboard viewer, detection author, and platform administrator. For each, list data access, capabilities, content rights, and prohibited actions. Then test inheritance for unintended privilege.

## Official Resources

- [Securing Splunk Enterprise](https://help.splunk.com/en/splunk-enterprise/administer/sec-splunk-enterprise)
- [Splunk Product Security](https://advisory.splunk.com/)

Previous: [Distributed deployment](02-distributed-deployment.md) · Next: [Monitoring and troubleshooting](04-monitoring-and-troubleshooting.md)

