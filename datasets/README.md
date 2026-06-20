# Practice Datasets

These files are synthetic and created for this repository. They contain documentation-only IP ranges and fictional identities.

## Field Contracts

### `web_access.log`

Space-delimited events with key-value pairs.

| Field | Type | Meaning |
|---|---|---|
| `_time` | time | ISO 8601 timestamp at event start |
| `client_ip` | string | Documentation-range client address |
| `method` | string | HTTP method |
| `uri` | string | Request path without query parameters |
| `status` | number | HTTP response status |
| `bytes` | number | Response bytes |
| `response_time` | number | Request duration in seconds |
| `host` | string | Synthetic web server name |
| `request_id` | string | Synthetic request identifier |

### `auth_events.csv`

| Field | Type | Meaning |
|---|---|---|
| `timestamp` | time | Event time in UTC |
| `user` | string | Fictional user or service identity |
| `src_ip` | string | Documentation-range source address |
| `action` | string | `success` or `failure` |
| `reason` | string | Authentication result reason |
| `app` | string | Target application |
| `device` | string | Simplified device classification |

### `orders.csv`

| Field | Type | Meaning |
|---|---|---|
| `timestamp` | time | Order event time in UTC |
| `order_id` | string | Synthetic order identifier |
| `customer_id` | string | Synthetic customer identifier |
| `region` | string | Sales region |
| `product` | string | Product family |
| `quantity` | number | Units ordered |
| `unit_price` | number | Price per unit in fictional currency |
| `status` | string | Order lifecycle status |

## Lab Ingestion

In a disposable environment, create or use a `tutorial` index. Upload each file separately and set:

| File | Suggested sourcetype |
|---|---|
| `web_access.log` | `splunk_for_all:web` |
| `auth_events.csv` | `splunk_for_all:auth` |
| `orders.csv` | `splunk_for_all:orders` |

For CSV files, use the preview to confirm header extraction and set `timestamp` as event time. For the web log, verify the ISO timestamp and automatic `key=value` fields. If fields do not appear, use the search-time extraction shown below while learning:

```spl
index=tutorial sourcetype="splunk_for_all:web"
| extract pairdelim=" " kvdelim="="
```

Quotes surrounding URI values may remain depending on sourcetype settings. The included values have no spaces.

## Validation Searches

```spl
index=tutorial sourcetype="splunk_for_all:*"
| stats count min(_time) AS earliest max(_time) AS latest BY sourcetype
| convert ctime(earliest) ctime(latest)
```

Expected event counts:

| Sourcetype | Events |
|---|---:|
| `splunk_for_all:web` | 36 |
| `splunk_for_all:auth` | 30 |
| `splunk_for_all:orders` | 20 |

If counts differ, stop before the labs and investigate duplicate ingestion, event breaking, or header handling.

## Production Warning

Manual upload is only a lab shortcut. Do not reuse it as a production collection plan. See [Getting Data In](../docs/01-foundations/03-getting-data-in.md).

