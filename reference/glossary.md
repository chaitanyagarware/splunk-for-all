# Splunk Glossary

| Term | Plain-language definition |
|---|---|
| App | Package and namespace for configuration, code, and knowledge content |
| Bucket | Physical unit of indexed data that moves through lifecycle stages |
| Capability | Permission controlling an operation or feature |
| CIM | Common Information Model; shared semantic conventions and data models |
| Cluster manager | Component coordinating an indexer cluster |
| Data model | Structured hierarchy of datasets and fields for a domain |
| Deployment server | Enterprise component for distributing apps to compatible forwarders |
| Deployer | Component used to distribute apps to a search head cluster |
| Event | Searchable record, usually retaining raw evidence and time |
| Event type | Named reusable search identifying a category of events |
| Field | Named value associated with an event or result |
| Forwarder | Component that collects and sends data to another Splunk tier |
| Heavy forwarder | Full Splunk instance used for richer forwarding/parsing needs |
| HEC | HTTP Event Collector, an HTTP-based event/metric input mechanism |
| Host | Metadata representing the event-producing host when applicable |
| Index | Logical data store with retention and access behavior |
| Indexer | Component that stores indexed data and serves search work |
| Job Inspector | Interface exposing search execution properties and diagnostics |
| Knowledge bundle | Search knowledge distributed from a search head to peers |
| Knowledge object | Reusable search-time content such as fields, lookups, reports, and alerts |
| Lookup | Enrichment mapping events to maintained contextual data |
| Macro | Named, optionally parameterized SPL expansion |
| Metrics | Numeric measurements organized by time and dimensions |
| Monitoring Console | Splunk interface for deployment health and topology monitoring |
| Search head | Component coordinating search and hosting user knowledge content |
| Search peer | Indexer participating in distributed search |
| SLI | Service-level indicator, a measured aspect of service behavior |
| Source | Metadata identifying where an event originated |
| Sourcetype | Classification describing data format and processing behavior |
| SPL | Search Processing Language used by Splunk Platform searches |
| Summary index | Index containing scheduled aggregate/search results |
| Tag | Label attached to field values or event types for categorization |
| `tstats` | Statistical command operating on eligible indexed fields and data-model summaries |
| Trace | Connected spans representing request flow across components |
| Transforming command | Command that changes events into an aggregate result table |
| Universal forwarder | Lightweight Splunk data collection and forwarding agent |

Product terminology evolves. Prefer the terminology used by the documentation for your installed release while recognizing older names you may encounter.

