# Troubleshooting Quick Reference

## Search Returns Nothing

1. Expand only to a known-safe bounded time.
2. Verify the index and role access.
3. Remove pipeline commands and optional terms.
4. Check `source`, `sourcetype`, and `host` values.
5. Inspect source freshness and ingestion lag.
6. Verify field extraction before field filtering.
7. Check spelling, case assumptions, quoting, and Boolean parentheses.

```spl
index=<known-index> earliest=-24h
| stats count latest(_time) AS latest BY sourcetype
| convert ctime(latest)
```

## Field Missing

- Inspect `_raw` and the field sidebar on a small sample.
- Determine whether the field is indexed, extracted, aliased, calculated, or looked up.
- Verify sourcetype and app context.
- Inspect effective `props.conf`/`transforms.conf` in self-managed environments.
- Check search-time operation ordering and permissions.
- Measure coverage rather than testing one event.

## Search Is Slow

- Bound time, index, and sourcetype.
- Move selective predicates to the base search where semantics allow.
- Remove fields before transfer/centralization.
- Inspect high-cardinality grouping.
- Challenge `join`, `transaction`, repeated subsearches, and `sort 0`.
- Open Job Inspector and compare one change at a time.

## Count Looks Wrong

- Identify the counting unit: event, entity, request, array item, or transaction.
- Check duplicate ingestion and multiline breaking.
- Look for `mvexpand`, many-to-many joins, append, and overlapping windows.
- Verify null coverage and denominator.
- Inspect what survives `dedup` and the input order.
- Compare a small known truth set.

## Alert Did Not Fire

- Run the saved search over the exact scheduled window.
- Check ingestion delay and timestamp correctness.
- Review dispatch status, skipped searches, owner, app, permissions, and expiration.
- Inspect threshold, suppression, and result count.
- Confirm the action destination and credentials.
- Test missing-data behavior separately.

## Dashboard Is Wrong For One User

- Compare roles, index access, search filters, capabilities, app permissions, and object ownership.
- Inspect token values and escaping.
- Run the panel SPL directly as the affected user.
- Check base-search post-process fields and result limits.
- Confirm lookup and macro permissions.

## Administrative Change Appears Ignored

- Confirm the setting belongs on this component/tier.
- Inspect effective configuration and provenance.
- Check deployment/app location and stanza spelling.
- Determine whether reload or topology-aware restart is required.
- Review internal logs for parse errors.
- Avoid repeated edits until one hypothesis is tested.

Full chapter: [Monitoring and troubleshooting](../docs/05-admin/04-monitoring-and-troubleshooting.md)

