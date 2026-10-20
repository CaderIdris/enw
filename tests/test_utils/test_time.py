import datetime as dt

import pytest

from enw.utils import get_timedelta, dt_to_name_string, parse_time_string


@pytest.mark.parametrize(
    "time_interval",
    [
        ( "1 day", 1, 0, 0 ),
        ( "1 hr", 0, 3600, 0 ),
        ( "1 min", 0, 60, 0 ),
        ( "1 sec", 0, 1, 0 ),
        ( "0.1 sec", 0, 0, 1000 ),
        ( "1 day 1 hr 1 min 1 sec", 1, 3661, 0 ),
        ( "1 day 1 hr 1 min 1 . 1 sec", 1, 3661, 1000 ),
        ( "-1 day", -1, 0, 0 ),
        ( "-1 hr", -1, 82800, 0 ),
        ( "-1 min", -1, 86340, 0 ),
        ( "-1 sec", -1, 86399, 0 ),
        ( "-0.1 sec", -1, 86399, 999000 ),
        ( "-1 day 1 hr 1 min 1 sec", -2, 82739, 0 ),
        ( "-1 day 1 hr 1 min 1 . 1 sec", -2, 82738, 999000 ),
        ( "2d45:34:4566.1523", 3, 82207, 523000 ),
        ( "64d00:00", 64, 0, 0 ),
        ( "23:23:23.23", 0, 84203, 23000 ),
        ( "600000000:3000000000:455555555555.665738", 32355967, 7420, 738000 ),
        ( "1d01:01", 1, 3660, 0 ),
        ( "0d01:01", 0, 3660, 0 ),
        ( "-2d45:34:4566.1523", -4, 4192, 477000 ),
        ( "-64d00:00", -64, 0, 0 ),
        ( "-23:23:23.23", -1, 2196, 977000 ),
        (
            "-600000000:3000000000:455555555555.665738",
            -32355968,
            78979,
            262000,
        ),
        ( "-1d01:01", -2, 82740, 0 ),
        ( "00:00", 0, 0, 0 )
    ]
)
def test_get_timedelta_good(time_interval: tuple[str, int, int, int]):
    """"""
    tests = {}
    td = get_timedelta(time_interval[0])
    tests["Correct Days"] = time_interval[1] == td.days
    tests["Correct Seconds"] = time_interval[2] == td.seconds
    tests["Correct Microseconds"] = time_interval[3] == td.microseconds

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_get_timedelta_bad():
    """"""
    with pytest.raises(
        ValueError,
        match=r"BAD VALUE is not a valid Time Interval string\."
    ):
        get_timedelta("BAD VALUE")


def test_to_name_string_good():
    """"""
    tests = {}

    test_val = dt.datetime(2020, 1, 1)
    expected_string = "01/01/2020 00:00:00"

    result = dt_to_name_string(test_val)

    tests["Expected string"] = result == expected_string

    string_type = parse_time_string(result)
    tests["Is valid datetime"] = string_type == "DateTime"

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())
