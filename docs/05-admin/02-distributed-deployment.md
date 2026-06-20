# Distributed Deployment And Scaling

## Learning Objectives

- Separate ingestion, indexing, search, management, and availability roles.
- Reason about capacity using workload dimensions.
- Plan topology changes without treating a diagram as a universal recipe.

## Workload Dimensions

Sizing is not based on daily ingest alone. Capture:

- Ingest rate, peaks, event size, compression, and parsing complexity.
- Search concurrency, time ranges, command shapes, and scheduled-search bursts.
- Retention by index, replication/search factors, and storage performance.
- Knowledge bundles, data-model acceleration, and summary workloads.
- Availability objectives, maintenance strategy, and recovery objectives.
- Growth, backfill, late data, and headroom.

Use official sizing guidance and qualified architecture review for production. Sample node counts from a tutorial are not a design.

## Indexer Clustering

An indexer cluster coordinates replicated bucket copies across peers. Important concepts include replication factor, search factor, searchable copies, manager coordination, site awareness, and bucket fix-up.

Replication consumes network and storage and provides defined availability properties. It does not eliminate the need for recovery planning or configuration backups.

## Search Head Clustering

A search head cluster provides a coordinated set of search heads with replicated runtime state and a deployer for app distribution. Design includes member count, captain behavior, artifact replication, load balancing, deployer workflow, and application compatibility.

Do not edit member-local content casually. Use supported cluster workflows and understand which objects replicate.

## Forwarder Management

A deployment server can distribute apps to compatible forwarders in self-managed Enterprise. Server classes should be mutually understandable, testable, and based on stable targeting. A broad target rule can deploy an input twice or restart thousands of clients.

Use staged rollout groups:

```text
development -> canary -> small production cohort -> broad rollout
```

Measure phone-home, deployment success, input duplication, and data health after each stage.

## Upgrade Planning

1. Read version-specific release notes, compatibility, and known issues.
2. Inventory apps, add-ons, APIs, authentication, and unsupported customizations.
3. Back up configuration and validate restore procedures.
4. Test representative ingestion, search, alerts, dashboards, and integrations.
5. Follow topology-specific order and maintenance guidance.
6. Define go/no-go checks and rollback boundaries.
7. Monitor cluster health, data delay, skipped searches, and user workflows.

## Cloud Responsibility Boundary

Splunk Cloud Platform is managed, but customers still design sources, semantics, RBAC, knowledge content, detection tuning, integrations, and operational ownership. Use supported Cloud workflows rather than transferring self-managed filesystem instructions.

## Practice

Create a capacity worksheet for an imaginary 500 GB/day deployment. Do not choose hardware. List every missing variable that prevents a responsible node count. This exercise teaches what a sizing conversation must discover.

## Official Resources

- [Indexer and indexer cluster management](https://help.splunk.com/en/splunk-enterprise/administer/manage-indexers-and-indexer-clusters)
- [Search head clustering](https://help.splunk.com/en/splunk-enterprise/administer/distributed-search)
- [Splunk Validated Architectures](https://www.splunk.com/en_us/pdfs/technical-briefs/splunk-validated-architectures.pdf)

Previous: [Configuration](01-configuration.md) · Next: [Security and RBAC](03-security-and-rbac.md)

