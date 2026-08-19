from jinja2 import Environment
import pytest

from enw.block import (
    NWPMetDefinitions,
    NWPMetModuleInstances,
    NWPMetFileStructureDefinitions
)
from enw.block._met import (
    NWPMetDefinitionsRow,
    NWPMetModuleInstancesRow,
    NWPMetFileStructureDefinitionsRow
)

pytestmark = [
    pytest.mark.block,
    pytest.mark.block_met
]

@pytest.fixture
def preset_definitions() -> dict[str, dict[str, str | int | float | None]]:
    """Preset rows for definitions."""
    return {
        "A": {
            "binary_format": "BIG_ENDIAN",
            "file_type": "Name II",
            "time_interval": "30:00",
            "day_per_file": True,
            "prefix": "MO",
            "suffix": "UM1p5km_Mk4_I_L57PT1.pp ;UM1p5km_Mk4_M_L57PT1.pp",
            "next_heat_flux": False,
            "next_precipitation": True,
            "next_cloud": False,
            "mesoscale_sigu": 0.55,
            "mesoscale_tauu": 2900.0,
            "met_file_structure_definition": "UM1p5km_Mk2_I;UM1p5km_Mk2_M",
            "z_coord_w": "m asl",
            "z_coord_cloud_height": "Pa",
            "z_grid": "ZGridA",
            "z_grid_u_v": "ZGridAUV",
            "z_grid_w": "ZGridAW",
            "z_grid_p": "ZGridAP",
            "h_grid": "HGridA",
            "h_grid_u": "HGridAU",
            "h_grid_v": "HGridAV",
            "topography_file": "TopoFileA"
        },
        "B": {
            "binary_format": "NATIVE",
            "file_type": "GRIB",
            "time_interval": "2d 30:00",
            "day_per_file": False,
            "prefix": "MO",
            "suffix": "UM1p5km_Mk4_I_L57PT1.pp ;UM1p5km_Mk4_M_L57PT1.pp",
            "next_heat_flux": True,
            "next_precipitation": False,
            "next_cloud": True,
            "mesoscale_sigu": 0.95,
            "mesoscale_tauu": 1200.0,
            "met_file_structure_definition": "UM1p5km_Mk2_I;UM1p5km_Mk2_M",
            "z_coord_w": "m agl",
            "z_coord_cloud_height": "m asl",
            "z_grid": "ZGridB",
            "z_grid_u_v": "ZGridBUV",
            "z_grid_w": "ZGridBW",
            "z_grid_p": "ZGridBP",
            "h_grid": "HGridB",
            "h_grid_u": "HGridBU",
            "h_grid_v": "HGridBV",
            "topography_file": "TopoFileB"
        },
    }

@pytest.fixture
def definitions_expected_str() -> dict[str, str]:
    return {
        "Header": (
            "NWP Met Definitions:\n"
            "Name,Binary Format,File Type,dT,Day Per File,Prefix,Suffix,"
            "Next Heat Flux,Next Precipitation,Next Cloud,Mesoscale SigU,"
            "Mesoscale TauU,Met File Structure Definition,Z-Coord - W,"
            "Z-Coord - Cloud Height,Z-Grid,Z-Grid - UV,Z-Grid - W,Z-Grid - P,"
            "H-Grid,H-Grid - U,H-Grid - V,Topography File"
        ),
        "A": (
            "A,BIG_ENDIAN,Name II,30:00,Yes,MO,"
            "UM1p5km_Mk4_I_L57PT1.pp ;UM1p5km_Mk4_M_L57PT1.pp,No,Yes,No,0.55,"
            "2900.0,UM1p5km_Mk2_I;UM1p5km_Mk2_M,m asl,Pa,ZGridA,ZGridAUV,"
            "ZGridAW,ZGridAP,HGridA,HGridAU,HGridAV,TopoFileA"
        ),
        "B": (
            "B,NATIVE,GRIB,2d 30:00,No,MO,"
            "UM1p5km_Mk4_I_L57PT1.pp ;UM1p5km_Mk4_M_L57PT1.pp,Yes,No,Yes,0.95,"
            "1200.0,UM1p5km_Mk2_I;UM1p5km_Mk2_M,m agl,m asl,ZGridB,ZGridBUV,"
            "ZGridBW,ZGridBP,HGridB,HGridBU,HGridBV,TopoFileB"
        )
    }

@pytest.fixture
def definitions_expected_repr() -> str:
    return "\n".join([
        "[NWP Met Definitions]",
        "\t[[A]]",
        "\t\tbinary_format                   : BIG_ENDIAN",
        "\t\tfile_type                       : Name II",
        "\t\ttime_interval                   : 30:00",
        "\t\tmin_time                        : None",
        "\t\tday_per_file                    : Yes",
        "\t\tprefix                          : MO",
        (
            "\t\tsuffix                          : UM1p5km_Mk4_I_L57PT1.pp "
            ";UM1p5km_Mk4_M_L57PT1.pp"
        ),
        "\t\tnext_heat_flux                  : No",
        "\t\tnext_precipitation              : Yes",
        "\t\tnext_cloud                      : No",
        "\t\tmesoscale_sigu                  : 0.55",
        "\t\tmesoscale_tauu                  : 2900.0",
        "\t\tmet_file_structure_definition   : UM1p5km_Mk2_I;UM1p5km_Mk2_M",
        "\t\tz_coord_w                       : m asl",
        "\t\tz_coord_cloud_height            : Pa",
        "\t\tz_grid                          : ZGridA",
        "\t\tz_grid_u_v                      : ZGridAUV",
        "\t\tz_grid_w                        : ZGridAW",
        "\t\tz_grid_p                        : ZGridAP",
        "\t\th_grid                          : HGridA",
        "\t\th_grid_u                        : HGridAU",
        "\t\th_grid_v                        : HGridAV",
        "\t\ttopography_file                 : TopoFileA",
        "\t[[B]]",
        "\t\tbinary_format                   : NATIVE",
        "\t\tfile_type                       : GRIB",
        "\t\ttime_interval                   : 2d 30:00",
        "\t\tmin_time                        : None",
        "\t\tday_per_file                    : No",
        "\t\tprefix                          : MO",
        (
            "\t\tsuffix                          : UM1p5km_Mk4_I_L57PT1.pp "
            ";UM1p5km_Mk4_M_L57PT1.pp"
        ),
        "\t\tnext_heat_flux                  : Yes",
        "\t\tnext_precipitation              : No",
        "\t\tnext_cloud                      : Yes",
        "\t\tmesoscale_sigu                  : 0.95",
        "\t\tmesoscale_tauu                  : 1200.0",
        "\t\tmet_file_structure_definition   : UM1p5km_Mk2_I;UM1p5km_Mk2_M",
        "\t\tz_coord_w                       : m agl",
        "\t\tz_coord_cloud_height            : m asl",
        "\t\tz_grid                          : ZGridB",
        "\t\tz_grid_u_v                      : ZGridBUV",
        "\t\tz_grid_w                        : ZGridBW",
        "\t\tz_grid_p                        : ZGridBP",
        "\t\th_grid                          : HGridB",
        "\t\th_grid_u                        : HGridBU",
        "\t\th_grid_v                        : HGridBV",
        "\t\ttopography_file                 : TopoFileB",
    ])

@pytest.mark.parametrize("row", ["A", "B"])
def test_init_definitions_preset_single(
    row: str,
    preset_definitions: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    tests = {}

    definitions = NWPMetDefinitions.setup(
        rows={row: preset_definitions[row]}
    )
    expected_used_cols = {
        "name": True,
        "binary_format": True,
        "file_type": True,
        "time_interval": True,
        "min_time": False,
        "day_per_file": True,
        "prefix": True,
        "suffix": True,
        "next_heat_flux": True,
        "next_precipitation": True,
        "next_cloud": True,
        "mesoscale_sigu": True,
        "mesoscale_tauu": True,
        "met_file_structure_definition": True,
        "z_coord_w": True,
        "z_coord_cloud_height": True,
        "z_grid": True,
        "z_grid_u_v": True,
        "z_grid_w": True,
        "z_grid_p": True,
        "h_grid": True,
        "h_grid_u": True,
        "h_grid_v": True,
        "topography_file": True,
    }
    expected_rows = {
        "A": NWPMetDefinitionsRow(
            name="A",
            binary_format="BIG_ENDIAN",
            file_type="Name II",
            time_interval="30:00",
            day_per_file="Yes",
            prefix="MO",
            suffix="UM1p5km_Mk4_I_L57PT1.pp ;UM1p5km_Mk4_M_L57PT1.pp",
            next_heat_flux="No",
            next_precipitation="Yes",
            next_cloud="No",
            mesoscale_sigu=0.55,
            mesoscale_tauu=2900.0,
            met_file_structure_definition="UM1p5km_Mk2_I;UM1p5km_Mk2_M",
            z_coord_w="m asl",
            z_coord_cloud_height="Pa",
            z_grid="ZGridA",
            z_grid_u_v="ZGridAUV",
            z_grid_w="ZGridAW",
            z_grid_p="ZGridAP",
            h_grid="HGridA",
            h_grid_u="HGridAU",
            h_grid_v="HGridAV",
            topography_file="TopoFileA"
        ),
        "B": NWPMetDefinitionsRow(
            name="B",
            binary_format="NATIVE",
            file_type="GRIB",
            time_interval="2d 30:00",
            day_per_file="No",
            prefix="MO",
            suffix="UM1p5km_Mk4_I_L57PT1.pp ;UM1p5km_Mk4_M_L57PT1.pp",
            next_heat_flux="Yes",
            next_precipitation="No",
            next_cloud="Yes",
            mesoscale_sigu=0.95,
            mesoscale_tauu=1200.0,
            met_file_structure_definition="UM1p5km_Mk2_I;UM1p5km_Mk2_M",
            z_coord_w="m agl",
            z_coord_cloud_height="m asl",
            z_grid="ZGridB",
            z_grid_u_v="ZGridBUV",
            z_grid_w="ZGridBW",
            z_grid_p="ZGridBP",
            h_grid="HGridB",
            h_grid_u="HGridBU",
            h_grid_v="HGridBV",
            topography_file="TopoFileB"
        )
    }
    vals = definitions.__dict__
    tests["Correct row"] = vals["rows"] = expected_rows[row]
    tests["Correct used_keys"] = vals["used_keys"] == expected_used_cols
    tests["Environment present"] = isinstance(
        definitions._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_definitions_preset_both(
    preset_definitions: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    tests = {}

    definitions = NWPMetDefinitions.setup(
        rows=preset_definitions
    )
    expected_used_cols = {
        "name": True,
        "binary_format": True,
        "file_type": True,
        "time_interval": True,
        "min_time": False,
        "day_per_file": True,
        "prefix": True,
        "suffix": True,
        "next_heat_flux": True,
        "next_precipitation": True,
        "next_cloud": True,
        "mesoscale_sigu": True,
        "mesoscale_tauu": True,
        "met_file_structure_definition": True,
        "z_coord_w": True,
        "z_coord_cloud_height": True,
        "z_grid": True,
        "z_grid_u_v": True,
        "z_grid_w": True,
        "z_grid_p": True,
        "h_grid": True,
        "h_grid_u": True,
        "h_grid_v": True,
        "topography_file": True,
    }
    expected_rows = {
        "A": NWPMetDefinitionsRow(
            name="A",
            binary_format="BIG_ENDIAN",
            file_type="Name II",
            time_interval="30:00",
            day_per_file="Yes",
            prefix="MO",
            suffix="UM1p5km_Mk4_I_L57PT1.pp ;UM1p5km_Mk4_M_L57PT1.pp",
            next_heat_flux="No",
            next_precipitation="Yes",
            next_cloud="No",
            mesoscale_sigu=0.55,
            mesoscale_tauu=2900.0,
            met_file_structure_definition="UM1p5km_Mk2_I;UM1p5km_Mk2_M",
            z_coord_w="m asl",
            z_coord_cloud_height="Pa",
            z_grid="ZGridA",
            z_grid_u_v="ZGridAUV",
            z_grid_w="ZGridAW",
            z_grid_p="ZGridAP",
            h_grid="HGridA",
            h_grid_u="HGridAU",
            h_grid_v="HGridAV",
            topography_file="TopoFileA"
        ),
        "B": NWPMetDefinitionsRow(
            name="B",
            binary_format="NATIVE",
            file_type="GRIB",
            time_interval="2d 30:00",
            day_per_file="No",
            prefix="MO",
            suffix="UM1p5km_Mk4_I_L57PT1.pp ;UM1p5km_Mk4_M_L57PT1.pp",
            next_heat_flux="Yes",
            next_precipitation="No",
            next_cloud="Yes",
            mesoscale_sigu=0.95,
            mesoscale_tauu=1200.0,
            met_file_structure_definition="UM1p5km_Mk2_I;UM1p5km_Mk2_M",
            z_coord_w="m agl",
            z_coord_cloud_height="m asl",
            z_grid="ZGridB",
            z_grid_u_v="ZGridBUV",
            z_grid_w="ZGridBW",
            z_grid_p="ZGridBP",
            h_grid="HGridB",
            h_grid_u="HGridBU",
            h_grid_v="HGridBV",
            topography_file="TopoFileB"
        )
    }
    vals = definitions.__dict__
    for i, r in enumerate(["A", "B"]):
        tests[f"{r}.Correct row"] = vals["rows"][i] = expected_rows[r]
    tests["Correct used_keys"] = vals["used_keys"] == expected_used_cols
    tests["Environment present"] = isinstance(
        definitions._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@pytest.mark.parametrize("row", ["A", "B"])
def test_init_definitions_single_str(
    row: str,
    preset_definitions: dict[str, dict[str, object]],
    definitions_expected_str: dict[str, str]
):
    """Does the Species class initialise?"""
    tests = {}

    definitions = NWPMetDefinitions.setup(
        rows={row: preset_definitions[row]}
    )

    expected = "\n".join([
        definitions_expected_str["Header"],
        definitions_expected_str[row],
    ])
    actual = str(definitions)

    tests["Expected str"] = actual == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_definitions_both_str(
    preset_definitions: dict[str, dict[str, object]],
    definitions_expected_str: dict[str, str]
):
    """Does the Species class initialise?"""
    tests = {}

    definitions = NWPMetDefinitions.setup(
        rows=preset_definitions
    )

    expected = "\n".join([
        definitions_expected_str["Header"],
        definitions_expected_str["A"],
        definitions_expected_str["B"],
    ])
    actual = str(definitions)

    tests["Expected str"] = actual == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_definitions_both_repr(
    preset_definitions: dict[str, dict[str, object]],
    definitions_expected_repr: str
):
    """Does the Species class initialise?"""
    tests = {}

    definitions = NWPMetDefinitions.setup(
        rows=preset_definitions
    )

    actual = repr(definitions)

    tests["Expected repr"] = actual == definitions_expected_repr

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("bad_arg", [
        ("name", 0),
        ("prefix", 0),
        ("suffix", 0),
        ("mesoscale_sigu", "BAD VALUE"),
        ("mesoscale_tauu", "BAD VALUE"),
        ("met_file_structure_definition", 0),
        ("z_grid",  0),
        ("z_grid_u_v",  0),
        ("z_grid_w", 0),
        ("z_grid_p", 0),
        ("h_grid", 0),
        ("h_grid_u", 0),
        ("h_grid_v", 0),
        ("topography_file", 0),
])
def test_init_definitions_bad_base_type(
    bad_arg: tuple[str, str | int],
    preset_definitions: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    rows = {"A": preset_definitions["A"]}
    if bad_arg[0] != "name":
        rows["A"] = rows["A"] | {bad_arg[0]: bad_arg[1]}
    else:
        rows[0] = rows["A"]
        rows.pop("A")
    with pytest.raises(
        TypeError,
        match=r"is not.*str.*Is.*int|is not.*float.*Is.*str"
    ):
        _ = NWPMetDefinitions.setup(
            rows=rows
        )


@pytest.mark.parametrize("bad_key", [
    "day_per_file",
    "next_heat_flux",
    "next_precipitation",
    "next_cloud"
])
def test_init_definitions_bad_switch(
    bad_key: str,
    preset_definitions: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    rows = {"A": preset_definitions["A"]}
    rows["A"] = rows["A"] | {bad_key: "BAD VALUE"}
    with pytest.raises(
        TypeError,
        match=r"is not.*bool.*Is.*str"
    ):
        _ = NWPMetDefinitions.setup(
            rows=rows
        )


@pytest.mark.parametrize("bad_key", [
    "time_interval"
])
def test_init_definitions_bad_time_interval(
    bad_key: str,
    preset_definitions: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    rows = {"A": preset_definitions["A"]}
    rows["A"] = rows["A"] | {bad_key: "BAD VALUE"}
    with pytest.raises(
        ValueError,
        match=r"not a valid time interval recognised by NAME\."
    ):
        _ = NWPMetDefinitions.setup(
            rows=rows
        )


@pytest.mark.parametrize("bad_key", [
    "binary_format",
    "file_type",
    "z_coord_w",
    "z_coord_cloud_height"
])
def test_init_definitions_bad_literal(
    bad_key: str,
    preset_definitions: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    rows = {"A": preset_definitions["A"]}
    rows["A"] = rows["A"] | {bad_key: "BAD VALUE"}
    with pytest.raises(
        TypeError,
        match=f"{bad_key} is not a member of.*Expected one of"
    ):
        _ = NWPMetDefinitions.setup(
            rows=rows
        )


@pytest.mark.parametrize("bad_key", [
    "min_time"
])
def test_init_definitions_unimplemented(
    bad_key: str,
    preset_definitions: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    rows = {"A": preset_definitions["A"]}
    rows["A"] = rows["A"] | {bad_key: "BAD VALUE"}
    with pytest.raises(
        NotImplementedError,
        match=(
            f"{bad_key} was specified but is not implemented for NWP Met "
            r"Definitions\."
        )
    ):
        _ = NWPMetDefinitions.setup(
            rows=rows
        )


@pytest.fixture
def preset_module() -> dict[str, dict[str, str | int | float | None]]:
    """Preset rows for module."""
    return {
        "A": {
            "min_bl_depth": 40,
            "max_bl_depth": 4000,
            "use_nwp_bl_depth": True,
            "restore_met_script": "/A/Path/To/Somewhere.txt",
            "delete_met": False,
            "met_folder": "/A/Path/To/Met/Folder/",
            "topography_folder": "/A/Path/To/Topography/Folder",
            "met_definition_name": "UM1p5km_Mk4_L57PT2pp",
            "update_on_demand": True,
        },
        "B": {
            "min_bl_depth": 20,
            "max_bl_depth": 5000,
            "use_nwp_bl_depth": False,
            "restore_met_script": "/B/Path/To/Somewhere.txt",
            "delete_met": True,
            "met_folder": "/B/Path/To/Met/Folder/",
            "topography_folder": "/B/Path/To/Topography/Folder",
            "met_definition_name": "UM1p5km_Mk4_L57PT2pp",
            "update_on_demand": False,
        },
    }

@pytest.fixture
def module_expected_str() -> dict[str, str]:
    return {
        "Header": (
            "NWP Met Module Instances:\n"
            "Name,Min B L Depth,Max B L Depth,Use NWP BL Depth?,"
            "Restore Met Script,Delete Met?,Met Folder,Topography Folder,"
            "Met Definition Name,Update on Demand?"
        ),
        "A": (
            "A,40,4000,Yes,/A/Path/To/Somewhere.txt,No,"
            "/A/Path/To/Met/Folder/,/A/Path/To/Topography/Folder,"
            "UM1p5km_Mk4_L57PT2pp,Yes"
        ),
        "B": (
            "B,20,5000,No,/B/Path/To/Somewhere.txt,Yes,"
            "/B/Path/To/Met/Folder/,/B/Path/To/Topography/Folder,"
            "UM1p5km_Mk4_L57PT2pp,No"
        )
    }

@pytest.fixture
def module_expected_repr() -> str:
    return "\n".join([
        "[NWP Met Module Instances]",
        "\t[[A]]",
        "\t\tmin_bl_depth        : 40",
        "\t\tmax_bl_depth        : 4000",
        "\t\tuse_nwp_bl_depth    : Yes",
        "\t\tmesoscale_sigu      : None",
        "\t\tmesoscale_tauu      : None",
        "\t\tfree_trop_sigu      : None",
        "\t\tfree_trop_sigw      : None",
        "\t\tfree_trop_tauu      : None",
        "\t\tfree_trop_tauw      : None",
        "\t\trestore_met_script  : /A/Path/To/Somewhere.txt",
        "\t\tdelete_met          : No",
        "\t\tmet_folder          : /A/Path/To/Met/Folder/",
        "\t\tensemble_met_folder : None",
        "\t\tmet_folder_stem     : None",
        "\t\tmet_folders         : None",
        "\t\ttopography_folder   : /A/Path/To/Topography/Folder",
        "\t\tmet_definition_name : UM1p5km_Mk4_L57PT2pp",
        "\t\tupdate_on_demand    : Yes",
        "\t\tprefetch            : None",
        "\t\tnew_threaded_method : None",
        "\t[[B]]",
        "\t\tmin_bl_depth        : 20",
        "\t\tmax_bl_depth        : 5000",
        "\t\tuse_nwp_bl_depth    : No",
        "\t\tmesoscale_sigu      : None",
        "\t\tmesoscale_tauu      : None",
        "\t\tfree_trop_sigu      : None",
        "\t\tfree_trop_sigw      : None",
        "\t\tfree_trop_tauu      : None",
        "\t\tfree_trop_tauw      : None",
        "\t\trestore_met_script  : /B/Path/To/Somewhere.txt",
        "\t\tdelete_met          : Yes",
        "\t\tmet_folder          : /B/Path/To/Met/Folder/",
        "\t\tensemble_met_folder : None",
        "\t\tmet_folder_stem     : None",
        "\t\tmet_folders         : None",
        "\t\ttopography_folder   : /B/Path/To/Topography/Folder",
        "\t\tmet_definition_name : UM1p5km_Mk4_L57PT2pp",
        "\t\tupdate_on_demand    : No",
        "\t\tprefetch            : None",
        "\t\tnew_threaded_method : None",
    ])

@pytest.mark.parametrize("row", ["A", "B"])
def test_init_module_preset_single(
    row: str,
    preset_module: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    tests = {}

    module = NWPMetModuleInstances.setup(
        rows={row: preset_module[row]}
    )
    expected_used_cols = {
        "name": True,
        "min_bl_depth": True,
        "max_bl_depth": True,
        "use_nwp_bl_depth": True,
        "mesoscale_sigu": False,
        "mesoscale_tauu": False,
        "free_trop_sigu": False,
        "free_trop_sigw": False,
        "free_trop_tauu": False,
        "free_trop_tauw": False,
        "restore_met_script": True,
        "delete_met": True,
        "met_folder": True,
        "ensemble_met_folder": False,
        "met_folder_stem": False,
        "met_folders": False,
        "topography_folder": True,
        "met_definition_name": True,
        "update_on_demand": True,
        "prefetch": False,
        "new_threaded_method": False,
    }
    expected_rows = {
        "A": NWPMetModuleInstancesRow(
            name="A",
            min_bl_depth=40,
            max_bl_depth=4000,
            use_nwp_bl_depth="Yes",
            restore_met_script="/A/Path/To/Somewhere.txt",
            delete_met="No",
            met_folder="/A/Path/To/Met/Folder/",
            topography_folder="/A/Path/To/Topography/Folder",
            met_definition_name="UM1p5km_Mk4_L57PT2pp",
            update_on_demand="Yes"
        ),
        "B": NWPMetModuleInstancesRow(
            name="B",
            min_bl_depth=20,
            max_bl_depth=5000,
            use_nwp_bl_depth="No",
            restore_met_script="/B/Path/To/Somewhere.txt",
            delete_met="Yes",
            met_folder="/B/Path/To/Met/Folder/",
            topography_folder="/B/Path/To/Topography/Folder",
            met_definition_name="UM1p5km_Mk4_L57PT2pp",
            update_on_demand="No"
        )
    }
    vals = module.__dict__
    tests["Correct row"] = vals["rows"] = expected_rows[row]
    tests["Correct used_keys"] = vals["used_keys"] == expected_used_cols
    tests["Environment present"] = isinstance(
        module._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_module_preset_both(
    preset_module: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    tests = {}

    module = NWPMetModuleInstances.setup(
        rows=preset_module
    )
    expected_used_cols = {
        "name": True,
        "min_bl_depth": True,
        "max_bl_depth": True,
        "use_nwp_bl_depth": True,
        "mesoscale_sigu": False,
        "mesoscale_tauu": False,
        "free_trop_sigu": False,
        "free_trop_sigw": False,
        "free_trop_tauu": False,
        "free_trop_tauw": False,
        "restore_met_script": True,
        "delete_met": True,
        "met_folder": True,
        "ensemble_met_folder": False,
        "met_folder_stem": False,
        "met_folders": False,
        "topography_folder": True,
        "met_definition_name": True,
        "update_on_demand": True,
        "prefetch": False,
        "new_threaded_method": False,
    }
    expected_rows = {
        "A": NWPMetModuleInstancesRow(
            name="A",
            min_bl_depth=40,
            max_bl_depth=4000,
            use_nwp_bl_depth="Yes",
            restore_met_script="/A/Path/To/Somewhere.txt",
            delete_met="No",
            met_folder="/A/Path/To/Met/Folder/",
            topography_folder="/A/Path/To/Topography/Folder",
            met_definition_name="UM1p5km_Mk4_L57PT2pp",
            update_on_demand="Yes"
        ),
        "B": NWPMetModuleInstancesRow(
            name="B",
            min_bl_depth=20,
            max_bl_depth=5000,
            use_nwp_bl_depth="No",
            restore_met_script="/B/Path/To/Somewhere.txt",
            delete_met="Yes",
            met_folder="/B/Path/To/Met/Folder/",
            topography_folder="/B/Path/To/Topography/Folder",
            met_definition_name="UM1p5km_Mk4_L57PT2pp",
            update_on_demand="No"
        )
    }
    vals = module.__dict__
    for i, r in enumerate(["A", "B"]):
        tests[f"{r}.Correct row"] = vals["rows"][i] = expected_rows[r]
    tests["Correct used_keys"] = vals["used_keys"] == expected_used_cols
    tests["Environment present"] = isinstance(
        module._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@pytest.mark.parametrize("row", ["A", "B"])
def test_init_module_single_str(
    row: str,
    preset_module: dict[str, dict[str, object]],
    module_expected_str: dict[str, str]
):
    """Does the Species class initialise?"""
    tests = {}

    module = NWPMetModuleInstances.setup(
        rows={row: preset_module[row]}
    )

    expected = "\n".join([
        module_expected_str["Header"],
        module_expected_str[row],
    ])
    actual = str(module)
    print(expected)
    print(actual)

    tests["Expected str"] = actual == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_module_both_str(
    preset_module: dict[str, dict[str, object]],
    module_expected_str: dict[str, str]
):
    """Does the Species class initialise?"""
    tests = {}

    module = NWPMetModuleInstances.setup(
        rows=preset_module
    )

    expected = "\n".join([
        module_expected_str["Header"],
        module_expected_str["A"],
        module_expected_str["B"],
    ])
    actual = str(module)

    print(expected)
    print(actual)
    tests["Expected str"] = actual == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_module_both_repr(
    preset_module: dict[str, dict[str, object]],
    module_expected_repr: str
):
    """Does the Species class initialise?"""
    tests = {}

    module = NWPMetModuleInstances.setup(
        rows=preset_module
    )

    actual = repr(module)

    tests["Expected repr"] = actual == module_expected_repr
    print(module_expected_repr)
    print(actual)

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("bad_arg", [
        ("name", 0),
        ("min_bl_depth", "BAD VALUE"),
        ("max_bl_depth", "BAD VALUE"),
        ("restore_met_script", 0),
        ("met_folder",  0),
        ("topography_folder",  0),
        ("met_definition_name", 0),
])
def test_init_module_bad_base_type(
    bad_arg: tuple[str, str | int],
    preset_module: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    rows = {"A": preset_module["A"]}
    if bad_arg[0] != "name":
        rows["A"] = rows["A"] | {bad_arg[0]: bad_arg[1]}
    else:
        rows[0] = rows["A"]
        rows.pop("A")
    with pytest.raises(
        TypeError,
        match=r"is not.*str.*Is.*int|is not.*float.*Is.*str"
    ):
        _ = NWPMetModuleInstances.setup(
            rows=rows
        )


@pytest.mark.parametrize("bad_key", [
    "use_nwp_bl_depth",
    "delete_met",
    "update_on_demand",
])
def test_init_module_bad_switch(
    bad_key: str,
    preset_module: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    rows = {"A": preset_module["A"]}
    rows["A"] = rows["A"] | {bad_key: "BAD VALUE"}
    with pytest.raises(
        TypeError,
        match=r"is not.*bool.*Is.*str"
    ):
        _ = NWPMetModuleInstances.setup(
            rows=rows
        )


@pytest.mark.parametrize("bad_key", [
    "mesoscale_sigu",
    "mesoscale_tauu",
    "free_trop_sigu",
    "free_trop_sigw",
    "free_trop_tauu",
    "free_trop_tauw",
    "ensemble_met_folder",
    "met_folder_stem",
    "met_folders",
    "prefetch",
    "new_threaded_method",
])
def test_init_module_unimplemented(
    bad_key: str,
    preset_module: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    rows = {"A": preset_module["A"]}
    rows["A"] = rows["A"] | {bad_key: "BAD VALUE"}
    with pytest.raises(
        NotImplementedError,
        match=(
            f"{bad_key} was specified but is not implemented for NWP Met "
            r"Module Instances\."
        )
    ):
        _ = NWPMetModuleInstances.setup(
            rows=rows
        )

@pytest.fixture
def preset_structure() -> dict[str, dict[str, str | int | float | None]]:
    """Preset rows for structure."""
    return {
        "A": {
            "lowest_level": 1,
            "highest_level": "Top",
            "field_code": 254,
            "three_d": True,
            "field_qualifiers": "Total"
        },
        "B": {
            "lowest_level": 2,
            "highest_level": 100,
            "field_code": 16004,
            "three_d": False,
            "field_qualifiers": None
        },
    }

@pytest.fixture
def structure_expected_str() -> dict[str, str]:
    return {
        "Header A": (
            "NWP Met File Structure Definition: Test\n"
            "Field Name,Lowest Level,Highest Level,Field Code,3-d?,"
            "Field Qualifiers"
        ),
        "Header B": (
            "NWP Met File Structure Definition: Test\n"
            "Field Name,Lowest Level,Highest Level,Field Code,3-d?"
        ),
        "A": (
            "A,1,Top,254,Yes,Total"
        ),
        "B": (
            "B,2,100,16004,No"
        )
    }

@pytest.fixture
def structure_expected_repr() -> str:
    return "\n".join([
        "[NWP Met File Structure Definitions]",
        "\t[[A]]",
        "\t\tfield_name          : A",
        "\t\tlowest_level        : 1",
        "\t\thighest_level       : Top",
        "\t\tfield_code          : 254",
        "\t\tthree_d             : Yes",
        "\t\tfield_qualifiers    : Total",
        "\t\tnc_field_name       : None",
        "\t[[B]]",
        "\t\tfield_name          : B",
        "\t\tlowest_level        : 2",
        "\t\thighest_level       : 100",
        "\t\tfield_code          : 16004",
        "\t\tthree_d             : No",
        "\t\tfield_qualifiers    : None",
        "\t\tnc_field_name       : None"
    ])

@pytest.mark.parametrize("row", ["A", "B"])
def test_init_structure_preset_single(
    row: str,
    preset_structure: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    tests = {}

    structure = NWPMetFileStructureDefinitions.setup(
        name="Test",
        rows={row: preset_structure[row]}
    )
    expected_used_cols = {
        "field_name": True,
        "lowest_level": True,
        "highest_level": True,
        "field_code": True,
        "three_d": True,
        "field_qualifiers": row != "B",
        "nc_field_name": False

    }
    expected_rows = {
        "A": NWPMetFileStructureDefinitionsRow(
            field_name="A",
            lowest_level=1,
            highest_level="Top",
            field_code=254,
            three_d="Yes",
            field_qualifiers="Total"
        ),
        "B": NWPMetFileStructureDefinitionsRow(
            field_name="B",
            lowest_level=2,
            highest_level=100,
            field_code=16004,
            three_d="No",
            field_qualifiers=None
        )
    }
    vals = structure.__dict__
    tests["Correct row"] = vals["rows"] = expected_rows[row]
    tests["Correct used_keys"] = vals["used_keys"] == expected_used_cols
    tests["Environment present"] = isinstance(
        structure._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_structure_preset_both(
    preset_structure: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    tests = {}

    structure = NWPMetFileStructureDefinitions.setup(
        name="Test",
        rows=preset_structure
    )
    expected_used_cols = {
        "field_name": True,
        "lowest_level": True,
        "highest_level": True,
        "field_code": True,
        "three_d": True,
        "field_qualifiers": True,
        "nc_field_name": False

    }
    expected_rows = {
        "A": NWPMetFileStructureDefinitionsRow(
            field_name="A",
            lowest_level=1,
            highest_level="Top",
            field_code=254,
            three_d="Yes",
            field_qualifiers="Total"
        ),
        "B": NWPMetFileStructureDefinitionsRow(
            field_name="B",
            lowest_level=2,
            highest_level=100,
            field_code=16004,
            three_d="No",
            field_qualifiers=None
        )
    }
    vals = structure.__dict__
    for i, r in enumerate(["A", "B"]):
        tests[f"{r}.Correct row"] = vals["rows"][i] = expected_rows[r]
    tests["Correct used_keys"] = vals["used_keys"] == expected_used_cols
    tests["Environment present"] = isinstance(
        structure._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@pytest.mark.parametrize("row", ["A", "B"])
def test_init_structure_single_str(
    row: str,
    preset_structure: dict[str, dict[str, object]],
    structure_expected_str: dict[str, str]
):
    """Does the Species class initialise?"""
    tests = {}

    structure = NWPMetFileStructureDefinitions.setup(
        name="Test",
        rows={row: preset_structure[row]}
    )

    expected = "\n".join([
        structure_expected_str[f"Header {row}"],
        structure_expected_str[row],
    ])
    actual = str(structure)
    print(expected)
    print(actual)

    tests["Expected str"] = actual == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_structure_both_str(
    preset_structure: dict[str, dict[str, object]],
    structure_expected_str: dict[str, str]
):
    """Does the Species class initialise?"""
    tests = {}

    structure = NWPMetFileStructureDefinitions.setup(
        name="Test",
        rows=preset_structure
    )

    expected = "\n".join([
        structure_expected_str["Header A"],
        structure_expected_str["A"],
        structure_expected_str["B"] + ",",
    ])
    actual = str(structure)

    print(expected)
    print(actual)
    tests["Expected str"] = actual == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_structure_both_repr(
    preset_structure: dict[str, dict[str, object]],
    structure_expected_repr: str
):
    """Does the Species class initialise?"""
    tests = {}

    structure = NWPMetFileStructureDefinitions.setup(
        name="Test",
        rows=preset_structure
    )

    actual = repr(structure)

    tests["Expected repr"] = actual == structure_expected_repr
    print(structure_expected_repr)
    print(actual)

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("bad_arg", [
        ("field_name", 0),
        ("lowest_level", "BAD VALUE"),
        ("field_code", "BAD VALUE"),
        ("field_qualifiers",  0),
])
def test_init_structure_bad_base_type(
    bad_arg: tuple[str, str | int],
    preset_structure: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    rows = {"A": preset_structure["A"]}
    if bad_arg[0] != "field_name":
        rows["A"] = rows["A"] | {bad_arg[0]: bad_arg[1]}
    else:
        rows[0] = rows["A"]
        rows.pop("A")
    with pytest.raises(
        TypeError,
        match=r"is not.*str.*Is.*int|is not.*int.*Is.*str"
    ):
        _ = NWPMetFileStructureDefinitions.setup(
            name="Test",
            rows=rows
        )


def test_init_structure_bad_highest_level(
    preset_structure: dict[str, dict[str, object]]
):
    """Special edge case for `highest_level`."""
    rows = {"A": preset_structure["A"]}
    rows["A"] = rows["A"] | {"highest_level": "BAD VALUE"}
    with pytest.raises(
        TypeError,
        match=r"highest_level is not an integer value or 'Top'\."
    ):
        _ = NWPMetFileStructureDefinitions.setup(
            name="Test",
            rows=rows
        )


@pytest.mark.parametrize("bad_key", [
    "three_d",
])
def test_init_structure_bad_switch(
    bad_key: str,
    preset_structure: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    rows = {"A": preset_structure["A"]}
    rows["A"] = rows["A"] | {bad_key: "BAD VALUE"}
    with pytest.raises(
        TypeError,
        match=r"is not.*bool.*Is.*str"
    ):
        _ = NWPMetFileStructureDefinitions.setup(
            name="Test",
            rows=rows
        )


@pytest.mark.parametrize("bad_key", [
    "nc_field_name",
])
def test_init_structure_unimplemented(
    bad_key: str,
    preset_structure: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    rows = {"A": preset_structure["A"]}
    rows["A"] = rows["A"] | {bad_key: "BAD VALUE"}
    with pytest.raises(
        NotImplementedError,
        match=(
            f"{bad_key} was specified but is not implemented for NWP Met "
            r"File Structure Definition\."
        )
    ):
        _ = NWPMetFileStructureDefinitions.setup(
            name="Test",
            rows=rows
        )
