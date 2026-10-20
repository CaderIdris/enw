import datetime as dt
import re
from typing import cast

from ._type_check import (
    _descriptive_regex,
    _non_descriptive_regex,
    parse_time_string,
    NAMEDateTimeEnum
)

def get_timedelta(string: str) -> dt.timedelta:
    """Get timedelta from a NAME time interval string.

    Parameters
    ----------
    string : str
        NAME time interval string.

    Returns
    -------
    dt.timedelta
        Python representation of time interval.

    """
    time_interval_type = parse_time_string(string)
    if time_interval_type == NAMEDateTimeEnum.Descriptive:
        vals = cast(
            "re.Match",
            re.search(_descriptive_regex, string)
        ).groupdict()
    elif time_interval_type == NAMEDateTimeEnum.NonDescriptive:
        vals = cast(
            "re.Match",
            re.search(_non_descriptive_regex, string)
        ).groupdict()
    else:
        msg = f"{string} is not a valid Time Interval string."
        raise ValueError(msg)
    none_keys = [k for k, v in vals.items() if v is None]
    for k in none_keys:
        vals.pop(k)

    typed_vals = {
        k: int(v)
        for k, v in vals.items()
        if v is not None and k != "minus"
    }
    time_delta = dt.timedelta(
        days=typed_vals.get("days", 0),
        hours=typed_vals.get("hours", 0),
        minutes=typed_vals.get("minutes", 0),
        seconds=typed_vals.get("seconds", 0),
        milliseconds=typed_vals.get("ms", 0)
    )
    if vals.get("minus") == "-":
        time_delta = -time_delta
    return time_delta


def dt_to_name_string(datetime: dt.datetime) -> str:
    """"""
    return datetime.strftime("%d/%m/%Y %H:%M:%S")

