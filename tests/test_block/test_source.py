from jinja2 import Environment
import pytest

from enw.block import (
    Sources,
    Species,
    SpeciesUses
)
from enw.block._source import (
    SourcesRow,
    SpeciesRow,
)

pytestmark = [
    pytest.mark.block,
    pytest.mark.block_source
]

@pytest.fixture
def preset_species() -> dict[str, dict[str, str | int | float | None]]:
    """Preset rows for species."""
    return {
        "A": {
            "category": "TEST",
            "deposition_velocity": 0,
            "molecular_weight": 1,
            "material_unit": "g",
            "uv_loss_rate": 0,
            "half_life": "0:30",
            "daughter": "TestDaughter",
            "surface_resistance": None
        },
        "B": {
            "category": "TEST",
            "deposition_velocity": 1,
            "molecular_weight": 2,
            "material_unit": "g",
            "uv_loss_rate": 5,
            "half_life": None,
            "surface_resistance": 1
        },
    }

@pytest.fixture
def species_expected_header() -> dict[str, str]:
    return {
        "A": (
            "Name,Category,Deposition Velocity,Molecular Weight,Material Unit,"
            "UV Loss Rate,Half Life,Daughter"
        ),
        "B": (
            "Name,Category,Deposition Velocity,Molecular Weight,Material Unit,"
            "UV Loss Rate,Half Life,Surface Resistance"
        ),
        "Both": (
            "Name,Category,Deposition Velocity,Molecular Weight,Material Unit,"
            "UV Loss Rate,Half Life,Daughter,Surface Resistance"
        )
    }

@pytest.fixture
def species_expected_rows() -> dict[str, str]:
    return {
        "A": (
            "A,TEST,0,1,g,0,0:30,TestDaughter"
        ),
        "B": (
            "B,TEST,1,2,g,5,Stable,1"
        )
    }

@pytest.fixture
def species_expected_repr() -> str:
    return "\n".join([
        "[Species]",
        "\t[[A]]",
        "\t\tcategory                   : TEST",
        "\t\tdeposition_velocity        : 0",
        "\t\tmolecular_weight           : 1",
        "\t\tmaterial_unit              : g",
        "\t\thalf_life                  : 0:30",
        "\t\tsurface_resistance         : None",
        "\t\tuv_loss_rate               : 0",
        "\t\tdaughter                   : TestDaughter",
        "\t\tbranching_ratio            : None",
        "\t\tcloud_gamma_parameters     : None",
        "\t\tbelow_cloud_rain_a         : None",
        "\t\tbelow_cloud_rain_b         : None",
        "\t\tin_cloud_rain_a            : None",
        "\t\tin_cloud_rain_b            : None",
        "\t\tbelow_cloud_snow_a         : None",
        "\t\tbelow_cloud_snow_b         : None",
        "\t\tin_cloud_snow_a            : None",
        "\t\tin_cloud_snow_b            : None",
        "\t\tland_use_dependent_dry_dep : None",
        "\t\tmean_aerosol_diameter      : None",
        "\t[[B]]",
        "\t\tcategory                   : TEST",
        "\t\tdeposition_velocity        : 1",
        "\t\tmolecular_weight           : 2",
        "\t\tmaterial_unit              : g",
        "\t\thalf_life                  : Stable",
        "\t\tsurface_resistance         : 1",
        "\t\tuv_loss_rate               : 5",
        "\t\tdaughter                   : TestDaughter",
        "\t\tbranching_ratio            : None",
        "\t\tcloud_gamma_parameters     : None",
        "\t\tbelow_cloud_rain_a         : None",
        "\t\tbelow_cloud_rain_b         : None",
        "\t\tin_cloud_rain_a            : None",
        "\t\tin_cloud_rain_b            : None",
        "\t\tbelow_cloud_snow_a         : None",
        "\t\tbelow_cloud_snow_b         : None",
        "\t\tin_cloud_snow_a            : None",
        "\t\tin_cloud_snow_b            : None",
        "\t\tland_use_dependent_dry_dep : None",
        "\t\tmean_aerosol_diameter      : None",
    ])

@pytest.mark.parametrize("row", ["A", "B"])
def test_init_species_preset_single(
    row: str,
    preset_species: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    tests = {}

    species = Species.setup(
        rows={row: preset_species[row]}
    )
    expected_used_cols = {
        "name": True,
        "category": True,
        "deposition_velocity": True,
        "molecular_weight": True,
        "material_unit": True,
        "half_life": True,
        "surface_resistance": row == "B",
        "uv_loss_rate": True,
        "daughter": row == "A",
        "branching_ratio": False,
        "cloud_gamma_parameters": False,
        "below_cloud_rain_a": False,
        "below_cloud_rain_b": False,
        "in_cloud_rain_a": False,
        "in_cloud_rain_b": False,
        "below_cloud_snow_a": False,
        "below_cloud_snow_b": False,
        "in_cloud_snow_a": False,
        "in_cloud_snow_b": False,
        "land_use_dependent_dry_dep": False,
        "mean_aerosol_diameter": False,
    }
    expected_rows = {
        "A": SpeciesRow(
            name="A",
            category="Test",
            deposition_velocity=0,
            molecular_weight=1,
            material_unit="g",
            uv_loss_rate=0,
            half_life="0:30",
            daughter="TestDaughter",
            surface_resistance=None
        ),
        "B": SpeciesRow(
            name="B",
            category="Test",
            deposition_velocity=1,
            molecular_weight=2,
            material_unit="g",
            uv_loss_rate=5,
            half_life="Stable",
            surface_resistance=1
        )
    }
    vals = species.__dict__
    tests["Correct row"] = vals["rows"] = expected_rows[row]
    tests["Correct used_keys"] = vals["used_keys"] == expected_used_cols
    tests["Environment present"] = isinstance(
        species._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_species_preset_both(
    preset_species: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    tests = {}

    species = Species.setup(
        rows=preset_species
    )
    expected_used_cols = {
        "name": True,
        "category": True,
        "deposition_velocity": True,
        "molecular_weight": True,
        "material_unit": True,
        "half_life": True,
        "surface_resistance": True,
        "uv_loss_rate": True,
        "daughter": True,
        "branching_ratio": False,
        "cloud_gamma_parameters": False,
        "below_cloud_rain_a": False,
        "below_cloud_rain_b": False,
        "in_cloud_rain_a": False,
        "in_cloud_rain_b": False,
        "below_cloud_snow_a": False,
        "below_cloud_snow_b": False,
        "in_cloud_snow_a": False,
        "in_cloud_snow_b": False,
        "land_use_dependent_dry_dep": False,
        "mean_aerosol_diameter": False,
    }
    expected_rows = [
        SpeciesRow(
            name="A",
            category="Test",
            deposition_velocity=0,
            molecular_weight=1,
            material_unit="g",
            uv_loss_rate=0,
            half_life="0:30",
            surface_resistance=None
        ),
        SpeciesRow(
            name="B",
            category="Test",
            deposition_velocity=1,
            molecular_weight=2,
            material_unit="g",
            uv_loss_rate=5,
            half_life="Stable",
            surface_resistance=1
        )
    ]
    vals = species.__dict__
    for i in range(2):
        tests[f"{i} Correct row"] = vals["rows"][i] = expected_rows[i]
    tests["Correct used_keys"] = vals["used_keys"] == expected_used_cols
    tests["Environment present"] = isinstance(
        species._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("row", ["A", "B"])
def test_species_str_single(
    row: str,
    preset_species: dict[str, dict[str, object]],
    species_expected_rows: dict[str, str],
    species_expected_header: dict[str, str],
):
    """Does the Species class initialise?"""
    tests = {}

    species = Species.setup(
        rows={row: preset_species[row]}
    )
    expected_str = "\n".join([
        "Species:",
        species_expected_header[row],
        species_expected_rows[row]
    ])
    actual_str = str(species)
    tests["Expected str"] = expected_str == actual_str

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

def test_species_str_both(
    preset_species: dict[str, dict[str, object]],
    species_expected_rows: dict[str, str],
    species_expected_header: dict[str, str],
):
    """Does the Species class initialise?"""
    tests = {}

    species = Species.setup(
        rows=preset_species
    )
    expected_str = "\n".join([
        "Species:",
        species_expected_header["Both"],
        species_expected_rows["A"] + ",",
        species_expected_rows["B"].replace("ble,", "ble,,")
    ])
    actual_str = str(species)
    print(expected_str)
    print(actual_str)
    tests["Expected str"] = expected_str == actual_str

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize(
    "bad_key",
    [
        "branching_ratio",
        "cloud_gamma_parameters",
        "below_cloud_rain_a",
        "below_cloud_rain_b",
        "in_cloud_rain_a",
        "in_cloud_rain_b",
        "below_cloud_snow_a",
        "below_cloud_snow_b",
        "in_cloud_snow_a",
        "in_cloud_snow_b",
        "land_use_dependent_dry_dep",
        "mean_aerosol_diameter"
    ]
)
def test_init_species_unimplemented_key(
    preset_species: dict[str, dict[str, object]],
    bad_key: str,
):
    """Does the Species class initialise?"""
    with pytest.raises(
        NotImplementedError,
        match=f"{bad_key} was specified but is not implemented for Species."
    ):
        _ = Species.setup(
            rows={"A": preset_species["A"] | {bad_key: "BAD VALUE"}}
        )

@pytest.mark.parametrize("popped_key", ["half_life", "daughter"])
def test_init_species_no_daughter_or_half_life(
    preset_species: dict[str, dict[str, object]],
    popped_key: str,
):
    """Does the Species class initialise?"""
    bad_config = preset_species["A"]
    bad_config.pop(popped_key)
    print(bad_config)
    with pytest.raises(
        ValueError,
        match=f"{popped_key} must be specified with"
    ):
        _ = Species.setup(
            rows={"A": bad_config}
        )

def test_init_species_daughter_half_life_stable(
    preset_species: dict[str, dict[str, object]]
):
    """Does the Species class initialise?"""
    bad_config = preset_species["A"]
    bad_config["half_life"] = "Stable"
    print(bad_config)
    with pytest.raises(
        ValueError,
        match=r"half_life must be specified with daughter\."
    ):
        _ = Species.setup(
            rows={"A": bad_config}
        )

def test_species_expected_repr(
    preset_species: dict[str, dict[str, object]],
    species_expected_repr: str
):
    """Does the Species class initialise?"""
    tests = {}

    species = Species.setup(
        rows=preset_species
    )
    tests["Expected str"] = repr(species) == species_expected_repr

    for test, result in tests.items():
        if not result:
            print(test)

@pytest.fixture
def preset_sources() -> dict[str, dict[str, str | bool | int | float | None]]:
    """Preset rows for species."""
    return {
        "A": {
            "shape": "Cuboid",
            "set_of_locations": "Set A",
            "location": "Location A",
            "h_coord": "Lat-Long",
            "z_coord": "m asl",
            "z": 20,
            "dh_metres": True,
            "dz_metres": False,
            "dx": 0,
            "dy": 0,
            "dz": 0,
            "angle": 0,
            "source_strength": "SpeciesA 1.0 g/s",
            "plume_rise": False,
            "temperature": 1,
            "volume_flow_rate": 5,
            "num_particles": 20000,
            "max_age": "infinity",
            "top_hat": True,
            "start_time": "01/01/2020 00:00",
            "stop_time": "02/01/2020 00:00",
        },
        "B": {
            "shape": "Ellipsoid",
            "set_of_locations": "Set B",
            "location": "Location B",
            "h_coord": "EMEP 50km Grid",
            "z_coord": "m agl",
            "z": 200,
            "dh_metres": False,
            "dz_metres": True,
            "dx": 20,
            "dy": 30,
            "dz": 40,
            "angle": 50,
            "source_strength": "SpeciesB 0.5 g/s",
            "plume_rise": True,
            "temperature": -20,
            "volume_flow_rate": 100,
            "num_particles": 20.5,
            "max_age": "2d 00:00",
            "top_hat": False,
            "start_time": "01/01/2020 12:00",
            "stop_time": "02/01/2020 12:00",
        },
        "C": {
            "shape": "Cylindroid",
            "set_of_locations": "Set C",
            "location": "Location C",
            "h_coord": "UK National Grid (m)",
            "z_coord": "Pa",
            "z": 0,
            "dh_metres": True,
            "dz_metres": True,
            "dx": 0,
            "dy": 1,
            "dz": 2,
            "angle": -30,
            "source_strength": "SpeciesC 10 g/s",
            "plume_rise": True,
            "temperature": 30,
            "volume_flow_rate": 300,
            "num_particles": 4,
            "max_age": "00:05",
            "top_hat": True,
            "start_time": "01/01/2020 12:00:12",
            "stop_time": "02/01/2020 12:00:11",
        },
    }

@pytest.fixture
def sources_expected_header() -> str:
    return (
        "Name,Shape,Set of Locations,Location,H-Coord,Z-Coord,Z,dH-Metres?,"
        "dZ-Metres?,dX,dY,dZ,Angle,Source Strength,Plume Rise?,Temperature,"
        "Volume Flow Rate,# Particles,Max Age,Top Hat,Start Time,Stop Time"
    )

@pytest.fixture
def sources_expected_rows() -> dict[str, str]:
    return {
        "A": (
            "A,Cuboid,Set A,Location A,Lat-Long,m asl,20,Yes,No,0,0,0,0,"
            "SpeciesA 1.0 g/s,No,1,5,20000,infinity,Yes,01/01/2020 00:00,"
            "02/01/2020 00:00"
        ),
        "B": (
            "B,Ellipsoid,Set B,Location B,EMEP 50km Grid,m agl,200,No,Yes,"
            "20,30,40,50,SpeciesB 0.5 g/s,Yes,-20,100,20.5,2d 00:00,No,"
            "01/01/2020 12:00,02/01/2020 12:00"
        ),
        "C": (
            "C,Cylindroid,Set C,Location C,UK National Grid (m),Pa,0,Yes,Yes,"
            "0,1,2,-30,SpeciesC 10 g/s,Yes,30,300,4,00:05,Yes,"
            "01/01/2020 12:00:12,02/01/2020 12:00:11"
        )
    }

@pytest.fixture
def sources_expected_repr() -> dict[str, str]:
    return {
        "A": "\n".join([
            "\t[[A]]",
            "\t\tshape                         : Cuboid",
            "\t\tset_of_locations              : Set A",
            "\t\tlocation                      : Location A",
            "\t\th_coord                       : Lat-Long",
            "\t\tz_coord                       : m asl",
            "\t\tz                             : 20",
            "\t\tdh_metres                     : Yes",
            "\t\tdz_metres                     : No",
            "\t\tdx                            : 0",
            "\t\tdy                            : 0",
            "\t\tdz                            : 0",
            "\t\tangle                         : 0",
            "\t\tsource_strength               : SpeciesA 1.0 g/s",
            "\t\tplume_rise                    : No",
            "\t\ttemperature                   : 1",
            "\t\tvolume_flow_rate              : 5",
            "\t\tnum_particles                 : 20000",
            "\t\tmax_age                       : infinity",
            "\t\ttop_hat                       : Yes",
            "\t\tstart_time                    : 01/01/2020 00:00",
            "\t\tstop_time                     : 02/01/2020 00:00",
            "\t\th_grid                        : None",
            "\t\tz_grid                        : None",
            "\t\tx                             : None",
            "\t\ty                             : None",
            "\t\tuniform_area                  : None",
            "\t\tno_reflect                    : None",
            "\t\ttime_dependency               : None",
            "\t\tflow_velocity                 : None",
            "\t\tparticle_diameter             : None",
            "\t\tparticle_density              : None",
            "\t\tparticle_size_distribution    : None",
            "\t\tmet_dependent_source_type     : None",
            "\t\tsource_groups                 : None",
        ]),
        "B": "\n".join([
            "\t[[B]]",
            "\t\tshape                         : Ellipsoid",
            "\t\tset_of_locations              : Set B",
            "\t\tlocation                      : Location B",
            "\t\th_coord                       : EMEP 50km Grid",
            "\t\tz_coord                       : m agl",
            "\t\tz                             : 200",
            "\t\tdh_metres                     : No",
            "\t\tdz_metres                     : Yes",
            "\t\tdx                            : 20",
            "\t\tdy                            : 30",
            "\t\tdz                            : 40",
            "\t\tangle                         : 50",
            "\t\tsource_strength               : SpeciesB 0.5 g/s",
            "\t\tplume_rise                    : Yes",
            "\t\ttemperature                   : -20",
            "\t\tvolume_flow_rate              : 100",
            "\t\tnum_particles                 : 20.5",
            "\t\tmax_age                       : 2d 00:00",
            "\t\ttop_hat                       : No",
            "\t\tstart_time                    : 01/01/2020 12:00",
            "\t\tstop_time                     : 02/01/2020 12:00",
            "\t\th_grid                        : None",
            "\t\tz_grid                        : None",
            "\t\tx                             : None",
            "\t\ty                             : None",
            "\t\tuniform_area                  : None",
            "\t\tno_reflect                    : None",
            "\t\ttime_dependency               : None",
            "\t\tflow_velocity                 : None",
            "\t\tparticle_diameter             : None",
            "\t\tparticle_density              : None",
            "\t\tparticle_size_distribution    : None",
            "\t\tmet_dependent_source_type     : None",
            "\t\tsource_groups                 : None",
        ]),
        "C": "\n".join([
            "\t[[C]]",
            "\t\tshape                         : Cylindroid",
            "\t\tset_of_locations              : Set C",
            "\t\tlocation                      : Location C",
            "\t\th_coord                       : UK National Grid (m)",
            "\t\tz_coord                       : Pa",
            "\t\tz                             : 0",
            "\t\tdh_metres                     : Yes",
            "\t\tdz_metres                     : Yes",
            "\t\tdx                            : 0",
            "\t\tdy                            : 1",
            "\t\tdz                            : 2",
            "\t\tangle                         : -30",
            "\t\tsource_strength               : SpeciesC 10 g/s",
            "\t\tplume_rise                    : Yes",
            "\t\ttemperature                   : 30",
            "\t\tvolume_flow_rate              : 300",
            "\t\tnum_particles                 : 4",
            "\t\tmax_age                       : 00:05",
            "\t\ttop_hat                       : Yes",
            "\t\tstart_time                    : 01/01/2020 12:00:12",
            "\t\tstop_time                     : 02/01/2020 12:00:11",
            "\t\th_grid                        : None",
            "\t\tz_grid                        : None",
            "\t\tx                             : None",
            "\t\ty                             : None",
            "\t\tuniform_area                  : None",
            "\t\tno_reflect                    : None",
            "\t\ttime_dependency               : None",
            "\t\tflow_velocity                 : None",
            "\t\tparticle_diameter             : None",
            "\t\tparticle_density              : None",
            "\t\tparticle_size_distribution    : None",
            "\t\tmet_dependent_source_type     : None",
            "\t\tsource_groups                 : None",
        ])
    }

@pytest.mark.parametrize("row", ["A", "B", "C"])
def test_init_sources_preset_single(
    row: str,
    preset_sources: dict[str, dict[str, str | int | float | bool | None]],
):
    """Does the Sources class initialise?"""
    tests = {}

    sources = Sources.setup(
        rows={row: preset_sources[row]}
    )
    expected_used_cols = {
        "name": True,
        "shape": True,
        "set_of_locations": True,
        "location": True,
        "h_coord": True,
        "z_coord": True,
        "z": True,
        "dh_metres": True,
        "dz_metres": True,
        "dx": True,
        "dy": True,
        "dz": True,
        "angle": True,
        "source_strength": True,
        "plume_rise": True,
        "temperature": True,
        "volume_flow_rate": True,
        "num_particles": True,
        "max_age": True,
        "top_hat": True,
        "start_time": True,
        "stop_time": True,
        "h_grid": False,
        "z_grid": False,
        "x": False,
        "y": False,
        "uniform_area": False,
        "no_reflect": False,
        "time_dependency": False,
        "flow_velocity": False,
        "particle_diameter": False,
        "particle_density": False,
        "particle_size_distribution": False,
        "met_dependent_source_type": False,
        "source_groups": False,
    }
    expected_rows = {
        "A": SourcesRow(
            name = "A",
            shape = "Cuboid",
            set_of_locations = "Set A",
            location = "Location A",
            h_coord = "Lat-Long",
            z_coord = "m asl",
            z = 20,
            dh_metres = "Yes",
            dz_metres = "No",
            dx = 0,
            dy = 0,
            dz = 0,
            angle = 0,
            source_strength = "SpeciesA 1.0 g/s",
            plume_rise = "No",
            temperature = 1,
            volume_flow_rate = 5,
            num_particles = 20000,
            max_age = "infinity",
            top_hat = "Yes",
            start_time = "01/01/2020 00:00",
            stop_time = "02/01/2020 00:00",
        ),
        "B": SourcesRow(
            name = "B",
            shape = "Ellipsoid",
            set_of_locations = "Set B",
            location = "Location B",
            h_coord = "EMEP 50km Grid",
            z_coord = "m agl",
            z = 200,
            dh_metres = "No",
            dz_metres = "Yes",
            dx = 20,
            dy = 30,
            dz = 40,
            angle = 50,
            source_strength = "SpeciesB 0.5 g/s",
            plume_rise = "Yes",
            temperature = -20,
            volume_flow_rate = 100,
            num_particles = 20.5,
            max_age = "2 days 00:00",
            top_hat = "No",
            start_time = "01/01/2020 12:00",
            stop_time = "02/01/2020 12:00",
        ),
        "C": SourcesRow(
            name = "C",
            shape = "Cylindroid",
            set_of_locations = "Set C",
            location = "Location C",
            h_coord = "UK National Grid (m)",
            z_coord = "Pa",
            z = 0,
            dh_metres = "Yes",
            dz_metres = "Yes",
            dx = 0,
            dy = 1,
            dz = 2,
            angle = -30,
            source_strength = "SpeciesC 10 g/s",
            plume_rise = "Yes",
            temperature = 30,
            volume_flow_rate = 300,
            num_particles = 4,
            max_age = "00:05",
            top_hat = "Yes",
            start_time = "01/01/2020 12:00:12",
            stop_time = "02/01/2020 12:00:11",
        )
    }
    vals = sources.__dict__
    tests["Correct row"] = vals["rows"] = expected_rows[row]
    tests["Correct used_keys"] = vals["used_keys"] == expected_used_cols
    print(vals["used_keys"])
    print(expected_used_cols)
    tests["Environment present"] = isinstance(
        sources._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

def test_init_sources_preset_all(
    preset_sources: dict[str, dict[str, str | int | float | bool | None]]
):
    """Does the Sources class initialise?"""
    tests = {}

    sources = Sources.setup(
        rows=preset_sources
    )
    expected_used_cols = {
        "name": True,
        "shape": True,
        "set_of_locations": True,
        "location": True,
        "h_coord": True,
        "z_coord": True,
        "z": True,
        "dh_metres": True,
        "dz_metres": True,
        "dx": True,
        "dy": True,
        "dz": True,
        "angle": True,
        "source_strength": True,
        "plume_rise": True,
        "temperature": True,
        "volume_flow_rate": True,
        "num_particles": True,
        "max_age": True,
        "top_hat": True,
        "start_time": True,
        "stop_time": True,
        "h_grid": False,
        "z_grid": False,
        "x": False,
        "y": False,
        "uniform_area": False,
        "no_reflect": False,
        "time_dependency": False,
        "flow_velocity": False,
        "particle_diameter": False,
        "particle_density": False,
        "particle_size_distribution": False,
        "met_dependent_source_type": False,
        "source_groups": False,
    }
    expected_rows = [
        SourcesRow(
            name = "A",
            shape = "Cuboid",
            set_of_locations = "Set A",
            location = "Location A",
            h_coord = "Lat-Long",
            z_coord = "m asl",
            z = 20,
            dh_metres = "Yes",
            dz_metres = "No",
            dx = 0,
            dy = 0,
            dz = 0,
            angle = 0,
            source_strength = "SpeciesA 1.0 g/s",
            plume_rise = "No",
            temperature = 1,
            volume_flow_rate = 5,
            num_particles = 20000,
            max_age = "infinity",
            top_hat = "Yes",
            start_time = "01/01/2020 00:00",
            stop_time = "02/01/2020 00:00",
        ),
        SourcesRow(
            name = "B",
            shape = "Ellipsoid",
            set_of_locations = "Set B",
            location = "Location B",
            h_coord = "EMEP 50km Grid",
            z_coord = "m agl",
            z = 200,
            dh_metres = "No",
            dz_metres = "Yes",
            dx = 20,
            dy = 30,
            dz = 40,
            angle = 50,
            source_strength = "SpeciesB 0.5 g/s",
            plume_rise = "Yes",
            temperature = -20,
            volume_flow_rate = 100,
            num_particles = 20.5,
            max_age = "2 days 00:00",
            top_hat = "No",
            start_time = "01/01/2020 12:00",
            stop_time = "02/01/2020 12:00",
        ),
        SourcesRow(
            name = "C",
            shape = "Cylindroid",
            set_of_locations = "Set C",
            location = "Location C",
            h_coord = "UK National Grid (m)",
            z_coord = "Pa",
            z = 0,
            dh_metres = "Yes",
            dz_metres = "Yes",
            dx = 0,
            dy = 1,
            dz = 2,
            angle = -30,
            source_strength = "SpeciesC 10 g/s",
            plume_rise = "Yes",
            temperature = 30,
            volume_flow_rate = 300,
            num_particles = 4,
            max_age = "00:05",
            top_hat = "Yes",
            start_time = "01/01/2020 12:00:12",
            stop_time = "02/01/2020 12:00:11",
        )
    ]
    vals = sources.__dict__
    for i in range(2):
        tests[f"{i} Correct row"] = vals["rows"][i] = expected_rows[i]
    tests["Correct used_keys"] = vals["used_keys"] == expected_used_cols
    print(vals["used_keys"])
    print(expected_used_cols)
    tests["Environment present"] = isinstance(
        sources._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@pytest.mark.parametrize(
    "bad_key",
    [
        "h_grid",
        "z_grid",
        "x",
        "y",
        "uniform_area",
        "no_reflect",
        "time_dependency",
        "flow_velocity",
        "particle_diameter",
        "particle_density",
        "particle_size_distribution",
        "met_dependent_source_type",
        "source_groups"
    ]
)
def test_init_sources_unimplemented_key(
    preset_sources: dict[
        str,
        dict[str, dict[str, str | int | float | bool | None]]
    ],
    bad_key: str,
):
    """Does the Sources class initialise with bad key?"""
    with pytest.raises(
        NotImplementedError,
        match=f"{bad_key} was specified but is not implemented for Sources."
    ):
        _ = Sources.setup(
            rows={"A": preset_sources["A"] | {bad_key: "BAD VALUE"}}
        )

@pytest.mark.parametrize("row", ["A", "B", "C"])
def test_sources_str_single(
    row: str,
    preset_sources: dict[str, dict[str, object]],
    sources_expected_header: str,
    sources_expected_rows: dict[str, str]
):
    """Does the Sources class create the correct str?"""
    tests = {}

    sources = Sources.setup(
        rows={row: preset_sources[row]}
    )
    expected_str = "\n".join([
        "Sources:",
        sources_expected_header,
        sources_expected_rows[row]
    ])
    actual_str = str(sources)
    tests["Expected str"] = expected_str == actual_str

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

def test_sources_str_all(
    preset_sources: dict[str, dict[str, object]],
    sources_expected_header: str,
    sources_expected_rows: dict[str, str]
):
    """Does the Sources class create the correct str?"""
    tests = {}

    sources = Sources.setup(
        rows=preset_sources
    )
    expected_str = "\n".join([
        "Sources:",
        sources_expected_header,
        *sources_expected_rows.values()
    ])
    actual_str = str(sources)
    tests["Expected str"] = expected_str == actual_str

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@pytest.mark.parametrize("row", ["A", "B", "C"])
def test_sources_repr_single(
    row: str,
    preset_sources: dict[str, dict[str, object]],
    sources_expected_repr: dict[str, str],
):
    """Does the Sources class create the correct repr?"""
    tests = {}

    sources = Sources.setup(
        rows={row: preset_sources[row]}
    )
    expected_repr = "\n".join([
        "[Sources]",
        sources_expected_repr[row]
    ])
    actual_repr = repr(sources)
    tests["Expected repr"] = expected_repr == actual_repr

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

def test_sources_repr_all(
    preset_sources: dict[str, dict[str, object]],
    sources_expected_repr: dict[str, str],
):
    """Does the Sources class create the correct repr?"""
    tests = {}

    sources = Sources.setup(
        rows=preset_sources
    )
    expected_repr = "\n".join([
        "[Sources]",
        *sources_expected_repr.values()
    ])
    actual_repr = repr(sources)
    tests["Expected repr"] = expected_repr == actual_repr

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@pytest.mark.parametrize(
    "bad_key_val",
    [
        ("shape", "Not a real shape"),
        ("set_of_locations", 0),
        ("location", 0),
        ("h_coord", "Not a real h_coord"),
        ("z_coord", "Not a real z_coord"),
        ("z", "BAD VALUE"),
        ("dh_metres", "BAD VALUE"),
        ("dz_metres", "BAD VALUE"),
        ("dx", "BAD VALUE"),
        ("dy", "BAD VALUE"),
        ("dz", "BAD VALUE"),
        ("angle", "BAD VALUE"),
        ("source_strength", 0),
        ("plume_rise", "BAD VALUE"),
        ("temperature", "BAD VALUE"),
        ("volume_flow_rate", "BAD VALUE"),
        ("num_particles", "BAD VALUE"),
        ("max_age", 0),
        ("top_hat", "BAD VALUE"),
        ("start_time", 0),
        ("stop_time", 0),
    ]
)
def test_init_bad_key(
    preset_sources: dict[
        str,
        dict[str, dict[str, str | int | float | bool | None]]
    ],
    bad_key_val: tuple[str, str | int]
):
    """Does the Sources class error with bad value?"""
    bad_key = bad_key_val[0]
    bad_value = bad_key_val[1]
    with pytest.raises(
        (TypeError, ValueError),
        match=f"{bad_key} is not.*. Is.*.|is not a member of"
    ):
        _ = Sources.setup(
            rows={"A": preset_sources["A"] | {bad_key: bad_value}}
        )


@pytest.fixture
def preset_uses() -> dict[str, dict[str, str | int | float | None]]:
    """Preset rows for uses."""
    return {
        "A": {
            "name": "TestA",
            "on_particles": True,
            "on_fields": False,
            "advect_field": True
        },
        "B": {
            "name": "TestB",
            "on_particles": False,
            "on_fields": True,
            "advect_field": False
        },
    }

@pytest.fixture
def uses_expected_str() -> dict[str, str]:
    return {
        "Header": (
            "Species Uses:\nSpecies,On Particles?,On Fields?,Advect Field?"
        ),
        "A": (
            "TestA,Yes,No,Yes"
        ),
        "B": (
            "TestB,No,Yes,No"
        )
    }

@pytest.fixture
def uses_expected_repr() -> dict[str, str]:
    return {
        "A": "\n".join([
            "[Species Uses]",
            "\tname                                    : TestA",
            "\ton_particles                            : Yes",
            "\ton_fields                               : No",
            "\tadvect_field                            : Yes",
            "\tparticle_size_distribution_for_fields   : None",
        ]),
        "B": "\n".join([
            "[Species Uses]",
            "\tname                                    : TestB",
            "\ton_particles                            : No",
            "\ton_fields                               : Yes",
            "\tadvect_field                            : No",
            "\tparticle_size_distribution_for_fields   : None",
        ]),
    }

@pytest.mark.parametrize("row", ["A", "B"])
def test_init_uses(
    row: str,
    preset_uses: dict[str, str | bool]
):
    """Does the Species class initialise?"""
    tests = {}

    uses = SpeciesUses.setup(
        **preset_uses[row]
    )
    expected_rows = {
        "A": {
            "name": "TestA",
            "on_particles": "Yes",
            "on_fields": "No",
            "advect_field": "Yes"
        },
        "B": {
            "name": "TestB",
            "on_particles": "No",
            "on_fields": "Yes",
            "advect_field": "No"
        }
    }
    vals = uses.__dict__
    print(vals)
    for k, v in expected_rows[row].items():
        tests[f"Correct val: {k}"] = v == vals[k]

    tests["Environment present"] = isinstance(
        uses._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("row", ["A", "B"])
def test_init_uses_str(
    row: str,
    preset_uses: dict[str, dict[str, object]],
    uses_expected_str: dict[str, str]
):
    """Does the Species class initialise?"""
    tests = {}

    uses = SpeciesUses.setup(
        **preset_uses[row]
    )

    expected = "\n".join([
        uses_expected_str["Header"],
        uses_expected_str[row],
    ])
    actual = str(uses)
    print(expected)
    print(actual)

    tests["Expected str"] = actual == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("row", ["A", "B"])
def test_init_uses_repr(
    row: str,
    preset_uses: dict[str, dict[str, object]],
    uses_expected_repr: dict[str, str]
):
    """Does the Species class initialise?"""
    tests = {}

    uses = SpeciesUses.setup(
        **preset_uses[row]
    )

    actual = repr(uses)

    tests["Expected repr"] = actual == uses_expected_repr[row]
    print(uses_expected_repr[row])
    print(actual)

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("bad_arg", [
        ("name", 0),
])
def test_init_uses_bad_base_type(
    bad_arg: tuple[str, str | int],
    preset_uses: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    vals = preset_uses["A"]
    vals[bad_arg[0]] = bad_arg[1]
    with pytest.raises(
        TypeError,
        match=r"is not.*str.*Is.*int"
    ):
        _ = SpeciesUses.setup(
            **vals
        )


@pytest.mark.parametrize("bad_key", [
    "on_particles",
    "on_fields",
    "advect_field",
])
def test_init_uses_bad_switch(
    bad_key: str,
    preset_uses: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    vals = preset_uses["A"]
    vals[bad_key] = "BAD VALUE"
    with pytest.raises(
        TypeError,
        match=r"is not.*bool.*Is.*str"
    ):
        _ = SpeciesUses.setup(
            **vals
        )


@pytest.mark.parametrize("bad_key", [
    "particle_size_distribution_for_fields",
])
def test_init_uses_unimplemented(
    bad_key: str,
    preset_uses: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    vals = preset_uses["A"]
    vals[bad_key] = "BAD VALUE"
    with pytest.raises(
        NotImplementedError,
        match=(
            f"{bad_key} was specified but is not implemented for Species Uses."
        )
    ):
        _ = SpeciesUses.setup(
            **vals
        )
