# Fields And Filtering

## Learning Objectives

- Create, normalize, select, and filter fields.
- Use `eval`, `where`, `search`, `rex`, and field commands intentionally.
- Handle types and nulls explicitly.

## Field Origins

Fields can be indexed metadata, default fields, automatic key-value extractions, configured search-time extractions, calculated fields, aliases, lookups, or values created in the pipeline. Before trusting a field, know who defines it and how consistently it is populated.

## `search` Versus `where`

Use `search` for search-expression syntax and straightforward field filtering. Use `where` for eval expressions and field-to-field comparisons:

```spl
index=tutorial sourcetype="splunk_for_all:web"
| search status>=400 method=POST
| where response_time > 2 * 0.250
```

Filter as early as semantics allow. A predicate that depends on a calculated field must come after its `eval`.

## `eval` Patterns

```spl
index=tutorial sourcetype="splunk_for_all:web"
| eval status_family=floor(status/100)."xx",
       latency_ms=round(response_time*1000, 0),
       is_error=if(status>=500, 1, 0)
| table _time uri status_family latency_ms is_error
```

Common functions:

| Need | Functions |
|---|---|
| Conditional logic | `if`, `case`, `coalesce`, `nullif` |
| Types | `tonumber`, `tostring`, `typeof` |
| Text | `lower`, `upper`, `trim`, `replace`, `substr` |
| Time | `now`, `relative_time`, `strftime`, `strptime` |
| Nulls | `isnull`, `isnotnull`, `coalesce` |
| Validation | `match`, `like`, `in` |

`case` should usually end with a default branch:

```spl
| eval severity=case(
    status>=500, "critical",
    status>=400, "warning",
    status>=200, "normal",
    true(), "other")
```

## Normalize Without Losing Evidence

Preserve original fields and create normalized ones:

```spl
| eval user_normalized=lower(trim(user)),
       src_normalized=coalesce(src_ip, client_ip, src)
```

This is safer during development than overwriting `user`, because you can compare the transformation with the source evidence.

## Extract With `rex`

Suppose `_raw` contains `duration=184ms`:

```spl
| rex field=_raw "duration=(?<duration_ms>\d+)ms"
| eval duration_ms=tonumber(duration_ms)
```

Use named capture groups. Anchor the pattern with reliable context. Avoid `.*` when a narrower character class works. Test failure cases and use configured extractions for fields shared by many searches.

Sed-mode `rex` can transform display values, including redaction in search results, but search-time masking is not a substitute for preventing sensitive data ingestion.

## Select And Rename

```spl
| fields _time host uri status response_time
| rename uri AS endpoint response_time AS latency_seconds
| table _time host endpoint status latency_seconds
```

`fields` controls what continues through the pipeline. `table` produces a tabular presentation and is commonly placed late. Renaming canonical fields too early can break later commands or shared conventions.

## Production Notes

- Normalize common schemas through governed knowledge objects, not copy-pasted `eval` chains.
- Check numeric conversion before comparison; lexicographic text ordering surprises people.
- Regex cost scales with events and input length. Narrow the event set first.
- Avoid silently filling all nulls with zero. Attach semantic meaning to the fill.

## Practice

Create `latency_band` with values `fast` (<250 ms), `normal` (<1000 ms), `slow` (<3000 ms), and `very_slow`. Count requests and calculate error rate by band.

## Official Resources

- [`eval` command and functions](https://help.splunk.com/en/splunk-enterprise/search/spl-search-reference/9.4/search-commands/eval)
- [`rex` command](https://help.splunk.com/en/splunk-enterprise/search/spl-search-reference/9.4/search-commands/rex)

Previous: [Search fundamentals](01-search-fundamentals.md) · Next: [Statistics and time](03-statistics-and-time.md)

