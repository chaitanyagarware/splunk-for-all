# Test-Driven SPL

SPL is easier to trust when logic is tested against small known inputs before live data.

## Test A Classifier

```spl
| makeresults count=6
| streamstats count AS n
| eval status=mvindex(split("200,201,404,429,500,503",","),n-1)
| eval actual=case(status>=500,"server_error",
                   status>=400,"client_error",
                   status>=200,"success",
                   true(),"other")
| eval expected=mvindex(split("success,success,client_error,client_error,server_error,server_error",","),n-1)
| eval passed=actual=expected
| table status expected actual passed
```

If type coercion is part of the behavior, test it explicitly with `typeof(status)` and `tonumber(status)`.

## Positive, Negative, Boundary, Null

```spl
| makeresults count=5
| streamstats count AS n
| eval response_time=case(n=1,0.999,n=2,1.000,n=3,1.001,n=4,null(),n=5,-1)
| eval actual=if(isnotnull(response_time) AND response_time<1,"good","not_good")
| table n response_time actual
```

Decide whether exactly one second is good, how null is handled, and whether negative latency should be rejected as data quality rather than classified.

## Detection Truth Table

```spl
| makeresults
| eval cases="low_volume:4:1:false,threshold:5:1:true,no_success:8:0:false"
| makemv delim="," cases
| mvexpand cases
| rex field=cases "(?<name>[^:]+):(?<failures>\d+):(?<successes>\d+):(?<expected>true|false)"
| eval actual=if(failures>=5 AND successes>=1,"true","false")
| eval passed=actual=expected
| table name failures successes expected actual passed
```

Add duplicate events, field absence, out-of-order events, source allowlists, and late arrival to a real analytic test suite.

## Test Contract

For reusable SPL, record:

1. Input schema and event unit.
2. Time and ordering assumptions.
3. Expected output schema.
4. Positive, negative, boundary, null, duplicate, malformed, and scale cases.
5. Limits and tolerated approximation.
6. Version and data model dependencies.

