# Regex, JSON, And Multivalue Data

## Learning Objectives

- Extract structured fields from text and JSON.
- Expand, combine, and aggregate multivalue fields.
- Avoid silent row multiplication and regex fragility.

## Regex Extraction

Use `rex` for exploratory extraction:

```spl
| rex field=uri "^(?<path>[^?]+)(?:\?(?<query_string>.*))?$"
```

Use `regex` to filter with a regular expression:

```spl
| regex user="^[a-z][a-z0-9._-]{2,31}$"
```

These commands have different purposes. A regex should be anchored when possible, tested against adversarial and malformed input, and replaced by a shared extraction when it becomes production knowledge.

## Structured JSON

Given JSON in `_raw`:

```json
{"service":"checkout","duration_ms":842,"labels":{"region":"us-central"},"errors":["timeout","retry"]}
```

Extract paths explicitly:

```spl
| spath path=service output=service
| spath path=duration_ms output=duration_ms
| spath path=labels.region output=region
| spath path=errors{} output=errors
| eval duration_ms=tonumber(duration_ms)
```

Automatic extraction is convenient but can produce many fields and naming surprises on variable payloads. Explicit paths make production searches reviewable.

## Multivalue Fundamentals

```spl
| eval roles=split(role_csv, ",")
| eval roles=mvmap(roles, lower(trim(roles)))
| eval unique_roles=mvdedup(roles), role_count=mvcount(unique_roles)
```

Useful functions include `mvappend`, `mvcount`, `mvdedup`, `mvfilter`, `mvfind`, `mvindex`, `mvjoin`, `mvmap`, `mvrange`, `mvsort`, and `mvzip`.

## Expansion Changes Cardinality

```spl
| mvexpand errors
| stats count BY service errors
```

`mvexpand` creates one result per value. Counts after expansion describe expanded values, not original events. Preserve an event identifier and be explicit about the unit:

```spl
| eval event_key=coalesce(request_id, md5(_raw))
| mvexpand errors
| stats dc(event_key) AS affected_events count AS error_occurrences BY errors
```

Hashing `_raw` is only an illustrative fallback and is not a guaranteed unique event identifier.

## Pair Related Arrays

If two arrays are positionally related, zip before expansion:

```spl
| eval pair=mvzip(item_ids, quantities, "::")
| mvexpand pair
| eval item_id=mvindex(split(pair, "::"), 0),
       quantity=tonumber(mvindex(split(pair, "::"), 1))
```

Confirm both arrays have equal length; otherwise positional meaning may be lost.

## `foreach` And Dynamic Fields

```spl
| foreach latency_* [ eval <<FIELD>>=round('<<FIELD>>', 2) ]
```

Dynamic field operations can save repetition but hide behavior. Use a narrow wildcard and document the expected field set.

## Production Notes

- Prefer native structured extraction and stable schemas over regex on arbitrary JSON.
- Bound multivalue size. User-controlled arrays can create expensive expansion.
- Decide whether the analytical unit is event, entity, array value, or pair.
- Preserve source evidence until normalization has been validated.

## Practice

Create synthetic JSON with an order ID and an array of items containing SKU and price. Extract the items, expand them, and calculate order revenue without double-counting the order.

## Official Resources

- [`spath` command](https://help.splunk.com/en/splunk-enterprise/search/spl-search-reference/9.4/search-commands/spath)
- [Multivalue eval functions](https://help.splunk.com/en/splunk-enterprise/search/spl2-search-reference/evaluation-functions/multivalue-eval-functions)

Previous: [Enrichment and correlation](04-enrichment-and-correlation.md) · Next: [Search products](../03-knowledge/01-search-products.md)

