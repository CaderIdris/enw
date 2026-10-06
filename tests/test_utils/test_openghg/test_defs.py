import openghg_defs
from pathlib import Path

import pytest

from enw.utils.openghg import (
    get_domain_keys,
    get_domain_info,
    get_location_keys,
    get_location_info,
    get_species_key_bridge,
    get_species_keys,
    get_species_info,
)
import enw.utils.openghg._defs as _defs

pytestmark = [
    pytest.mark.utils,
    pytest.mark.utils_openghg,
    pytest.mark.utils_openghg_defs,
]

def test_get_domain_keys():
    """"""
    tests = {}

    expected = {"A", "B", "C", "D", "E"}
    actual = get_domain_keys()

    tests["Expected Keys"] = expected == actual

    for test, outcome in tests.items():
        if not outcome:
            print(test)

    assert all(tests.values())

def test_get_domain_info():
    """"""
    tests = {}

    expected = {
        "name": "A",
        "x": {
            "min": -97.9000015258789,
            "max": -96.8453140258789,
            "num": 4,
            "step": 0.2,
            "unbounded": False
        },
        "y": {
            "min": 36.093746185302734,
            "max": 37.499996185302734,
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
    actual = get_domain_info("A")

    tests["Expected result"] = expected == actual

    for test, outcome in tests.items():
        if not outcome:
            print(test)

    assert all(tests.values())

def test_get_domain_info_bad_key():
    """"""
    with pytest.raises(
        KeyError,
        match=(
            r"BAD KEY is not a domain specified in the openghg_defs package\."
        )
    ):
        _ = get_domain_info("BAD KEY")

def test_get_location_keys():
    """"""
    tests = {}

    expected = {"A", "B", "C", "D", "E"}
    actual = get_location_keys()

    tests["Expected Keys"] = expected == actual

    for test, outcome in tests.items():
        if not outcome:
            print(test)

    assert all(tests.values())

def test_get_location_info_single_val():
    """"""
    tests = {}

    expected = {
        "name": (
            "Airborne Aerosol Observatory, Bondville, Illinois, United States"
        ),
        "x": -88.37,
        "y": 40.05,
        "inlet_height": 230.0,
        "hcoord": "Lat-Long",
        "subset": "1"
    }
    actual = get_location_info("A")

    tests["Expected result"] = expected == actual

    for test, outcome in tests.items():
        if not outcome:
            print(test)

    assert all(tests.values())

def test_get_location_info_subset():
    """"""
    tests = {}

    expected = {
        "name": (
            "Adrigole, Ireland, 2"
        ),
        "x": -9.72,
        "y": 51.7,
        "inlet_height": 10,
        "hcoord": "Lat-Long",
        "subset": "2"
    }
    actual = get_location_info("E", subset="2")

    tests["Expected result"] = expected == actual

    for test, outcome in tests.items():
        if not outcome:
            print(test)

    assert all(tests.values())

def test_get_location_info_bad_key():
    """"""
    with pytest.raises(
        KeyError,
        match=(
            r"BAD KEY is not a site specified in the openghg_defs package\."
        )
    ):
        _ = get_location_info("BAD KEY")

def test_get_location_info_bad_subset_not_defined():
    """"""
    with pytest.raises(
        KeyError,
        match=(
            r"E has more than one definition\. "
            r"Need to define a subset from: 1, 2\."
        )
    ):
        _ = get_location_info("E")

def test_get_location_info_bad_subset():
    """"""
    with pytest.raises(
        KeyError,
        match=(
            r"3 is not valid for E\."
        )
    ):
        _ = get_location_info("E", subset="3")

def test_get_species_key_bridge():
    """"""
    tests = {}

    expected = {
        "A": "A",
        "A1": "A",
        "A2": "A",
        "A3": "A",
        "B": "B",
        "B1": "B",
        "C": "C",
        "C1": "C",
        "C2": "C",
        "C3": "C",
        "C4": "C",
        "D": "D",
        "E": "E",
        "E1": "E",
        "E2": "E"
    }
    actual = get_species_key_bridge()

    tests["Expected Bridge"] = expected == actual

    for test, outcome in tests.items():
        if not outcome:
            print(test)

    assert all(tests.values())

def test_get_species_keys():
    """"""
    tests = {}

    expected = {
        "A",
        "A1",
        "A2",
        "A3",
        "B",
        "B1",
        "C",
        "C1",
        "C2",
        "C3",
        "C4",
        "D",
        "E",
        "E1",
        "E2"
    }
    actual = get_species_keys()

    tests["Expected keys"] = expected == actual

    for test, outcome in tests.items():
        if not outcome:
            print(test)

    assert all(tests.values())

@pytest.mark.parametrize("species", ["A", "A1", "A2", "A3"])
def test_get_species_info(species: str):
    """"""
    tests = {}

    expected = {
        "category": "Group A",
        "molecular_weight": 3.01,
        "deposition_velocity": 0,
        "material_unit": "g",
        "uv_loss_rate": 0,
        "half_life": "Stable",
        "surface_resistance": None,
        "on_particles": True,
        "on_fields": False,
        "advect_fields": False,
    }
    actual = get_species_info(species)
    print(expected)
    print(actual)

    tests["Expected result"] = expected == actual

    for test, outcome in tests.items():
        if not outcome:
            print(test)

    assert all(tests.values())

def test_get_species_info_bad_key():
    """"""
    with pytest.raises(
        KeyError,
        match=(
            r"BAD KEY is not a species specified in the openghg_defs package\."
        )
    ):
        _ = get_species_info("BAD KEY")
