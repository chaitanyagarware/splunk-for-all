# SPL Search Cookbook

## Data Inventory

```spl
| tstats count min(_time) AS earliest max(_time) AS latest
    WHERE index=* BY index sourcetype
| convert ctime(earliest) ctime(latest)
| sort index sourcetype
```

This requires broad index visibility and can expose inventory. Narrow `index=*` to the indexes you are authorized to review.

## Source Freshness

```spl
| metadata type=sourcetypes index=tutorial
| eval minutes_since_seen=round((now()-recentTime)/60,1)
| convert ctime(recentTime)
| sort - minutes_since_seen
```

This lists observed sources, not expected sources that never reported.

## Field Coverage

```spl
index=tutorial sourcetype="splunk_for_all:web"
| stats count AS events count(status) AS with_status
        count(response_time) AS with_latency count(request_id) AS with_request_id
| foreach with_* [ eval <<FIELD>>_pct=round(100*'<<FIELD>>'/events,2) ]
```

## Error Rate By Endpoint

```spl
index=tutorial sourcetype="splunk_for_all:web" uri!="/health"
| stats count AS requests count(eval(status>=500)) AS errors
        perc95(response_time) AS p95_seconds BY uri
| where requests>=3
| eval error_rate=round(100*errors/requests,2), p95_seconds=round(p95_seconds,3)
| sort 0 - error_rate - p95_seconds
```

## Compare Current And Previous Period

```spl
index=web sourcetype=access_combined earliest=-2h@h latest=@h
| eval period=if(_time>=relative_time(now(),"-1h@h"),"current","previous")
| stats count AS requests count(eval(status>=500)) AS errors BY period
| eval error_rate=round(100*errors/requests,2)
```

This assumes dispatch near the hour boundary. For scheduled use, anchor exact boundaries and account for ingestion delay.

## Top Error Contribution

```spl
index=web sourcetype=access_combined status>=500 earliest=-24h
| stats count AS errors BY uri
| eventstats sum(errors) AS all_errors
| eval contribution_pct=round(100*errors/all_errors,2)
| sort 0 - errors
| head 20
```

## Authentication Spray Candidate

```spl
index=auth sourcetype=auth_events action=failure earliest=-10m@m latest=@m
| stats count AS failures dc(user) AS targeted_users values(user) AS sample_users
        BY src_ip
| where failures>=10 AND targeted_users>=5
| sort 0 - targeted_users
```

Tune source semantics, thresholds, allowlists, retries, and identities.

## Authentication Failure Then Success

```spl
index=auth sourcetype=auth_events earliest=-30m
| stats count(eval(action="failure")) AS failures
        min(eval(if(action="failure",_time,null()))) AS first_failure
        min(eval(if(action="success",_time,null()))) AS first_success
        values(app) AS apps BY user src_ip
| where failures>=5 AND first_success>first_failure
```

This is aggregate ordering, not a full state machine.

## Completed Order Value

```spl
index=tutorial sourcetype="splunk_for_all:orders" status=completed
| eval order_value=quantity*unit_price
| stats sum(order_value) AS completed_value dc(order_id) AS orders BY region product
| eval completed_value=round(completed_value,2)
| sort region - completed_value
```

## Outlier Context

```spl
index=web sourcetype=access_combined earliest=-24h
| eventstats avg(response_time) AS mean stdev(response_time) AS sigma BY uri
| eval z=if(sigma>0,(response_time-mean)/sigma,null())
| where z>=3
| table _time request_id uri host response_time mean sigma z
```

Small groups, skewed distributions, and nonstationary traffic weaken this simple z-score pattern.

## Lookup Quality

```spl
index=web sourcetype=access_combined earliest=-24h
| lookup asset_inventory host OUTPUTNEW owner criticality
| eval matched=if(isnotnull(owner),1,0)
| stats count AS events sum(matched) AS matched dc(host) AS hosts
| eval match_rate=round(100*matched/events,2)
```

## Scheduled Search Inventory

```spl
| rest /services/saved/searches splunk_server=local
| search is_scheduled=1
| table title eai:acl.app eai:acl.owner disabled cron_schedule alert_type
| sort eai:acl.app title
```

Requires appropriate capabilities; endpoint fields vary by version.

## Accelerated Authentication Count

```spl
| tstats summariesonly=true count AS failures
    FROM datamodel=Authentication.Authentication
    WHERE Authentication.action=failure
    BY _time span=15m Authentication.user Authentication.src
| rename Authentication.* AS *
```

Validate CIM mapping, summary coverage, late data, and normalized values before using this operationally.

