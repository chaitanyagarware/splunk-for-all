# Knowledge Objects

## Learning Objectives

- Explain how search-time knowledge forms a semantic layer.
- Organize fields, aliases, calculated fields, lookups, event types, tags, and macros.
- Manage ownership, permissions, dependencies, and lifecycle.

## The Semantic Layer

Raw data is evidence. Knowledge objects give it reusable meaning without rewriting the source event. A healthy layer makes equivalent concepts discoverable while preserving provenance.

| Object | Purpose | Example |
|---|---|---|
| Field extraction | Parse a value | Extract `request_id` from text |
| Field alias | Expose an existing field under a canonical name | `clientip` -> `src_ip` |
| Calculated field | Derive a value with eval logic | `duration_ms=duration*1000` |
| Lookup | Add maintained context | IP -> owner and asset tier |
| Event type | Name a reusable event search | `failed_authentication` |
| Tag | Classify field values or event types | `authentication`, `error` |
| Macro | Parameterize reusable SPL | `` `business_hours(2)` `` |
| Workflow action | Link a field to an investigation action | Open asset record |

## Ordering And Precedence

Search-time operations happen in an ordered sequence and configuration is merged across app, user, and system contexts. A field used by a lookup or calculated field must exist at the correct stage. Use the platform's configuration inspection tools to see the effective result rather than guessing which file won.

## Field Normalization

Use aliases when the correct value already exists under another name. Use calculated fields when transformation is needed. Avoid multiple objects writing contradictory values to the same canonical field.

Example normalization logic:

```spl
| eval user=lower(coalesce(user, user_name, principal)),
       src=coalesce(src, src_ip, client_ip)
```

During development, measure coverage and disagreements before turning this into shared knowledge.

## Macros

Macros can hide repetitive or sensitive implementation details, but hidden SPL is still code. Name parameters, validate arguments, document expansion, scope permissions, and avoid accepting untrusted text into search fragments.

Illustrative definition:

```text
Name: web_errors(2)
Arguments: index_name, minutes
Definition: index=$index_name$ sourcetype=access_combined status>=500 earliest=-$minutes$m
```

Call:

```spl
`web_errors(web,15)`
| stats count BY host
```

Macro argument syntax and validation must be tested in your version. Do not use this example as a substitute for permission and injection review.

## Governance

Every shared object should have:

- A stable name and description.
- Team ownership rather than a departing individual.
- Intended app context and minimum sharing.
- Dependencies and compatible sourcetypes.
- Example use and expected field coverage.
- A test and a deprecation path.

Export shared content as an app with version control when possible. Review private objects before users leave and prevent duplicate names that differ only by capitalization or app context.

## Practice

Choose one common concept, such as user identity or application name. Inventory every source field that represents it, define precedence, retain the original fields, and write a coverage query that reports conflicts.

## Official Resources

- [Knowledge Manager Manual](https://help.splunk.com/en/splunk-enterprise/manage-knowledge-objects/knowledge-management-manual)
- [Search-time operation sequence](https://help.splunk.com/en/splunk-enterprise/manage-knowledge-objects/knowledge-management-manual/9.4/get-started-with-knowledge-objects/the-sequence-of-search-time-operations)

Previous: [Search products](01-search-products.md) · Next: [Data models and tstats](03-data-models-and-tstats.md)

