from typing import TYPE_CHECKING

from enw.types import (
    DateTime,
    DescriptiveTimeInterval,
    NonDescriptiveTimeInterval,
)

from ._type_check import parse_time_string

if TYPE_CHECKING:
    from enw.types import (
        Switch,
        TimeInterval,
    )

def make_switch(opt: bool) -> Switch:  #noqa: FBT001
    """Get a Switch value from a boolean variable.

    Boolean or "Switch" values in NAME input headers are represented by either
    a 'Yes' or a 'No'. This function takes a boolean variable declared in the
    config file and converts it into a 'Yes' or a 'No' string to be recognised
    by NAME III.

    Parameters
    ----------
    opt : bool
        The boolean value to convert to "Yes" (True) or "No" (False).


    Notes
    -----
    Normally a boolean value shouldn't be used as a positional argument,
    but as it's the only argument and it's type checked, it is safe.
    See [here]( https://adamj.eu/tech/2021/07/10/python-type-hints-how-
    to-avoid-the-boolean-trap/ ) for more.

    Raises
    ------
    ValueError
        If provided argument is not a strict boolean (True/False).
        This provents truthy values from causing unexpected behaviour.
        (e.g. The string "False" is True in Python)


    """
    if not isinstance(opt, bool):
        msg = "Incorrect type provided. Expected bool value."
        raise TypeError(msg)
    return "Yes" if opt else "No"


def make_time_interval(string: str) -> TimeInterval:
    """Determine if a string is a time interval recognised by NAME.

    Parameters
    ----------
    string : str
        The string to be cast to a TimeInterval type.

    Returns
    -------
    TimeInterval
        The string with the appropriate type.

    Raises
    ------
    ValueError
        The string provided is not a valid time interval recognised by NAME.

    """
    interval_type = parse_time_string(string)
    if interval_type == "Descriptive":
        return DescriptiveTimeInterval(string)
    if interval_type == "NonDescriptive":
        return NonDescriptiveTimeInterval(string)
    msg = f"{string} is not a valid time interval."
    raise ValueError(msg)


def make_datetime(string: str) -> DateTime:
    """Determine if a string is a datetime format recognised by NAME.

    Parameters
    ----------
    string : str
        The string to be cast to a DateTime type.

    Returns
    -------
    DateTime
        The string with the appropriate type.

    Raises
    ------
    ValueError
        The string provided is not a valid datetime recognised by NAME.

    """
    interval_type = parse_time_string(string)
    if interval_type == "DateTime":
        return DateTime(string)
    msg = f"{string} is not a valid datetime."
    raise ValueError(msg)
