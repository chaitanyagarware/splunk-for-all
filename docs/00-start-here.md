# Start Here

## Learning Objectives

By the end of this guide, you will be able to choose a learning environment, load the sample data, run a first search, and follow the curriculum without guessing what comes next.

## Choose Your Environment

You need lawful access to a Splunk environment. Common options are:

- A non-production Splunk Enterprise lab you are authorized to administer.
- An organization-provided Splunk Cloud Platform search environment.
- An official trial, workshop, or education environment available in your region.

Licensing, download terms, operating-system support, and trial availability change. Confirm them in [official installation documentation](https://help.splunk.com/en/splunk-enterprise/administer/install-and-upgrade) before installing. Do not expose a lab directly to the internet, reuse production credentials, or ingest private data for practice.

## The Mental Model

Splunk turns machine data into searchable events:

```text
source -> input -> parsing -> index -> search -> knowledge -> action
```

- A **source** is where data originates: file, stream, API, endpoint, or network input.
- A **sourcetype** describes the data format and parsing behavior.
- An **index** is a logical data store with retention and access controls.
- An **event** is a searchable record, normally with `_time`, `_raw`, `host`, `source`, and `sourcetype`.
- SPL is the pipeline language used to retrieve, transform, analyze, and present events.

Keep three questions beside every search: **What data? What time? What decision?**

## Load The Practice Data

The repository includes three synthetic sources:

| File | Suggested sourcetype | Purpose |
|---|---|---|
| `datasets/web_access.log` | `splunk_for_all:web` | HTTP traffic and reliability |
| `datasets/auth_events.csv` | `splunk_for_all:auth` | Authentication investigations |
| `datasets/orders.csv` | `splunk_for_all:orders` | Business analytics |

For a disposable lab, use **Settings > Add Data > Upload**. Preview timestamps and fields before completing ingestion. Use a dedicated `tutorial` index if you can create one; otherwise ask the lab owner which index to use. Detailed steps and field contracts are in [the dataset guide](../datasets/README.md).

> Upload is useful for learning, not a production collection architecture. Production inputs require ownership, parsing tests, capacity planning, security review, and lifecycle decisions.

## Run Your First Search

Replace `tutorial` only if you used another index:

```spl
index=tutorial sourcetype="splunk_for_all:web"
| head 20
| table _time client_ip method uri status bytes response_time host
```

Then answer a question:

```spl
index=tutorial sourcetype="splunk_for_all:web"
| stats count AS requests, avg(response_time) AS avg_seconds BY status
| sort - requests
```

The base search selects events. Each pipe sends results to the next command. `stats` transforms events into one row per status, then `sort` ranks those rows.

## How To Study

Use a 45-minute loop:

1. Read one concept and predict the result of each example.
2. Type the query rather than pasting it.
3. Change one element: time range, grouping field, function, or filter.
4. Explain the result in one sentence without SPL vocabulary.
5. Record one production risk or data-quality assumption.

### Suggested Schedules

| Pace | Commitment | Route |
|---|---:|---|
| Sprint | 2 weeks, 90 min/day | Foundations, SPL, Labs 1-3, cheat sheet |
| Practitioner | 6 weeks, 4 hours/week | Entire analyst path plus one applied track |
| Platform | 8 weeks, 5 hours/week | Full curriculum, admin track, all labs |

## Progress Tracker

- [ ] I can explain index, sourcetype, source, host, event, and field.
- [ ] I can set an intentional time range.
- [ ] I can move between raw events, statistics, and visualization.
- [ ] I can debug a search one pipeline stage at a time.
- [ ] I can identify assumptions and false-positive risks.
- [ ] I can use Job Inspector to reason about performance.
- [ ] I can explain when `stats` is preferable to `transaction` or `join`.
- [ ] I can describe the production data path and ownership boundaries.

## Checkpoint

Without looking back, explain why `index=*` over all time is a poor default. A strong answer covers performance, permissions, relevance, cost, and the fact that broad retrieval hides unclear intent.

## Official Resources

- [Splunk documentation home](https://help.splunk.com/)
- [Search Tutorial](https://help.splunk.com/en/splunk-enterprise/search/search-tutorial)
- [Search Reference](https://help.splunk.com/en/splunk-enterprise/search/spl-search-reference)

Next: [What is Splunk?](01-foundations/01-what-is-splunk.md)

