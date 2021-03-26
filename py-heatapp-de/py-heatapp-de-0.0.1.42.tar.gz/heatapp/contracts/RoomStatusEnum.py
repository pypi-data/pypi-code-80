from .enum import Enum

class RoomStatusCode(Enum):
    """Enum containing roomstatus codes for different scenes for heatapp heating system"""
    41 = "Party"
    99 = "Problem"
    127 = "Holiday"
    132 = "Standby"
    130 = "Go"
    46  = "Boost"
    122 = "Schedule"
    51  = "Manual"
