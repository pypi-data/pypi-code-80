import enum

import pydantic


class Interval(str, enum.Enum):
    i1m = "1m"
    i2m = "2m"
    i5m = "5m"
    i15m = "15m"
    i30m = "30m"
    i60m = "60m"
    i90m = "90m"
    i1h = "1h"
    i1d = "1d"
    i5d = "5d"
    i1wk = "1wk"
    i1mo = "1mo"
    i3mo = "3mo"


class Range(str, enum.Enum):
    r1d = "1d"
    r5d = "5d"
    r1mo = "1mo"
    r3mo = "3mo"
    r6mo = "6mo"
    r1y = "1y"
    r2y = "2y"
    r5y = "5y"
    r10y = "10y"
    rytd = "ytd"
    rmax = "max"


class Parameters(pydantic.BaseModel):
    includePrePost: bool
    interval: Interval
    range: Range
