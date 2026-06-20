# Splunk Architecture

## Learning Objectives

- Describe collection, indexing, and search roles.
- Follow a distributed search from request to result.
- Separate scaling, availability, and disaster-recovery concerns.

## Core Components

| Component | Primary responsibility |
|---|---|
| Universal Forwarder | Lightweight collection and forwarding |
| Heavy Forwarder | Full Splunk instance used when richer parsing/routing is required |
| Indexer | Parse incoming data when applicable, create searchable indexes, answer search peers |
| Search Head | Coordinate searches and host user-facing knowledge objects |
| Cluster Manager | Coordinate an indexer cluster |
| Search Head Cluster Deployer | Distribute configuration to a search head cluster |
| Deployment Server | Manage forwarder app configuration in suitable Enterprise deployments |
| License Manager | Manage license pools and usage in applicable deployments |
| Monitoring Console | Observe Splunk deployment health |

Names, responsibilities, and customer-managed boundaries differ across deployment types. In Splunk Cloud Platform, Splunk manages substantial platform infrastructure while customers retain responsibilities such as data, access, content, and integration design.

## Data Path

```text
producer -> forwarder/input -> receiving tier -> parsing -> index buckets
                                                        -> searchable events
```

Data is generally acknowledged and forwarded in streams. During indexing, metadata and compressed raw data are written into buckets that progress through lifecycle stages. Retention is governed by index configuration and available storage, not by deleting individual matching events as a normal workflow.

## Search Path

```text
user -> search head -> search peers -> partial results -> search head -> user/action
```

The search head parses and plans the search. Distributable work can run on indexers close to the data. Centralized work runs on the search head after results move across the network. This is why filtering early and understanding command types matters.

### Streaming And Transforming

- A streaming command handles events as they flow, such as `eval`, `fields`, and many uses of `rex`.
- A transforming command converts events into a results table, such as `stats`, `chart`, and `timechart`.
- Some commands centralize results or have limits; verify command behavior in Search Reference rather than memorizing a simplistic label.

## Deployment Patterns

### Single Instance

One Enterprise instance performs collection, indexing, search, and management. Good for an isolated lab, not a production reference architecture.

### Distributed Enterprise

Roles are separated. Indexer clustering can provide data availability and search affinity. Search head clustering can provide a coordinated search tier. Capacity planning must consider ingestion, search concurrency, retention, replication, and workload shape.

### Splunk Cloud Platform

A managed service with defined supported workflows, service limits, and responsibility boundaries. Do not assume filesystem or command-line access described for self-managed Enterprise exists in Cloud.

## Availability Is Not Backup

Replication protects service continuity from certain component failures. It does not automatically protect against every operator error, malicious change, configuration loss, or region-level event. Define recovery objectives, configuration backup, restore testing, and data archive strategy separately.

## Practice

Draw your environment and label:

1. Data ownership and transport trust boundaries.
2. Where timestamps and event boundaries are decided.
3. Where data is stored and for how long.
4. Where user knowledge objects live.
5. Which component failure each availability control addresses.

## Official Resources

- [Splunk Validated Architectures](https://www.splunk.com/en_us/pdfs/technical-briefs/splunk-validated-architectures.pdf)
- [Distributed deployment documentation](https://help.splunk.com/en/splunk-enterprise/administer/distributed-deployment-manual)

Previous: [What is Splunk?](01-what-is-splunk.md) · Next: [Getting data in](03-getting-data-in.md)

