from dataclasses import dataclass


@dataclass(frozen=True)
class PercentageFocus:
    """Percentage up per share to consider purchasing"""
    percentage_up: float

    """Percentage up per share total to decide to sell"""
    percentage_total: float

    """If should sell at the end of day"""
    sell_at_end_of_day: bool
