"""Utilities for type checking arguments."""
from enum import StrEnum
from pathlib import Path
import re
from typing import (
    get_args,
    get_origin,
    Literal,
    _LiteralGenericAlias,  #type: ignore[ty:unresolved-import]
    #INFO: I don't know why ty doesn't like this, the underscore maybe?
    # In any case, it does actually exist so I'm ignoring the error.
    TYPE_CHECKING
)

if TYPE_CHECKING:
    from types import UnionType

class NAMEDateTimeEnum(StrEnum):
    """The types of time interval available."""

    Invalid = "Invalid"
    Descriptive = "Descriptive"
    NonDescriptive = "NonDescriptive"
    DateTime = "DateTime"

_non_descriptive_regex = re.compile(
    "^" #INFO: Start of string
    r"\s*" #INFO: Optional spaces
    r"\-{,1}" #INFO: Optional negative sign
    r"\s*" #INFO: Optional spaces
    "(?:" #INFO: Start of number of days
    r"(?:[1-9]\d*|0)d" #INFO: Number of days
    "){,1}" #INFO: End of number of days
    r"\s*" #INFO: Optional spaces
    r"\d{1,}" #INFO: Number of hours
    r"\s*" #INFO: Optional spaces
    ":" #INFO: Separator of hours and minutes
    r"\s*" #INFO: Optional spaces
    r"\d{1,}" #INFO: Number of seconds
    r"\s*" #INFO: Optional spaces
    "(?:" #INFO: Start of number of seconds
    r"\:" #INFO: Separator of minutes and seconds
    r"\s*" #INFO: Optional spaces
    r"\d{1,}" # INFO: Number of seconds
    r"\s*" #INFO: Optional spaces
    "(?:" #INFO: Start of number of milliseconds
    r"\."  #INFO: Separator of seconds and milliseconds
    r"\s*" #INFO: Optional spaces
    r"\d{1,}" #INFO: Number of milliseconds
    "){,1}" #INFO: End of number of milliseconds
    "){,1}" #INFO: End of number of seconds
    r"\s*" #INFO: Optional spaces
    "$" #INFO: End of string
)

_descriptive_regex = re.compile(
    "^" #INFO: Start of string
    r"\s*" #INFO: Optional spaces
    "-{,1}" #INFO: Optional negative sign
    r"\s*" #INFO: Optional spaces
    "(?:" #INFO: Start of time interval
    r"(?:\d*\s*day\s*){,1}" #INFO: Number of days
    r"(?:\d*\s*hr\s*){,1}" #INFO: Number of hours
    r"(?:\d*\s*min\s*){,1}" #INFO: Number of minutes
    r"(?:\d*\s*(?:\.\s*\d*\s*){,1}sec\s*){,1}" #INFO: Number of seconds
    #INFO: and milliseconds
    ")" #INFO: End of time interval
    r"\s*" #INFO: Optional spaces
    "$" #INFO: End of string
)

_datetime_regex = re.compile(
    "^" #INFO: Start of string
    r"\s*" #INFO: Optional spaces
    r"[0-3]\d" #INFO: DD
    r"\s*" #INFO: Optional spaces
    r"\/" #INFO: / Character
    r"\s*" #INFO: Optional spaces
    r"[01]\d" #INFO: MM
    r"\s*" #INFO: Optional spaces
    r"\/" #INFO: / Character
    r"\s*" #INFO: Optional spaces
    r"\d{4}" #INFO: YYYY
    r"\s{1,}" #INFO: Mandatory space between date and time
    r"[0-2]\d" #INFO: HH
    r"\s*" #INFO: Optional spaces
    ":" #INFO: : Character
    r"\s*" #INFO: Optional spaces
    r"[0-5]\d" #INFO: MM
    r"\s*" #INFO: Optional spaces
    "(?:" #INFO: Start of optional seconds block
    ":" #INFO: : Character
    r"[0-5]\d" #INFO: SS
    r"\s*" #INFO: Optional spaces
    "(?:" #INFO: Start of optional centiseconds block
    r"\.\s*\d{2}" #INFO: .CS
    "){,1}" #INFO: End of optional centiseconds block
    "){,1}" #INFO: End of optional seconds block
    r"\s*" #INFO: Optional spaces
    "(?:" #INFO: Start of optional timezone block
    "UTC" # (16)! #INFO: Timezone (UTC only)
    r"\s*" #INFO: Optional spaces
    "(?:" #INFO: Start of optional time offset block
    "[+-]" #INFO: + or - character
    r"\s*" #INFO: Optional spaces
    r"[0-2]\d" #INFO: HH time offset
    r"\s*" #INFO: Optional spaces
    ":" #INFO: : Character
    r"[0-5]\d" #INFO: MM time offset
    "){,1}" #INFO: End of optional time offset block
    "){,1}" #INFO: End of optional timezone block
    r"\s*" #INFO: Optional spaces
    "$" #INFO: End of string
)

_source_strength_regex = re.compile(
    r"^" #INFO: Start of string
    r"\s*" #INFO: Optional spaces
    r"\w+" #INFO: Species name
    r"\s*" #INFO: Optional spaces
    r"(?:" #INFO: Start of compulsory emission strength amount
    r"(?:[1-9]\d*)|0)" #INFO: Left side of decimal point, cannot start with 0
    r"(?:\.\d*){,1}" #INFO: Optional right side of decimal point
    r"\s*" #INFO: Optional spaces
    r"g/s" #INFO: g/s units
    r"\s*" #INFO: Optional spaces
    r"$" #INFO: End of string
)

def check_path_like(arg_name: str, string: str) -> None:
    """Check is string is path-like.

    Parameters
    ----------
    arg_name : str
        Name of argument. Used when raising error.
    string : str
        The string being tested.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        `string` is not path-like

    """
    try:
        _ = Path(string)
    except TypeError as err:
        msg = f"{arg_name} is not a valid path: {string}"
        raise TypeError(msg) from err


def check_pos_int(arg_name: str, val: int) -> None:
    """Check for positive integer.

    This could be done each time with a single if statement. However,
    wrapping this in a function allows the standardisation of the
    resulting `TypeError` message.

    Parameters
    ----------
    arg_name : str
        Name of the argument being tested. Used when raising error.
    val : int
        Value being tested.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        `val` is not a positive integer.

    """
    if not val > 0:
        msg = f"Expected +ve integer value for {arg_name}. Got {val} instead."
        raise TypeError(msg)


def check_pos_float(arg_name: str, val: float) -> None:
    """Check for positive flaot.

    This could be done each time with a single if statement. However,
    wrapping this in a function allows the standardisation of the
    resulting `TypeError` message.

    Parameters
    ----------
    arg_name : str
        Name of the argument being tested. Used when raising error.
    val : float
        Value being tested.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        `val` is not a positive integer.

    """
    if not val > 0:
        msg = f"Expected +ve float value for {arg_name}. Got {val} instead."
        raise TypeError(msg)



def check_type(
    arg_name: str,
    val: object,
    expected_type: type | tuple[type, ...] | UnionType
) -> None:
    """Check for the type of a value.

    This could be done each time with a single if  isinstance statement.
    However, wrapping this in a function allows the standardisation of the
    resulting `TypeError` message.


    Parameters
    ----------
    arg_name : str
        Name of the argument being tested. Used when raising error.
    val : object
        Value being tested.
    expected_type : type | tuple[type, ...] | UnionType
        The type(s) that `val` is expected to belong to.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        `val` type does not match `expected_type`.

    """
    if not isinstance(val, expected_type):
        msg = f"{arg_name} is not {expected_type}. Is {type(val)}."
        raise TypeError(msg)


def check_literal(
    arg_name: str,
    val: str,
    literal_name: str,
    literal: _LiteralGenericAlias,
) -> None:
    """Check if value belongs in literal type.

    Parameters
    ----------
    arg_name : str
        Name of the argument being tested. Used when raising error.
    val : str
        Value being tested.
    literal_name : str
        Name of the literal type. Used when raising error.
    literal : TypeAliasType
        The Literal type used to determine `val`'s membership of.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        `val` is not a member of `literal`.

    """
    if get_origin(literal) is not Literal:
        msg = f"{literal_name} is not a Literal type."
        raise TypeError(msg)
    if val not in get_args(literal):
        msg = (
            f"{arg_name} is not a member of {literal_name}. Expected one of: "
            f"'{"', '".join(get_args(literal))}'. Got: {val}"
        )
        raise TypeError(msg)


def check_mutually_exclusive(
    first_name: str,
    first_val: str | bool | int | float | dict | None,  #noqa: FBT001
    second_name: str,
    second_val: str | bool | int | float | dict | None  #noqa: FBT001
) -> None:
    """Check two arguments, raise an error if both are set.

    !!! note
        Two positional arguments are type hinted as boolean values.
        This is normally not recommended, but as the "truthyness" of these
        values is not being tested, it can be allowed in this case.

    Parameters
    ----------
    first_name : str
        The name of the first argument.
    first_val : str | bool | int | float | None
        The first value.
    second_name : str
        The name of the second argument.
    second_val : str | bool | int | float | None
        The second value.


    Raises
    ------
    ValueError
        If both values are set.

    """
    if first_val is not None and second_val is not None:
        msg = (
            f"Both {first_name} and {second_name} are set, but these are "
            "mutually exclusive. Unset one value to proceed."
        )
        raise ValueError(msg)


def check_time_interval(arg_name: str, string: str) -> None:
    """Check if the argument is a time interval recognised by NAME.

    Parameters
    ----------
    arg_name : str
        The name of the argument. Used in the error message.
    string : str
        The string to check for a valid time interval.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        The provided string is not a time interval recognised by NAME.

    """
    if parse_time_string(string) in (
        NAMEDateTimeEnum.Invalid,
        NAMEDateTimeEnum.DateTime
    ):
        msg = f"{arg_name} is not a valid time interval recognised by NAME."
        raise ValueError(msg)


def check_datetime(arg_name: str, string: str) -> None:
    """Check if the argument is a datetime recognised by NAME.

    Parameters
    ----------
    arg_name : str
        The name of the argument. Used in the error message.
    string : str
        The string to check for a valid datetime.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        The provided string is not a datetime recognised by NAME.

    """
    if parse_time_string(string) != NAMEDateTimeEnum.DateTime:
        msg = f"{arg_name} is not a valid time interval recognised by NAME."
        raise ValueError(msg)


def check_source_strength(arg_name: str, string: str) -> None:
    """Check if the argument matches the source strength format in NAME.

    Parameters
    ----------
    arg_name : str
        The name of the argument. Used in the error message.
    string : str
        The string to check for a valid source strength.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        The provided string is not a source strength format recognised by NAME.

    """
    if not bool(re.search(_source_strength_regex, string)):
        msg = f"{arg_name} is not a valid source strength recognised by NAME."
        raise ValueError(msg)


OutputColumnF = Literal[
    "across",
    "separate_file",
    "output_format",
    "output_route"
]

def check_output_string_fields(
    arg_name: str,
    string: str,
    output_type: OutputColumnF
) -> None:
    """Check if the argument matches one of the output string formats in NAME.

    Parameters
    ----------
    arg_name : str
        The name of the argument. Used in the error message.
    string : str
        The string to check for a valid output string.
    output_type : OutputColumn
        The format to check for.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        The format string is not a format recognised by NAME.

    """
    check_literal("output_type", output_type, "OutputColumnF", OutputColumnF)
    valid_characters: dict[str, str] = {
        "across": "TSXYZ",
        "separate_file": "TSXYZN",
        "output_format": "IAZF2",
        "output_route": "DSN"
    }
    chars = valid_characters[output_type]
    regex_str = f"^(?:\\s*[{chars}]\\s*){{1,{len(chars)}}}$"
    compiled = re.compile(regex_str)
    if not bool(re.search(compiled, string)):
        msg = (
            f"{arg_name} is not a valid {output_type} format string "
            "recognised by NAME."
        )
        raise ValueError(msg)
    no_spaces = string.replace(" ", "")
    if len(no_spaces) > len(set(no_spaces)):
        msg = f"{arg_name} contains duplicate characters."
        raise ValueError(msg)

OutputColumnPP = Literal[
    "output_format",
    "output_route"
]

def check_output_string_pp(
    arg_name: str,
    string: str,
    output_type: OutputColumnPP
) -> None:
    """Check if the argument matches one of the output string formats in NAME.

    Parameters
    ----------
    arg_name : str
        The name of the argument. Used in the error message.
    string : str
        The string to check for a valid output string.
    output_type : OutputColumn
        The format to check for.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        The format string is not a format recognised by NAME.

    """
    check_literal("output_type", output_type, "OutputColumnPP", OutputColumnPP)
    valid_characters: dict[str, str] = {
        "output_format": "FTP",
        "output_route": "DS"
    }
    chars = valid_characters[output_type]
    regex_str = f"^(?:\\s*[{chars}]\\s*){{1,{len(chars)}}}$"
    compiled = re.compile(regex_str)
    if not bool(re.search(compiled, string)):
        msg = (
            f"{arg_name} is not a valid {output_type} format string "
            "recognised by NAME."
        )
        raise ValueError(msg)
    no_spaces = string.replace(" ", "")
    if len(no_spaces) > len(set(no_spaces)):
        msg = f"{arg_name} contains duplicate characters."
        raise ValueError(msg)


def parse_time_string(string: str) -> NAMEDateTimeEnum:
    """Determine if a string is a time interval recognised by NAME.

    Parameters
    ----------
    string : str
        The string to be parsed.

    Returns
    -------
    NAMEDateTimeEnum
        Which time interval is it?

    """
    if not string.strip() or string.strip() == "-":
        return NAMEDateTimeEnum.Invalid
    is_descriptive = bool(re.search(_descriptive_regex, string))
    if is_descriptive:
        return NAMEDateTimeEnum.Descriptive
    is_non_descriptive = bool(re.search(_non_descriptive_regex, string))
    if is_non_descriptive:
        return NAMEDateTimeEnum.NonDescriptive
    is_datetime = bool(re.search(_datetime_regex, string))
    if is_datetime:
        return NAMEDateTimeEnum.DateTime
    return NAMEDateTimeEnum.Invalid


