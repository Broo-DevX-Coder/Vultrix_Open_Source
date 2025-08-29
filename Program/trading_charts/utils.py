from datetime import datetime
import re
import pyqtgraph as pg
from Styles import QSS_BINANCE_STYLE,binance_charts_theme,GlobalCursor,CandalsChart
from core.utils import TIME_FRAMES_INTERVALS

# Convert timestamp (milliseconds) to human-readable date string
DATE = lambda v: datetime.fromtimestamp(v / 1000).strftime("%Y-%m-%d %H:%M:%S")


class TimeAxis(pg.AxisItem):
    """Custom time axis for pyqtgraph plots"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Initialize base AxisItem

    def tickStrings(self, values, scale, spacing):
        """
        Override default tick labels to display time format.
        :param values: List of tick positions (in ms)
        :param scale: Scale factor for the axis
        :param spacing: Tick spacing
        :return: List of formatted date strings
        """
        out = []
        for v in values:
            try:
                out.append(DATE(v))  # Convert timestamp to date string
            except Exception:
                out.append("")  # Fallback for invalid values
        return out


def to_milliseconds(frame: str):
    """
    Convert a time frame string (e.g., '5min', '1h') into milliseconds.
    :param frame: String containing number and unit (ms, s, min, h, d, w, M)
    :return: Tuple (milliseconds, unit_string)
    """
    # Mapping of units to (milliseconds, short label)
    units = {
        "ms": [1, "ms"],              # milliseconds
        "s": [1000, "s"],             # seconds
        "min": [60000, "m"],          # minutes
        "m": [60000, "m"],          # minutes
        "h": [3600000, "h"],          # hours
        "d": [86400000, "d"],         # days
        "w": [604800000, "w"],        # weeks
        "M": [2592000000, "M"],       # months (approximate)
    }

    # Match pattern like "15min", "1h", "500ms"
    match = re.match(r"(\d+)(ms|s|min|m|h|d|w|M)", frame)
    if not match:
        raise ValueError("The time frame is not correct")

    # Extract numeric value and unit
    value, unit = match.groups()

    # Convert value to milliseconds and return with unit label
    return int(value) * units[unit][0], str(value) + str(units[unit][1])
