from dataclasses import dataclass

from ctlml_commons.entity.price_window import PriceWindow


@dataclass(frozen=True)
class PriceFocus:
    """Per share price window range"""

    share_price_window: PriceWindow

    """Total lot profit/loss threshold"""
    total_threshold: float

    """Number of periods to consider for purchase decisions"""
    num_periods: int

    """If should sell at the end of day"""
    sell_at_end_of_day: bool
