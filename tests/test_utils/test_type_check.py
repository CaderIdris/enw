from typing import Literal, no_type_check

import pytest

from enw.utils import (
    check_datetime,
    check_literal,
    check_pos_float,
    check_pos_int,
    check_time_interval,
    check_output_string_fields,
    check_output_string_pp,
    check_type,
    parse_time_string, check_source_strength,
)

pytestmark = [
    pytest.mark.utils,
    pytest.mark.utils_type_check
]

def test_check_pos_int_good():
    check_pos_int("test", 1)

def test_check_pos_int_bad():
    with pytest.raises(
        TypeError,
        match=r"Expected \+ve integer value for bad\."
    ):
        check_pos_int("bad", -1)

def test_check_literal_good():
    TestLiteral = Literal["1", "2", "3"]  #noqa: N806
    check_literal("test", "1", "TestLiteral", TestLiteral)

def test_check_literal_bad():
    TestLiteral = Literal["1", "2", "3"]  #noqa: N806
    with pytest.raises(
        TypeError,
        match=r"bad is not a member of TestLiteral."
    ):
        check_literal("bad", "4", "TestLiteral", TestLiteral)

@no_type_check
def test_check_literal_not_lit():
    TestLiteral = int  #noqa: N806
    with pytest.raises(
        TypeError,
        match=r"TestLiteral is not a Literal type."
    ):
        check_literal("bad", "4", "TestLiteral", TestLiteral)

def test_check_type_good():
    """Check if the type checker works."""
    check_type("test", 1, int)

def test_check_type_bad():
    """Check if the type checker fails properly."""
    with pytest.raises(TypeError, match=r"bad is not.*str.*int"):
        check_type("bad", 1, str)

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
def test_parse_time_string_descriptive(descriptive: str):
    """Test making a descriptive time interval."""
    tests = {}

    interval = parse_time_string(descriptive)

    tests["Is Descriptive"] = interval == "Descriptive"


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
        "-1d01:01",
        "00:00"
    ]
)
def test_parse_time_string_nondescriptive(nondescriptive: str):
    """Test making a nondescriptive time interval."""
    tests = {}

    interval = parse_time_string(nondescriptive)

    tests["Is NonDescriptive"] = interval == "NonDescriptive"

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

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
def test_parse_time_string_datetime(datetime: str):
    """Test making a nondescriptive time interval."""
    tests = {}

    interval = parse_time_string(datetime)

    tests["Is DateTime"] = interval == "DateTime"

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
def test_parse_time_string_bad(invalid: str):
    """Test errors with bad descriptive time intervals."""
    tests = {}

    interval = parse_time_string(invalid)

    tests["Is NonDescriptive"] = interval == "Invalid"

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


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
def test_check_time_interval_descriptive(descriptive: str):
    """Test making a descriptive time interval."""
    _ = check_time_interval("descriptive", descriptive)


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
        "-1d01:01",
        "00:00"
    ]
)
def test_check_time_interval_nondescriptive(nondescriptive: str):
    """Test making a nondescriptive time interval."""
    _ = check_time_interval("test", nondescriptive)


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
def test_check_datetime(datetime: str):
    """Test making a datetime."""
    _ = check_datetime("test", datetime)


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
        "-01d01:01:01",
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
def test_check_time_interval_bad(invalid: str):
    """Test errors with bad descriptive time intervals."""
    with pytest.raises(
        ValueError,
        match=r"invalid is not a valid time interval recognised by NAME."
    ):
        _ = check_time_interval("invalid", invalid)


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
        "-01d01:01:01",
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
def test_check_datetime_bad(invalid: str):
    """Test errors with bad datetimes."""
    with pytest.raises(
        ValueError,
        match=r"invalid is not a valid time interval recognised by NAME."
    ):
        _ = check_datetime("invalid", invalid)


def test_check_pos_float():
    """Test if a positive float is detected successfully."""
    _ = check_pos_float("test", 0.1)


def test_check_pos_float_bad():
    """Test if a negative float raises an error."""
    with pytest.raises(
        TypeError,
        match=r"Expected \+ve float value for test\. Got -0\.1 instead."
    ):
        _ = check_pos_float("test", -0.1)


@pytest.mark.parametrize("val", ["1", 1, 1.0])
def test_check_type_good_multi_type(val):
    """Check if the type checker works."""
    check_type("test", val, (int, float, str))


@pytest.mark.parametrize("val", ["1", 1, 1.0])
def test_check_type_good_multi_type_union(val):
    """Check if the type checker works."""
    check_type("test", val, int | float | str)


@pytest.mark.parametrize(
    "valid",
    [
        "INERT 1.0 g/s",
        "METHANE 0.5 g/s",
        "SUBSTANCE 2 g/s"
    ]
)
def test_check_source_strength_good(valid: str):
    """Test if check_source_strength works."""
    _ = check_source_strength("valid", valid)


@pytest.mark.parametrize(
    "invalid",
    [
        "BAD EXAMPLE",
        "METHANE 01.0 g/s",
        "INERT -1.0 g/s",
        "SUBSTANCE 02 g/s",
    ]
)
def test_check_source_strength_bad(invalid: str):
    """Test errors with bad source strengths."""
    with pytest.raises(
        ValueError,
        match=r"invalid is not a valid source strength recognised by NAME."
    ):
        _ = check_source_strength("invalid", invalid)

@pytest.mark.parametrize(
    "valid",
    [
        ("S", "across"),
        ("X", "across"),
        ("SX", "across"),
        ("XS", "across"),
        ("S X", "across"),
        ("STXYZ", "across"),
        ("S T X Y Z", "across"),
        ("XYZST", "across"),
        ("S", "separate_file"),
        ("X", "separate_file"),
        ("SX", "separate_file"),
        ("XS", "separate_file"),
        ("S X", "separate_file"),
        ("STXYZN", "separate_file"),
        ("S T X Y Z N", "separate_file"),
        ("NXYZST", "separate_file"),
        ("I", "output_format"),
        ("A", "output_format"),
        ("IA2", "output_format"),
        ("IAZF", "output_format"),
        ("I A Z F 2", "output_format"),
        ("2FZAI", "output_format"),
        ("D", "output_route"),
        ("S", "output_route"),
        ("DSN", "output_route"),
        ("D S N", "output_route"),
        ("NSD", "output_route"),
    ]
)
def test_check_output_string_fields_good(valid: tuple[str, str]):
    """Test valid output strings."""
    _ = check_output_string_fields("valid", valid[0], valid[1])


@pytest.mark.parametrize(
    "invalid",
    [
        ("s", "across"),
        ("E", "across"),
        ("ASX", "across"),
        ("BAD VALUE", "across"),
        ("010101", "across"),
        ("s", "separate_file"),
        ("E", "separate_file"),
        ("ASX", "separate_file"),
        ("BAD VALUE", "separate_file"),
        ("010101", "separate_file"),
        ("i", "output_format"),
        ("E", "output_format"),
        ("IE", "output_format"),
        ("BAD VALUE", "output_format"),
        ("010101", "output_format"),
        ("d", "output_route"),
        ("E", "output_route"),
        ("G", "output_route"),
        ("DE", "output_route"),
        ("BAD VALUE", "output_route"),
        ("010101", "output_route"),
    ]
)
def test_check_output_string_fields_bad_chars(invalid: tuple[str, str]):
    """Test invalid output strings."""
    with pytest.raises(
        ValueError,
        match=r"invalid is not a valid .* format string recognised by NAME."
    ):
        _ = check_output_string_fields("invalid", invalid[0], invalid[1])

@pytest.mark.parametrize(
    "invalid",
    [
        ("SS", "across"),
        ("STXZX", "across"),
        ("SS", "separate_file"),
        ("STXYNT", "separate_file"),
        ("II", "output_format"),
        ("IAZ22", "output_format"),
        ("DD", "output_route"),
        ("DSS", "output_route"),
    ]
)
def test_check_output_string_fields_bad_dupe(invalid: tuple[str, str]):
    """Test valid output strings."""
    with pytest.raises(
        ValueError,
        match=r"contains duplicate characters\."
    ):
        _ = check_output_string_fields("invalid", invalid[0], invalid[1])


def test_check_output_string_fields_bad_output_type():
    """Test valid output strings."""
    with pytest.raises(
        TypeError,
        match=r"is not a member of OutputColumn"
    ):
        _ = check_output_string_fields("invalid", "BAD VALUE", "BAD NAME")

@pytest.mark.parametrize(
    "valid",
    [
        ("T", "output_format"),
        ("P", "output_format"),
        ("TP", "output_format"),
        ("TPF", "output_format"),
        ("T P F", "output_format"),
        ("FPT", "output_format"),
        ("D", "output_route"),
        ("S", "output_route"),
        ("DS", "output_route"),
        ("D S ", "output_route"),
        ("SD", "output_route"),
    ]
)
def test_check_output_string_pp_good(valid: tuple[str, str]):
    """Test valid output strings."""
    _ = check_output_string_pp("valid", valid[0], valid[1])


@pytest.mark.parametrize(
    "invalid",
    [
        ("t", "output_format"),
        ("E", "output_format"),
        ("TE", "output_format"),
        ("BAD VALUE", "output_format"),
        ("010101", "output_format"),
        ("d", "output_route"),
        ("E", "output_route"),
        ("N", "output_route"),
        ("G", "output_route"),
        ("DE", "output_route"),
        ("BAD VALUE", "output_route"),
        ("010101", "output_route"),
    ]
)
def test_check_output_string_pp_bad_chars(invalid: tuple[str, str]):
    """Test invalid output strings."""
    with pytest.raises(
        ValueError,
        match=r"invalid is not a valid .* format string recognised by NAME."
    ):
        _ = check_output_string_pp("invalid", invalid[0], invalid[1])

@pytest.mark.parametrize(
    "invalid",
    [
        ("TT", "output_format"),
        ("TPP", "output_format"),
        ("DD", "output_route"),
        ("SS", "output_route"),
    ]
)
def test_check_output_string_pp_bad_dupe(invalid: tuple[str, str]):
    """Test valid output strings."""
    with pytest.raises(
        ValueError,
        match=r"contains duplicate characters\."
    ):
        _ = check_output_string_pp("invalid", invalid[0], invalid[1])


def test_check_output_string_pp_bad_output_type():
    """Test valid output strings."""
    with pytest.raises(
        TypeError,
        match=r"is not a member of OutputColumn"
    ):
        _ = check_output_string_pp("invalid", "BAD VALUE", "BAD NAME")
