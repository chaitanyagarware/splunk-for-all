# SPL Command Map

Command behavior can depend on arguments and version. Use [Search Reference](https://help.splunk.com/en/splunk-enterprise/search/spl-search-reference) for exact syntax, limits, and distributability.

| Goal | Reach for | Caution |
|---|---|---|
| Filter retrieved events | Base search, `search`, `where` | Filter early; `where` needs fields already present |
| Select fields | `fields` | Removing a field makes it unavailable later |
| Derive values | `eval` | Types and nulls matter |
| Extract regex fields | `rex` | Narrow input; configure shared fields |
| Parse JSON/XML | `spath`, `xpath` | Explicit paths reduce field explosion |
| Frequency | `top`, `rare` | Understand default limits/percentages |
| Aggregate | `stats` | Non-group/non-aggregate fields disappear |
| Add group stats to events | `eventstats` | Adds repeated values and memory use |
| Running/window stats | `streamstats` | Ordering and windows are semantic inputs |
| Time series | `timechart` | Span and split cardinality matter |
| Cross-tab | `chart` | Wide result sets can grow rapidly |
| Bucket values | `bin`/`bucket` | Boundaries affect interpretation |
| Enrich | `lookup` | Track freshness and unmatched values |
| Event grouping | `transaction` | Expensive; use only for required sequence/group semantics |
| Small right-side correlation | `join` | Subsearch/result limits and row multiplication |
| Precomputed/indexed stats | `tstats` | Only eligible indexed/model fields |
| Metadata inventory | `metadata` | Not a complete substitute for expected-source inventory |
| Remove duplicates | `dedup` | Which event survives depends on order |
| Expand arrays | `mvexpand` | Multiplies rows and changes counting unit |
| Sort | `sort` | Default result behavior and global cost matter |
| Limit | `head`, `tail` | Limiting before aggregation changes population |
| Append results | `append`, `appendcols` | Limits and row alignment can surprise |
| Trend prediction | `predict` | Validate statistical assumptions and suitability |
| Anomalies | `anomalies`, `anomalousvalue` | Statistical oddity is not operational impact |
| REST inventory | `rest` | Requires capability; select endpoints/fields narrowly |
| Test data | `makeresults`, `gentimes` | Label synthetic outputs clearly |

## Transform Boundaries

After a transforming command, pause and inspect the new schema:

```spl
... | stats count AS events latest(_time) AS latest BY host
```

Only `host`, `events`, and `latest` remain. A later reference to `_raw`, `status`, or `_time` will not work unless it was aggregated or grouped.

## Commands That Deserve Extra Review

`join`, `transaction`, `map`, `append*`, unrestricted `rest`, `mvexpand`, global `sort 0`, and custom search commands are not forbidden. They deserve explicit semantics, bounds, limits, permissions, and performance evidence.

## Choosing A Correlation Shape

| Need | Typical shape |
|---|---|
| Events sharing a key in one population | `stats ... BY key` |
| Conditional occurrence of types | `stats count(eval(...)) BY key` |
| Ordered rolling history | Sort plus `streamstats` |
| Maintained small enrichment | `lookup` |
| Bounded event grouping with start/end | `transaction`, after review |
| Accelerated normalized domain | `tstats FROM datamodel=...` |

