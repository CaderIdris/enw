from jinja2 import Environment
import pytest

from enw.block import (
    TemporalGrids
)


pytestmark = [
    pytest.mark.block,
    pytest.mark.block_temporal
]

@pytest.fixture
def temporal_grids_config() -> dict[str, dict[str, int | str]]:
    return {
        "A": {
            "t_num": 100,
            "t_spacing": "00:30",
            "t_min": "01/01/2020 00:00",
        },
        "B": {
            "t_num": 10,
            "t_spacing": "30 min",
            "t_min": "01/02/2020 00:00",
        },
    }

@pytest.fixture
def temporal_grids_expected_block() -> dict[str, str]:
    return {
        "Header": "Temporal Grids:\nName,nT,dT,T0",
        "A": "A,100,00:30,01/01/2020 00:00",
        "B": "B,10,30 min,01/02/2020 00:00"
    }

@pytest.fixture
def temporal_grids_expected_repr() -> str:
    return "\n".join([
        "[Temporal Grids]",
        "\t[[A]]",
        "\t\tt_num               : 100",
        "\t\tt_spacing           : 00:30",
        "\t\tt_min               : 01/01/2020 00:00",
        "\t\tt_array             : None",
        "\t[[B]]",
        "\t\tt_num               : 10",
        "\t\tt_spacing           : 30 min",
        "\t\tt_min               : 01/02/2020 00:00",
        "\t\tt_array             : None",
    ])


@pytest.mark.parametrize("row", ["A", "B"])
def test_init_temporal_grids_single(
    temporal_grids_config: dict[str, dict[str, str | int]],
    row: str,
):
    """Does the Temporal Grids class initialise?"""
    tests = {}
    expected_vals = {
        "A": {
            "name": "A",
            "t_num": 100,
            "t_spacing": "00:30",
            "t_min": "01/01/2020 00:00",
            "t_array": None
        },
        "B": {
            "name": "B",
            "t_num": 10,
            "t_spacing": "30 min",
            "t_min": "01/02/2020 00:00",
            "t_array": None
        }
    }

    temporal_grids = TemporalGrids.setup(
        rows={row: temporal_grids_config[row]}
    )
    vals = temporal_grids.__dict__

    actual_vals = vals["rows"][0].__dict__
    for k, v in expected_vals[row].items():
        tests[f"{k} present"] = k in actual_vals
        tests[f"{k} correct"] = v == actual_vals.get(k)

    tests["Environment present"] = isinstance(
        temporal_grids._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

def test_init_temporal_grids_all(
    temporal_grids_config: dict[str, dict[str, str | int]]
):
    """Does the Temporal Grids class initialise?"""
    tests = {}
    expected_vals = {
        "A": {
            "name": "A",
            "t_num": 100,
            "t_spacing": "00:30",
            "t_min": "01/01/2020 00:00",
            "t_array": None
        },
        "B": {
            "name": "B",
            "t_num": 10,
            "t_spacing": "30 min",
            "t_min": "01/02/2020 00:00",
            "t_array": None
        }
    }

    temporal_grids = TemporalGrids.setup(
        rows=temporal_grids_config
    )
    vals = temporal_grids.__dict__

    for i, name in enumerate(["A", "B"]):
        actual_vals = vals["rows"][i].__dict__
        for k, v in expected_vals[name].items():
            tests[f"{name}.{k} present"] = k in actual_vals
            tests[f"{name}.{k} correct"] = v == actual_vals.get(k)

    tests["Environment present"] = isinstance(
        temporal_grids._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("row", ["A", "B"])
def test_temporal_grids_str_single(
    temporal_grids_config: dict[str, dict[str, str | int]],
    temporal_grids_expected_block: dict[str, str],
    row: str
):
    """Does the Main class have the right output?"""
    tests = {}

    temporal_grids = TemporalGrids.setup(
        rows={row: temporal_grids_config[row]}
    )

    expected_block = "\n".join([
        temporal_grids_expected_block["Header"],
        temporal_grids_expected_block[row],
    ])

    block = str(temporal_grids)
    tests["Expected str"] = block == expected_block

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

def test_temporal_grids_str_all(
    temporal_grids_config: dict[str, dict[str, str | int]],
    temporal_grids_expected_block: dict[str, str],
):
    """Does the Main class have the right output?"""
    tests = {}

    temporal_grids = TemporalGrids.setup(
        rows=temporal_grids_config
    )

    expected_block = "\n".join([
        temporal_grids_expected_block["Header"],
        temporal_grids_expected_block["A"],
        temporal_grids_expected_block["B"],
    ])

    block = str(temporal_grids)
    tests["Expected str"] = block == expected_block

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_temporal_grids_repr_all(
    temporal_grids_config: dict[str, dict[str, str | int]],
    temporal_grids_expected_repr: str
):
    """Does the Main class have the right repr?"""
    tests = {}

    temporal_grids = TemporalGrids.setup(
        rows=temporal_grids_config
    )

    result = repr(temporal_grids)
    tests["Expected repr"] = result == temporal_grids_expected_repr

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("bad_arg", [
    {"t_num": "BAD VALUE"},
    {"t_spacing": 0},
    {"t_min": 0},
])
def test_main_init_bad_val_types(
    temporal_grids_config: dict[str, dict[str, str | int]],
    bad_arg: dict[str, str | int]
):
    """Does the Main class error properly?"""
    bad_config = temporal_grids_config["A"] | bad_arg

    bad_key = next(iter(bad_arg.keys()))
    bad_val = type(next(iter(bad_arg.values())))

    with pytest.raises(TypeError, match=f"{bad_key}.*{bad_val}"):
        _ = TemporalGrids.setup(
            rows = {"A": bad_config}
        )


@pytest.mark.parametrize("bad_arg", [
    {"t_spacing": "BAD VALUE"},
    {"t_min": "BAD VALUE"},
])
def test_main_init_bad_val_time(
    temporal_grids_config: dict[str, dict[str, str | int]],
    bad_arg: dict[str, str | int]
):
    """Does the Main class error properly?"""
    bad_config = temporal_grids_config["A"] | bad_arg

    bad_key = next(iter(bad_arg.keys()))

    with pytest.raises(
        ValueError,
        match=f"{bad_key} is not a valid.*recognised by NAME."
    ):
        _ = TemporalGrids.setup(
            rows = {"A": bad_config}
        )


def test_main_init_bad_val_not_implemented(
    temporal_grids_config: dict[str, dict[str, str | int]],
):
    """Does the Main class error properly?"""
    bad_config = temporal_grids_config["A"] | {"t_array": "BAD VALUE"}

    with pytest.raises(NotImplementedError, match="t_array was specified"):
        _ = TemporalGrids.setup(
            rows = {"A": bad_config}
        )


