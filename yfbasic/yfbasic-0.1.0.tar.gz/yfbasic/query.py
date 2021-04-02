import os
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, Generator, Iterable

import requests as _requests

from yfbasic.models import chart
from yfbasic.models.parameters import Interval, Parameters, Range

BASE_URL = "https://query1.finance.yahoo.com/"


def query(
    symbol: str,
    range: Range = Range.r5d,
    interval: Interval = Interval.i15m,
    include_pre_post: bool = False,
) -> chart.Model:
    """Retrieves and maps trading data from yahoo finance.

    Args:
        symbol: The security to look up data for.
        range: The time range to retrieve data for.
        interval: The granularity of data to retrieve.
        include_pre_post: Whether to include after market data.

    Returns:
        Trading data for the given symbol.
    """
    params: Dict[str, Any] = {}
    params["range"] = range.value
    params["interval"] = interval.value
    params["includePrePost"] = include_pre_post
    _params = Parameters(**params)

    url = f"{BASE_URL}/v8/finance/chart/{symbol}"
    response: _requests.Response = _requests.get(url=url, params=_params.dict())
    data: Dict[str, Any] = response.json()
    return chart.Model(**data)


def query_threaded(
    symbols: Iterable[str],
    range: Range = Range.r5d,
    interval: Interval = Interval.i15m,
    include_pre_post: bool = False,
    workers: int = os.cpu_count() or 1,
) -> Generator[chart.Model, None, None]:
    """Retrieves trading data for symbols simultaneously using threads.

    Args:
        symbols: The securities to look up data for.
        range: The time range to retrieve data for.
        interval: The granularity of data to retrieve.
        include_pre_post: Whether to include after market data.
        workers: How many threads to use.

    Yields:
        Trading data.
    """

    def _query_handler(symbol: str) -> chart.Model:
        return query(
            symbol=symbol,
            range=range,
            interval=interval,
            include_pre_post=include_pre_post,
        )

    with ThreadPoolExecutor(max_workers=workers) as executor:
        for data in executor.map(_query_handler, symbols):
            yield data
