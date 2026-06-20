# Regex Reference For SPL

Splunk commonly uses PCRE-compatible regular expressions, but supported behavior depends on command and product version. Test in your environment.

## Named Extraction

```spl
| rex field=_raw "request_id=(?<request_id>[A-Za-z0-9-]+)"
```

## Reliable Patterns

| Need | Pattern | Note |
|---|---|---|
| Integer | `(?<value>\d+)` | Add signs/decimals if needed |
| IPv4-like token | `(?<src_ip>\d{1,3}(?:\.\d{1,3}){3})` | Shape only; does not validate octets |
| Quoted value | `user=\"(?<user>[^\"]+)\"` | Avoid greedy `.*` |
| Until whitespace | `status=(?<status>\S+)` | Confirm values cannot contain spaces |
| URI path | `^(?<path>[^?]+)` | Apply to the URI field, not arbitrary raw text |
| Optional suffix | `name=(?<name>[^,]+)(?:,|$)` | Anchor with delimiters |

## Extract Repeated Values

```spl
| rex field=_raw max_match=0 "role=(?<roles>[A-Za-z0-9_-]+)"
| eval role_count=mvcount(roles)
```

`max_match=0` can create a large multivalue field. Bound the input and expected repetitions.

## Filter

```spl
| regex user="^[a-z][a-z0-9._-]{2,31}$"
```

To retain non-matches, negate the field name according to supported `regex` syntax and verify the treatment of null fields.

## Redact Search Results

```spl
| rex mode=sed field=_raw "s/(token=)[^& ]+/\1REDACTED/g"
```

This changes the search result field, not the already indexed raw data or all other access paths. Prevent sensitive ingestion when possible.

## Performance And Safety

- Filter events before applying regex.
- Apply regex to a narrow field instead of `_raw` when possible.
- Anchor and use explicit character classes.
- Avoid nested ambiguous quantifiers and broad greedy captures.
- Test empty, malformed, very long, and adversarial strings.
- Promote stable shared extractions into governed configuration.

## Debug Pattern

```spl
| rex field=_raw "your-pattern"
| eval extraction_state=if(isnull(new_field),"miss","match")
| stats count values(_raw) AS examples BY extraction_state
```

Limit examples before sharing them; raw data may contain sensitive values.

