# Search Fundamentals

## Learning Objectives

- Write a selective base search.
- Control time and understand the SPL pipeline.
- Inspect events before transforming them.

## Search Anatomy

```spl
index=tutorial sourcetype="splunk_for_all:web" status>=500 earliest=-24h
| fields _time host uri status response_time
| sort - _time
| head 20
```

The first line retrieves events. Pipes pass results through commands. Search terms before the first pipe should use indexed metadata and restrictive predicates where possible. The time picker can set the range; inline `earliest` and `latest` modifiers make shared examples explicit.

## Boolean Logic

`NOT` is evaluated before `OR`, and `OR` before implicit `AND` in search expressions. Parentheses make intent reviewable:

```spl
index=tutorial sourcetype="splunk_for_all:web"
(status=500 OR status=503) NOT uri="/health"
```

Quoted values preserve spaces and special characters. Field names and values have case behavior that varies by context; do not rely on accidental casing.

## Time

```spl
index=tutorial sourcetype="splunk_for_all:web" earliest=-7d@d latest=@d
```

This requests the seven complete calendar days before today. Useful forms include `-15m`, `-24h`, `@d`, `-1d@d`, and absolute timestamps. Relative time uses the search user's or system's configured time context. Daylight-saving boundaries mean a calendar day is not always 24 hours.

## Inspect Before You Transform

```spl
index=tutorial sourcetype="splunk_for_all:web" earliest=-24h
| head 20
| table _time _raw host source sourcetype
```

Then inspect field coverage:

```spl
index=tutorial sourcetype="splunk_for_all:web" earliest=-24h
| stats count AS events
        count(status) AS with_status
        count(response_time) AS with_response_time
```

An average over 60% field coverage may tell a different story than an average over all requests.

## Pipeline Debugging

Build in stages. After each pipe, verify row count, fields, and meaning. Temporarily add `| head 100` after a selective base search while developing, but remove it before calculating production statistics because it changes the population.

Useful inspection commands:

```spl
index=tutorial sourcetype="splunk_for_all:web"
| fieldsummary
```

```spl
index=tutorial sourcetype="splunk_for_all:web"
| top limit=10 status showperc=true
```

```spl
index=tutorial sourcetype="splunk_for_all:web"
| rare limit=10 uri
```

## Null Is Not Zero

A missing field, an empty string, the number zero, and the text `"0"` are different states. Treating all as zero can conceal parsing failures.

```spl
index=tutorial sourcetype="splunk_for_all:web"
| eval response_state=case(
    isnull(response_time), "missing",
    response_time=0, "zero",
    true(), "present")
| stats count BY response_state
```

## Practice

Using the web dataset, find the 10 most recent non-health-check requests with a status of 400 or greater. Return only time, client IP, method, URI, status, and host.

## Checkpoint

Explain why `index=tutorial error` and `index=tutorial status>=500` are not equivalent. One searches for a term in searchable event content; the other applies a field predicate and depends on field extraction and typing.

## Official Resources

- [Search Manual](https://help.splunk.com/en/splunk-enterprise/search/search-manual)
- [Search Reference](https://help.splunk.com/en/splunk-enterprise/search/spl-search-reference)

Previous: [Getting data in](../01-foundations/03-getting-data-in.md) · Next: [Fields and filtering](02-fields-and-filtering.md)

