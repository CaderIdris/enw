import datetime as dt
import logging
from pathlib import Path
import tomllib
from typing import no_type_check

import pytest
import tomli_w

from enw.config import (
    load_config,
    load_openghg,
    load_toml,
    load_defaults,
    create_run_name
)

pytestmark = [
    pytest.mark.config,
    pytest.mark.config_load
]

def test_load_toml_good():
    """Test whether the toml file loads."""
    tests = {}
    good_toml = Path("./tests/test_config/files/good.toml")
    toml = load_toml(good_toml)
    for k in ["Test 1", "Test 2"]:
        tests[f"{k} in result"] = k in toml

    t1 = toml.get("Test 1", {})
    t2 = toml.get("Test 2", {})

    tests["a correct"] = t1.get("a") == 1
    tests["b correct"] = t1.get("b") == "2"
    tests["c correct"] = t2.get("c") == dt.datetime(2020, 1, 1)
    tests["d correct"] = not t2.get("d") and isinstance(t2.get("d"), bool)

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_load_toml_bad():
    """Test whether decode error is raised."""
    bad_toml = Path("./tests/test_config/files/bad.toml")
    with pytest.raises(tomllib.TOMLDecodeError):
        _ = load_toml(bad_toml)


def test_load_toml_does_not_exist():
    """Test when file doesn't exist."""
    bad_toml = Path("/this/file/does/not/exist.toml")
    #INFO: A better test would set up a temporary directory that we know
    # doesn't contain the file but honestly, if this path is valid on your
    # system, what on earth are you doing?
    with pytest.raises(
        FileNotFoundError,
        match=r"Could not find config file at /this/file/does/not/exist.toml"
    ):
        _ = load_toml(bad_toml)


def test_set_defaults():
    """Test whether defaults are properly set."""
    tests = {}
    default = load_defaults({}, "test")  #type: ignore[ty:invalid-argument-type]

    tests["Key in result"] = "a" in default
    tests["Correct value"] = default.get("a") == 1

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@pytest.mark.parametrize(
    "toml",
    [
        "test.toml",
        "test-minimal.toml"
    ]
)
def test_load_config(
    toml: str,
):
    """Test if the example config loads properly."""
    tests = {}
    test_config = load_config(Path(f"./tests/test_config/files/{toml}"))

    tests["Main block present"] = "Main" in test_config
    main_keys = [
        "name",
        "backwards",
        "max_num_sources",
        "max_num_field_reqs",
        "max_num_field_output_groups",
        "absolute_or_relative",
        "fixed_met",
        "flat_earth",
        "random_seed"
    ]
    for k in main_keys:
        tests[f"{k} in Main"] = k in test_config.get("Main", {})

    tests["Output block present"] = "Output" in test_config
    output_keys = [
        "folder",
        "seconds"
    ]
    for k in output_keys:
        tests[f"{k} in Output"] = k in test_config.get("Output", {})

    tests["Restart block present"] = "Restart" in test_config
    restart_keys = [
        "cases_between_writes",
        "delete_old_files",
        "write_on_suspend"
    ]
    for k in restart_keys:
        tests[f"{k} in Restart"] = k in test_config.get("Restart", {})

    tests["Multiple Case block present"] = "MultipleCase" in test_config
    multiple_case_keys = [
        "dispersion_options_ensemble_size",
        "met_ensemble_size"
    ]
    for k in multiple_case_keys:
        tests[f"{k} in Multiple Case"] = k in test_config.get(
            "MultipleCase",
            {}
        )

    tests["OpenMP block present"] = "OpenMP" in test_config
    openmp_keys = [
        "use_openmp",
        "threads"
    ]
    for k in openmp_keys:
        tests[f"{k} in OpenMP"] = k in test_config.get("OpenMP", {})

    tests["Coordinate Systems block present"] = (
        "CoordinateSystems" in test_config
    )
    tests["At least one Horizontal Coord System"] = len(
        test_config.get(
            "CoordinateSystems",
            {}
        ).get("horizontal", {})
    ) > 0
    tests["At least one Vertical Coord System"] = len(
        test_config.get(
            "CoordinateSystems",
            {}
        ).get("vertical", {})
    ) > 0
    coordinate_system_keys = [
        "horizontal",
        "vertical"
    ]
    for k in coordinate_system_keys:
        tests[f"{k} in Coordinate Systems"] = k in test_config.get(
            "CoordinateSystems",
            {}
        )

    tests["Locations block present"] = "Locations" in test_config
    tests["At least one Location"] = len(
        test_config.get("Locations", {})
    ) > 0
    locations_keys = [
        "name",
        "x",
        "y",
        "inlet_height",
        "hcoord"
    ]
    for loc, loc_config in test_config.get("Locations", {}).items():
        for k in locations_keys:
            tests[f"{k} in Locations.{loc}"] = k in loc_config
        tests[f"subset not in Locations.{loc}"] = "subset" not in loc_config

    tests["Domains block present"] = "Domains" in test_config
    tests["At least one Domain"] = len(
        test_config.get("Domains", {})
    ) > 0
    domain_keys = [
        "name",
        "x",
        "y",
        "z",
        "t",
        "hcoord",
        "zcoord"
    ]
    h_keys = [
        "min",
        "max",
        "unbounded"
    ]
    v_keys = [
        "max",
        "unbounded"
    ]
    t_keys = [
        "unbounded"
    ]
    for dom, dom_config in test_config.get("Domains", {}).items():
        for k in domain_keys:
            tests[f"{k} in Domains.{dom}"] = k in dom_config
        for h in ["x", "y"]:
            for k in h_keys:
                tests[f"{k} in Domains.{dom}.{h}"] = k in dom_config.get(h, {})
        for k in v_keys:
            tests[f"{k} in Domains.{dom}.z"] = k in dom_config.get("z", {})
        for k in t_keys:
            tests[f"{k} in Domains.{dom}.t"] = k in dom_config.get("t", {})

    tests["Horizontal Grids block present"] = "HorizontalGrid" in test_config
    tests["At least one Horizontal Grid"] = len(
        test_config.get("HorizontalGrid", {})
    ) > 0

    hgrid_keys = [
        "name",
        "x",
        "y",
        "hcoord",
    ]
    h_keys = [
        "min",
        "max",
        "step",
    ]
    for hgrid, hgrid_config in test_config.get("HorizontalGrid", {}).items():
        for k in hgrid_keys:
            tests[f"{k} in HorizontalGrids.{hgrid}"] = k in hgrid_config
        for h in ["x", "y"]:
            for k in h_keys:
                tests[f"{k} in Horizontal Grids.{hgrid}.{h}"] = (
                    k in hgrid_config.get(h, {})
                )

    species_keys = [
        "category",
        "molecular_weight",
        "deposition_velocity",
        "material_unit",
        "uv_loss_rate",
        "half_life",
        "surface_resistance",
        "uses"
    ]
    tests["Species block present"] = "Species" in test_config
    tests["At least one Species"] = len(
        test_config.get("Species", {})
    ) > 0
    for species, species_config in test_config.get("Species", {}).items():
        for k in species_keys:
            tests[f"{k} in Species.{species}"] = k in species_config

    vertical_grids_keys = [
        "zcoord",
        "num",
        "min",
        "spacing"
    ]
    tests["Vertical Grids block present"] = "VerticalGrid" in test_config
    for k in vertical_grids_keys:
        tests[f"{k} in Vertical Grids"] = (
            k in test_config.get("VerticalGrid", {})
        )

    output_requirements_keys = [
        "Run",
        "Global"
    ]
    output_requirements_subkeys = [
        "quantity",
        "bl_average",
        "t_av_or_int",
        "av_time",
        "num_av_times",
        "sync",
        "output_route"
    ]

    tests[
        "Output Requirements block present"
    ] = "OutputRequirements" in test_config
    for k in output_requirements_keys:
        tests[f"OutputRequirements.{k} present"] = k in test_config.get(
            "OutputRequirements",
            {}
        )
        for sub_k in output_requirements_subkeys:
            for subsub_k, v in test_config.get(
                "OutputRequirements",
                {}
            ).get(
                k,
                {}
            ).items():
                tests[
                    f"OutputRequirements.{k}.{subsub_k}.{sub_k} present"
                ] = sub_k in v


    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

    #TODO: Other components of config, fail until they're done
    pytest.xfail("UNFINISHED")


@no_type_check
def test_load_config_no_main_error(tmp_path: pytest.TempPathFactory):
    """Test if a warning is logged when no Main config is present."""
    good_config = load_config(Path("./tests/test_config/files/test.toml"))
    good_config.pop("Main")
    good_config.pop("MultipleCase")
    good_config["Species"]["C3"].pop("surface_resistance")

    bad_config = tmp_path / "no_main.toml"
    with bad_config.open("wb") as toml_file:
        tomli_w.dump(good_config, toml_file)

    with pytest.raises(ValueError, match=r"Mandatory.*'Main'"):
        _ = load_config(bad_config)


@no_type_check
def test_load_config_no_output_error(tmp_path: pytest.TempPathFactory):
    """Test if a error is raised when no Output config is present."""
    good_config = load_config(Path("./tests/test_config/files/test.toml"))
    good_config.pop("Output")
    good_config.pop("MultipleCase")
    good_config["Horizontal Grids"] = good_config["HorizontalGrid"]
    good_config["Species"]["C3"].pop("surface_resistance")

    bad_config = tmp_path / "no_output.toml"
    with bad_config.open("wb") as toml_file:
        tomli_w.dump(good_config, toml_file)

    with pytest.raises(
        ValueError,
        match="Mandatory section 'Output'"
    ):
        _ = load_config(bad_config)


@no_type_check
def test_load_config_no_restart_fine(tmp_path: pytest.TempPathFactory):
    """Test if no error raised when no Restart config is present."""
    good_config = load_config(Path("./tests/test_config/files/test.toml"))
    good_config.pop("Restart")
    good_config.pop("MultipleCase")
    good_config["Horizontal Grids"] = good_config["HorizontalGrid"]
    good_config.pop("HorizontalGrid")
    good_config["Vertical Grids"] = good_config["VerticalGrid"]
    good_config.pop("VerticalGrid")
    good_config["Species"]["C3"].pop("surface_resistance")

    bad_config = tmp_path / "no_restart.toml"
    with bad_config.open("wb") as toml_file:
        tomli_w.dump(good_config, toml_file)

    _ = load_config(bad_config)


@no_type_check
def test_load_config_multiple_case_error(tmp_path: pytest.TempPathFactory):
    """Test if a error is raised when Multiple Case config is present."""
    good_config = load_config(Path("./tests/test_config/files/test.toml"))
    good_config.pop("MultipleCase")
    good_config["Multiple Case"] = {
        "name": "Bad",
        "dispersion_options_ensemble_size": 2,
        "met_ensemble_size": 2
    }
    good_config["Horizontal Grids"] = good_config["HorizontalGrid"]
    good_config.pop("HorizontalGrid")
    good_config["Vertical Grids"] = good_config["VerticalGrid"]
    good_config.pop("VerticalGrid")
    good_config["Species"]["C3"].pop("surface_resistance")

    bad_config = tmp_path / "multiple_case.toml"
    with bad_config.open("wb") as toml_file:
        tomli_w.dump(good_config, toml_file)

    with pytest.raises(
        NotImplementedError,
        match="Configuration for Multiple Case not enabled!"
    ):
        _ = load_config(bad_config)


@no_type_check
def test_load_config_no_openmp_warning(
    tmp_path: pytest.TempPathFactory,
    caplog: pytest.LogCaptureFixture,
):
    """Test if a warning is logged when no OpenMP config is present."""
    tests = {}
    good_config = load_config(Path("./tests/test_config/files/test.toml"))
    good_config.pop("OpenMP")
    good_config.pop("MultipleCase")
    good_config["Horizontal Grids"] = good_config["HorizontalGrid"]
    good_config.pop("HorizontalGrid")
    good_config["Vertical Grids"] = good_config["VerticalGrid"]
    good_config.pop("VerticalGrid")
    good_config["Species"]["C3"].pop("surface_resistance")

    bad_config = tmp_path / "no_openmp.toml"
    with bad_config.open("wb") as toml_file:
        tomli_w.dump(good_config, toml_file)

    with caplog.at_level(logging.INFO):
        no_openmp = load_config(bad_config)
        tests["OpenMP defaults used"] = "OpenMP" in no_openmp
        warning_text = caplog.text

    tests["Main block warning"] = "OpenMP config not present" in warning_text

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@no_type_check
def test_load_config_no_coords_warning(
    tmp_path: pytest.TempPathFactory,
    caplog: pytest.LogCaptureFixture,
):
    """Test if a warning is logged when no OpenMP config is present."""
    tests = {}
    good_config = load_config(Path("./tests/test_config/files/test.toml"))
    good_config.pop("CoordinateSystems")
    good_config.pop("MultipleCase")
    good_config["Horizontal Grids"] = good_config["HorizontalGrid"]
    good_config.pop("HorizontalGrid")
    good_config["Vertical Grids"] = good_config["VerticalGrid"]
    good_config.pop("VerticalGrid")
    good_config["Species"]["C3"].pop("surface_resistance")

    bad_config = tmp_path / "no_coords.toml"
    with bad_config.open("wb") as toml_file:
        tomli_w.dump(good_config, toml_file)

    with caplog.at_level(logging.INFO):
        no_openmp = load_config(bad_config)
        tests["Coordinate Systems defaults used"] = (
            "CoordinateSystems" in no_openmp
        )
        warning_text = caplog.text

    tests["Main block warning"] = (
        "Coordinate Systems config not present" in warning_text
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@no_type_check
def test_load_config_domain_error(
    tmp_path: pytest.TempPathFactory,
):
    """Test if a error is raised when Multiple Case config is present."""
    good_config = load_config(Path("./tests/test_config/files/test.toml"))
    good_config.pop("MultipleCase")
    good_config.pop("Domains")
    good_config["Species"]["C3"].pop("surface_resistance")

    bad_config = tmp_path / "no_domain.toml"
    with bad_config.open("wb") as toml_file:
        tomli_w.dump(good_config, toml_file)

    with pytest.raises(
        ValueError,
        match=r"Mandatory section 'Domains' not found in config."
    ):
        _ = load_config(bad_config)


@no_type_check
def test_load_config_horizontal_grids_error(
    tmp_path: pytest.TempPathFactory,
):
    """Test if a error is raised when Multiple Case config is present."""
    good_config = load_config(Path("./tests/test_config/files/test.toml"))
    good_config.pop("MultipleCase")
    good_config.pop("Domains")
    good_config.pop("HorizontalGrid")
    good_config["Species"]["C3"].pop("surface_resistance")
    good_config["Domains"] = {
        "A": {
            "name": "A",
            "hcoord": "Lat-Long",
            "zcoord": "m agl",
            "x": {"min": 1, "max": 2, "num": 20},
            "y": {"min": 1, "max": 2, "num": 20},
            "z": {"max": 100, "unbounded": False},
            "t": {"unbounded": True, "max_travel_time": "24:00"},
            "location_block_name": "BLOCK",
            "location": "A"
        }
    }

    bad_config = tmp_path / "no_hgrids.toml"
    with bad_config.open("wb") as toml_file:
        tomli_w.dump(good_config, toml_file)

    with pytest.raises(
        ValueError,
        match=r"Mandatory section 'Horizontal Grids' not found in config."
    ):
        _ = load_config(bad_config)


@no_type_check
def test_load_config_species_error(
    tmp_path: pytest.TempPathFactory,
):
    """Test if a error is raised when Multiple Case config is present."""
    good_config = load_config(Path("./tests/test_config/files/test.toml"))
    good_config.pop("MultipleCase")
    good_config.pop("Species")
    good_config["Horizontal Grids"] = good_config["HorizontalGrid"]
    good_config.pop("HorizontalGrid")

    bad_config = tmp_path / "no_species.toml"
    with bad_config.open("wb") as toml_file:
        tomli_w.dump(good_config, toml_file)

    with pytest.raises(
        ValueError,
        match=r"Mandatory section 'Species' not found in config."
    ):
        _ = load_config(bad_config)


@no_type_check
def test_load_config_no_vertical_grids_warning(
    tmp_path: pytest.TempPathFactory,
    caplog: pytest.LogCaptureFixture,
):
    """Test if a warning is logged when no OpenMP config is present."""
    tests = {}
    good_config = load_config(Path("./tests/test_config/files/test.toml"))
    good_config.pop("OpenMP")
    good_config.pop("MultipleCase")
    good_config.pop("VerticalGrid")
    good_config["Horizontal Grids"] = good_config["HorizontalGrid"]
    good_config.pop("HorizontalGrid")
    good_config["Species"]["C3"].pop("surface_resistance")

    bad_config = tmp_path / "no_vgrids.toml"
    with bad_config.open("wb") as toml_file:
        tomli_w.dump(good_config, toml_file)

    with caplog.at_level(logging.INFO):
        no_openmp = load_config(bad_config)
        tests["OpenMP defaults used"] = "OpenMP" in no_openmp
        warning_text = caplog.text

    tests["Main block warning"] = "Vertical Grids config not present" in warning_text

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@no_type_check
def test_load_config_specific_output_requirements(
    tmp_path: pytest.TempPathFactory
):
    """Test if a warning is logged when no OpenMP config is present."""
    tests = {}
    good_config = load_config(Path("./tests/test_config/files/test.toml"))
    good_config.pop("OpenMP")
    good_config.pop("MultipleCase")
    good_config.pop("OutputRequirements")
    good_config["Horizontal Grids"] = good_config["HorizontalGrid"]
    good_config["Species"]["C3"].pop("surface_resistance")
    good_config["Output Requirements"] = {
        "Run": {
            "preset_a": {}
        },
        "Global": {
            "preset_a": {}
        }
    }

    bad_config = tmp_path / "specific_or.toml"
    with bad_config.open("wb") as toml_file:
        tomli_w.dump(good_config, toml_file)

    specific_or = load_config(bad_config)
    output_requirements_keys = [
        "Run",
        "Global"
    ]
    output_requirements_subkeys = [
        "quantity",
        "bl_average",
        "t_av_or_int",
        "av_time",
        "num_av_times",
        "sync",
        "output_route"
    ]

    tests[
        "Output Requirements block present"
    ] = "OutputRequirements" in specific_or
    for k in output_requirements_keys:
        tests[f"OutputRequirements.{k} present"] = k in specific_or.get(
            "OutputRequirements",
            {}
        )
        tests[
            f"OutputRequirements.{k}.preset_a present"
        ] = "preset_a" in specific_or.get(
            "OutputRequirements",
            {}
        ).get(
            k,
            {}
        )
        for subsub_k in output_requirements_subkeys:
            v = specific_or.get(
                "OutputRequirements"
            ).get(
                k,
                {}
            ).get(
                "preset_a",
                {}
            )
            tests[
                f"OutputRequirements.{k}.preset_a.{subsub_k} present"
            ] = subsub_k in v

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@no_type_check
def test_load_config_specific_output_requirements_with_overrides(
    tmp_path: pytest.TempPathFactory,
):
    """Test if a warning is logged when no OpenMP config is present."""
    tests = {}
    good_config = load_config(Path("./tests/test_config/files/test.toml"))
    good_config.pop("OpenMP")
    good_config.pop("MultipleCase")
    good_config.pop("OutputRequirements")
    good_config["Horizontal Grids"] = good_config["HorizontalGrid"]
    good_config["Species"]["C3"].pop("surface_resistance")
    good_config["Output Requirements"] = {
        "Run": {
            "preset_a": {
                "bl_average": True
            }
        },
        "Global": {
            "preset_a": {
                "sync": True
            }
        }
    }

    bad_config = tmp_path / "specific_or.toml"
    with bad_config.open("wb") as toml_file:
        tomli_w.dump(good_config, toml_file)

    specific_or = load_config(bad_config)

    tests["bl_average changed Run"] = specific_or["OutputRequirements"]["Run"][
        "preset_a"
    ]["bl_average"]
    tests["bl_average unchanged Global"] = not specific_or["OutputRequirements"]["Global"][
        "preset_a"
    ]["bl_average"]
    tests["sync changed Global"] = specific_or["OutputRequirements"]["Global"][
        "preset_a"
    ]["sync"]
    tests["sync unchanged Run"] = not specific_or["OutputRequirements"]["Run"][
        "preset_a"
    ]["sync"]

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())



@pytest.mark.parametrize("domains", [True, False])
@pytest.mark.parametrize("locations", [True, False])
@pytest.mark.parametrize("species", [True, False])
def test_load_openghg_single_vals_good(
    *,
    domains: bool,
    locations: bool,
    species: bool
):
    """"""
    tests = {}

    test_config = {}
    expected = {}

    if domains:
        test_config["Domains"] = {"C": {}}
        expected["Domains"] = {
            "C": {
                "name": "C",
                "x": {
                    "min": -77.9000015258789,
                    "max": -76.8453140258789,
                    "num": 4,
                    "step": 0.2,
                    "unbounded": False
                },
                "y": {
                    "min": 56.093746185302734,
                    "max": 57.499996185302734,
                    "num": 7,
                    "step": 0.1,
                    "unbounded": False
                },
                "z": {
                    "max": 20000,
                    "unbounded": False
                },
                "t": {
                    "unbounded": True,
                    "max_travel_time": "720:00"
                },
                "hcoord": "Lat-Long",
                "zcoord": "m agl"
            }
        }

    if locations:
        test_config["Locations"] = {"D": {}}
        expected["Locations"] = {
            "D": {
                "name": "Alaska Coast Guard, United States",
                "x": -152.5042,
                "y": 57.7366,
                "inlet_height": 6.0,
                "hcoord": "Lat-Long"
            }
        }

    if species:
        test_config["Species"] = {"E2": {}}
        expected["Species"] = {
            "E2": {
                "category": "Group E",
                "molecular_weight": 5.5,
                "deposition_velocity": 0,
                "material_unit": "g",
                "uv_loss_rate": 0,
                "half_life": "Stable",
                "surface_resistance": None,
                "uses": {
                    "on_particles": True,
                    "on_fields": False,
                    "advect_fields": False,
                }
            }
        }

    actual = load_openghg(test_config)
    tests["Expected presets"] = expected == actual

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("domains", [True, False])
@pytest.mark.parametrize("locations", [True, False])
@pytest.mark.parametrize("species", [True, False])
def test_load_openghg_multiple_vals_good(
    *,
    domains: bool,
    locations: bool,
    species: bool
):
    """"""
    tests = {}

    test_config = {}
    expected = {}

    if domains:
        test_config["Domains"] = {"C": {}, "D": {}}
        expected["Domains"] = {
            "C": {
                "name": "C",
                "x": {
                    "min": -77.9000015258789,
                    "max": -76.8453140258789,
                    "num": 4,
                    "step": 0.2,
                    "unbounded": False
                },
                "y": {
                    "min": 56.093746185302734,
                    "max": 57.499996185302734,
                    "num": 7,
                    "step": 0.1,
                    "unbounded": False
                },
                "z": {
                    "max": 20000,
                    "unbounded": False
                },
                "t": {
                    "unbounded": True,
                    "max_travel_time": "720:00"
                },
                "hcoord": "Lat-Long",
                "zcoord": "m agl"
            },
            "D": {
                "name": "D",
                "x": {
                    "min": -67.9000015258789,
                    "max": -66.8453140258789,
                    "num": 4,
                    "step": 0.2,
                    "unbounded": False
                },
                "y": {
                    "min": 66.093746185302734,
                    "max": 67.499996185302734,
                    "num": 7,
                    "step": 0.1,
                    "unbounded": False
                },
                "z": {
                    "max": 20000,
                    "unbounded": False
                },
                "t": {
                    "unbounded": True,
                    "max_travel_time": "720:00"
                },
                "hcoord": "Lat-Long",
                "zcoord": "m agl"
            },
        }

    if locations:
        test_config["Locations"] = {"C": {}, "D": {}}
        expected["Locations"] = {
            "C": {
                "name": "Abbotsford, British Columbia, Canada",
                "x": -122.3353,
                "y": 49.0114,
                "inlet_height": 60.0,
                "hcoord": "Lat-Long"
            },
            "D": {
                "name": "Alaska Coast Guard, United States",
                "x": -152.5042,
                "y": 57.7366,
                "inlet_height": 6.0,
                "hcoord": "Lat-Long"
            }
        }

    if species:
        test_config["Species"] = {"D": {}, "E2": {}}
        expected["Species"] = {
            "D": {
                "category": "Group D",
                "molecular_weight": 1.01,
                "deposition_velocity": 0,
                "material_unit": "g",
                "uv_loss_rate": 0,
                "half_life": "Stable",
                "surface_resistance": None,
                "uses": {
                    "on_particles": True,
                    "on_fields": False,
                    "advect_fields": False,
                }

            },
            "E2": {
                "category": "Group E",
                "molecular_weight": 5.5,
                "deposition_velocity": 0,
                "material_unit": "g",
                "uv_loss_rate": 0,
                "half_life": "Stable",
                "surface_resistance": None,
                "uses": {
                    "on_particles": True,
                    "on_fields": False,
                    "advect_fields": False,
                }

            }
        }

    actual = load_openghg(test_config)
    tests["Expected presets"] = expected == actual

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("subset", ["1", "2"])
def test_load_openghg_subsets_vals_good(
    *,
    subset: str,
):
    """"""
    tests = {}

    test_config = {}
    expected = {}

    test_config["Locations"] = {"E": {"subset": subset}}
    expected["Locations"] = {
        "E": {
            "name": f"Adrigole, Ireland, {subset}",
            "x": -9.72,
            "y": 51.7,
            "inlet_height": 10,
            "hcoord": "Lat-Long"
        }
    }

    test_config["Species"] = {"E2": {}}
    expected["Species"] = {
        "E2": {
            "category": "Group E",
            "molecular_weight": 5.5,
            "deposition_velocity": 0,
            "material_unit": "g",
            "uv_loss_rate": 0,
            "half_life": "Stable",
            "surface_resistance": None,
            "uses": {
                "on_particles": True,
                "on_fields": False,
                "advect_fields": False,
            }
        }
    }

    test_config["Domains"] = {"C": {}}
    expected["Domains"] = {
        "C": {
            "name": "C",
            "x": {
                "min": -77.9000015258789,
                "max": -76.8453140258789,
                "num": 4,
                "step": 0.2,
                "unbounded": False
            },
            "y": {
                "min": 56.093746185302734,
                "max": 57.499996185302734,
                "num": 7,
                "step": 0.1,
                "unbounded": False
            },
            "z": {
                "max": 20000,
                "unbounded": False
            },
            "t": {
                "unbounded": True,
                "max_travel_time": "720:00"
            },
            "hcoord": "Lat-Long",
            "zcoord": "m agl"
        }
    }

    actual = load_openghg(test_config)

    tests["Expected presets"] = expected == actual

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@no_type_check
def test_create_run_name(
):
    """Test create_run_name function"""
    tests = {}
    good_config = load_config(Path("./tests/test_config/files/test.toml"))
    run_name = create_run_name(good_config)
    tests["Correct name"] = run_name == "NAME_E_C3_20250101_20260101"

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@no_type_check
def test_create_run_name_no_run_name_in_config(
    tmp_path: pytest.TempPathFactory,
):
    """Test create_run_name function"""
    tests = {}
    good_config = load_config(Path("./tests/test_config/files/test.toml"))
    good_config["Main"].pop("name")
    good_config.pop("OpenMP")
    good_config.pop("MultipleCase")
    good_config["Horizontal Grids"] = good_config["HorizontalGrid"]
    good_config["Species"]["C3"].pop("surface_resistance")

    bad_config = tmp_path / "bad_name.toml"
    with bad_config.open("wb") as toml_file:
        tomli_w.dump(good_config, toml_file)

    run_name = load_config(bad_config)

    tests["Correct name"] = (
        run_name["Main"]["name"] == "NAME_E_C3_20250101_20260101"
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())
