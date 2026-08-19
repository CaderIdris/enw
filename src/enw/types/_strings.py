"""String based types for NAME input blocks."""

class NonDescriptiveTimeInterval(str):
    r"""Represents a string that represents a non-descriptive time interval.

    =={-}{**a**d}HH:MM{:SS{.MS}}==

    The non-descriptive time interval:

    - Can be positive or negative, as indicated by the leading "-"
    - Can have any number of days associated with it, including 0
        - **However, if the number of days is greater than 0, the number cannot
        start with 0**
    - Must have an HH:MM componenent, where HH:MM can both be any positive
    integer value, or 0
        - Therefore, 100:00 and 00:6000 are both valid.
    - Can have an optional :SS component, where SS can be any positive integer
    , or 0
    - Can have an optional .MS component, where MS can be any positive integer
    , or 0

    Assessed using the following regex:

    ``` python title="Non-Descriptive Time Interval Regex"
    re.compile(r"^\s*\-{,1}\s*(?:(?:[1-9]\d*|0)d){,1}\s*\d{1,}\s*:\s*\d{1,}\s*\
    (?:\:\s*\d{1,}\s*(?:\.\s*\d{1,}){,1}){,1}\s*$")
    ```

    ``` python title="Non-Descriptive Time Interval Regex Explained"
    re.compile(
        "^" # (1)!
        r"\s*" # (2)!
        r"\-{,1}" # (3)!
        r"\s*"
        "(?:" # (4)!
        r"(?:[1-9]\d*|0)d" # (5)!
        "){,1}" # (6)!
        r"\s*"
        r"\d{1,}" # (7)!
        r"\s*"
        ":" # (8)!
        r"\s*"
        r"\d{1,}" # (9)!
        r"\s*"
        "(?:"
        r"\:" # (10)!
        r"\s*"
        r"\d{1,}" # (11)!
        r"\s*"
        "(?:"
        r"\."  # (12)!
        r"\s*"
        r"\d{1,}" # (13)!
        "){,1}"
        "){,1}"
        r"\s*"
        "$" # (14)!
    )
    ```

    1. `^` represents the start of the string.
    2. `\s*` represents an optional arbitrary number of whitespace characters.
    3. `\-{,1}` allows for an optional "-" sign, indicating a negative interval
    4. `(?:` indicates the start of a non-capturing group. All non essential
    elements are contained within these groups.
    5. This is the day portion of the time interval. It determines if there is
    an integer value for days and it does not start with a zero if greater than
    0.
    6. `){,1}` indicates the closing of a group. The `{,1}` section indicates
    there can either be 0 or one of the items contained within the group.
    7. The HH component of the timestamp, it can be any valid positive integer
    value, or 0
    8. The ":" in HH:MM
    9. The MM component of the timestamp, it can be any valid positive integer
    value, or 0
    10. The ":" in MM:SS
    11. The optional SS component of the timestamp, it can be any valid
    positive integer value, or 0
    12. The "." in SS.ms
    13. The optional microseconds in the timestamp. It can be any valid
    positive integer value, or 0.
    14. `$` represents the end of the string.

    Valid Examples
    --------

    - 2d45:34:4566.1523
    - 64d00:00
    - 23:23:23.23
    - 600000000:3000000000:455555555555.665738
    - 1d01:01
    - 0d01:01
    - -2d45:34:4566.1523
    - -64d00:00
    - -23:23:23.23
    - -600000000:3000000000:455555555555.665738
    - -1d01:01
    - -0d:01:01

    !!! warning
        Not all of these values have been tested and are instead inferred from
        the NAME literature. Some of these may cause errors, please raise an
        issue if this is the case.

    Invalid Examples
    ------------

    - 01d01:01:01
    - -01d01:01:01
    - BAD VALUE

    """

    __slots__ = ()
#WARN: These examples haven't all been tested.

class DescriptiveTimeInterval(str):
    r"""Represents a string that represents a descriptive time interval.

    =={-}{**a**day}{**b**hr}{**c**min}{**d**{.**e**}sec}==

    The descriptive time interval:

    - Can be positive or negative, as indicated by the leading "-".
    - Can have an optional number of days, hours, minutes, seconds and
    milliseconds
    , but must have at least one.
    - Each time period can only be specified once.

    Assessed using the following regex:

    ``` python title="Descriptive Time Interval Regex"
    re.compile(r"^\s*-{,1}\s*(?:(?:\d*\s*day\s*){,1}(?:\d*\s*hr\s*){,1}\
    (?:\d*\s*min\s*){,1}(?:\d*\s*(?:\.\s*\d*\s*){,1}sec\s*){,1})$")
    ```
    ``` python title="Descriptive Time Interval Regex Explained"
    re.compile(
        "^" # (1)!
        r"\s*" # (2)!
        "-{,1}" # (3)!
        r"\s*"
        "(?:" # (4)!
        r"(?:\d*\s*day\s*){,1}" # (5)!
        r"(?:\d*\s*hr\s*){,1}" # (6)!
        r"(?:\d*\s*min\s*){,1}" # (7)!
        r"(?:\d*\s*(?:\.\s*\d*\s*){,1}sec\s*){,1})" # (8)!
        r"\s*"
        "$" # (9)!
    )
    ```

    1. `^` represents the start of the string.
    2. `\s*` represents an optional arbitrary number of whitespace characters.
    3. `\-{,1}` allows for an optional "-" sign, indicating a negative interval
    4. `(?:` indicates the start of a non-capturing group. All non essential
    elements are contained within these groups.
    5. The number of days in the time interval
    6. The number of hours in the time interval
    7. The number of minutes in the time interval
    8. The number of seconds (and milliseconds) in the time interval
    9. `$` represents the end of the string.

    Valid Examples
    --------------

    - 1 day
    - 1 hr
    - 1 min
    - 1 sec
    - 0.1 sec
    - 1 day 1 hr 1 min 1 sec
    - 1 day 1 hr 1 min 1 . 1 sec
    - -1 day
    - -1 hr
    - -1 min
    - -1 sec
    - -0.1 sec
    - -1 day 1 hr 1 min 1 sec
    - -1 day 1 hr 1 min 1 . 1 sec

    !!! warning
        Not all of these values have been tested and are instead inferred from
        the NAME literature. Some of these may cause errors, please raise an
        issue if this is the case.

    Invalid Examples
    ----------------

    - -
    - 1day2day
    - BAD VALUE

    """

    __slots__ = ()
#WARN: These examples haven't all been tested.

class DateTime(str):
    r"""Represents a string that corresponds to a date and time in NAME.

    ==D/M/Y HH:MM{:SS{.MS}} {TZ {±HH:MM}}==

    A datetime value:

    - States the specific date and time.
    - Has an optional seconds and milliseconds component.
    - Has an optional timezone.
    - Has an optional time offset.

    Assessed using the following regex:

    ``` python title="DateTime Regex"
    re.compile(
        r"^\s*[0-3]\d\s*\/\s*[01]\d\s*\/\s*\d{4}\s{1,}[0-2]\d\s*:\s*[0-5]\d\s*"
        r"(?::[0-5]\d\s*(?:\.\s*\d{2}){,1}){,1}\s*"
        r"(?:UTC\s*(?:[+-]\s*[0-2]\d\s*:\s*[0-5]\d){,1}){,1}\s*$"
    )
    ```

    ``` python title="DateTime Regex Explained"
    re.compile(
        "^" # (1)!
        r"\s*" # (2)!
        r"[0-3]\d" # (3)!
        r"\s*"
        r"\/" # (4)!
        r"\s*"
        r"[01]\d" # (5)!
        r"\s*"
        r"\/"
        r"\s*"
        r"\d{4}" # (6)!
        r"\s{1,}" # (7)!
        r"[0-2]\d" # (8)!
        r"\s*"
        ":" # (9)!
        r"\s*"
        r"[0-5]\d" # (10)!
        r"\s*"
        "(?:" # (11)!
        ":" # (12)!
        r"[0-5]\d" # (13)!
        r"\s*"
        "(?:"
        r"\.\s*\d{2}" # (14)!
        "){,1}" # (15)!
        "){,1}"
        r"\s*"
        "(?:"
        "UTC" # (16)!
        r"\s*"
        "(?:"
        "[+-]" # (17)!
        r"\s*"
        r"[0-2]\d" # (18)!
        r"\s*"
        ":" # (19)!
        r"[0-5]\d" # (20)!
        "){,1}"
        "){,1}"
        r"\s*"
        "$" # (21)!
    )
    ```

    1. `^` represents the start of the string.
    2. `\s*` represents an optional arbitrary number of whitespace characters.
    3. `[0-3]\d` represents the day (DD) component of the date
    (==DD==/MM/YYYY).
    4. `\/` represents the separator between date components
    (DD ==**/**== MM ==**/**== YYYY).
    5. `[01]\d` represents the month (MM) component of the date
    (DD/==MM==/YYYY).
    6. `\d{4}` represents the year (YYYY) component of the date
    (DD/MM/==YYYY==).
    7. `\s{1,}` represents at least 1 whitespace character. A space between the
    date and time is mandatory.
    8. `[0-2]\d` represents the hour (HH) component of the time (==HH==:MM).
    9. `:` represents the separator between hours and minutes (HH ==:== MM).
    10. `[0-5]\d` represents the minute (MM) component of the time (HH:==MM==).
    11. `(?:` indicates the start of a non-capturing group. All non essential
    elements are contained within these groups.
    12. `:` represents the separator between minutes and the optional seconds
    group (HH:MM ==:== SS).
    13. `[0-5]\d` represents the optional seconds (SS) component of the time
    (HH:MM:==SS==).
    14. `\.\s*\d{2}` represents the optional centiseconds (CS) component of the
    time group (HH:MM:SS ==.CS== )
    15. `){,1}` represents an optional group.
    16. `UTC` represents the optional timezone component.
    17. `[+-]` represents the start of the optional time offset.
    18. `[0-2]\d` represents the hour (HH) component of the optional time
    offset (±==HH==:MM).
    19. `:` represents the separator between hours and minutes of the optional
    time offset component.
    20. `[0-5]\d` represents the minute (MM) component of the optional time
    offset (±HH:==MM==)
    21. `$` represents the end of the string.

    Valid Examples
    --------------

    - 01/05/2001 15:30
    - 12/11/1998 21:06:09
    - 21/01/2021 01:02:59.98
    - 31/01/2000 21:30 UTC
    - 28/02/2012 03:04 UTC +01:00
    - 03/06/2016 12:11:20 UTC
    - 09/09/2009 05:21:45 UTC +02:00
    - 11/12/2013 21:54:45.79 UTC
    - 15/01/2004 12:12:12.12 UTC -02:00

    !!! warning
        Not all of these values have been tested and are instead inferred from
        the NAME literature. Some of these may cause errors, please raise an
        issue if this is the case.

    Invalid Examples
    ----------------

    - 1/5/2001 15:30
    - 01/05/01 15:30
    - 01/05/2001 03:30 PM
    - 01/05/2001 3:30 PM
    - 01/05/2001 3:30
    - 01/05/2001
    - 01/05/2001 03
    - 01/05/200115:30
    - 01 05 2001 15 30
    - 01/05/2001 15:30:45.79 U T C
    - 01/05/2001 15:30 UTC ±01:00
    - BAD VALUE

    """

    __slots__ = ()
#WARN: These examples haven't all been tested.

class SourceStrength(str):
    r"""A string representing a species and its emission strength.

    ==SPECIES STRENGTH UNITS==

    e.g. INERT 1.0 g/s

    Other units may be valid but it's not clear which so stick with g/s for
    now.

    Assessed using the following regex:

    ``` python title="SourceStrength Regex"
    re.compile(
        r"^\s*"\w+"\s*"(?:"(?:[1-9]\d*)|0)"(?:\.\d*){,1}"\s*"g/s"\s*"$"
    )
    ```

    ``` python title="SourceStrength Regex Explained"
    re.compile(
        "^" # (1)!
        r"\s*" # (2)!
        r"\w+" # (3)!
        r"\s*"
        r"(?:" # (4)!
        r"(?:[1-9]\d*)|0)" # (5)!
        r"(?:\.\d*){,1}" # (6)!
        r"\s*"
        r"g/s" # (7)!
        r"\s*"
        "$" # (8)!
    )
    ```

    1. `^` represents the start of the string.
    2. `\s*` represents an optional arbitrary number of whitespace characters.
    3. `\w+` represents the species name. No spaces are allowed.
    4. `(?:` indicates the start of the left side of the decimal point for
    source strength
    5. `(?:[1-9]\d*)|0)` represents the left side of the decimal point, which
    cannot start with a 0 if it is > 0.
    6. `(?:\.\d*){,1}` represents the optional decimal point and values for the
    source strength.
    7. `g/s` represents the units, currently only accepting g/s.
    8. `$` represents the end of the string.

    Valid Examples
    --------------
    - INERT 1.0 g/s
    - METHANE 0.5 g/s
    - SUBSTANCE 2 g/s

    !!! warning
        Not all of these values have been tested and are instead inferred from
        the NAME literature. Some of these may cause errors, please raise an
        issue if this is the case.

    Invalid Examples
    ----------------
    - BAD EXAMPLE
    - METHANE 01.0 g/s
    - INERT -1.0 g/s
    - SUBSTANCE 02 g/s

    """

    __slots__ = ()
#WARN: These examples haven't all been tested.

TimeInterval = NonDescriptiveTimeInterval | DescriptiveTimeInterval
"""Represents a string that has the format of a time interval.

This encompasses both the descriptive and non-descriptive formats.
"""

class AcrossString(str):
    """A string representing the Across options.

    It is a string containing the following characters:

    |Character|Description|
    |---------|-----------|
    |T|Time|
    |S|Travel time|
    |X|Coordinate|
    |Y|Coordinate|
    |Z|Coordinate|

    If any/multiple of these characters are specified, these values will be
    placed at the top of columns instead of to the left of the rows

    Valid Examples
    --------------
    - S
    - X
    - SX
    - XS
    - S X
    - STXYZ
    - S T X Y Z
    - XYZST

    Invalid Examples
    ----------------
    - s
    - E
    - ASX
    - BAD VALUE
    - 010101
    """

    __slots__ = ()
#WARN: These examples haven't all been tested.

class SeparateFileString(str):
    """A string representing the Separate File options.

    It is a string containing the following characters:

    |Character|Description|
    |---------|-----------|
    |T|Time|
    |S|Travel time|
    |X|Coordinate|
    |Y|Coordinate|
    |Z|Coordinate|
    |N|Start output from scratch after restart (can overwrite previous files)|

    If any/multiple of these characters are specified, these values will be
    placed in a separate file.

    Valid Examples
    --------------
    - S
    - X
    - SX
    - XS
    - S X
    - STXYZN
    - S T X Y Z N
    - NXYZST

    Invalid Examples
    ----------------
    - s
    - E
    - ASX
    - BAD VALUE
    - 010101
    """

    __slots__ = ()
#WARN: These examples haven't all been tested.

class OutputFormatStringF(str):
    """A string representing the Output Format options for OR - Fields.

    It is a string containing the following characters:

    |Character|Description|
    |---------|-----------|
    |I|Include grid point indices|
    |A|Align columns|
    |Z|Output all grid points, including those with zero values|
    |F|Flush buffer after writing to file to keep it up to date|
    |2|Format as NAME II. (Deprecated, will be accepted for now...)|

    The output file will be formatted according to the characters chosen.

    Valid Examples
    --------------
    - I
    - A
    - IA2
    - IAZF
    - I A Z F 2
    - 2FZAI

    Invalid Examples
    ----------------
    - i
    - E
    - IE
    - BAD VALUE
    - 010101
    """

    __slots__ = ()
#WARN: These examples haven't all been tested.

class OutputRouteStringF(str):
    """A string representing the Output Route options for OR - Fields.

    It is a string containing the following characters:

    |Character|Description|
    |---------|-----------|
    |D|Numerical output to Disk|
    |S|Numerical output to Screen|
    |N|Numerical output to NetCDF|
    |G|Graphical output to screen (Windows only, not accepted here)|

    The output file will be saved according to the characters chosen.

    Valid Examples
    --------------
    - D
    - S
    - DSN
    - D S N
    - NSD

    Invalid Examples
    ----------------
    - d
    - E
    - G
    - DE
    - BAD VALUE
    - 010101
    """

    __slots__ = ()
#WARN: These examples haven't all been tested.

class OutputFormatStringPP(str):
    """A string representing the Output Format options for OR - P/P Info.

    It is a string containing the following characters:

    |Character|Description|
    |---------|-----------|
    |T|Separate times into separate files|
    |P|particles times into separate files|
    |F|Flush buffer after sync interval to keep it up to date|

    The output file will be formatted according to the characters chosen.

    Valid Examples
    --------------
    - T
    - P
    - TP
    - TPF
    - T P F
    - FPT

    Invalid Examples
    ----------------
    - t
    - E
    - TE
    - BAD VALUE
    - 010101
    """

    __slots__ = ()
#WARN: These examples haven't all been tested.

class OutputRouteStringPP(str):
    """A string representing the Output Route options for OR - P/P Info.

    It is a string containing the following characters:

    |Character|Description|
    |---------|-----------|
    |D|Numerical output to Disk|
    |S|Numerical output to Screen|
    |G|Graphical output to screen (Windows only, not accepted here)|

    The output file will be saved according to the characters chosen.

    Valid Examples
    --------------
    - D
    - S
    - DS
    - D S
    - SD

    Invalid Examples
    ----------------
    - d
    - E
    - N
    - G
    - DE
    - BAD VALUE
    - 010101
    """
