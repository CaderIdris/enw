from copy import copy
import logging
from typing import Any, no_type_check

import pytest

from enw.config import (
    check_coord_options,
    check_main_options,
    check_output_options,
    check_restart_options,
    check_openmp_options,
    check_location_options,
    check_species_options,
    check_domain_options,
    check_set_of_dispersion_options,
    check_vertical_grids_options
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


@pytest.fixture
def example_location_config() -> dict[str, dict[str, object]]:
    """An example config for the Locations block."""
    return {
        "TLoc": {
            "name": "Test Location",
            "x": 1.23,
            "y": -4.56,
            "inlet_height": 78,
            "hcoord": "Lat-Long",
            "subset": "Test Subset",
        }
    }


def test_check_locations_options_good(example_location_config: dict[str, Any]):
    """Test if a good location config doesn't error."""
    tests = {}
    output = check_location_options(example_location_config)

    tests["Is dict"] = isinstance(output, dict)
    tests["Has keys"] = len(output)

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize(
    "bad_options",
    [
        {
            "name": 0,
        },
        {
            "subset": 0,
        }
    ]
)
def test_locations_options_bad_str(
    example_location_config: dict[str, dict[str, object]],
    bad_options: dict[str, str | list[str]],
):
    """Test if bad coords error."""
    bad_config = {
        "TLoc": example_location_config["TLoc"] | bad_options,
    }
    with pytest.raises(TypeError, match=r"TLoc\..*is not.*str.*int"):
        _ = check_location_options(bad_config)

@pytest.mark.parametrize(
    "bad_options",
    [
        {
            "x": "BAD",
        },
        {
            "y": "BAD",
        },
        {
            "inlet_height": "BAD",
        },
    ]
)
def test_locations_options_bad_num(
    example_location_config: dict[str, dict[str, object]],
    bad_options: dict[str, str | list[str]],
):
    """Test if bad coords error."""
    bad_config = {
        "TLoc": example_location_config["TLoc"] | bad_options,
    }
    with pytest.raises(TypeError, match=r"TLoc.*is not.*int.*str"):
        _ = check_location_options(bad_config)


@pytest.mark.parametrize(
    "bad_options",
    [
        {
            "hcoord": "BAD VALUE",
        },
    ]
)
def test_locations_options_bad_literal(
    example_location_config: dict[str, dict[str, object]],
    bad_options: dict[str, str | list[str]],
):
    """Test if bad coords error."""
    bad_config = {
        "TLoc": example_location_config["TLoc"] | bad_options,
    }
    with pytest.raises(TypeError, match=r"Got: BAD VALUE"):
        _ = check_location_options(bad_config)


@pytest.fixture
def example_species_config() -> dict[str, dict[str, object]]:
    """An example config for the speciess block."""
    return {
        "TSpec": {
            "name": "Test Species",
            "category": "Test Category",
            "molecular_weight": 123,
            "deposition_velocity": 0,
            "material_unit": "g",
            "uv_loss_rate": 0,
            "half_life": "Stable",
            "surface_resistance": None,
            "on_particles": True,
            "on_fields": False,
            "advect_fields": False
        }
    }


def test_check_species_options_good(example_species_config: dict[str, Any]):
    """Test if a good species config doesn't error."""
    tests = {}
    output = check_species_options(example_species_config)

    tests["Is dict"] = isinstance(output, dict)
    tests["Has keys"] = len(output)

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize(
    "bad_options",
    [
        {"name": 0},
        {"category": 0},
        {"material_unit": 0},
    ]
)
def test_species_options_bad_str(
    example_species_config: dict[str, dict[str, object]],
    bad_options: dict[str, str | list[str]],
):
    """Test if bad coords error."""
    bad_config = {
        "TSpec": example_species_config["TSpec"] | bad_options
    }
    with pytest.raises(TypeError, match=r"TSpec\..*is not.*str.*int"):
        _ = check_species_options(bad_config)

@pytest.mark.parametrize(
    "bad_options",
    [
        {"molecular_weight": "BAD"},
        {"deposition_velocity": "BAD"},
        {"uv_loss_rate": "BAD"},
        {"surface_resistance": "BAD"},
        {"half_life": ["BAD"]},
    ]
)
def test_species_options_bad_num(
    example_species_config: dict[str, dict[str, object]],
    bad_options: dict[str, str | list[str]],
):
    """Test if bad coords error."""
    bad_config = {
        "TSpec": example_species_config["TSpec"] | bad_options,
    }
    with pytest.raises(TypeError, match=r"TSpec.*is not.*int.*str"):
        _ = check_species_options(bad_config)

@pytest.mark.parametrize(
    "bad_options",
    [
        {"on_particles": "BAD"},
        {"on_fields": "BAD"},
        {"advect_fields": "BAD"},
    ]
)
def test_species_options_bad_bool(
    example_species_config: dict[str, dict[str, object]],
    bad_options: dict[str, str | list[str]],
):
    """Test if bad coords error."""
    bad_config = {
        "TSpec": example_species_config["TSpec"] | bad_options,
    }
    with pytest.raises(TypeError, match=r"TSpec.*is not.*bool.*str"):
        _ = check_species_options(bad_config)


@pytest.fixture
def example_domain_config() -> dict[str, dict[str, object]]:
    """An example config for the domains block."""
    return {
        "TDom": {
            "name": "Test Domain",
            "hcoord": "Lat-Long",
            "zcoord": "m asl",
            "x": {
                "min": -1,
                "max": 1,
                "num": 10,
                "unbounded": False
            },
            "y": {
                "min": -1,
                "max": 1,
                "num": 10,
                "unbounded": False
            },
            "z": {
                "max": 1,
                "unbounded": False
            },
            "t": {
                "unbounded": True
            },
        }
    }


def test_check_domain_options_good(example_domain_config: dict[str, Any]):
    """Test if a good domain config doesn't error."""
    tests = {}
    output = check_domain_options(example_domain_config)

    tests["Is dict"] = isinstance(output, dict)
    tests["Has keys"] = len(output)

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize(
    "bad_options",
    [
        {"name": 0},
    ]
)
def test_domain_options_bad_str(
    example_domain_config: dict[str, dict[str, object]],
    bad_options: dict[str, str | list[str]],
):
    """Test if bad coords error."""
    bad_config = {
        "TDom": example_domain_config["TDom"] | bad_options
    }
    with pytest.raises(TypeError, match=r"TDom\..*is not.*str.*int"):
        _ = check_domain_options(bad_config)

@pytest.mark.parametrize(
    "bad_options",
    [
        {"min": "BAD"},
        {"max": "BAD"},
        {"num": "BAD"},
    ]
)
@pytest.mark.parametrize("axis", ["x", "y"])
def test_domain_options_bad_num_h(
    example_domain_config: dict[str, dict[str, object]],
    bad_options: dict[str, object],
    axis: str
):
    """Test if bad coords error."""
    bad_config = example_domain_config

    bad_config["TDom"][axis] = bad_config["TDom"][axis] | bad_options

    with pytest.raises(TypeError, match=r"TDom.*is not.*int.*str"):
        _ = check_domain_options(bad_config)

@pytest.mark.parametrize(
    "bad_options",
    [
        {"unbounded": "BAD"},
    ]
)
@pytest.mark.parametrize("axis", ["x", "y", "z", "t"])
def test_domain_options_bad_bool(
    example_domain_config: dict[str, dict[str, object]],
    bad_options: dict[str, str | list[str]],
    axis: str
):
    """Test if bad coords error."""
    bad_config = example_domain_config

    bad_config["TDom"][axis] = bad_config["TDom"][axis] | bad_options

    with pytest.raises(TypeError, match=r"TDom.*is not.*bool.*str"):
        _ = check_domain_options(bad_config)

@pytest.mark.parametrize(
    "bad_options",
    [
        {"max": "BAD"},
    ]
)
def test_domain_options_bad_num_v(
    example_domain_config: dict[str, dict[str, object]],
    bad_options: dict[str, object],
):
    """Test if bad coords error."""
    bad_config = example_domain_config

    bad_config["TDom"]["z"] = bad_config["TDom"]["z"] | bad_options

    with pytest.raises(TypeError, match=r"TDom.*is not.*int.*str"):
        _ = check_domain_options(bad_config)


@pytest.mark.parametrize(
    "bad_options",
    [
        {"hcoord": "BAD VALUE"},
        {"zcoord": "BAD VALUE"},
    ]
)
def test_domains_options_bad_literal(
    example_domain_config: dict[str, dict[str, object]],
    bad_options: dict[str, str | list[str]],
):
    """Test if bad coords error."""
    bad_config = {
        "TDom": example_domain_config["TDom"] | bad_options,
    }
    with pytest.raises(TypeError, match=r"Got: BAD VALUE"):
        _ = check_domain_options(bad_config)


@pytest.fixture
def example_set_of_dispersion_config() -> dict[str, object]:
    """An example config for the set_of_dispersions block."""
    return {
        "max_num_particles": 10,
        "max_num_full_particles": 1,
        "max_num_puffs": 2,
        "max_num_original_puffs": 3,
        "skew_time": "15:00",
        "velocity_memory_time": "10:00",
        "mesoscale_velocity_memory_time": "30:00",
        "inhomogeneous_time": "00:00",
        "delta_opt": "1",
        "puff_time": "12:00",
        "sync_time": "12:00",
        "puff_interval": "14:00",
        "deep_convection": True,
        "radioactive_decay": False,
        "agent_decay": True,
        "dry_deposition": False,
        "wet_deposition": True,
        "turbulence": False,
        "mesoscale_motions": True,
        "chemistry": True,
    }


def test_check_set_of_dispersion_options_good(
    example_set_of_dispersion_config: dict[str, Any],
):
    """Test if a good set_of_dispersion config doesn't error."""
    tests = {}
    output = check_set_of_dispersion_options(example_set_of_dispersion_config)

    tests["Is dict"] = isinstance(output, dict)
    tests["Has keys"] = len(output)

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize(
    "bad_options",
    [
        {"delta_opt": 0},
    ]
)
def test_set_of_dispersion_options_bad_str(
    example_set_of_dispersion_config: dict[str, dict[str, object]],
    bad_options: dict[str, str | list[str]],
):
    """Test if bad coords error."""
    bad_config = example_set_of_dispersion_config | bad_options

    with pytest.raises(TypeError, match=r"is not.*str.*int"):
        _ = check_set_of_dispersion_options(bad_config)

@pytest.mark.parametrize(
    "bad_options",
    [
        {"max_num_particles": "BAD"},
        {"max_num_full_particles": "BAD"},
        {"max_num_puffs": "BAD"},
        {"max_num_original_puffs": "BAD"},
    ]
)
def test_set_of_dispersion_options_bad_num(
    example_set_of_dispersion_config: dict[str, dict[str, object]],
    bad_options: dict[str, object],
):
    """Test if bad coords error."""
    bad_config = example_set_of_dispersion_config | bad_options

    with pytest.raises(TypeError, match=r"is not.*int.*str"):
        _ = check_set_of_dispersion_options(bad_config)

@pytest.mark.parametrize(
    "bad_options",
    [
        {"max_num_particles": -1},
        {"max_num_full_particles": -1},
        {"max_num_puffs": -1},
        {"max_num_original_puffs": -1},
    ]
)
def test_set_of_dispersion_options_bad_neg_int(
    example_set_of_dispersion_config: dict[str, dict[str, object]],
    bad_options: dict[str, object],
):
    """Test if bad coords error."""
    bad_config = example_set_of_dispersion_config | bad_options

    with pytest.raises(
        TypeError,
        match=r"Expected \+ve integer value for.*Got -1 instead\."
    ):
        _ = check_set_of_dispersion_options(bad_config)

@pytest.mark.parametrize(
    "bad_options",
    [
        {"deep_convection": "BAD"},
        {"radioactive_decay": "BAD"},
        {"agent_decay": "BAD"},
        {"dry_deposition": "BAD"},
        {"wet_deposition": "BAD"},
        {"turbulence": "BAD"},
        {"mesoscale_motions": "BAD"},
        {"chemistry": "BAD"},
    ]
)
def test_set_of_dispersion_options_bad_bool(
    example_set_of_dispersion_config: dict[str, dict[str, object]],
    bad_options: dict[str, str | list[str]],
):
    """Test if bad coords error."""
    bad_config = example_set_of_dispersion_config | bad_options

    with pytest.raises(TypeError, match=r"is not.*bool.*str"):
        _ = check_set_of_dispersion_options(bad_config)


@pytest.mark.parametrize(
    "bad_options",
    [
        {"skew_time": "BAD VALUE"},
        {"velocity_memory_time": "BAD VALUE"},
        {"mesoscale_velocity_memory_time": "BAD VALUE"},
        {"inhomogeneous_time": "BAD VALUE"},
        {"puff_time": "BAD VALUE"},
        {"sync_time": "BAD VALUE"},
        {"puff_interval": "BAD VALUE"},
    ]
)
def test_set_of_dispersions_options_bad_timestamp(
    example_set_of_dispersion_config: dict[str, dict[str, object]],
    bad_options: dict[str, str | list[str]],
):
    """Test if bad coords error."""
    bad_config = example_set_of_dispersion_config | bad_options
    with pytest.raises(
        ValueError,
        match=r"is not a valid time interval recognised by NAME\."
    ):
        _ = check_set_of_dispersion_options(bad_config)


@pytest.fixture
def example_vertical_grids_config() -> dict[str, object]:
    """An example config for the vertical_gridss block."""
    return {
        "zcoord": "m asl",
        "num": 10,
        "min": 12.0,
        "spacing": 7.9
    }


def test_check_vertical_grids_options_good(
    example_vertical_grids_config: dict[str, Any],
):
    """Test if a good vertical_grids config doesn't error."""
    tests = {}
    output = check_vertical_grids_options(example_vertical_grids_config)

    tests["Is dict"] = isinstance(output, dict)
    tests["Has keys"] = len(output)

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize(
    "bad_options",
    [
        {"zcoord": "BAD"},
    ]
)
def test_vertical_grids_options_bad_literal(
    example_vertical_grids_config: dict[str, dict[str, object]],
    bad_options: dict[str, str | list[str]],
):
    """Test if bad coords error."""
    bad_config = example_vertical_grids_config | bad_options

    with pytest.raises(TypeError, match=r"is not a member of.*Got: BAD"):
        _ = check_vertical_grids_options(bad_config)

@pytest.mark.parametrize(
    "bad_options",
    [
        {"num": "BAD"},
        {"min": "BAD"},
        {"spacing": "BAD"},
    ]
)
def test_vertical_grids_options_bad_num(
    example_vertical_grids_config: dict[str, dict[str, object]],
    bad_options: dict[str, object],
):
    """Test if bad coords error."""
    bad_config = example_vertical_grids_config | bad_options

    with pytest.raises(TypeError, match=r"is not.*int.*str"):
        _ = check_vertical_grids_options(bad_config)

@pytest.mark.parametrize(
    "bad_options",
    [
        {"num": -1},
    ]
)
def test_vertical_grids_options_bad_neg_int(
    example_vertical_grids_config: dict[str, dict[str, object]],
    bad_options: dict[str, object],
):
    """Test if bad coords error."""
    bad_config = example_vertical_grids_config | bad_options

    with pytest.raises(
        TypeError,
        match=r"Expected \+ve integer value for.*Got -1 instead\."
    ):
        _ = check_vertical_grids_options(bad_config)
