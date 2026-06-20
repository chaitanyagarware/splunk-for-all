# Configuration Files And Precedence

## Learning Objectives

- Explain configuration layering and app structure.
- Inspect effective configuration safely.
- Plan, test, deploy, and roll back a configuration change.

## Configuration Model

Splunk Enterprise behavior is composed from configuration files, usually organized into apps. Files contain named stanzas and attributes. Multiple copies can contribute to the effective configuration according to context and precedence.

Never edit files under a `default` directory supplied by Splunk or an add-on. Put local changes in a controlled app's `local` directory. Upgrades can replace default content.

```text
my_app/
├── default/          # Version-controlled defaults shipped by the app
├── local/            # Local overrides; manage deliberately
├── metadata/         # Object permissions and export behavior
├── lookups/
├── bin/
└── README/
```

Exact supported structure depends on app purpose and deployment type.

## Common Files

| File | Responsibility |
|---|---|
| `inputs.conf` | Data inputs |
| `outputs.conf` | Forwarding destinations and behavior |
| `props.conf` | Parsing and search-time source type behavior |
| `transforms.conf` | Transform definitions, routing, and lookup/extraction support |
| `indexes.conf` | Index storage and retention behavior |
| `server.conf` | Server and clustering settings |
| `web.conf` | Splunk Web settings |
| `authentication.conf` | Authentication configuration |
| `authorize.conf` | Roles and capabilities |
| `limits.conf` | Resource and search limits |

Do not copy a stanza from the internet without checking the configuration specification for your exact version.

## Inspect Effective Configuration

On self-managed Enterprise, `btool` can show merged configuration and provenance:

```powershell
& "$env:SPLUNK_HOME\bin\splunk.exe" btool props list "splunk_for_all:web" --debug
```

On Unix-like systems, use the corresponding Splunk CLI path. Access, tooling, and supported workflows differ in Splunk Cloud Platform.

The `--debug` provenance is essential: seeing the effective value without its source file can hide a precedence conflict.

## Change Workflow

1. Record the requirement, owner, affected tier, and current effective values.
2. Check the configuration spec and topology-specific deployment method.
3. Make the smallest change in a version-controlled app.
4. Validate syntax, secrets handling, and permissions.
5. Test representative good, bad, and boundary data in a lower environment.
6. Plan restart/reload behavior and rollback.
7. Deploy through the supported mechanism.
8. Verify effective configuration and service/data health.
9. Monitor long enough to cover delayed effects.

## Parsing Responsibility

Parsing settings must reach the component that performs parsing for that input path, not automatically every forwarder. Search-time settings must reach search participants in the relevant app context. Misplacing configuration can make a correct stanza appear ineffective.

## Secrets

Do not commit passwords, tokens, private keys, session cookies, or exported encrypted values. Splunk-managed encrypted values may still be environment-bound sensitive material. Use supported credential storage and deployment workflows.

## Practice

Given a sourcetype with a timestamp error, write a change plan without editing anything. Include the parsing tier, representative samples, current `btool` output, proposed app, test assertions, deployment order, and rollback signal.

## Official Resources

- [Configuration file reference](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/9.4/configuration-file-reference)
- [Configuration file precedence](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/9.4/administer-splunk-enterprise-with-configuration-files/configuration-file-precedence)

Previous: [API and automation](../04-advanced/03-api-and-automation.md) · Next: [Distributed deployment](02-distributed-deployment.md)

