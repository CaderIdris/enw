from jinja2 import Environment
import pytest

from enw.block import (
    Fields,
    PPInfo
)
from enw.block._output import (
    FieldRow, PPInfoRow,
)

pytestmark = [
    pytest.mark.block,
    pytest.mark.block_output
]

@pytest.fixture
def preset_fields() -> dict[str, dict[str, str | int | float | None]]:
    """Preset rows for species."""
    return {
        "A": {
            "quantity": "# Particles",
            "t_grid": "TGridA",
            "t_av_or_int": "No",
            "sync": True,
            "output_format": "IA2",
            "output_route": "D",
            "output_group": "Group A",
            "species": "SpeciesA",
            "source": "SourceA",
            "h_grid": "HGridA",
            "z_grid": "ZGridA",
            "bl_average": True,
            "av_time": "00:30",
            "num_av_times": 200,
            "across": "SX",
            "separate_file": "YZ",
        },
        "B": {
            "quantity": "Mixing Ratio",
            "t_grid": "TGridB",
            "t_av_or_int": "Int",
            "sync": False,
            "output_format": "FZ",
            "output_route": "N",
            "output_group": "Group B",
            "species": "SpeciesB",
            "source": "SourceB",
            "h_grid": "HGridB",
            "z_grid": "ZGridB",
            "bl_average": False,
            "av_time": "30min",
            "num_av_times": 40,
            "across": "TZ",
            "separate_file": "YS",
        },
    }


@pytest.fixture
def fields_expected_str() -> dict[str, str]:
    return {
        "Header": (
            "Output Requirements - Fields:\n"
            "Name,Quantity,Species,Source,H-Grid,Z-Grid,T-Grid,BL Average?,"
            "T Av Or Int,Av Time,# Av Times,Sync?,Across,Separate File,"
            "Output Format,Output Route,Output Group"
        ),
        "A": (
            "A,# Particles,SpeciesA,SourceA,HGridA,ZGridA,TGridA,Yes,No,00:30,"
            "200,Yes,SX,YZ,IA2,D,Group A"
        ),
        "B": (
            "B,Mixing Ratio,SpeciesB,SourceB,HGridB,ZGridB,TGridB,No,Int,"
            "30min,40,No,TZ,YS,FZ,N,Group B"
        )
    }

@pytest.fixture
def fields_expected_repr() -> str:
    return "\n".join([
        "[Output Requirements - Fields]",
        "\t[[A]]",
        "\t\tquantity                      : # Particles",
        "\t\tspecies                       : SpeciesA",
        "\t\tsource                        : SourceA",
        "\t\th_grid                        : HGridA",
        "\t\tz_grid                        : ZGridA",
        "\t\tt_grid                        : TGridA",
        "\t\tbl_average                    : Yes",
        "\t\tt_av_or_int                   : No",
        "\t\tav_time                       : 00:30",
        "\t\tnum_av_times                  : 200",
        "\t\tsync                          : Yes",
        "\t\tacross                        : SX",
        "\t\tseparate_file                 : YZ",
        "\t\toutput_format                 : IA2",
        "\t\toutput_route                  : D",
        "\t\toutput_group                  : Group A",
        "\t\tdecay_deposition              : None",
        "\t\tsource_group                  : None",
        "\t\ts_grid                        : None",
        "\t\th_coord                       : None",
        "\t\tz_coord                       : None",
        "\t\tensemble_av                   : None",
        "\t\tprobabilities                 : None",
        "\t\tpercentiles                   : None",
        "\t\tp_time                        : None",
        "\t\tp_interval                    : None",
        "\t\tensemble_p                    : None",
        "\t\tfluctuations                  : None",
        "\t\tx_scale                       : None",
        "\t\ty_scale                       : None",
        "\t\tparticle_size_distribution    : None",
        "\t\tsemi_infinite_approx          : None",
        "\t\tmaterial_unit                 : None",
        "\t\tmasking_threshold             : None",
        "\t[[B]]",
        "\t\tquantity                      : Mixing Ratio",
        "\t\tspecies                       : SpeciesB",
        "\t\tsource                        : SourceB",
        "\t\th_grid                        : HGridB",
        "\t\tz_grid                        : ZGridB",
        "\t\tt_grid                        : TGridB",
        "\t\tbl_average                    : No",
        "\t\tt_av_or_int                   : Int",
        "\t\tav_time                       : 30min",
        "\t\tnum_av_times                  : 40",
        "\t\tsync                          : No",
        "\t\tacross                        : TZ",
        "\t\tseparate_file                 : YS",
        "\t\toutput_format                 : FZ",
        "\t\toutput_route                  : N",
        "\t\toutput_group                  : Group B",
        "\t\tdecay_deposition              : None",
        "\t\tsource_group                  : None",
        "\t\ts_grid                        : None",
        "\t\th_coord                       : None",
        "\t\tz_coord                       : None",
        "\t\tensemble_av                   : None",
        "\t\tprobabilities                 : None",
        "\t\tpercentiles                   : None",
        "\t\tp_time                        : None",
        "\t\tp_interval                    : None",
        "\t\tensemble_p                    : None",
        "\t\tfluctuations                  : None",
        "\t\tx_scale                       : None",
        "\t\ty_scale                       : None",
        "\t\tparticle_size_distribution    : None",
        "\t\tsemi_infinite_approx          : None",
        "\t\tmaterial_unit                 : None",
        "\t\tmasking_threshold             : None"
    ])

@pytest.mark.parametrize("row", ["A", "B"])
@pytest.mark.parametrize("species", [True, False])
@pytest.mark.parametrize("source", [True, False])
@pytest.mark.parametrize("h_grid", [True, False])
@pytest.mark.parametrize("z_grid", [True, False])
@pytest.mark.parametrize("bl_average", [True, False])
@pytest.mark.parametrize("av_time", [True, False])
@pytest.mark.parametrize("num_av_times", [True, False])
@pytest.mark.parametrize("across", [True, False])
@pytest.mark.parametrize("separate_file", [True, False])
def test_init_fields_preset_single(
    preset_fields: dict[str, dict[str, object]],
    row: str,
    *,
    species: bool,
    source: bool,
    h_grid: bool,
    z_grid: bool,
    bl_average: bool,
    av_time: bool,
    num_av_times: bool,
    across: bool,
    separate_file: bool
):
    """Does the Species class initialise?"""
    tests = {}
    optional_args = (
        ("species", species),
        ("source", source),
        ("h_grid", h_grid),
        ("z_grid", z_grid),
        ("bl_average", bl_average),
        ("av_time", av_time),
        ("num_av_times", num_av_times),
        ("across", across),
        ("separate_file", separate_file)
    )

    row_vals = preset_fields[row]
    for k, v in optional_args:
        if not v:
            row_vals[k] = None

    fields = Fields.setup(
        rows={row: row_vals}
    )
    expected_used_cols = {
        "name": True,
        "quantity": True,
        "species": species,
        "source": source,
        "h_grid": h_grid,
        "z_grid": z_grid,
        "t_grid": True,
        "bl_average": bl_average,
        "t_av_or_int": True,
        "av_time": av_time,
        "num_av_times": num_av_times,
        "sync": True,
        "across": across,
        "separate_file": separate_file,
        "output_format": True,
        "output_route": True,
        "output_group": True,
        "decay_deposition": False,
        "source_group": False,
        "s_grid": False,
        "h_coord": False,
        "z_coord": False,
        "ensemble_av": False,
        "probabilities": False,
        "percentiles": False,
        "p_time": False,
        "p_interval": False,
        "ensemble_p": False,
        "fluctuations": False,
        "x_scale": False,
        "y_scale": False,
        "particle_size_distribution": False,
        "semi_infinite_approx": False,
        "material_unit": False,
        "masking_threshold": False,
    }
    expected_rows = {
        "A": FieldRow(
            name="A",
            quantity="# Particles",
            t_grid="TGridA",
            t_av_or_int="No",
            sync=True,
            output_format="IA2",
            output_route="D",
            output_group="Group A",
            species="SpeciesA" if species else None,
            source="SourceA" if source else None,
            h_grid="HGridA" if h_grid else None,
            z_grid="ZGridA" if z_grid else None,
            bl_average=True if bl_average else None,
            av_time="00:30" if av_time else None,
            num_av_times=200 if num_av_times else None,
            across="SX" if across else None,
            separate_file="YZ" if separate_file else None,
            decay_deposition = None,
            source_group = None,
            s_grid = None,
            h_coord = None,
            z_coord = None,
            ensemble_av = None,
            probabilities = None,
            percentiles = None,
            p_time = None,
            p_interval = None,
            ensemble_p = None,
            fluctuations = None,
            x_scale = None,
            y_scale = None,
            particle_size_distribution = None,
            semi_infinite_approx = None,
            material_unit = None,
            masking_threshold = None,
        ),
        "B": FieldRow(
            name="B",
            quantity="# Particles",
            t_grid="TGridB",
            t_av_or_int="Int",
            sync=False,
            output_format="FZ",
            output_route="N",
            output_group="Group B",
            species="SpeciesB" if species else None,
            source="SourceB" if source else None,
            h_grid="HGridB" if h_grid else None,
            z_grid="ZGridB" if z_grid else None,
            bl_average=False if bl_average else None,
            av_time="30min" if av_time else None,
            num_av_times=40 if num_av_times else None,
            across="TZ" if across else None,
            separate_file="YS" if separate_file else None,
            decay_deposition = None,
            source_group = None,
            s_grid = None,
            h_coord = None,
            z_coord = None,
            ensemble_av = None,
            probabilities = None,
            percentiles = None,
            p_time = None,
            p_interval = None,
            ensemble_p = None,
            fluctuations = None,
            x_scale = None,
            y_scale = None,
            particle_size_distribution = None,
            semi_infinite_approx = None,
            material_unit = None,
            masking_threshold = None,
        )
    }
    vals = fields.__dict__
    tests["Correct row"] = vals["rows"] = expected_rows[row]
    tests["Correct used_keys"] = vals["used_keys"] == expected_used_cols
    tests["Environment present"] = isinstance(
        fields._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("row", ["A", "B"])
def test_fields_str_single(
    preset_fields: dict[str, dict[str, str | int]],
    fields_expected_str: dict[str, str],
    row: str
):
    """Does the Main class have the right output?"""
    tests = {}

    fields = Fields.setup(
        rows={row: preset_fields[row]}
    )

    expected_block = "\n".join([
        fields_expected_str["Header"],
        fields_expected_str[row],
    ])


    block = str(fields)
    tests["Expected str"] = block == expected_block

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("row", ["A", "B"])
@pytest.mark.parametrize("species", [True, False])
@pytest.mark.parametrize("source", [True, False])
@pytest.mark.parametrize("h_grid", [True, False])
@pytest.mark.parametrize("z_grid", [True, False])
@pytest.mark.parametrize("bl_average", [True, False])
@pytest.mark.parametrize("av_time", [True, False])
@pytest.mark.parametrize("num_av_times", [True, False])
@pytest.mark.parametrize("across", [True, False])
@pytest.mark.parametrize("separate_file", [True, False])
def test_init_fields_preset_all(
    preset_fields: dict[str, dict[str, object]],
    row: str,
    *,
    species: bool,
    source: bool,
    h_grid: bool,
    z_grid: bool,
    bl_average: bool,
    av_time: bool,
    num_av_times: bool,
    across: bool,
    separate_file: bool
):
    """Does the Species class initialise?"""
    tests = {}
    optional_args = (
        ("species", species),
        ("source", source),
        ("h_grid", h_grid),
        ("z_grid", z_grid),
        ("bl_average", bl_average),
        ("av_time", av_time),
        ("num_av_times", num_av_times),
        ("across", across),
        ("separate_file", separate_file)
    )

    row_vals = preset_fields
    for k, v in optional_args:
        if not v:
            row_vals[row][k] = None

    fields = Fields.setup(
        rows=row_vals
    )
    expected_used_cols = {
        "name": True,
        "quantity": True,
        "species": True,
        "source": True,
        "h_grid": True,
        "z_grid": True,
        "t_grid": True,
        "bl_average": True,
        "t_av_or_int": True,
        "av_time": True,
        "num_av_times": True,
        "sync": True,
        "across": True,
        "separate_file": True,
        "output_format": True,
        "output_route": True,
        "output_group": True,
        "decay_deposition": False,
        "source_group": False,
        "s_grid": False,
        "h_coord": False,
        "z_coord": False,
        "ensemble_av": False,
        "probabilities": False,
        "percentiles": False,
        "p_time": False,
        "p_interval": False,
        "ensemble_p": False,
        "fluctuations": False,
        "x_scale": False,
        "y_scale": False,
        "particle_size_distribution": False,
        "semi_infinite_approx": False,
        "material_unit": False,
        "masking_threshold": False,
    }
    expected_rows = {
        "A": FieldRow(
            name="A",
            quantity="# Particles",
            t_grid="TGridA",
            t_av_or_int="No",
            sync=True,
            output_format="IA2",
            output_route="D",
            output_group="Group A",
            species="SpeciesA" if species and row == "A" else None,
            source="SourceA" if source and row == "A" else None,
            h_grid="HGridA" if h_grid and row == "A" else None,
            z_grid="ZGridA" if z_grid and row == "A" else None,
            bl_average=True if bl_average and row == "A" else None,
            av_time="00:30" if av_time and row == "A" else None,
            num_av_times=200 if num_av_times and row == "A" else None,
            across="SX" if across and row == "A" else None,
            separate_file="YZ" if separate_file and row == "A" else None,
            decay_deposition = None,
            source_group = None,
            s_grid = None,
            h_coord = None,
            z_coord = None,
            ensemble_av = None,
            probabilities = None,
            percentiles = None,
            p_time = None,
            p_interval = None,
            ensemble_p = None,
            fluctuations = None,
            x_scale = None,
            y_scale = None,
            particle_size_distribution = None,
            semi_infinite_approx = None,
            material_unit = None,
            masking_threshold = None,
        ),
        "B": FieldRow(
            name="B",
            quantity="# Particles",
            t_grid="TGridB",
            t_av_or_int="Int",
            sync=False,
            output_format="FZ",
            output_route="N",
            output_group="Group B",
            species="SpeciesB" if species and row == "A" else None,
            source="SourceB" if source and row == "A" else None,
            h_grid="HGridB" if h_grid and row == "A" else None,
            z_grid="ZGridB" if z_grid and row == "A" else None,
            bl_average=False if bl_average and row == "A" else None,
            av_time="30min" if av_time and row == "A" else None,
            num_av_times=40 if num_av_times and row == "A" else None,
            across="TZ" if across and row == "A" else None,
            separate_file="YS" if separate_file and row == "A" else None,
            decay_deposition = None,
            source_group = None,
            s_grid = None,
            h_coord = None,
            z_coord = None,
            ensemble_av = None,
            probabilities = None,
            percentiles = None,
            p_time = None,
            p_interval = None,
            ensemble_p = None,
            fluctuations = None,
            x_scale = None,
            y_scale = None,
            particle_size_distribution = None,
            semi_infinite_approx = None,
            material_unit = None,
            masking_threshold = None,
        )
    }
    vals = fields.__dict__
    for i, r in enumerate(["A", "B"]):
        tests[f"{r}.Correct row"] = vals["rows"][i] = expected_rows[r]
    tests["Correct used_keys"] = vals["used_keys"] == expected_used_cols
    tests["Environment present"] = isinstance(
        fields._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_fields_str_all(
    preset_fields: dict[str, dict[str, str | int]],
    fields_expected_str: dict[str, str],
):
    """Does the Main class have the right output?"""
    tests = {}

    fields = Fields.setup(
        rows=preset_fields
    )

    expected_block = "\n".join([
        fields_expected_str["Header"],
        fields_expected_str["A"],
        fields_expected_str["B"],
    ])


    block = str(fields)
    tests["Expected str"] = block == expected_block

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_fields_repr_all(
    preset_fields: dict[str, dict[str, str | int]],
    fields_expected_repr: dict[str, str],
):
    """Does the Main class have the right output?"""
    tests = {}

    fields = Fields.setup(
        rows=preset_fields
    )

    result = repr(fields)

    print(fields_expected_repr)
    print(result)

    tests["Expected repr"] = result == fields_expected_repr

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@pytest.mark.parametrize(
    "bad_key",
    [
        "decay_deposition",
        "source_group",
        "s_grid",
        "h_coord",
        "z_coord",
        "ensemble_av",
        "probabilities",
        "percentiles",
        "p_time",
        "p_interval",
        "ensemble_p",
        "fluctuations",
        "x_scale",
        "y_scale",
        "particle_size_distribution",
        "semi_infinite_approx",
        "material_unit",
        "masking_threshold"
    ]
)
def test_init_fields_not_implemented_error(
    preset_fields: dict[str, dict[str, object]],
    bad_key: str
):
    """Does the Species class initialise?"""
    with pytest.raises(
        NotImplementedError,
        match=(
            f"{bad_key} was specified but is not implemented for Output "
            "Requirements - Fields."
        )
    ):
        _ = Fields.setup(
            rows={"A": preset_fields["A"] | {bad_key: "BAD VALUE"}}
        )


@pytest.mark.parametrize(
    "bad_value",
    [
        { "quantity": 0 },
        { "species": 0 },
        { "source": 0 },
        { "h_grid": 0 },
        { "z_grid": 0 },
        { "t_grid": 0 },
        { "t_av_or_int": 0 },
        { "av_time": 0 },
        { "num_av_times": "BAD VALUE" },
        { "bl_average": "BAD VALUE" },
        { "sync": "BAD VALUE" },
        { "across": 0 },
        { "separate_file": 0 },
        { "output_format": 0 },
        { "output_route": 0 },
        { "output_group": 0 },
    ]
)
def test_init_fields_bad_val(
    preset_fields: dict[str, dict[str, object]],
    bad_value: str
):
    """Does the Species class initialise?"""
    with pytest.raises(
        TypeError,
        match=r"is not.*[(?:bool)|(?:str)]"
    ):
        _ = Fields.setup(
            rows={"A": preset_fields["A"] | bad_value}
        )


@pytest.mark.parametrize(
    "bad_value",
    [
        { "quantity": "BAD VALUE" },
        { "t_av_or_int": "BAD VALUE" }
    ]
)
def test_init_fields_bad_literal(
    preset_fields: dict[str, dict[str, object]],
    bad_value: str
):
    """Does the Species class initialise?"""
    with pytest.raises(
        TypeError,
        match=r"is not a member of"
    ):
        _ = Fields.setup(
            rows={"A": preset_fields["A"] | bad_value}
        )

def test_init_fields_bad_time_interval(
    preset_fields: dict[str, dict[str, object]]
):
    """Does the Species class initialise?"""
    with pytest.raises(
        ValueError,
        match=r"is not a valid time interval recognised by NAME\."
    ):
        _ = Fields.setup(
            rows={"A": preset_fields["A"] | { "av_time": "BAD VALUE" }}
        )

@pytest.mark.parametrize(
    "bad_key",
    [
        "across",
        "separate_file",
        "output_format",
        "output_route"
    ]
)
def test_init_fields_bad_output_string(
    preset_fields: dict[str, dict[str, object]],
    bad_key: str
):
    """Does the Species class initialise?"""
    with pytest.raises(
        ValueError,
        match=r"string recognised by NAME."
    ):
        _ = Fields.setup(
            rows={"A": preset_fields["A"] | {bad_key: "BV"}}
        )

@pytest.fixture
def preset_ppinfo() -> dict[str, dict[str, str | int | float | None]]:
    """Preset rows for species."""
    return {
        "A": {
            "particles": True,
            "puffs": False,
            "met": True,
            "mass": False,
            "plume_rise": True,
            "dispersion_scheme": False,
            "puff_family": True,
            "fate_info": False,
            "h_coord": "Lat-Long",
            "z_coord": "m asl",
            "sync": True,
            "output_route": "D"
        },
        "B": {
            "particles": False,
            "puffs": True,
            "met": False,
            "mass": True,
            "plume_rise": False,
            "dispersion_scheme": True,
            "puff_family": False,
            "fate_info": True,
            "h_coord": "EMEP 50km Grid",
            "z_coord": "m agl",
            "sync": False,
            "output_route": "S"
        },
    }


@pytest.fixture
def ppinfo_expected_str() -> dict[str, str]:
    return {
        "Header": (
            "Output Requirements - Sets of Particle/Puff Information:\n"
            "Output Name,Particles?,Puffs?,"
            "Met?,Mass?,Plume Rise?,"
            "Dispersion Scheme?,Puff Family?,Fate Info?,H-Coord,Z-Coord,"
            "Sync?,Output Route"
        ),
        "A": "A,Yes,No,Yes,No,Yes,No,Yes,No,Lat-Long,m asl,Yes,D",
        "B": "B,No,Yes,No,Yes,No,Yes,No,Yes,EMEP 50km Grid,m agl,No,S"
    }

@pytest.fixture
def ppinfo_expected_repr() -> str:
    return "\n".join([
        "[Output Requirements - Sets of Particle/Puff Information]",
        "\t[[A]]",
        "\t\tparticles           : Yes",
        "\t\tpuffs               : No",
        "\t\tfirst_particle      : None",
        "\t\tlast_particle       : None",
        "\t\tfirst_puff          : None",
        "\t\tlast_puff           : None",
        "\t\tsource              : None",
        "\t\tmet                 : Yes",
        "\t\tmass                : No",
        "\t\tplume_rise          : Yes",
        "\t\tdispersion_scheme   : No",
        "\t\tpuff_family         : Yes",
        "\t\tfate_info           : No",
        "\t\th_coord             : Lat-Long",
        "\t\tz_coord             : m asl",
        "\t\tt_grid              : None",
        "\t\tsync                : Yes",
        "\t\toutput_format       : None",
        "\t\toutput_route        : D",
        "\t[[B]]",
        "\t\tparticles           : No",
        "\t\tpuffs               : Yes",
        "\t\tfirst_particle      : None",
        "\t\tlast_particle       : None",
        "\t\tfirst_puff          : None",
        "\t\tlast_puff           : None",
        "\t\tsource              : None",
        "\t\tmet                 : No",
        "\t\tmass                : Yes",
        "\t\tplume_rise          : No",
        "\t\tdispersion_scheme   : Yes",
        "\t\tpuff_family         : No",
        "\t\tfate_info           : Yes",
        "\t\th_coord             : EMEP 50km Grid",
        "\t\tz_coord             : m agl",
        "\t\tt_grid              : None",
        "\t\tsync                : No",
        "\t\toutput_format       : None",
        "\t\toutput_route        : S"
    ])

@pytest.mark.parametrize("row", ["A", "B"])
def test_init_ppinfo_preset_single(
    preset_ppinfo: dict[str, dict[str, object]],
    row: str,
):
    """Does the PPInfo class initialise?"""
    tests = {}

    row_vals = {row: preset_ppinfo[row]}

    ppinfo = PPInfo.setup(
        rows=row_vals
    )
    expected_used_cols = {
        "name": True,
        "particles": True,
        "puffs": True,
        "met": True,
        "mass": True,
        "plume_rise": True,
        "dispersion_scheme": True,
        "puff_family": True,
        "fate_info": True,
        "h_coord": True,
        "z_coord": True,
        "sync": True,
        "output_route": True,
        "first_particle": False,
        "last_particle": False,
        "first_puff": False,
        "last_puff": False,
        "source": False,
        "t_grid": False,
        "output_format": False
    }
    expected_rows = {
        "A": PPInfoRow(
            name="A",
            particles = "Yes",
            puffs = "No",
            met = "Yes",
            mass = "No",
            plume_rise = "Yes",
            dispersion_scheme = "No",
            puff_family = "Yes",
            fate_info = "No",
            h_coord = "Lat-Long",
            z_coord = "m asl",
            sync = "Yes",
            output_route = "D",
            first_particle = None,
            last_particle = None,
            first_puff = None,
            last_puff = None,
            source = None,
            t_grid = None,
            output_format = None,
        ),
        "B": PPInfoRow(
            name="B",
            particles = "No",
            puffs = "Yes",
            met = "No",
            mass = "Yes",
            plume_rise = "No",
            dispersion_scheme = "Yes",
            puff_family = "No",
            fate_info = "Yes",
            h_coord = "EMEP 50km Grid",
            z_coord = "m agl",
            sync = "No",
            output_route = "S",
            first_particle = None,
            last_particle = None,
            first_puff = None,
            last_puff = None,
            source = None,
            t_grid = None,
            output_format = None,
        )
    }
    vals = ppinfo.__dict__
    tests["Correct row"] = vals["rows"][0] = expected_rows[row]
    tests["Correct used_keys"] = vals["used_keys"] == expected_used_cols
    tests["Environment present"] = isinstance(
        ppinfo._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@pytest.mark.parametrize("row", ["A", "B"])
def test_init_ppinfo_str_single(
    preset_ppinfo: dict[str, dict[str, object]],
    ppinfo_expected_str: dict[str, str],
    row: str,
):
    """Does the PPInfo class initialise?"""
    tests = {}

    row_vals = {row: preset_ppinfo[row]}

    ppinfo = PPInfo.setup(
        rows=row_vals
    )
    expected_str = "\n".join([
        ppinfo_expected_str["Header"],
        ppinfo_expected_str[row]
    ])
    actual = str(ppinfo)
    tests["Expected str"] = actual == expected_str

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())



def test_init_ppinfo_preset_all(
    preset_ppinfo: dict[str, dict[str, object]]
):
    """Does the PPInfo class initialise?"""
    tests = {}

    row_vals = preset_ppinfo

    ppinfo = PPInfo.setup(
        rows=row_vals
    )
    expected_used_cols = {
        "name": True,
        "particles": True,
        "puffs": True,
        "met": True,
        "mass": True,
        "plume_rise": True,
        "dispersion_scheme": True,
        "puff_family": True,
        "fate_info": True,
        "h_coord": True,
        "z_coord": True,
        "sync": True,
        "output_route": True,
        "first_particle": False,
        "last_particle": False,
        "first_puff": False,
        "last_puff": False,
        "source": False,
        "t_grid": False,
        "output_format": False
    }
    expected_rows = {
        "A": PPInfoRow(
            name="A",
            particles = "Yes",
            puffs = "No",
            met = "Yes",
            mass = "No",
            plume_rise = "Yes",
            dispersion_scheme = "No",
            puff_family = "Yes",
            fate_info = "No",
            h_coord = "Lat-Long",
            z_coord = "m asl",
            sync = "Yes",
            output_route = "D",
            first_particle = None,
            last_particle = None,
            first_puff = None,
            last_puff = None,
            source = None,
            t_grid = None,
            output_format = None,
        ),
        "B": PPInfoRow(
            name="B",
            particles = "No",
            puffs = "Yes",
            met = "No",
            mass = "Yes",
            plume_rise = "No",
            dispersion_scheme = "Yes",
            puff_family = "No",
            fate_info = "Yes",
            h_coord = "EMEP 50km Grid",
            z_coord = "m agl",
            sync = "No",
            output_route = "S",
            first_particle = None,
            last_particle = None,
            first_puff = None,
            last_puff = None,
            source = None,
            t_grid = None,
            output_format = None,
        )
    }
    vals = ppinfo.__dict__
    for i, row in enumerate(["A", "B"]):
        tests[f"{row}.Correct row"] = vals["rows"][i] = expected_rows[row]
    tests["Correct used_keys"] = vals["used_keys"] == expected_used_cols
    tests["Environment present"] = isinstance(
        ppinfo._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

def test_init_ppinfo_str_all(
    preset_ppinfo: dict[str, dict[str, object]],
    ppinfo_expected_str: dict[str, str],
):
    """Does the PPInfo class initialise?"""
    tests = {}

    row_vals = preset_ppinfo

    ppinfo = PPInfo.setup(
        rows=row_vals
    )
    expected_str = "\n".join([
        ppinfo_expected_str["Header"],
        ppinfo_expected_str["A"],
        ppinfo_expected_str["B"]
    ])
    actual = str(ppinfo)
    tests["Expected str"] = actual == expected_str

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

def test_init_ppinfo_repr_all(
    preset_ppinfo: dict[str, dict[str, object]],
    ppinfo_expected_repr: str,
):
    """Does the PPInfo class initialise?"""
    tests = {}

    row_vals = preset_ppinfo

    ppinfo = PPInfo.setup(
        rows=row_vals
    )
    actual = repr(ppinfo)
    print(actual)
    tests["Expected repr"] = actual == ppinfo_expected_repr

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

    assert all(tests.values())

@pytest.mark.parametrize(
    "bad_key",
    [
        "particles",
        "puffs",
        "met",
        "mass",
        "plume_rise",
        "dispersion_scheme",
        "puff_family",
        "fate_info",
        "sync",
    ]
)
def test_init_ppinfo_bad_val(
    preset_ppinfo: dict[str, dict[str, object]],
    bad_key: str
):
    """Does the Species class initialise?"""
    with pytest.raises(
        TypeError,
        match=r"is not.*bool.*str"
    ):
        _ = PPInfo.setup(
            rows={"A": preset_ppinfo["A"] | {bad_key: "BAD VALUE"}}
        )

@pytest.mark.parametrize(
    "bad_key",
    [
        "first_particle",
        "last_particle",
        "first_puff",
        "last_puff",
        "source",
        "t_grid",
        "output_format"
    ]
)
def test_init_ppinfo_not_implemented_error(
    preset_ppinfo: dict[str, dict[str, object]],
    bad_key: str
):
    """Does the Species class initialise?"""
    with pytest.raises(
        NotImplementedError,
        match=(
            f"{bad_key} was specified but is not implemented for Output "
            r"Requirements - Sets of PP Info\."
        )
    ):
        _ = PPInfo.setup(
            rows={"A": preset_ppinfo["A"] | {bad_key: "BAD VALUE"}}
        )

@pytest.mark.parametrize(
    "bad_key",
    [
        "h_coord",
        "z_coord",
    ]
)
def test_init_ppinfo_bad_literal(
    preset_ppinfo: dict[str, dict[str, object]],
    bad_key: str
):
    """Does the Species class initialise?"""
    with pytest.raises(
        TypeError,
        match=(
            f"{bad_key} is not a member of.*Expected one of.*"
        )
    ):
        _ = PPInfo.setup(
            rows={"A": preset_ppinfo["A"] | {bad_key: "BAD VALUE"}}
        )


@pytest.mark.parametrize(
    "bad_key",
    [
        # "output_format",
        "output_route"
    ]
)
def test_init_ppinfo_bad_output_string(
    preset_ppinfo: dict[str, dict[str, object]],
    bad_key: str
):
    """Does the Species class initialise?"""
    with pytest.raises(
        ValueError,
        match=r"string recognised by NAME."
    ):
        _ = PPInfo.setup(
            rows={"A": preset_ppinfo["A"] | {bad_key: "BV"}}
        )
