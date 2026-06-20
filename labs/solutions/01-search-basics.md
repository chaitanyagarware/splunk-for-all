# Solution 01: Search Flight School

## 1. Verify The Source

```spl
index=tutorial sourcetype="splunk_for_all:web"
| stats count AS events min(_time) AS earliest max(_time) AS latest
        values(host) AS hosts count(status) AS with_status
        count(response_time) AS with_response_time
| eval status_coverage=round(100*with_status/events,2),
       response_time_coverage=round(100*with_response_time/events,2)
| convert ctime(earliest) ctime(latest)
```

Expected: 36 events and complete coverage if ingestion extracted key-value pairs correctly.

## 2. Inspect Evidence

```spl
index=tutorial sourcetype="splunk_for_all:web" uri!="/health"
| sort 0 - _time
| head 5
| table _time request_id client_ip method uri status response_time host
```

Sorting all events is acceptable for this tiny lab. At scale, use a selective window and consider whether normal reverse-time event order already serves the inspection.

## 3. Classify Status

```spl
index=tutorial sourcetype="splunk_for_all:web"
| eval status_family=case(status>=200 AND status<300,"2xx",
                          status>=400 AND status<500,"4xx",
                          status>=500 AND status<600,"5xx",
                          true(),"other")
| stats count AS requests BY status_family
| eventstats sum(requests) AS all_requests
| eval percentage=round(100*requests/all_requests,2)
| sort status_family
```

`eventstats` retains each family row while adding the denominator.

## 4. Rank Endpoints

```spl
index=tutorial sourcetype="splunk_for_all:web"
| stats count AS requests count(eval(status>=500)) AS errors
        avg(response_time) AS average perc95(response_time) AS p95 BY uri
| eval average=round(average,2), p95=round(p95,2)
| sort 0 - errors - p95
```

The checkout endpoint contains every 5xx event and those events are served by `web-03`. This is concentration evidence, not root-cause proof: the host may be assigned checkout traffic, while the actual fault could be a dependency, deployment, or input artifact.

## Stretch

```spl
index=tutorial sourcetype="splunk_for_all:web"
| eval latency_band=case(response_time<0.25,"fast",
                         response_time<1,"normal",
                         response_time<3,"slow",
                         true(),"very_slow")
| stats count AS requests count(eval(status>=500)) AS errors BY latency_band
| eval error_rate=round(100*errors/requests,2)
```

The association is partly constructed by the dataset and does not establish which condition caused the other.

