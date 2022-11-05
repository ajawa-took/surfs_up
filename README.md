# surfs_up


## Overview

 We seek weather statistics for the months of June and December, aggregated over all years and all weather stations in this dataset.


## Results

![results](/both.png)


- December is slightly colder on average than June.
- In December temperatures vary a bit more than in June.
- The lowest temperature recorded in December is much lower than the lowest ever recorded in June, 56F vs 64F.


## Summary

December is colder; but is it rainier?
These two queries can help you find out!

```
june_results = session.query(Measurement.prcp).filter(extract('month', Measurement.date) == '06').all()
```

```
december_results = session.query(Measurement.prcp).filter(extract('month', Measurement.date) == '12').all()
```
