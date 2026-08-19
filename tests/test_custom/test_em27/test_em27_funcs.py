from pathlib import Path
import sqlite3 as db

from netCDF4 import Dataset
import pytest

from enw.custom.em27 import (
    from_fs
)

pytestmark = [
    pytest.mark.custom,
    pytest.mark.custom_em27,
    pytest.mark.custom_em27_func
]

@pytest.fixture(scope="session")
def file_path(tmp_path_factory: pytest.TempdirFactory) -> Path:
    """Path for the DuckDB databases."""
    pth = Path(tmp_path_factory.mktemp("em27_files"))
    sites = {
        "Site A": [
            "project_country_DeviceA_SiteA_250205",
            "project_country_DeviceA_SiteA_250206",
        ],
        "Site B": [
            "project_country_DeviceA_SiteB_250207",
            "project_country_DeviceB_SiteB_250208",
        ],
        "Site C": [
            "project_country_DeviceC_SiteC_250205",
            "project_country_DeviceD_SiteC_250206",
        ],
        "Site D": [
            "project_country_DeviceD_SiteD_250205",
            "project_country_DeviceC_SiteD_250206",
        ],
        "Site E": [
            "project_country_DeviceE_SiteE_250205",
            "project_country_DeviceF_SiteE_250207",
        ],
    }
    for k, v in sites.items():
        pth.joinpath(k).mkdir()
        for f in v:
            make_netcdf(pth.joinpath(k), f)
    return Path(pth)

def make_netcdf(site_pth: Path, name: str) -> Path:
    """Path for the DuckDB databases."""
    pth = site_pth / f"{name}.nc"
    varis = {}
    time_varis = [
        "time",
        "gndP",
        "gndT",
        "azimuth",
        "appSZA",
        "qual_flag",
    ]
    altitude_varis = [
        "height_grid",
        "pressure_grid"
    ]
    time_altitude_varis = [
        "XCO2_AK",
        "XCO2_STR_AK",
        "XCH4_AK",
        "XCH4_S5P_AK",
        "XCO_AK",
    ]
    with Dataset(pth, "w") as nc:
        nc.createDimension("time", 5)
        nc.createDimension("altitude", 4)
        for v in time_varis:
            varis[v] = nc.createVariable(v, "f8", ("time",))
        for v in altitude_varis:
            varis[v] = nc.createVariable(v, "f8", ("altitude",))
        for v in time_altitude_varis:
            varis[v] = nc.createVariable(v, "f8", ("time", "altitude"))
        varis["time"][:] = [
            1747911037,
            1747911337,
            1747911637,
            1747911937,
            1747912237,
        ]
        for v in ["gndP", "gndT", "azimuth", "appSZA"]:
            varis[v][:] = [0.2, 0.4, 0.6, 0.8, 1.0]
        varis["qual_flag"][:] = [1, 1, 0, 1, 0]

        for v in ["height_grid", "pressure_grid"]:
            varis[v][:] = [0.2, 0.4, 0.6, 0.8]

        for v in [
            "XCO2_AK",
            "XCO2_STR_AK",
            "XCH4_AK",
            "XCH4_S5P_AK",
            "XCO_AK",
        ]:
            varis[v][:] = [
                [0.1, 0.2, 0.3, 0.4],
                [1.1, 1.2, 1.3, 1.4],
                [2.1, 2.2, 2.3, 2.4],
                [3.1, 3.2, 3.3, 3.4],
                [4.1, 4.2, 4.3, 4.4],
            ]
    return Path(pth)

@pytest.fixture(scope="session")
def db_path(tmp_path_factory: pytest.TempdirFactory) -> Path:
    """Path for the DuckDB databases."""
    return Path(tmp_path_factory.mktemp("em27_integration_db"))

@pytest.mark.parametrize(
    "species",
    [
        "CH4",
        "CO",
        "CO2",
        ["CH4"],
        ["CO"],
        ["CO2"],
        ["CH4", "CO"],
        ["CO", "CO2"],
        ["CH4", "CO2"],
        ["CH4", "CO", "CO2"]
    ],

)
def test_from_fs_good(
    file_path: Path,
    db_path: Path,
    species: str | list[str]
):
    """"""
    db_file = db_path / f"test_from_fs_good_{species}.db"
    counts = {}
    tests = {}

    species_mult = 1 if isinstance(species, str) else len(species)

    expected_counts = {
        "device": 6,
        "site": 5,
        "height": 27,
        "height_var": 135 * species_mult,
        "surface_var": 45,
        "pfiles": 10
    }

    conn = db.connect(db_file)
    cur = conn.cursor()
    from_fs(
        file_path,
        conn,
        species
    )
    cur.execute("""SELECT COUNT(*) FROM dim_device;""")
    counts["device"] = cur.fetchone()[0]

    cur.execute("""SELECT COUNT(*) FROM dim_site;""")
    counts["site"] = cur.fetchone()[0]

    cur.execute("""SELECT COUNT(*) FROM dim_height;""")
    counts["height"] = cur.fetchone()[0]

    cur.execute("""SELECT COUNT(*) FROM fact_height_vars;""")
    counts["height_var"] = cur.fetchone()[0]

    cur.execute("""SELECT COUNT(*) FROM fact_surface_vars;""")
    counts["surface_var"] = cur.fetchone()[0]

    cur.execute("""SELECT COUNT(*) FROM meta_processed_files;""")
    counts["pfiles"] = cur.fetchone()[0]


    cur.close()
    conn.close()

    for k, v in counts.items():
        tests[f"Correct count: {k}"] = expected_counts[k] == v

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

def test_from_fs_bad_empty_species(
    file_path: Path,
    db_path: Path,
):
    """"""
    db_file = db_path / "test_from_fs_bad_empty_species.db"
    conn = db.connect(db_file)
    with pytest.raises(ValueError, match=r"Expected at least one species\."):
        from_fs(file_path, conn, [])
    conn.close()
