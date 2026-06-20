# Solution 03: Authentication Investigation

## Data Validation

```spl
index=tutorial sourcetype="splunk_for_all:auth"
| stats count AS events min(_time) AS earliest max(_time) AS latest
        dc(user) AS users dc(src_ip) AS sources values(action) AS actions
        values(reason) AS reasons
| convert ctime(earliest) ctime(latest)
```

## Password Spray

```spl
index=tutorial sourcetype="splunk_for_all:auth" action=failure
| stats count AS failures dc(user) AS targeted_users values(user) AS users
        min(_time) AS first_seen max(_time) AS last_seen BY src_ip
| where failures>=8 AND targeted_users>=5
| convert ctime(first_seen) ctime(last_seen)
```

The expected result is `198.51.100.90`. It distributes failures across nine identities, matching the lab hypothesis.

## Failure Then Success

```spl
index=tutorial sourcetype="splunk_for_all:auth"
| stats count(eval(action="failure")) AS failures
        count(eval(action="success")) AS successes
        min(eval(if(action="failure",_time,null()))) AS first_failure
        max(eval(if(action="failure",_time,null()))) AS last_failure
        min(eval(if(action="success",_time,null()))) AS first_success
        values(app) AS apps values(reason) AS reasons
        BY user src_ip
| where failures>=5 AND successes>=1 AND first_success>first_failure
| convert ctime(first_failure) ctime(last_failure) ctime(first_success)
```

Expected candidates include `svc_backup` and `dave`. The service account has repeated expired-password events followed by valid credentials, a plausible operational repair. Dave has MFA denials and bad passwords followed by success, which deserves deeper identity, device, and network context.

The aggregation does not guarantee an uninterrupted sequence or associate each success with a particular failure. It collapses all events in the selected window. A stateful ordered approach is needed for stricter semantics.

## Data Silence

A simple lab freshness check:

```spl
index=tutorial sourcetype="splunk_for_all:auth"
| stats max(_time) AS latest count AS events
| eval age_seconds=now()-latest
| convert ctime(latest)
```

For fixed historical data this will always be old. In production, compare against source-specific expected cadence and monitor the collection path.

False positives to assess include service-account credential rotation, vulnerability testing, shared NAT, user password managers, identity-provider retry behavior, and support-desk activity. Treat thresholds as starting hypotheses.

