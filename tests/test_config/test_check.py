from copy import copy
import logging
from typing import Any, no_type_check

import pytest

from enw.config import (
    check_coord_options,
    check_main_options,
    check_output_options,
    check_restart_options,
    check_openmp_options
)

pytestmark = [
    pytest.mark.config,
    pytest.mark.config_check
]


@pytest.fixture
def example_main_config() -> dict[str, Any]:
    """An example config for the Main Options block."""
    return {
        "name": "Example Fixture",
        "backwards": False,
        "max_num_sources": 100,
        "max_num_field_reqs": 200,
        "max_num_field_output_groups": 300,
        "absolute_or_relative": "Absolute",
        "fixed_met": True,
        "flat_earth": True,
        "random_seed": "Fixed (Parallel)"
    }


def test_check_main_options_good(example_main_config: dict[str, Any]):
    """Test if a good Main config doesn't error."""
    tests = {}
    main = check_main_options(example_main_config)

    tests["Is dict"] = isinstance(main, dict)
    tests["Has keys"] = len(main)

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_check_main_options_no_name(example_main_config: dict[str, Any]):
    """Test if not adding a name is allowed."""
    pytest.xfail()
    updated_config = copy(example_main_config)
    updated_config.pop("name")
    result = check_main_options(updated_config)
    assert "name" not in result


@pytest.mark.parametrize("bad_key", [
    "run_to",
    "same_results_with_update_on_demand",
])
def test_check_main_options_not_implemented_key_error(
    example_main_config: dict[str, Any],
    bad_key: str,
):
    """Test if a NotImplementedError is raised with a bad config option."""
    bad_conf = example_main_config | {bad_key: "BAD"}
    with pytest.raises(
        NotImplementedError,
        match=f"{bad_key} configuration is currently not implemented."
    ):
        check_main_options(bad_conf)


def test_check_main_options_warn_unexpected_option(
    example_main_config: dict[str, Any],
    caplog: pytest.LogCaptureFixture
):
    """Test if warning emitted with unexpected option."""
    tests = {}
    unexpected = example_main_config | {"Unexpected": "Option"}
    with caplog.at_level(logging.WARNING):
        check_main_options(unexpected)
        warning_text = caplog.text
    tests["Unexpected key warning"] = (
        "Unexpected is not a valid configuration option for Main, ignoring."
    ) in warning_text

@pytest.fixture
def example_output_config() -> dict[str, Any]:
    """An example config for the Output Options block."""
    return {
        "folder": "some/random/path",
        "seconds": True
    }


def test_check_output_options_good(example_output_config: dict[str, Any]):
    """Test if a good output config doesn't error."""
    tests = {}
    output = check_output_options(example_output_config)

    tests["Is dict"] = isinstance(output, dict)
    tests["Has keys"] = len(output)

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_check_output_options_no_folder(example_output_config: dict[str, Any]):
    """Test if not adding a name is allowed."""
    updated_config = copy(example_output_config)
    updated_config.pop("folder")
    with pytest.raises(
        ValueError,
        match=r"Missing mandatory variable 'folder' in 'Output'."
    ):
        _ = check_output_options(updated_config)


@pytest.mark.parametrize("bad_key", [
    "time_decimal_places"
])
def test_check_output_options_not_implemented_key_error(
    example_output_config: dict[str, Any],
    bad_key: str,
):
    """Test if a NotImplementedError is raised with a bad config option."""
    bad_conf = example_output_config | {bad_key: "BAD"}
    with pytest.raises(
        NotImplementedError,
        match=f"{bad_key} configuration is currently not implemented."
    ):
        check_output_options(bad_conf)


def test_check_output_options_warn_unexpected_option(
    example_output_config: dict[str, Any],
    caplog: pytest.LogCaptureFixture
):
    """Test if warning emitted with unexpected option."""
    tests = {}
    unexpected = example_output_config | {"Unexpected": "Option"}
    with caplog.at_level(logging.WARNING):
        check_output_options(unexpected)
        warning_text = caplog.text
    tests["Unexpected key warning"] = (
        "Unexpected is not a valid configuration option for Output, ignoring."
    ) in warning_text

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.fixture
def example_restart_configs() -> list[dict[str, Any]]:
    """An example config for the Output Options block."""
    return [
        {
            "cases_between_writes": 100,
            "delete_old_files": False,
            "write_on_suspend": True
        },
        {
            "time_between_writes": "2d10:20",
            "delete_old_files": True,
            "write_on_suspend": False
        },
        {
            "time_between_writes": "-2 day 10 hr 20 min",
            "delete_old_files": True,
            "write_on_suspend": False
        },
    ]

@pytest.mark.parametrize("index", range(3))
def test_check_restart_options_good(
    example_restart_configs: list[dict[str, Any]],
    index: int
):
    """Check example config for Restart Options."""
    tests = {}
    restart = check_restart_options(example_restart_configs[index])

    tests["Is dict"] = isinstance(restart, dict)
    tests["Has keys"] = len(restart)

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_check_restart_options_mutually_exclusive():
    """Check if an error is raised with mutually exclusive keys."""
    bad_config = {
        "cases_between_writes": 100,
        "time_between_writes": "2d10:10",
        "delete_old_files": True,
        "write_on_suspend": True
    }
    with pytest.raises(
        ValueError,
        match=(
            r"Both Restart.cases_between_writes and "
            r"Restart.time_between_writes are set"
        )
    ):
        check_restart_options(bad_config)


@pytest.mark.parametrize("bad_case", [-100, "100"])
def test_check_restart_options_cases_bad(bad_case: str | int):
    """Check if an error is raised with bad num of cases."""
    bad_config = {
        "cases_between_writes": bad_case,
        "delete_old_files": True,
        "write_on_suspend": True
    }
    with pytest.raises(
        TypeError,
        match=(
            r"Restart.cases_between_writes is not.*int.*str|"
            r"Expected \+ve integer value for Restart.cases_between_writes"
        )
    ):
        check_restart_options(bad_config)


@pytest.mark.parametrize(
    "bad_interval",
    [
        "1 day 1 hr 1 day",
        "",
        " ",
        "-",
        "--",
        "BAD VALUE",
        "--1 day",
        "01d01:01:01",
        "-01d01:01:01"
    ]
)
@no_type_check
def test_check_restart_options_interval_bad(bad_interval: str | int):
    """Check if an error is raised with bad time interval."""
    bad_config = {
        "time_between_writes": bad_interval,
        "delete_old_files": True,
        "write_on_suspend": True
    }
    with pytest.raises(
        ValueError,
        match="time_between_writes is not a valid time interval recognised by"
    ):
        check_restart_options(bad_config)


@no_type_check
@pytest.mark.parametrize("bad_arg", [
    "delete_old_files",
    "write_on_suspend",
])
def test_check_restart_options_bool_bad(bad_arg: str):
    """Test if an error is raised with bad types."""
    bad_config = {
        "cases_between_writes": 100,
        "delete_old_files": False,
        "write_on_suspend": True
    } | {bad_arg: "BAD VALUE"}
    with pytest.raises(
        TypeError,
        match=r"Restart.* is not.*bool.*str"
    ):
        check_restart_options(bad_config)


@pytest.fixture
def example_openmp_config() -> dict[str, Any]:
    """An example config for the OpenMP Options block."""
    return {
        "use_openmp": True,
        "threads": 1,
        "particle_threads": 2,
        "particle_update_threads": 3,
        "chemistry_threads": 4,
        "output_group_threads": 5,
        "output_process_threads": 6,
        "parallel_metread": True,
        "parallel_metprocess": False
    }


def test_check_openmp_options_good(example_openmp_config: dict[str, Any]):
    """Test if a good output config doesn't error."""
    tests = {}
    output = check_openmp_options(example_openmp_config)

    tests["Is dict"] = isinstance(output, dict)
    tests["Has keys"] = len(output)

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_check_openmp_options_warn_unexpected_option(
    example_openmp_config: dict[str, Any],
    caplog: pytest.LogCaptureFixture
):
    """Test if warning emitted with unexpected option."""
    tests = {}
    unexpected = example_openmp_config | {"Unexpected": "Option"}
    with caplog.at_level(logging.WARNING):
        check_openmp_options(unexpected)
        warning_text = caplog.text
    tests["Unexpected key warning"] = (
        "Unexpected is not a valid configuration option for OpenMP, ignoring."
    ) in warning_text

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@pytest.mark.parametrize("bad_case", [-100, "100"])
@pytest.mark.parametrize("integer_option", [
    "threads",
    "particle_threads",
    "particle_update_threads",
    "chemistry_threads",
    "output_group_threads",
    "output_process_threads"
])
def test_check_openmp_options_bad_int(
    example_openmp_config: dict[str, Any],
    bad_case: str | int,
    integer_option: str
):
    """Check if an error is raised with bad num of cases."""
    bad_config = example_openmp_config | {integer_option: bad_case}
    with pytest.raises(
        TypeError,
        match=(
            r"OpenMP.\w* is not.*int.*str|"
            r"Expected \+ve integer value for OpenMP.\w*"
        )
    ):
        check_openmp_options(bad_config)

@pytest.mark.parametrize("bool_option", [
    "use_openmp",
    "parallel_metread",
    "parallel_metprocess"
])
def test_check_openmp_options_bad_bool(
    example_openmp_config: dict[str, Any],
    bool_option: str
):
    """Check if an error is raised with bad num of cases."""
    bad_config = example_openmp_config | {bool_option: "BAD"}
    with pytest.raises(
        TypeError,
        match=(
            r"OpenMP.\w* is not.*bool.*str"
        )
    ):
        check_openmp_options(bad_config)

@pytest.fixture
def example_coords_config() -> list[dict[str, Any]]:
    """An example config for the Coordinate Systems blocks."""
    return [
        {
            "horizontal": "Lat-Long",
            "vertical": [
                "m asl",
                "m agl"
            ]
        },
        {
            "horizontal":[
                "Lat-Long",
                "EMEP 50km Grid"
            ],
            "vertical": "m asl"
        },
    ]

@pytest.mark.parametrize("index", range(2))
def test_check_coords_options_good(
    index: int,
    example_coords_config: list[dict[str, Any]],
):
    """Test if a good coords config doesn't error."""
    tests = {}
    output = check_coord_options(example_coords_config[index])

    tests["Is dict"] = isinstance(output, dict)
    tests["Has keys"] = len(output)
    tests["Horizontal is list"] = isinstance(output["horizontal"], list)
    tests["Vertical is list"] = isinstance(output["vertical"], list)

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@pytest.mark.parametrize(
    "bad_options",
    [
        {
            "horizontal": "BAD"
        },
        {
            "vertical": "BAD"
        },
        {
            "horizontal": "BAD",
            "vertical": "BAD"
        },
        {
            "horizontal": ["BAD"]
        },
        {
            "vertical": ["BAD"]
        },
        {
            "horizontal": ["BAD"],
            "vertical": ["BAD"]
        },
        {
            "horizontal": ["Lat-Long", "BAD"]
        },
        {
            "vertical": ["m asl", "BAD"]
        },
        {
            "horizontal": ["Lat-Long", "BAD"],
            "vertical": ["m asl", "BAD"]
        },
    ]
)
def test_check_coords_options_bad(bad_options: dict[str, str | list[str]]):
    """Test if bad coords error."""
    bad_config = {
        "horizontal": "Lat-Long",
        "vertical": [
            "m asl",
            "m agl"
        ]
    } | bad_options
    with pytest.raises(TypeError, match=r"Got: BAD"):
        _ = check_coord_options(bad_config)

