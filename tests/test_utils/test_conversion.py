from typing import no_type_check

import pytest

from enw.types import (
    DescriptiveTimeInterval,
    NonDescriptiveTimeInterval,
    TimeInterval, DateTime
)
from enw.utils import make_switch, make_time_interval, make_datetime

pytestmark = [
    pytest.mark.utils,
    pytest.mark.utils_conversion
]

@pytest.mark.parametrize("bool_value", [True, False])
def test_make_switch(bool_value: bool):  #noqa: FBT001
    """Test whether the expected value is returned."""
    returned_val = make_switch(bool_value)
    assert returned_val == "Yes" if bool_value else "No"

@no_type_check
def test_make_switch_bad_type_error():
    """Test if passing an invalid type raises the expected error."""
    with pytest.raises(
        TypeError,
        match=r"Incorrect type provided. Expected bool value."
    ):
        _ = make_switch("BAD VALUE")

@pytest.mark.parametrize(
    "descriptive",
    [
        "1 day",
        "1 hr",
        "1 min",
        "1 sec",
        "0.1 sec",
        "1 day 1 hr 1 min 1 sec",
        "1 day 1 hr 1 min 1 . 1 sec",
        "-1 day",
        "-1 hr",
        "-1 min",
        "-1 sec",
        "-0.1 sec",
        "-1 day 1 hr 1 min 1 sec",
        "-1 day 1 hr 1 min 1 . 1 sec"
    ]
)
def test_make_time_interval_descriptive(descriptive: str):
    """Test making a descriptive time interval."""
    tests = {}

    interval = make_time_interval(descriptive)

    tests["Is TimeInterval"] = isinstance(
        interval,
        TimeInterval
    )
    tests["Is DescriptiveTimeInterval"] = isinstance(
        interval,
        DescriptiveTimeInterval
    )
    tests["Not NonDescriptiveTimeInterval"] = not isinstance(
        interval,
        NonDescriptiveTimeInterval
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize(
    "nondescriptive",
    [
        "2d45:34:4566.1523",
        "64d00:00",
        "23:23:23.23",
        "600000000:3000000000:455555555555.665738",
        "1d01:01",
        "0d01:01",
        "-2d45:34:4566.1523",
        "-64d00:00",
        "-23:23:23.23",
        "-600000000:3000000000:455555555555.665738",
        "-1d01:01"
    ]
)
def test_make_time_interval_nondescriptive(nondescriptive: str):
    """Test making a nondescriptive time interval."""
    tests = {}

    interval = make_time_interval(nondescriptive)

    tests["Is TimeInterval"] = isinstance(
        interval,
        TimeInterval
    )
    tests["Not DescriptiveTimeInterval"] = not isinstance(
        interval,
        DescriptiveTimeInterval
    )
    tests["Is NonDescriptiveTimeInterval"] = isinstance(
        interval,
        NonDescriptiveTimeInterval
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize(
    "invalid",
    [
        "1 day 1 hr 1 day",
        "",
        "-",
        "--",
        "BAD VALUE",
        "--1 day",
        "01d01:01:01",
        "-01d01:01:01"
    ]
)
def test_make_time_interval_bad(invalid: str):
    """Test errors with bad descriptive time intervals."""
    with pytest.raises(
        ValueError,
        match=f"{invalid} is not a valid time interval"
    ):
        _ = make_time_interval(invalid)


@pytest.mark.parametrize(
    "datetime",
    [
        "01/05/2001 15:30",
        "12/11/1998 21:06:09",
        "21/01/2021 01:02:59.98",
        "31/01/2000 21:30 UTC",
        "28/02/2012 03:04 UTC +01:00",
        "03/06/2016 12:11:20 UTC",
        "09/09/2009 05:21:45 UTC +02:00",
        "11/12/2013 21:54:45.79 UTC",
        "15/01/2004 12:12:12.12 UTC -02:00"
    ]
)
def test_make_datetime(datetime: str):
    """Test making a descriptive time interval."""
    tests = {}

    dt = make_datetime(datetime)

    tests["Is DateTime"] = isinstance(
        dt,
        DateTime
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@pytest.mark.parametrize(
    "invalid",
    [
        "1/5/2001 15:30",
        "01/05/01 15:30",
        "01/05/2001 03:30 PM",
        "01/05/2001 3:30 PM",
        "01/05/2001 3:30",
        "01/05/2001",
        "01/05/2001 03",
        "01/05/200115:30",
        "01 05 2001 15 30",
        "01/05/2001 15:30:45.79 U T C",
        "01/05/2001 15:30 UTC ±01:00"
    ]
)
def test_make_datetime_bad(invalid: str):
    """Test errors with bad datetimes."""
    with pytest.raises(
        ValueError,
        match=f"{invalid} is not a valid datetime."
    ):
        _ = make_datetime(invalid)
