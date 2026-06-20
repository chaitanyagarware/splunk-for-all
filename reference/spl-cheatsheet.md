# SPL Cheat Sheet

Use this as a recall aid after reading the curriculum. Replace example index and sourcetype names with authorized values from your environment.

## Search Shape

```spl
index=<index> sourcetype=<sourcetype> <selective terms> earliest=<time>
| <streaming work>
| <transforming work>
| <presentation>
```

## Retrieve And Inspect

```spl
index=web sourcetype=access_combined status>=500 earliest=-15m
| head 20
| table _time host source sourcetype status uri _raw
```

```spl
index=web sourcetype=access_combined earliest=-24h
| fieldsummary
```

```spl
index=web sourcetype=access_combined
| top limit=10 status showperc=true
```

## Boolean And Comparison

```spl
index=auth (action=failure OR action=blocked) NOT user="health-check"
```

```spl
| where status>=500 AND response_time>1
```

```spl
| where src_ip=dest_ip OR match(user,"^svc_")
```

Use parentheses. `search` uses search syntax; `where` evaluates expressions and supports field-to-field comparison.

## Fields And Types

```spl
| fields _time host uri status response_time
| rename response_time AS latency_seconds
```

```spl
| eval latency_ms=round(1000*response_time,0),
       user=lower(trim(user)),
       src=coalesce(src_ip,client_ip,src)
```

```spl
| eval numeric_value=tonumber(value), text_value=tostring(value), type=typeof(value)
```

## Conditional Logic And Nulls

```spl
| eval severity=case(status>=500,"critical",
                     status>=400,"warning",
                     isnull(status),"unknown",
                     true(),"normal")
```

```spl
| eval region=coalesce(region,site,"unmapped")
| fillnull value=0 error_count
```

Fill only when zero has the correct meaning.

## Aggregate

```spl
| stats count AS events dc(user) AS users
        values(action) AS actions latest(status) AS latest_status BY host
```

```spl
| stats count AS requests count(eval(status>=500)) AS errors BY host
| eval error_rate=round(100*errors/requests,2)
```

```spl
| eventstats avg(response_time) AS average stdev(response_time) AS sigma BY host
| eval z=if(sigma>0,(response_time-average)/sigma,null())
```

```spl
| sort 0 host _time
| streamstats window=5 avg(response_time) AS rolling_average BY host
```

## Time

```spl
index=web earliest=-7d@d latest=@d
| timechart span=1h count AS requests count(eval(status>=500)) AS errors
```

```spl
| bin _time span=15m
| stats count BY _time host
```

```spl
| eval formatted=strftime(_time,"%Y-%m-%d %H:%M:%S %Z"),
       parsed=strptime(timestamp,"%Y-%m-%dT%H:%M:%SZ")
```

## Extract And Parse

```spl
| rex field=_raw "request_id=(?<request_id>[A-Za-z0-9-]+)"
```

```spl
| spath path=service output=service
| spath path=errors{} output=errors
```

```spl
| extract pairdelim=" " kvdelim="="
```

## Multivalue

```spl
| eval roles=split(role_csv,","), roles=mvmap(roles,lower(trim(roles)))
| eval role_count=mvcount(mvdedup(roles))
```

```spl
| eval event_key=coalesce(request_id,md5(_raw))
| mvexpand roles
| stats dc(event_key) AS events BY roles
```

Expansion changes the row count; preserve the original analytical unit.

## Enrich

```spl
| lookup asset_inventory host OUTPUTNEW owner environment criticality
| fillnull value="unmapped" owner environment criticality
```

Check lookup match rate:

```spl
| eval lookup_matched=if(isnotnull(owner),1,0)
| stats count AS events sum(lookup_matched) AS matched
| eval match_rate=round(100*matched/events,2)
```

## Correlate Without `join`

```spl
(index=auth action=failure) OR (index=auth action=success)
| stats count(eval(action="failure")) AS failures
        count(eval(action="success")) AS successes BY user src_ip
| where failures>=5 AND successes>0
```

## `tstats`

```spl
| tstats count WHERE index=web BY sourcetype host
```

```spl
| tstats summariesonly=true count
    FROM datamodel=Authentication.Authentication
    WHERE Authentication.action=failure
    BY _time span=15m Authentication.user
| rename Authentication.* AS *
```

Data model names and fields are environment-specific. Validate summary coverage.

## Present

```spl
| sort 0 - errors
| head 20
| table host requests errors error_rate p95
```

```spl
| chart count OVER host BY status limit=10 useother=true
```

## Generate Test Data

```spl
| makeresults count=10
| streamstats count AS n
| eval _time=now()-n*60, status=if(n%4=0,500,200), host="demo-".(n%2)
| timechart span=1m count BY status
```

`makeresults` is excellent for testing logic without production data.

## Performance Checklist

- [ ] Explicit indexes, sourcetypes, and bounded time.
- [ ] Selective filters before regex, expansion, or centralized commands.
- [ ] Only necessary fields cross expensive stages.
- [ ] High-cardinality `BY` fields are bounded.
- [ ] `stats` considered before `transaction`, `join`, or repeated subsearches.
- [ ] Result and command limits understood.
- [ ] Job Inspector evidence captured.
- [ ] Faster version proven semantically equivalent.

Related: [command map](command-map.md) · [time reference](time-reference.md) · [regex reference](regex-reference.md)

