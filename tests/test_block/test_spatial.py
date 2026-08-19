from enw.block._spatial import LocationRow
from typing import no_type_check

from jinja2 import Environment
import pytest

from enw.block import (
    Domains,
    HorizontalCoords,
    HorizontalGrids,
    Locations,
    VerticalCoords,
    VerticalGrids
)


pytestmark = [
    pytest.mark.block,
    pytest.mark.block_spatial
]

@pytest.fixture
def hcoord_expected_block() -> str:
    return "\n".join([
        "Horizontal Coordinate Systems:",
        "Name"
    ])

@pytest.mark.parametrize(
    "preset_hcoord",
    [
        "Lat-Long",
        "EMEP 50km Grid",
        "EMEP 150km Grid",
        "UK National Grid (m)",
        "UK National Grid (100m)"
    ]
)
def test_init_hcoord_preset(
    preset_hcoord: str,
):
    """Does the HorizontalCoords class initialise?"""
    tests = {}
    expected_vals = {
        "names": (preset_hcoord,)
    }

    hcoords = HorizontalCoords.setup(
        names=[preset_hcoord]
    )
    vals = hcoords.__dict__

    for k, v in expected_vals.items():
        tests[f"{k} present"] = k in vals
        tests[f"{k} is expected val"] = vals.get(k) == v

    tests["Environment present"] = isinstance(
        hcoords._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize(
    "preset_hcoord",
    [
        "Lat-Long",
        "EMEP 50km Grid",
        "EMEP 150km Grid",
        "UK National Grid (m)",
        "UK National Grid (100m)"
    ]
)
def test_hcoord_str_preset(
    preset_hcoord: str,
    hcoord_expected_block: str
):
    """Does the HorizontalCoords class create the right str?"""
    tests = {}

    hcoord = HorizontalCoords.setup(
        names=[preset_hcoord]
    )
    block = str(hcoord)

    expected = "\n".join([hcoord_expected_block, preset_hcoord])
    print(block)
    print(expected)

    tests["Expected str"] = block == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize(
    "preset_hcoord",
    [
        "Lat-Long",
        "EMEP 50km Grid",
        "EMEP 150km Grid",
        "UK National Grid (m)",
        "UK National Grid (100m)"
    ]
)
def test_hcoord_repr_preset(
    preset_hcoord: str
):
    """Does the HorizontalCoords create the right repr?"""
    tests = {}

    hcoord = HorizontalCoords.setup(
        names=[preset_hcoord]
    )
    block = repr(hcoord)
    expected = "\n".join([
        "[Horizontal Coordinate Systems]",
        f"\t{preset_hcoord}"
    ])

    tests["Expected repr"] = block == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@no_type_check
def test_hcoord_bad_preset(
):
    """Does HorizontalCoords error with bad preset?"""

    with pytest.raises(
        TypeError,
        match=r"names index 0 is not a member of HorizontalCoordSystems"
    ):
        _ = HorizontalCoords.setup(
            names=["BAD NAME"]
        )


@pytest.fixture
def vcoord_expected_block() -> str:
    return "\n".join([
        "Vertical Coordinate Systems:",
        "Name"
    ])

@pytest.mark.parametrize(
    "preset_vcoord",
    [
        "m agl",
        "m asl",
        "FL",
        "Pa"
    ]
)
def test_init_vcoord_preset(
    preset_vcoord: str,
):
    """Does the VerticalCoords class initialise?"""
    tests = {}
    expected_vals = {
        "names": (preset_vcoord,)
    }

    vcoords = VerticalCoords.setup(
        names=[preset_vcoord]
    )
    vals = vcoords.__dict__

    for k, v in expected_vals.items():
        tests[f"{k} present"] = k in vals
        tests[f"{k} is expected val"] = vals.get(k) == v

    tests["Environment present"] = isinstance(
        vcoords._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize(
    "preset_vcoord",
    [
        "m agl",
        "m asl",
        "FL",
        "Pa"
    ]
)
def test_vcoord_str_preset(
    preset_vcoord: str,
    vcoord_expected_block: str
):
    """Does the VerticalCoords class create the right str?"""
    tests = {}

    vcoord = VerticalCoords.setup(
        names=[preset_vcoord]
    )
    block = str(vcoord)

    expected = "\n".join([vcoord_expected_block, preset_vcoord])

    tests["Expected str"] = block == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize(
    "preset_vcoord",
    [
        "m agl",
        "m asl",
        "FL",
        "Pa"
    ]
)
def test_vcoord_repr_preset(
    preset_vcoord: str
):
    """Does the VerticalCoords create the right repr?"""
    tests = {}

    vcoord = VerticalCoords.setup(
        names=[preset_vcoord]
    )
    block = repr(vcoord)
    expected = "\n".join([
        "[Vertical Coordinate Systems]",
        f"\t{preset_vcoord}"
    ])

    tests["Expected repr"] = block == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@no_type_check
def test_vcoord_bad_preset(
):
    """Does VerticalCoords error with bad preset?"""

    with pytest.raises(
        TypeError,
        match=r"names index 0 is not a member of VerticalCoordSystems"
    ):
        _ = VerticalCoords.setup(
            names=["BAD NAME"]
        )

def test_init_hcoord_mutliple():
    """Does the HorizontalCoords class initialise?"""
    mulvals = ("Lat-Long", "UK National Grid (m)")
    tests = {}
    expected_vals = {
        "names": mulvals
    }

    hcoords = HorizontalCoords.setup(
        names=list(mulvals)
    )
    vals = hcoords.__dict__

    for k, v in expected_vals.items():
        tests[f"{k} present"] = k in vals
        tests[f"{k} is expected val"] = vals.get(k) == v

    tests["Environment present"] = isinstance(
        hcoords._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_hcoord_str_mutliple(hcoord_expected_block: str):
    """Does the HorizontalCoords class create the right str?"""
    mulvals = ("Lat-Long", "UK National Grid (m)")
    tests = {}

    hcoord = HorizontalCoords.setup(
        names=list(mulvals)
    )
    block = str(hcoord)

    expected = "\n".join([hcoord_expected_block, *mulvals])

    tests["Expected str"] = block == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_hcoord_repr_mutliple():
    """Does the HorizontalCoords create the right repr?"""
    mulvals = ("Lat-Long", "UK National Grid (m)")
    tests = {}

    hcoord = HorizontalCoords.setup(
        names=list(mulvals)
    )
    block = repr(hcoord)
    expected = "\n".join([
        "[Horizontal Coordinate Systems]",
        "\tLat-Long",
        "\tUK National Grid (m)"
    ])

    tests["Expected repr"] = block == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_vcoord_mutliple():
    """Does the VerticalCoords class initialise?"""
    mulvals = ("m agl", "m asl")
    tests = {}
    expected_vals = {
        "names": mulvals
    }

    vcoords = VerticalCoords.setup(
        names=list(mulvals)
    )
    vals = vcoords.__dict__

    for k, v in expected_vals.items():
        tests[f"{k} present"] = k in vals
        tests[f"{k} is expected val"] = vals.get(k) == v

    tests["Environment present"] = isinstance(
        vcoords._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_vcoord_str_mutliple(vcoord_expected_block: str):
    """Does the VerticalCoords class create the right str?"""
    mulvals = ("m agl", "m asl")
    tests = {}

    vcoord = VerticalCoords.setup(
        names=list(mulvals)
    )
    block = str(vcoord)

    expected = "\n".join([vcoord_expected_block, *mulvals])

    tests["Expected str"] = block == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_vcoord_repr_mutliple():
    """Does the VerticalCoords create the right repr?"""
    mulvals = ("m agl", "m asl")
    tests = {}

    vcoord = VerticalCoords.setup(
        names=list(mulvals)
    )
    block = repr(vcoord)
    expected = "\n".join([
        "[Vertical Coordinate Systems]",
        "\tm agl",
        "\tm asl"
    ])

    tests["Expected repr"] = block == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@pytest.fixture
def preset_locations() -> dict[str, dict[str, str | float]]:
    """Preset config for locations."""
    return {
        "Test A": {
            "hcoord": "Lat-Long",
            "x": -0.73,
            "y": -21
        },
        "Test B": {
            "hcoord": "Lat-Long",
            "x": 12,
            "y": 34
        }
    }

@pytest.fixture
def locations_expected_str() -> str:
    return "\n".join([
        "Locations: Test",
        "Name,H-Coord,X,Y",
        "Test A,Lat-Long,-0.73,-21.0",
        "Test B,Lat-Long,12.0,34.0",
    ])

@pytest.fixture
def locations_expected_repr() -> str:
    return "\n".join([
        "[Locations]",
        "\t[[Test A]]",
        "\t\thcoord = Lat-Long",
        "\t\tx      = -0.73",
        "\t\ty      = -21.0",
        "\t[[Test B]]",
        "\t\thcoord = Lat-Long",
        "\t\tx      = 12.0",
        "\t\ty      = 34.0",
    ])

def test_init_location_preset(
    preset_locations: dict[str, dict[str, str | float]],
):
    """Does the Locations class initialise?"""
    tests = {}
    expected_vals = {
        "block_name": "Test",
        "rows": (
            LocationRow(name="Test A", hcoord="Lat-Long", x=-0.73, y=-21),
            LocationRow(name="Test B", hcoord="Lat-Long", x=12, y=34),
        )
    }

    locations = Locations.setup(
        rows=preset_locations,
        block_name="Test"
    )
    vals = locations.__dict__

    for k, v in expected_vals.items():
        tests[f"{k} present"] = k in vals
        tests[f"{k} is expected val"] = vals.get(k) == v

    tests["Environment present"] = isinstance(
        locations._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_location_str(
    preset_locations: dict[str, dict[str, str | float]],
    locations_expected_str: str
):
    """Does the Locations class produce the right string?"""
    tests = {}

    locations = Locations.setup(
        rows=preset_locations,
        block_name="Test"
    )

    print(str(locations))
    print(locations_expected_str)
    tests["Expected str"] = str(locations) == locations_expected_str

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_location_repr(
    preset_locations: dict[str, dict[str, str | float]],
    locations_expected_repr: str
):
    """Does the Locations class produce the right repr?"""
    tests = {}

    locations = Locations.setup(
        rows=preset_locations,
        block_name="Test"
    )

    tests["Expected repr"] = repr(locations) == locations_expected_repr

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_location_no_rows():
    """Does the locations setup error if rows aren't provided?"""
    with pytest.raises(
        ValueError,
        match=r"No rows provided for locations block\."
    ):
        _ = Locations.setup(
            rows={},
            block_name="No rows? 👀"
        )

@no_type_check
def test_init_location_bad_name():
    """Does the locations setup error if bad name?"""
    with pytest.raises(
        TypeError,
        match=r"name is not.*str.*int"
    ):
        _ = Locations.setup(
            rows={21: {"hcoord": "Lat-Long", "x": 1.0, "y": 2.0}},
            block_name="Bad name? 👀"
        )

@no_type_check
def test_init_location_bad_hcoord():
    """Does the locations setup error if bad hcoord?"""
    with pytest.raises(
        TypeError,
        match=r"hcoord is not a member of HorizontalCoordSystems"
    ):
        _ = Locations.setup(
            rows={"Bad Hcoord": {"hcoord": "BAD VALUE", "x": 1.0, "y": 2.0}},
            block_name="Bad Hcoord? 👀"
        )

@no_type_check
@pytest.mark.parametrize("bad_val", ["x", "y"])
def test_init_location_bad_xy(bad_val):
    """Does the locations setup error if bad coord?"""
    with pytest.raises(
        TypeError,
        match=r"is not.*float.*str"
    ):
        _ = Locations.setup(
            rows={
                f"Bad {bad_val}": {
                    "hcoord": "Lat-Long",
                    "x": 1.0,
                    "y": 2.0,
                } | {bad_val: "BAD VALUE"},
            },
            block_name=f"Bad {bad_val}? 👀"
        )

@no_type_check
def test_init_location_bad_block_name():
    """Does the locations setup error if bad name?"""
    with pytest.raises(
        TypeError,
        match=r"block_name is not.*str.*int"
    ):
        _ = Locations.setup(
            rows={"Test": {"hcoord": "Lat-Long", "x": 1.0, "y": 2.0}},
            block_name=21
        )


def good_h_values() -> list[dict[str, str | int | float | None]]:
    """"""
    return [
        {
            "spacing": 0.7,
            "min": -10.2,
        },
        {
            "spacing": 0.2,
            "max": 10.3
        },
        {
            "spacing": 0.9,
            "centre": 5.3
        },
        {
            "min": -10.2,
            "max": 10.3
        },
        {
            "min": -10.2,
            "centre": 5.3
        },
        {
            "min": -10.2,
            "range": 20
        },
        {
            "max": 10.3,
            "centre": 5.3
        },
        {
            "max": 10.3,
            "range": 20
        },
        {
            "centre": 10.3,
            "range": 20
        },
    ]

@pytest.fixture
def preset_horizontal_grids() -> dict[str, str]:
    """Preset config for locations."""
    return {
        "name": "Test",
        "hcoord": "Lat-Long"
    }

@pytest.mark.parametrize("x", good_h_values())
@pytest.mark.parametrize("y", good_h_values())
def test_init_horizontal_grids_preset(
    x: dict[str, str | int | float | None],
    y: dict[str, str | int | float | None],
    preset_horizontal_grids: dict[str, str]
):
    """Does the HorizontalGrids class initialise?"""
    tests = {}
    expected_vals = {
        "name": "Test",
        "hcoord": "Lat-Long",
        "x_count": 10,
        "y_count": 10,
        **{f"x_{k}": v for k, v in x.items()},
        **{f"y_{k}": v for k, v in y.items()}
    }

    args = preset_horizontal_grids
    args["x"] = {"count": 10} | x
    args["y"] = {"count": 10} | y

    hgrids = HorizontalGrids.setup(
        **args
    )
    vals = hgrids.__dict__

    for k, v in expected_vals.items():
        tests[f"{k} present"] = k in vals
        tests[f"{k} is expected val"] = vals.get(k) == v

    tests["Environment present"] = isinstance(
        hgrids._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("x", good_h_values())
@pytest.mark.parametrize("y", good_h_values())
def test_horizontal_grids_str(
    x: dict[str, str | int | float | None],
    y: dict[str, str | int | float | None],
    preset_horizontal_grids: dict[str, str]
):
    """Does the HorizontalGrids class give the right str?"""
    tests = {}
    headers = {
        "name": "Name",
        "hcoord": "H-Coord",
        "x_count": "nX",
        "x_spacing": "dX",
        "x_min": "X Min",
        "x_max": "X Max",
        "x_centre": "X Centre",
        "x_range": "X Range",
        "y_count": "nY",
        "y_spacing": "dY",
        "y_min": "Y Min",
        "y_max": "Y Max",
        "y_centre": "Y Centre",
        "y_range": "Y Range"
    }

    args = preset_horizontal_grids
    args["x"] = {"count": 10} | x
    args["y"] = {"count": 10} | y

    hgrids = HorizontalGrids.setup(
        **args
    )
    vals = hgrids.__dict__

    cols = ",".join([
        "Name,H-Coord,nX",
    ] + [
        headers[f"x_{k}"] for k in x
    ] + [
        "nY",
    ] + [
        headers[f"y_{k}"] for k in y
    ])

    values = ",".join([
        "Test,Lat-Long,10"
    ] + [
        str(vals[f"x_{k}"]) for k in x
    ] + [
            "10"
    ] + [
        str(vals[f"y_{k}"]) for k in y
    ]
    )

    expected_str = "\n".join([
        "Horizontal Grids:",
        cols,
        values
    ])
    print(repr(str(hgrids)))
    print(repr(expected_str))

    tests["Expected str"] = str(hgrids) == expected_str

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("x", good_h_values())
@pytest.mark.parametrize("y", good_h_values())
def test_horizontal_grids_repr(
    x: dict[str, str | int | float | None],
    y: dict[str, str | int | float | None],
    preset_horizontal_grids: dict[str, str]
):
    """Does the HorizontalGrids class give the right str?"""
    tests = {}

    args = preset_horizontal_grids
    args["x"] = {"count": 10} | x
    args["y"] = {"count": 10} | y

    hgrids = HorizontalGrids.setup(
        **args
    )
    expected_repr = "\n".join([
        "[Horizontal Grids]",
        "\tname                : Test",
        "\thcoord              : Lat-Long",
        "\tx_count             : 10",
        f"\tx_spacing           : {x.get("spacing")}",
        f"\tx_min               : {x.get("min")}",
        f"\tx_max               : {x.get("max")}",
        f"\tx_centre            : {x.get("centre")}",
        f"\tx_range             : {x.get("range")}",
        f"\tx_array             : {x.get("array")}",
        "\ty_count             : 10",
        f"\ty_spacing           : {y.get("spacing")}",
        f"\ty_min               : {y.get("min")}",
        f"\ty_max               : {y.get("max")}",
        f"\ty_centre            : {y.get("centre")}",
        f"\ty_range             : {y.get("range")}",
        f"\ty_array             : {y.get("array")}",
    ])

    tests["Expected repr"] = repr(hgrids) == expected_repr

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@no_type_check
def test_init_horizontal_grids_bad_name(
    preset_horizontal_grids: dict[str, str]
):
    """Does the HorizontalGrids class error with bad name?"""
    args = preset_horizontal_grids | {
        "x": {
            "count": 10,
            "spacing": 0.1,
            "min": -7.3
        },
        "y": {
            "count": 10,
            "spacing": 0.1,
            "min": -7.3
        },
    }

    args["name"] = 23

    with pytest.raises(TypeError, match=r"name.*str.*int"):
        _ = HorizontalGrids.setup(**args)


@no_type_check
def test_init_horizontal_grids_bad_hcoord(
    preset_horizontal_grids: dict[str, str]
):
    """Does the HorizontalGrids class error with bad hcoord?"""
    args = preset_horizontal_grids | {
        "x": {
            "count": 10,
            "spacing": 0.1,
            "min": -7.3
        },
        "y": {
            "count": 10,
            "spacing": 0.1,
            "min": -7.3
        },
    }

    args["hcoord"] = "BAD VALUE"

    with pytest.raises(
        TypeError,
        match=r"hcoord is not a member of HorizontalCoordSystems"
    ):
        _ = HorizontalGrids.setup(**args)

@no_type_check
@pytest.mark.parametrize("axis", ["x", "y"])
def test_init_horizontal_grids_too_many(
    preset_horizontal_grids: dict[str, str],
    axis: str
):
    """Does the HorizontalGrids class error with bad hcoord?"""
    args = preset_horizontal_grids | {
        "x": {
            "count": 10,
            "spacing": 0.1,
            "min": -7.3
        },
        "y": {
            "count": 10,
            "spacing": 0.1,
            "min": -7.3
        },
    }

    args[axis]["max"] = 7.3

    with pytest.raises(
        ValueError,
        match=r"Incorrect number of values provided for [xy]\."
    ):
        _ = HorizontalGrids.setup(**args)

@no_type_check
@pytest.mark.parametrize("axis", ["x", "y"])
def test_init_horizontal_grids_mutually_exclusive(
    preset_horizontal_grids: dict[str, str],
    axis: str
):
    """Does the HorizontalGrids class error with bad hcoord?"""
    args = preset_horizontal_grids | {
        "x": {
            "count": 10,
            "spacing": 0.1,
            "min": -7.3
        },
        "y": {
            "count": 10,
            "spacing": 0.1,
            "min": -7.3
        },
    }

    args[axis].pop("min")
    args[axis]["range"] = 100

    with pytest.raises(
        ValueError,
        match=r"Both [xy]\.spacing and [xy]\.range are set"
    ):
        _ = HorizontalGrids.setup(**args)

@no_type_check
@pytest.mark.parametrize("axis", ["x", "y"])
def test_init_horizontal_grids_bad_key(
    preset_horizontal_grids: dict[str, str],
    axis: str
):
    """Does the HorizontalGrids class error with bad hcoord?"""
    args = preset_horizontal_grids | {
        "x": {
            "count": 10,
            "spacing": 0.1,
            "min": -0.3
        },
        "y": {
            "count": 10,
            "spacing": 0.1,
            "min": -0.3
        },
    }

    args[axis].pop("min")
    args[axis]["BAD KEY"] = 100

    with pytest.raises(
        ValueError,
        match=r"Unexpected keys in [xy]: {'BAD KEY'}"
    ):
        _ = HorizontalGrids.setup(**args)


@no_type_check
@pytest.mark.parametrize("axis", ["x", "y"])
@pytest.mark.parametrize(
    "bad_key",
    ["min", "max", "spacing", "centre", "range"]
)
def test_init_horizontal_grids_not_float_value(
    preset_horizontal_grids: dict[str, str],
    axis: str,
    bad_key: str
):
    """Does the HorizontalGrids class error with bad x or y float?"""
    other_key = "min" if bad_key != "min" else "max"
    args = preset_horizontal_grids | {
        "x": {
            "count": 10,
            "spacing": 0.1,
            "min": -0.3
        },
        "y": {
            "count": 10,
            "spacing": 0.1,
            "min": -0.3
        },
    } | {
        axis: {
            "count": 10,
            other_key: 0.01,
            bad_key: "BAD VALUE"
        }
    }

    with pytest.raises(
        TypeError,
        match=f"{axis}.{bad_key} is not .*float.*str"
    ):
        _ = HorizontalGrids.setup(**args)


@no_type_check
@pytest.mark.parametrize("axis", ["x", "y"])
def test_init_horizontal_grids_count_not_int(
    preset_horizontal_grids: dict[str, str],
    axis: str
):
    """Does the HorizontalGrids class error with bad count value?"""
    args = preset_horizontal_grids | {
        "x": {
            "count": 10,
            "spacing": 0.1,
            "min": -7.3
        },
        "y": {
            "count": 10,
            "spacing": 0.1,
            "min": -7.3
        },
    }

    args[axis]["count"] = "BAD VALUE"

    with pytest.raises(
        TypeError,
        match=r"[xy].count is not.*int.*str"
    ):
        _ = HorizontalGrids.setup(**args)


@no_type_check
@pytest.mark.parametrize("axis", ["x", "y"])
def test_init_horizontal_grids_array_not_implemented(
    preset_horizontal_grids: dict[str, str],
    axis: str
):
    """Does the HorizontalGrids class error with bad count value?"""
    args = preset_horizontal_grids | {
        "x": {
            "count": 10,
            "spacing": 0.1,
            "min": -7.3
        },
        "y": {
            "count": 10,
            "spacing": 0.1,
            "min": -7.3
        },
    }

    args[axis].pop("min")
    args[axis]["array"] = "HELLO"

    with pytest.raises(
        NotImplementedError,
        match=r"Array not implemented for HorizontalGrids."
    ):
        _ = HorizontalGrids.setup(**args)


@pytest.fixture
def preset_vertical_grids() -> dict[str, str | float | int]:
    """Preset config for locations."""
    return {
        "name": "Test",
        "zcoord": "m asl",
        "count": 100,
        "spacing": 0.01,
        "min_point": 10
    }

def test_init_vertical_grids_preset(
    preset_vertical_grids: dict[str, str | float | int]
):
    """Does the VerticalGrids class initialise?"""
    tests = {}
    expected_vals = preset_vertical_grids

    args = preset_vertical_grids

    hgrids = VerticalGrids.setup(
        **args
    )
    vals = hgrids.__dict__

    for k, v in expected_vals.items():
        tests[f"{k} present"] = k in vals
        tests[f"{k} is expected val"] = vals.get(k) == v

    tests["Environment present"] = isinstance(
        hgrids._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@pytest.mark.parametrize(
    "array_key",
    ["array_name", "av_array_name", "index_array_name"]
)
def test_init_vertical_grids_error_array(
    preset_vertical_grids: dict[str, str | float | int],
    array_key: str
):
    """Does the VerticalGrids class initialise?"""
    args = preset_vertical_grids | {array_key: "Bad value"}

    with pytest.raises(
        NotImplementedError,
        match="Array not implemented for VerticalGrids"
    ):
        _ = VerticalGrids.setup(
            **args
        )


@pytest.mark.parametrize("count", [None, 100])
@pytest.mark.parametrize("spacing", [None, 10])
@pytest.mark.parametrize("min_point", [None, 20])
def test_vertical_grids_str(
    count: int | None,
    spacing: int | None,
    min_point: int | None,
):
    """Does the VerticalGrids class give the right str?"""
    tests = {}
    base_config = {
        "name": "Test",
        "zcoord": "m agl"
    }
    extra_config = {}
    if count is not None:
        extra_config = extra_config | {"count": count}
    if spacing is not None:
        extra_config = extra_config | {"spacing": spacing}
    if min_point is not None:
        extra_config = extra_config | {"min_point": min_point}

    args = base_config | extra_config

    headers = {
        "name": "Name",
        "zcoord": "Z-Coord",
        "count": "nZ",
        "spacing": "dZ",
        "min_point": "Z0",
    }

    vgrids = VerticalGrids.setup(
        **args
    )

    cols = ",".join([
        "Name,Z-Coord",
    ] + [
        headers[k] for k in extra_config
    ])

    values = ",".join([
        "Test,m agl"
    ] + [
        str(v) for v in extra_config.values()
    ])

    expected_str = "\n".join([
        "Vertical Grids:",
        cols,
        values
    ])

    print(str(vgrids))
    print(expected_str)

    tests["Expected str"] = str(vgrids) == expected_str

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("count", [None, 100])
@pytest.mark.parametrize("spacing", [None, 10])
@pytest.mark.parametrize("min_point", [None, 20])
def test_vertical_grids_repr(
    count: int | None,
    spacing: int | None,
    min_point: int | None,
):
    """Does the VerticalGrids class give the right repr?"""
    tests = {}
    base_config = {
        "name": "Test",
        "zcoord": "m agl"
    }
    extra_config = {}
    if count is not None:
        extra_config = extra_config | {"count": count}
    if spacing is not None:
        extra_config = extra_config | {"spacing": spacing}
    if min_point is not None:
        extra_config = extra_config | {"min_point": min_point}

    args = base_config | extra_config

    vgrids = VerticalGrids.setup(
        **args
    )
    expected_repr = "\n".join([
        "[Vertical Grids]",
        "\tname                : Test",
        "\tzcoord              : m agl",
        f"\tcount               : {extra_config.get('count')}",
        f"\tspacing             : {extra_config.get('spacing')}",
        f"\tmin_point           : {extra_config.get('min_point')}",
        "\tarray_name          : None",
        "\tav_array_name       : None",
        "\tindex_array_name    : None",
    ])

    tests["Expected repr"] = repr(vgrids) == expected_repr

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@no_type_check
def test_init_vertical_grids_bad_name(
    preset_vertical_grids: dict[str, str]
):
    """Does the VerticalGrids class error with bad name?"""
    args = preset_vertical_grids

    args["name"] = 23

    with pytest.raises(TypeError, match=r"name.*str.*int"):
        _ = VerticalGrids.setup(**args)


@no_type_check
def test_init_vertical_grids_bad_zcoord(
    preset_vertical_grids: dict[str, str]
):
    """Does the VerticalGrids class error with bad zcoord?"""
    args = preset_vertical_grids

    args["zcoord"] = "BAD VALUE"

    with pytest.raises(
        TypeError,
        match=r"zcoord.*VerticalCoordSystems.*BAD VALUE"
    ):
        _ = VerticalGrids.setup(**args)


@no_type_check
@pytest.mark.parametrize(
    "bad_key",
    ["count", "spacing", "min_point"]
)
def test_init_vertical_grids_not_float_value(
    preset_vertical_grids: dict[str, str],
    bad_key: str
):
    """Does the HorizontalGrids class error with bad x or y float?"""
    args = preset_vertical_grids | {bad_key: "BAD VALUE"}

    with pytest.raises(
        TypeError,
        match=f"{bad_key} is not .*float.*str"
    ):
        _ = VerticalGrids.setup(**args)


@pytest.fixture
def preset_domains() -> dict[str, str | float | int]:
    """Preset config for locations."""
    return {
        "name": "Test",
        "hcoord": "Lat-Long",
        "zcoord": "m agl",
    }


def good_t_values() -> list[dict[str, str | bool]]:
    """"""
    return [
        {"start": "01/05/2025 01:00", "end": "21/05/2025 01:00"},
        {"start": "15/01/2025 01:00", "duration": "24:00"},
        {"duration": "24:00", "end": "21/01/2025 01:00"},
        {"unbounded": True},
    ]


def good_h_values_domain() -> list[dict[str, str | int | float | None]]:
    """"""
    return [
        {
            "min": -10.2,
            "max": 10.3
        },
        {
            "min": -10.2,
            "centre": 5.3
        },
        {
            "min": -10.2,
            "range": 20
        },
        {
            "max": 10.3,
            "centre": 5.3
        },
        {
            "max": 10.3,
            "range": 20
        },
        {
            "centre": 10.3,
            "range": 20
        },
    ]

@pytest.mark.parametrize("x", [*good_h_values_domain(), {"unbounded": True}])
@pytest.mark.parametrize("y", [*good_h_values_domain(), {"unbounded": True}])
@pytest.mark.parametrize("z", [{"max": 30}, {"unbounded": True}])
@pytest.mark.parametrize("t", good_t_values())
def test_init_domains_preset(
    x: dict[str, str | int | float | None],
    y: dict[str, str | int | float | None],
    z: dict[str, int | bool],
    t: dict[str, str | bool],
    preset_domains: dict[str, str | float | int]
):
    """Does the Domains class initialise?"""
    tests = {}
    args = preset_domains | {
        "x": x
    } | {
        "y": y
    } | {
        "t": t | {"max_travel_time": "24:00"}
    } | {
        "z": z
    }

    expected_vals = {
        "name": "Test",
        "hcoord": "Lat-Long",
        "zcoord": "m agl",
        **{f"x_{k}": v for k, v in x.items()},
        **{f"y_{k}": v for k, v in y.items()},
        **{f"z_{k}": v for k, v in z.items()},
        "start_time": t.get("start"),
        "end_time": t.get("end"),
        "duration": t.get("duration"),
        "max_travel_time": "24:00"
    }

    if x.get("unbounded") is not None:
        expected_vals["x_unbounded"] = "Yes" if x["unbounded"] else "No"
    if y.get("unbounded") is not None:
        expected_vals["y_unbounded"] = "Yes" if y["unbounded"] else "No"
    if z.get("unbounded") is not None:
        expected_vals["z_unbounded"] = "Yes" if z["unbounded"] else "No"
    if t.get("unbounded") is not None:
        expected_vals["t_unbounded"] = "Yes" if t["unbounded"] else "No"

    domains = Domains.setup(rows=[args])
    vals = domains.rows[0].__dict__

    for k, v in expected_vals.items():
        tests[f"{k} present"] = k in vals
        tests[f"{k} is expected val"] = vals.get(k) == v

    tests["Environment present"] = isinstance(
        domains._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("x", [*good_h_values_domain(), {"unbounded": True}])
@pytest.mark.parametrize("y", [*good_h_values_domain(), {"unbounded": True}])
@pytest.mark.parametrize("z", [{"max": 30}, {"unbounded": True}])
@pytest.mark.parametrize("t", good_t_values())
def test_init_domains_str(
    x: dict[str, str | int | float | None],
    y: dict[str, str | int | float | None],
    z: dict[str, int | bool],
    t: dict[str, str | bool],
    preset_domains: dict[str, str | float | int]
):
    """Does the Domains class give the right str?"""
    tests = {}
    args = preset_domains | {
        "x": x
    } | {
        "y": y
    } | {
        "t": t | {"max_travel_time": "24:00"}
    } | {
        "z": z
    }

    headers = {
        "name": "Name",
        "h_unbounded": "H Unbounded?",
        "x_unbounded": "X Unbounded?",
        "y_unbounded": "Y Unbounded?",
        "z_unbounded": "Z Unbounded?",
        "t_unbounded": "T Unbounded?",
        "start_time": "Start Time",
        "end_time": "End Time",
        "duration": "Duration",
        "max_travel_time": "Max Travel Time",
        "hcoord": "H-Coord",
        "zcoord": "Z-Coord",
        "x_spacing": "dX",
        "x_min": "X Min",
        "x_max": "X Max",
        "x_centre": "X Centre",
        "x_range": "X Range",
        "y_spacing": "dY",
        "y_min": "Y Min",
        "y_max": "Y Max",
        "y_centre": "Y Centre",
        "y_range": "Y Range",
        "z_max": "Z Max",
    }

    expected_vals = {
        "name": "Test",
        "max_travel_time": "24:00",
        "h_unbounded": None,
        "x_unbounded": x.get("unbounded"),
        "y_unbounded": y.get("unbounded"),
        "z_unbounded": z.get("unbounded"),
        "t_unbounded": t.get("unbounded"),
        "hcoord": "Lat-Long",
        "zcoord": "m agl",
        "start_time": t.get("start"),
        "end_time": t.get("end"),
        "duration": t.get("duration"),
        **{f"x_{k}": v for k, v in x.items()},
        **{f"y_{k}": v for k, v in y.items()},
        **{f"z_{k}": v for k, v in z.items()},
    }

    if x.get("unbounded") is not None:
        expected_vals["x_unbounded"] = "Yes" if x["unbounded"] else "No"
    if y.get("unbounded") is not None:
        expected_vals["y_unbounded"] = "Yes" if y["unbounded"] else "No"
    if z.get("unbounded") is not None:
        expected_vals["z_unbounded"] = "Yes" if z["unbounded"] else "No"
    if t.get("unbounded") is not None:
        expected_vals["t_unbounded"] = "Yes" if t["unbounded"] else "No"

    cols = ",".join([
        headers[k] for k, v in expected_vals.items() if v is not None
    ])

    values = ",".join([
        str(v) for v in expected_vals.values() if v is not None
    ])

    domains = Domains.setup(rows=[args])

    expected_str = "\n".join([
        "Domains:",
        cols,
        values
    ])

    print(str(domains))
    print(expected_str)

    tests["Expected str"] = str(domains) == expected_str

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("x", [*good_h_values_domain(), {"unbounded": True}])
@pytest.mark.parametrize("y", [*good_h_values_domain(), {"unbounded": True}])
@pytest.mark.parametrize("z", [{"max": 30}, {"unbounded": True}])
@pytest.mark.parametrize("t", good_t_values())
def test_init_domains_repr(
    x: dict[str, str | int | float | None],
    y: dict[str, str | int | float | None],
    z: dict[str, int | bool],
    t: dict[str, str | bool],
    preset_domains: dict[str, str | float | int]
):
    """Does the Domains class give the right str?"""
    tests = {}
    args = preset_domains | {
        "x": x
    } | {
        "y": y
    } | {
        "t": t | {"max_travel_time": "24:00"}
    } | {
        "z": z
    }

    expected_vals = {
        "hcoord": "Lat-Long",
        "zcoord": "m agl",
        "max_travel_time": "24:00",
        "h_unbounded": None,
        "x_unbounded": x.get("unbounded"),
        "y_unbounded": y.get("unbounded"),
        "z_unbounded": z.get("unbounded"),
        "t_unbounded": t.get("unbounded"),
        "start_time": t.get("start"),
        "end_time": t.get("end"),
        "duration": t.get("duration"),
        "x_min": x.get("min"),
        "x_max": x.get("max"),
        "x_centre": x.get("centre"),
        "x_range": x.get("range"),
        "y_min": y.get("min"),
        "y_max": y.get("max"),
        "y_centre": y.get("centre"),
        "y_range": y.get("range"),
        "z_max": z.get("max"),
        "location_block_name": None,
        "location": None,
    }

    if x.get("unbounded") is not None:
        expected_vals["x_unbounded"] = "Yes" if x["unbounded"] else "No"
    if y.get("unbounded") is not None:
        expected_vals["y_unbounded"] = "Yes" if y["unbounded"] else "No"
    if z.get("unbounded") is not None:
        expected_vals["z_unbounded"] = "Yes" if z["unbounded"] else "No"
    if t.get("unbounded") is not None:
        expected_vals["t_unbounded"] = "Yes" if t["unbounded"] else "No"


    domains = Domains.setup(rows=[args])

    expected_repr = "\n".join([
        "[Domains]",
        "\t[[Test]]"
    ] + [
        f"\t\t{k:<20}: {v}" for k, v in expected_vals.items()
    ])


    print(repr(domains))
    print(expected_repr)

    tests["Expected repr"] = repr(domains) == expected_repr

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@pytest.mark.parametrize("z", [{"max": 30}, {"unbounded": True}])
@pytest.mark.parametrize("t", good_t_values())
def test_init_domains_preset_h_unbounded(
    z: dict[str, int | bool],
    t: dict[str, str | bool],
    preset_domains: dict[str, str | float | int]
):
    """Does the Domains class initialise?"""
    tests = {}
    args = preset_domains | {
        "h_unbounded": True
    } | {
        "t": t | {"max_travel_time": "24:00"}
    } | {
        "z": z
    }

    expected_vals = {
        "h_unbounded": "Yes",
        "hcoord": "Lat-Long",
        "zcoord": "m agl",
        **{f"z_{k}": v for k, v in z.items()},
        "start_time": t.get("start"),
        "end_time": t.get("end"),
        "duration": t.get("duration"),
        "max_travel_time": "24:00"
    }

    if z.get("unbounded") is not None:
        expected_vals["z_unbounded"] = "Yes" if z["unbounded"] else "No"
    if t.get("unbounded") is not None:
        expected_vals["t_unbounded"] = "Yes" if t["unbounded"] else "No"

    domains = Domains.setup(rows=[args])
    vals = domains.rows[0].__dict__

    for k, v in expected_vals.items():
        tests[f"{k} present"] = k in vals
        tests[f"{k} is expected val"] = vals.get(k) == v

    tests["Environment present"] = isinstance(
        domains._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("loc_name", ["location", "location_block_name"])
def test_init_domains_bad_loc_name(
    loc_name: str,
    preset_domains: dict[str, str | float | int]
):
    """Does the Domains class initialise?"""
    args = preset_domains | {
        "h_unbounded": True,
        "t": {
            "start": "12/01/2025 01:00",
            "duration": "24:00",
            "max_travel_time": "24:00",
        },
        "z": {"max": 30},
        loc_name: "BAD VALUE"
    }

    with pytest.raises(
        NotImplementedError,
        match=r"Specific location not implemented for Domains\."
    ):
        _ = Domains.setup(rows=[args])


@pytest.mark.parametrize("axis", ["x", "y"])
def test_init_domains_bad_h_unbounded_with_value(
    axis: str,
    preset_domains: dict[str, str | float | int]
):
    """Does the Domains class initialise?"""
    other = {
        "x": {
            "min": -10.2,
            "max": 10.3
        },
        "y": {
            "min": -10.2,
            "max": 10.3
        },
    }
    args = preset_domains | {
        "h_unbounded": True,
        "t": {
            "start": "12/01/2025 01:00",
            "duration": "24:00",
            "max_travel_time": "24:00",
        },
        "z": {"max": 30}
    }
    args[axis] = other[axis]

    with pytest.raises(
        ValueError,
        match=r"Both h_unbounded and [xy] are set, but these are mutually"
    ):
        _ = Domains.setup(rows=[args])

@pytest.mark.parametrize("axis", ["x", "y", "z", "t"])
def test_init_domains_bad_axis_unbounded_with_value(
    axis: str,
    preset_domains: dict[str, str | float | int]
):
    """Does the Domains class initialise?"""
    args = preset_domains | {
        "t": {
            "start": "12/01/2025 01:00",
            "duration": "24:00",
            "max_travel_time": "24:00",
        },
        "x": {
            "min": -10.2,
            "max": 10.3
        },
        "y": {
            "min": -10.2,
            "max": 10.3
        },
        "z": {"max": 30}
    }
    args[axis]["unbounded"] = True

    with pytest.raises(
        ValueError,
        match=r"Specific values provided for [xyzt] when unbounded."
    ):
        _ = Domains.setup(rows=[args])


@pytest.mark.parametrize("axis", ["x", "y"])
def test_init_domains_bad_too_many_vals(
    axis: str,
    preset_domains: dict[str, str | float | int]
):
    """Does the Domains class initialise?"""
    args = preset_domains | {
        "t": {
            "start": "12/01/2025 01:00",
            "duration": "24:00",
            "max_travel_time": "24:00",
        },
        "x": {
            "min": -10.2,
            "max": 10.3
        },
        "y": {
            "min": -10.2,
            "max": 10.3
        },
        "z": {"max": 30}
    }
    args[axis]["range"] = 10

    with pytest.raises(
        ValueError,
        match=r"Incorrect number of values provided for [xy]\. Expected 2\."
    ):
        _ = Domains.setup(rows=[args])


@pytest.mark.parametrize("axis", ["x", "y", "z", "t"])
def test_init_domains_bad_key(
    axis: str,
    preset_domains: dict[str, str | float | int]
):
    """Does the Domains class initialise?"""
    args = preset_domains | {
        "t": {
            "start": "12/01/2025 01:00",
            "duration": "24:00",
            "max_travel_time": "24:00",
        },
        "x": {
            "min": -10.2,
            "max": 10.3
        },
        "y": {
            "min": -10.2,
            "max": 10.3
        },
        "z": {"max": 30}
    }
    if axis in ("x", "y"):
        args[axis].pop("max")
    args[axis]["BAD KEY"] = "BAD VALUE"

    with pytest.raises(
        ValueError,
        match=r"Unexpected keys in [xzyt]:.*BAD KEY.*"
    ):
        _ = Domains.setup(rows=[args])


def test_init_domains_bad_no_max_travel_time(
    preset_domains: dict[str, str | float | int]
):
    """Does the Domains class initialise?"""
    args = preset_domains | {
        "t": {
            "start": "12/01/2025 01:00",
            "duration": "24:00",
        },
        "x": {
            "min": -10.2,
            "max": 10.3
        },
        "y": {
            "min": -10.2,
            "max": 10.3
        },
        "z": {"max": 30}
    }

    with pytest.raises(
        ValueError,
        match=r"max_travel_time not provided for t\."
    ):
        _ = Domains.setup(rows=[args])


def test_init_domains_descriptive_time_intervals(
    preset_domains: dict[str, str | float | int]
):
    """Does the Domains class initialise?"""
    args = preset_domains | {
        "t": {
            "start": "-12 day",
            "end": "-6 day",
            "max_travel_time": "72:00"
        },
        "x": {
            "min": -10.2,
            "max": 10.3
        },
        "y": {
            "min": -10.2,
            "max": 10.3
        },
        "z": {"max": 30}
    }

    _ = Domains.setup(rows=[args])


def test_init_domains_nondescriptive_time_intervals(
    preset_domains: dict[str, str | float | int]
):
    """Does the Domains class initialise?"""
    args = preset_domains | {
        "t": {
            "start": "-1d 02:00",
            "end": "2d 01:00",
            "max_travel_time": "72:00"
        },
        "x": {
            "min": -10.2,
            "max": 10.3
        },
        "y": {
            "min": -10.2,
            "max": 10.3
        },
        "z": {"max": 30}
    }

    _ = Domains.setup(rows=[args])


@pytest.mark.parametrize("bad_time", ["start", "end"])
def test_init_domains_bad_time_interval(
    preset_domains: dict[str, str | float | int],
    bad_time: str
):
    """Does the Domains class initialise?"""
    args = preset_domains | {
        "t": {
            "start": "-1d 02:00",
            "end": "2d 01:00",
            "max_travel_time": "72:00"
        },
        "x": {
            "min": -10.2,
            "max": 10.3
        },
        "y": {
            "min": -10.2,
            "max": 10.3
        },
        "z": {"max": 30}
    }
    args["t"][bad_time] = "BAD VALUE"

    with pytest.raises(
        ValueError,
        match=rf"{bad_time}_time is not in datetime or time interval format\."
    ):
        _ = Domains.setup(rows=[args])


def test_init_multi_domains_preset():
    """Does the Domains class initialise with 2 rows?"""
    tests = {}
    args = [
        {
            "name": "Row 1",
            "hcoord": "Lat-Long",
            "zcoord": "m agl",
            "x": {
                "min": -10.2,
                "max": 10.3
            },
            "y": {
                "min": -10.2,
                "centre": 5.3
            },
            "z": {
                "max": 30,
            },
            "t": {
                "start": "01/05/2025 01:00",
                "end": "21/05/2025 01:00",
                "max_travel_time": "48:00"
            }
        },
        {
            "name": "Row 2",
            "hcoord": "Lat-Long",
            "zcoord": "m agl",
            "x": {
                "min": -10.2,
                "range": 20
            },
            "y": {
                "max": 10.3,
                "centre": 5.3
            },
            "z": {
                "unbounded": True,
            },
            "t": {
                "start": "15/01/2025 01:00",
                "duration": "24:00",
                "max_travel_time": "24:00"
            }
        }
    ]

    expected_vals = [
        {
            "name": "Row 1",
            "hcoord": "Lat-Long",
            "zcoord": "m agl",
            "x_min": -10.2,
            "x_max": 10.3,
            "y_min": -10.2,
            "y_centre": 5.3,
            "z_max": 30,
            "start_time": "01/05/2025 01:00",
            "end_time": "21/05/2025 01:00",
            "max_travel_time": "48:00"
        },
        {
            "name": "Row 2",
            "hcoord": "Lat-Long",
            "zcoord": "m agl",
            "x_min": -10.2,
            "x_range": 20,
            "y_max": 10.3,
            "y_centre": 5.3,
            "z_unbounded": "Yes",
            "start_time": "15/01/2025 01:00",
            "duration": "24:00",
            "max_travel_time": "24:00"
        }
    ]


    domains = Domains.setup(rows=args)

    for i, row in enumerate(expected_vals):
        vals = domains.rows[i].__dict__
        for k, v in row.items():
            tests[f"{i}.{k} present"] = k in vals
            tests[f"{i}.{k} is expected val"] = vals.get(k) == v

    tests["Environment present"] = isinstance(
        domains._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_multi_domains_str():
    """Does the Domains class give the right str?"""
    tests = {}
    args = [
        {
            "name": "Row 1",
            "hcoord": "Lat-Long",
            "zcoord": "m agl",
            "x": {
                "min": -10.2,
                "max": 10.3
            },
            "y": {
                "min": -10.2,
                "centre": 5.3
            },
            "z": {
                "max": 30,
            },
            "t": {
                "start": "01/05/2025 01:00",
                "end": "21/05/2025 01:00",
                "max_travel_time": "48:00"
            }
        },
        {
            "name": "Row 2",
            "hcoord": "Lat-Long",
            "zcoord": "m agl",
            "x": {
                "min": -10.2,
                "range": 20
            },
            "y": {
                "max": 10.3,
                "centre": 5.3
            },
            "z": {
                "unbounded": True,
            },
            "t": {
                "start": "15/01/2025 01:00",
                "duration": "24:00",
                "max_travel_time": "24:00"
            }
        }
    ]

    expected_vals = [
        {
            "name": "Row 1",
            "hcoord": "Lat-Long",
            "zcoord": "m agl",
            "x_min": -10.2,
            "x_max": 10.3,
            "y_min": -10.2,
            "y_centre": 5.3,
            "z_max": 30,
            "start_time": "01/05/2025 01:00",
            "end_time": "21/05/2025 01:00",
            "max_travel_time": "48:00"
        },
        {
            "name": "Row 2",
            "hcoord": "Lat-Long",
            "zcoord": "m agl",
            "x_min": -10.2,
            "x_range": 20,
            "y_max": 10.3,
            "y_centre": 5.3,
            "z_unbounded": "Yes",
            "start_time": "15/01/2025 01:00",
            "duration": "24:00",
            "max_travel_time": "24:00"
        }
    ]

    valid_cols = [
        "name",
        "max_travel_time",
        "z_unbounded",
        "hcoord",
        "zcoord",
        "start_time",
        "end_time",
        "duration",
        "x_min",
        "x_max",
        "x_range",
        "y_min",
        "y_max",
        "y_centre",
        "z_max"
    ]


    domains = Domains.setup(rows=args)

    headers = {
        "name": "Name",
        "h_unbounded": "H Unbounded?",
        "x_unbounded": "X Unbounded?",
        "y_unbounded": "Y Unbounded?",
        "z_unbounded": "Z Unbounded?",
        "t_unbounded": "T Unbounded?",
        "start_time": "Start Time",
        "end_time": "End Time",
        "duration": "Duration",
        "max_travel_time": "Max Travel Time",
        "hcoord": "H-Coord",
        "zcoord": "Z-Coord",
        "x_spacing": "dX",
        "x_min": "X Min",
        "x_max": "X Max",
        "x_centre": "X Centre",
        "x_range": "X Range",
        "y_spacing": "dY",
        "y_min": "Y Min",
        "y_max": "Y Max",
        "y_centre": "Y Centre",
        "y_range": "Y Range",
        "z_max": "Z Max",
    }

    cols = ",".join([headers[k] for k in valid_cols])
    value_list = [
        ",".join([
            str(row.get(k, "")) for k in valid_cols
        ]) for row in expected_vals
    ]
    values = "\n".join(value_list)


    expected_str = "\n".join([
        "Domains:",
        cols,
        values
    ])

    print(str(domains))
    print(expected_str)

    tests["Expected str"] = str(domains) == expected_str

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_multi_domains_repr(
):
    """Does the Domains class give the right str?"""
    tests = {}
    args = [
        {
            "name": "Row 1",
            "hcoord": "Lat-Long",
            "zcoord": "m agl",
            "x": {
                "min": -10.2,
                "max": 10.3
            },
            "y": {
                "min": -10.2,
                "centre": 5.3
            },
            "z": {
                "max": 30,
            },
            "t": {
                "start": "01/05/2025 01:00",
                "end": "21/05/2025 01:00",
                "max_travel_time": "48:00"
            }
        },
        {
            "name": "Row 2",
            "hcoord": "Lat-Long",
            "zcoord": "m agl",
            "x": {
                "min": -10.2,
                "range": 20
            },
            "y": {
                "max": 10.3,
                "centre": 5.3
            },
            "z": {
                "unbounded": True,
            },
            "t": {
                "start": "15/01/2025 01:00",
                "duration": "24:00",
                "max_travel_time": "24:00"
            }
        }
    ]

    expected_vals = [
        {
            "name": "Row 1",
            "hcoord": "Lat-Long",
            "zcoord": "m agl",
            "max_travel_time": "48:00",
            "h_unbounded": None,
            "x_unbounded": None,
            "y_unbounded": None,
            "z_unbounded": None,
            "t_unbounded": None,
            "start_time": "01/05/2025 01:00",
            "end_time": "21/05/2025 01:00",
            "duration": None,
            "x_min": -10.2,
            "x_max": 10.3,
            "x_centre": None,
            "x_range": None,
            "y_min": -10.2,
            "y_max": None,
            "y_centre": 5.3,
            "y_range": None,
            "z_max": 30,
            "location_block_name": None,
            "location": None
        },
        {
            "name": "Row 2",
            "hcoord": "Lat-Long",
            "zcoord": "m agl",
            "max_travel_time": "24:00",
            "h_unbounded": None,
            "x_unbounded": None,
            "y_unbounded": None,
            "z_unbounded": "Yes",
            "t_unbounded": None,
            "start_time": "15/01/2025 01:00",
            "end_time": None,
            "duration": "24:00",
            "x_min": -10.2,
            "x_max": None,
            "x_centre": None,
            "x_range": 20,
            "y_min": None,
            "y_max": 10.3,
            "y_centre": 5.3,
            "y_range": None,
            "z_max": None,
            "location_block_name": None,
            "location": None
        }
    ]

    domains = Domains.setup(rows=args)

    expected_repr_list = ["[Domains]"]
    for row in expected_vals:
        expected_repr_list.append(f"\t[[{row["name"]}]]")
        expected_repr_list.extend([
            f"\t\t{k:<20}: {v}" for k, v in row.items()
            if k != "name"
        ])
    expected_repr = "\n".join(expected_repr_list)

    print(repr(domains))
    print(expected_repr)

    tests["Expected repr"] = repr(domains) == expected_repr

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

def test_init_multi_domains_preset_h_unbounded(
):
    """Does the Domains class initialise?"""
    tests = {}
    args = [
        {
            "name": "Row 1",
            "hcoord": "Lat-Long",
            "zcoord": "m agl",
            "h_unbounded": True,
            "z": {
                "max": 30,
            },
            "t": {
                "start": "01/05/2025 01:00",
                "end": "21/05/2025 01:00",
                "max_travel_time": "48:00"
            }
        },
        {
            "name": "Row 2",
            "hcoord": "Lat-Long",
            "zcoord": "m agl",
            "h_unbounded": True,
            "z": {
                "unbounded": True,
            },
            "t": {
                "start": "15/01/2025 01:00",
                "duration": "24:00",
                "max_travel_time": "24:00"
            }
        }
    ]

    expected_vals = [
        {
            "name": "Row 1",
            "hcoord": "Lat-Long",
            "zcoord": "m agl",
            "h_unbounded": "Yes",
            "z_max": 30,
            "start_time": "01/05/2025 01:00",
            "end_time": "21/05/2025 01:00",
            "max_travel_time": "48:00"
        },
        {
            "name": "Row 2",
            "hcoord": "Lat-Long",
            "zcoord": "m agl",
            "h_unbounded": "Yes",
            "z_unbounded": "Yes",
            "start_time": "15/01/2025 01:00",
            "duration": "24:00",
            "max_travel_time": "24:00"
        }
    ]


    domains = Domains.setup(rows=args)


    for i, row in enumerate(expected_vals):
        vals = domains.rows[i].__dict__
        for k, v in row.items():
            tests[f"{i}.{k} present"] = k in vals
            tests[f"{i}.{k} is expected val"] = vals.get(k) == v

    tests["Environment present"] = isinstance(
        domains._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())
