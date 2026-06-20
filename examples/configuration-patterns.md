# Configuration Patterns

These fragments teach configuration shape. They are deliberately incomplete and must not be deployed unchanged. Check the `.conf.spec` reference for your exact release and use topology-specific deployment workflows.

## App Layout

```text
TA-example_source/
├── default/
│   ├── app.conf
│   └── props.conf
├── local/
├── metadata/
│   └── default.meta
├── README/
│   └── inputs.conf.spec
└── README.md
```

Keep shipped defaults version-controlled. Use local overrides only for environment-specific values, and never store secrets in Git.

## File Monitor Shape

```ini
# inputs.conf - illustrative only
[monitor:///var/log/example/app.log]
disabled = false
index = application
sourcetype = example:app
```

Production review: component placement, path expansion, rotation, permissions, duplicate/overlapping monitors, host assignment, throughput, and downstream index existence.

## Event Breaking And Time Shape

```ini
# props.conf - illustrative only
[example:app]
SHOULD_LINEMERGE = false
LINE_BREAKER = ([\r\n]+)
TIME_PREFIX = ^
TIME_FORMAT = %Y-%m-%dT%H:%M:%S.%3NZ
MAX_TIMESTAMP_LOOKAHEAD = 24
TRUNCATE = 20000
```

Test representative multiline, malformed, long, zone, and precision cases. Deploy parsing settings to the tier that parses this input path and search-time knowledge to the tiers that need it.

## Search-Time Extraction Shape

```ini
# props.conf
[example:app]
EXTRACT-request = request_id=(?<request_id>[A-Za-z0-9-]+)
FIELDALIAS-source_address = client_ip AS src_ip
EVAL-duration_ms = round(duration_seconds * 1000, 0)
```

Confirm search-time operation order. An alias does not transform a value, and a calculated field cannot safely depend on a field that does not yet exist.

## Index Lifecycle Shape

```ini
# indexes.conf - placeholders, not deployable values
[application]
homePath = $SPLUNK_DB/application/db
coldPath = $SPLUNK_DB/application/colddb
thawedPath = $SPLUNK_DB/application/thaweddb
frozenTimePeriodInSecs = <retention-seconds>
```

Retention also depends on storage behavior, bucket settings, and deployment type. `thawedPath` does not automatically restore archived data. Design archive and restore testing separately.

## Safe Review Checklist

- Requirement and owner documented.
- Exact version's spec checked.
- Correct deployment component identified.
- Effective current configuration captured with provenance.
- Syntax and representative data tested.
- No secret or private data included.
- Restart/reload behavior understood.
- Canary, rollback, and success metrics defined.
- Post-deployment effective configuration verified.

