# Advanced SPL Patterns

## Learning Objectives

- Build cohorts, funnels, sessions, baselines, and sequence-aware analysis.
- Preserve the analytical unit and ordering assumptions.
- Recognize when an elegant query still makes a weak claim.

## Funnel Analysis

```spl
index=app sourcetype=events earliest=-24h
| stats min(eval(if(action="view", _time, null()))) AS viewed
        min(eval(if(action="cart", _time, null()))) AS carted
        min(eval(if(action="purchase", _time, null()))) AS purchased
        BY session_id
| eval reached_view=if(isnotnull(viewed),1,0),
       reached_cart=if(isnotnull(carted) AND carted>=viewed,1,0),
       reached_purchase=if(isnotnull(purchased) AND purchased>=carted,1,0)
| stats sum(reached_view) AS viewed sum(reached_cart) AS carted
        sum(reached_purchase) AS purchased
```

This uses first occurrence times. Real funnels must define repeated steps, session expiration, cross-device identity, late events, and whether intervening actions invalidate progression.

## Sessionization With Gaps

```spl
index=app sourcetype=events earliest=-4h
| sort 0 user _time
| streamstats current=f last(_time) AS previous_time BY user
| eval new_session=if(isnull(previous_time) OR _time-previous_time>1800,1,0)
| streamstats sum(new_session) AS session_number BY user
| stats min(_time) AS start max(_time) AS end count AS events
        values(action) AS actions BY user session_number
| eval duration=end-start
```

Sorting and memory cost grow with data. Prefer an existing reliable session ID. `values(action)` does not preserve sequence; use it as a set, not a path.

## Sequence-Aware Authentication Pattern

```spl
index=auth sourcetype=auth_events earliest=-1h
| sort 0 user src_ip _time
| streamstats window=10 current=f count(eval(action="failure")) AS prior_failures
        time_window=10m BY user src_ip
| where action="success" AND prior_failures>=5
```

Validate the exact `streamstats` behavior and limits in your Splunk version. This pattern expresses sequence more directly than unordered aggregation, but attackers, shared IPs, retries, and ingestion order still affect interpretation.

## Dynamic Baseline

```spl
index=web sourcetype=access_combined earliest=-8d@h
| bin _time span=1h
| stats count AS requests BY host _time
| eventstats avg(requests) AS baseline stdev(requests) AS sigma BY host
| eval deviation=if(sigma>0,(requests-baseline)/sigma,null())
| where abs(deviation)>=3
```

This pedagogical baseline mixes current and historical points and ignores time-of-week seasonality. A production baseline should exclude evaluation periods where appropriate, handle missing buckets, and be validated against operationally relevant anomalies.

## Cohort Retention

```spl
index=app action IN (signup,login) earliest=-90d@d
| stats min(eval(if(action="signup",_time,null()))) AS signup_time
        values(eval(if(action="login",_time,null()))) AS login_times BY user
| mvexpand login_times
| eval cohort=strftime(signup_time,"%Y-%m"),
       age_days=floor((login_times-signup_time)/86400)
| where age_days>=0
| stats dc(user) AS active_users BY cohort age_days
```

The denominator for retention should be cohort size, not total active users. Add it deliberately and decide how identity deletion and late signups are handled.

## Summary Indexing Pattern

Repeated expensive searches can write scheduled aggregates to a summary index, then dashboards query the smaller result. Design idempotency, backfill, late data, ownership, retention, and duplicate prevention before enabling collection. Acceleration features may be more suitable depending on the workload.

## Practice

Implement one pattern against synthetic data, then write a paragraph titled “What this does not prove.” Advanced SPL is as much about claim boundaries as command fluency.

## Official Resources

- [`streamstats` command](https://help.splunk.com/en/splunk-enterprise/search/spl-search-reference/9.4/search-commands/streamstats)
- [Summary indexing](https://help.splunk.com/en/splunk-enterprise/manage-knowledge-objects/knowledge-management-manual/9.4/use-data-summaries-to-accelerate-searches/use-summary-indexing-for-increased-reporting-efficiency)

Previous: [Performance](01-performance.md) · Next: [API and automation](03-api-and-automation.md)

