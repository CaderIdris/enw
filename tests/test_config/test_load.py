from contextlib import suppress
import datetime as dt
import logging
from pathlib import Path
import tomllib
from typing import no_type_check

import pytest
import tomli_w

from enw.config import (
    load_config,
    load_toml,
    load_defaults,
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


def test_load_config():
    """Test if the example config loads properly."""
    tests = {}
    test_config = load_config(Path("./tests/test_config/files/test.toml"))

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

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

    #TODO: Other components of config, fail until they're done
    pytest.xfail("UNFINISHED")


@no_type_check
def test_load_config_no_main_warning(
    tmp_path: pytest.TempPathFactory,
    caplog: pytest.LogCaptureFixture,
):
    """Test if a warning is logged when no Main config is present."""
    tests = {}
    good_config = load_config(Path("./tests/test_config/files/test.toml"))
    good_config.pop("Main")
    good_config.pop("Multiple Case")

    bad_config = tmp_path / "no_main.toml"
    with bad_config.open("wb") as toml_file:
        tomli_w.dump(good_config, toml_file)

    with caplog.at_level(logging.WARNING):
        with suppress(NotImplementedError):
            no_main = load_config(bad_config)
            tests["Main defaults used"] = "Main" in no_main
        warning_text = caplog.text

    tests["Main block warning"] = "Main config not present" in warning_text

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@no_type_check
def test_load_config_no_output_error(
    tmp_path: pytest.TempPathFactory
):
    """Test if a error is raised when no Output config is present."""
    good_config = load_config(Path("./tests/test_config/files/test.toml"))
    good_config.pop("Output")
    good_config.pop("Multiple Case")

    bad_config = tmp_path / "no_output.toml"
    with bad_config.open("wb") as toml_file:
        tomli_w.dump(good_config, toml_file)

    with pytest.raises(
        ValueError,
        match="Mandatory section 'Output'"
    ):
        _ = load_config(bad_config)


@no_type_check
def test_load_config_no_restart_fine(
    tmp_path: pytest.TempPathFactory
):
    """Test if no error raised when no Restart config is present."""
    good_config = load_config(Path("./tests/test_config/files/test.toml"))
    good_config.pop("Restart")
    good_config.pop("Multiple Case")

    bad_config = tmp_path / "no_restart.toml"
    with bad_config.open("wb") as toml_file:
        tomli_w.dump(good_config, toml_file)

    _ = load_config(bad_config)


@no_type_check
def test_load_config_multiple_case_error(
    tmp_path: pytest.TempPathFactory
):
    """Test if a error is raised when Multiple Case config is present."""
    good_config = load_config(Path("./tests/test_config/files/test.toml"))
    good_config.pop("Multiple Case")
    good_config["Multiple Case"] = {
        "name": "Bad",
        "dispersion_options_ensemble_size": 2,
        "met_ensemble_size": 2
    }

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
    good_config.pop("Multiple Case")

    bad_config = tmp_path / "no_openmp.toml"
    with bad_config.open("wb") as toml_file:
        tomli_w.dump(good_config, toml_file)

    with caplog.at_level(logging.WARNING):
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
    good_config.pop("Multiple Case")

    bad_config = tmp_path / "no_coords.toml"
    with bad_config.open("wb") as toml_file:
        tomli_w.dump(good_config, toml_file)

    with caplog.at_level(logging.WARNING):
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
