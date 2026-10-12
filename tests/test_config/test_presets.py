import pytest

from enw.config import (
    load_preset,
)

pytestmark = [
    pytest.mark.config,
    pytest.mark.config_check
]

@pytest.mark.parametrize(
    "preset_name",
    [
        "preset_a",
        "PRESET_A",
        "PrEsEt_A"
    ]
)
def test_load_preset_good(preset_name):
    tests = {}

    expected = {
        "quantity": "Mixing Ratio",
        "bl_average": False,
        "t_av_or_int": "Int",
        "av_time": "24:00",
        "num_av_times": 1440,
        "sync": False,
        "output_route": "N"
    }

    result = load_preset(
        preset_name,
        "output_requirements"
    )

    tests["Expected Result"] = result == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_load_preset_bad():
    tests = {}

    expected = {
    }

    result = load_preset(
        "BAD NAME",
        "output_requirements"
    )

    tests["Expected Result"] = result == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())
