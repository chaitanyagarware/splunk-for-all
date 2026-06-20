# REST API And Automation

## Learning Objectives

- Use Splunk's management API with scoped authentication and TLS verification.
- Understand search job lifecycle and result retrieval.
- Build automation that handles pagination, errors, limits, and secrets.

## API Mental Model

Splunk exposes management and search capabilities through REST endpoints, commonly on the management port for self-managed Enterprise. Splunk Cloud Platform access, approved endpoints, authentication, and network routes depend on the service and tenant configuration.

Never assume an administrative endpoint is reachable or permitted. Follow the official API reference for your deployment.

## Authentication

Prefer a narrowly scoped service identity and a supported token mechanism. Keep tokens out of source code, shell history, logs, screenshots, and query parameters. Verify TLS and rotate credentials.

Illustrative PowerShell request using an environment variable:

```powershell
$headers = @{ Authorization = "Bearer $env:SPLUNK_TOKEN" }
Invoke-RestMethod `
  -Uri "https://splunk.example:8089/services/server/info?output_mode=json" `
  -Headers $headers
```

This is a pattern, not a promise that bearer tokens or that route are enabled in your environment.

## Search Job Lifecycle

For asynchronous export and search APIs, the broad flow is:

1. Create a search job with an explicit search and time range.
2. Capture the search ID (SID).
3. Poll job state with bounded retry and backoff.
4. Retrieve results or events with pagination/stream handling.
5. Inspect warnings and partial-result status.
6. Clean up when appropriate and record an audit trail.

Splunk searches sent to the API generally include the `search` command prefix:

```text
search index=web sourcetype=access_combined status>=500 earliest=-15m
| stats count by host
```

## Resilient Automation Checklist

- Set connection and overall deadlines.
- Retry only transient failures, with backoff and jitter.
- Respect `429` and server guidance.
- Handle non-JSON error bodies and partial results.
- Bound result size and stream large exports.
- Record SID, time range, query version, result count, and warnings.
- Make write operations idempotent or safely repeatable.
- Separate query logic from credentials and endpoints.

## In-Product REST Search

Authorized users can inspect exposed REST resources through SPL:

```spl
| rest /services/saved/searches splunk_server=local
| table title eai:acl.app eai:acl.owner disabled is_scheduled cron_schedule
```

REST search visibility follows capabilities and endpoint behavior. Avoid broad endpoint scans in shared environments; select fields and use a narrow purpose.

## Configuration As Code

Package shared configuration in apps, version it, review it, test it in a lower environment, and deploy with the supported mechanism for your topology. Validate the effective merged configuration after deployment. Never store passwords or tokens in plain configuration committed to Git.

## Practice

Design a read-only automation that inventories scheduled searches. Specify authentication, pagination, timeout, output schema, sensitive fields to omit, and behavior when one page fails. You do not need to run it against a real server.

## Official Resources

- [Splunk REST API Reference](https://help.splunk.com/en/splunk-enterprise/rest-api-reference)
- [Developing with the Splunk Platform](https://dev.splunk.com/enterprise/docs/)

Previous: [Advanced patterns](02-advanced-patterns.md) · Next: [Configuration](../05-admin/01-configuration.md)

