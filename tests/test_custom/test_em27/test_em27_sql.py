from pathlib import Path
import sqlite3 as db

from netCDF4 import Dataset
import pytest

from enw.custom.em27 import (
    configure_db,
    create_tables,
    insert_device,
    insert_heights,
    insert_height_vars,
    insert_site,
    insert_surface_vars,
    insert_meta_files,
    select_all_meta_processed_files
)

pytestmark = [
    pytest.mark.custom,
    pytest.mark.custom_em27,
    pytest.mark.custom_em27_sql
]

@pytest.fixture(scope="session")
def db_path(tmp_path_factory: pytest.TempdirFactory) -> Path:
    """Path for the DuckDB databases."""
    pth = tmp_path_factory.mktemp("em27_db")
    return Path(pth)

@pytest.fixture(scope="session")
def example_netcdf(tmp_path_factory: pytest.TempdirFactory) -> Path:
    """Path for the DuckDB databases."""
    pth = tmp_path_factory.mktemp("netcdf") / "example.nc"
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


def test_configure_db_good(db_path: Path):
    """Test the configure_db function."""
    db_file = db_path / "test_configure_db_good.db"
    tests = {}
    pragmas = {}
    pragmas["initial"] = {}
    pragmas["updated"] = {}
    conn = db.connect(db_file)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys;")
    pragmas["initial"]["foreign_keys"] = cur.fetchone()[0]
    cur.execute("PRAGMA journal_mode;")
    pragmas["initial"]["journal_mode"] = cur.fetchone()[0]
    configure_db(conn)
    cur.execute("PRAGMA foreign_keys;")
    pragmas["updated"]["foreign_keys"] = cur.fetchone()[0]
    cur.execute("PRAGMA journal_mode;")
    pragmas["updated"]["journal_mode"] = cur.fetchone()[0]
    cur.close()
    conn.close()
    for pragma in ["foreign_keys", "journal_mode"]:
        tests[f"{pragma} updated"] = (
            pragmas["initial"][pragma] != pragmas["updated"][pragma]
        )
    tests["foreign_keys correct"] = (
        pragmas["updated"]["foreign_keys"] == 1
    )
    tests["journal_mode correct"] = pragmas["updated"]["journal_mode"] == "wal"

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_create_tables_good(db_path: Path):
    """Test the create_tables function."""
    db_file = db_path / "test_create_tables_good.db"

    expected_tables = {
        "dim_site",
        "dim_device",
        "dim_height",
        "fact_height_vars",
        "fact_surface_vars",
        "meta_processed_files"
    }

    tests = {}
    conn = db.connect(db_file)
    cur = conn.cursor()
    configure_db(conn)
    create_tables(conn)
    cur.execute("""
        SELECT * FROM sqlite_master where type='table';
    """)
    tables = {t[1] for t in cur.fetchall()}
    tests["Expected tables"] = tables == expected_tables
    conn.close()

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_insert_device_single_good(db_path: Path):
    """Test the insert_device function with one row."""
    db_file = db_path / "test_insert_device_single_good.db"

    tests = {}
    conn = db.connect(db_file)
    cur = conn.cursor()
    configure_db(conn)
    create_tables(conn)
    rowid = insert_device("TEST A", conn)

    cur.execute("""SELECT COUNT(*) FROM dim_device;""")
    counts = cur.fetchone()[0]
    cur.close()
    conn.close()

    tests["Rowid == 1"] = rowid == 1
    tests["One row"] = counts == 1

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

def test_insert_device_duplicate_good(db_path: Path):
    """Test the insert_device function with one row."""
    db_file = db_path / "test_insert_device_duplicate_good.db"

    tests = {}
    conn = db.connect(db_file)
    cur = conn.cursor()
    configure_db(conn)
    create_tables(conn)
    _ = insert_device("TEST A", conn)
    rowid = insert_device("TEST A", conn)

    cur.execute("""SELECT COUNT(*) FROM dim_device;""")
    counts = cur.fetchone()[0]
    cur.close()
    conn.close()

    tests["Rowid == 1"] = rowid == 1
    tests["One row"] = counts == 1

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_insert_device_multiple_good(db_path: Path):
    """Test the insert_device function with multiple rows."""
    db_file = db_path / "test_insert_device_multiple_good.db"

    tests = {}
    conn = db.connect(db_file)
    cur = conn.cursor()
    configure_db(conn)
    create_tables(conn)
    _ = insert_device("TEST A", conn)
    _ = insert_device("TEST B", conn)
    rowid = insert_device("TEST C", conn)

    cur.execute("""SELECT COUNT(*) FROM dim_device;""")
    counts = cur.fetchone()[0]
    cur.close()
    conn.close()

    tests["Rowid == 3"] = rowid == 3
    tests["Three rows"] = counts == 3

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_insert_site_single_good(db_path: Path):
    """Test the insert_site function with one row."""
    db_file = db_path / "test_insert_site_single_good.db"

    tests = {}
    conn = db.connect(db_file)
    cur = conn.cursor()
    configure_db(conn)
    create_tables(conn)
    rowid = insert_site("TEST A", conn)

    cur.execute("""SELECT COUNT(*) FROM dim_site;""")
    counts = cur.fetchone()[0]
    cur.close()
    conn.close()

    tests["Rowid == 1"] = rowid == 1
    tests["One row"] = counts == 1

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_insert_site_duplicate_good(db_path: Path):
    """Test the insert_site function with one row."""
    db_file = db_path / "test_insert_site_duplicate_good.db"

    tests = {}
    conn = db.connect(db_file)
    cur = conn.cursor()
    configure_db(conn)
    create_tables(conn)
    _ = insert_site("TEST A", conn)
    rowid = insert_site("TEST A", conn)

    cur.execute("""SELECT COUNT(*) FROM dim_site;""")
    counts = cur.fetchone()[0]
    cur.close()
    conn.close()

    tests["Rowid == 1"] = rowid == 1
    tests["One row"] = counts == 1

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_insert_site_multiple_good(db_path: Path):
    """Test the insert_site function with multiple rows."""
    db_file = db_path / "test_insert_site_multiple_good.db"

    tests = {}
    conn = db.connect(db_file)
    cur = conn.cursor()
    configure_db(conn)
    create_tables(conn)
    _ = insert_site("TEST A", conn)
    _ = insert_site("TEST B", conn)
    rowid = insert_site("TEST C", conn)

    cur.execute("""SELECT COUNT(*) FROM dim_site;""")
    counts = cur.fetchone()[0]
    cur.close()
    conn.close()

    tests["Rowid == 3"] = rowid == 3
    tests["Three rows"] = counts == 3

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_insert_heights_good(db_path: Path, example_netcdf: Path):
    """"""
    db_file = db_path / "test_insert_heights_good.db"

    tests = {}
    conn = db.connect(db_file)
    cur = conn.cursor()
    configure_db(conn)
    create_tables(conn)
    _ = insert_site("TEST A", conn)
    _ = insert_device("TEST A", conn)
    with Dataset(example_netcdf, "r") as _nc:
        _ = insert_heights(
            nc=_nc,
            site="TEST A",
            device="TEST A",
            conn=conn
        )

    cur.execute("""SELECT COUNT(*) FROM dim_height;""")
    counts = cur.fetchone()[0]
    cur.close()
    conn.close()
    tests["Three rows"] = counts == 3

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_insert_heights_duplicate_good(db_path: Path, example_netcdf: Path):
    """"""
    db_file = db_path / "test_insert_heights_duplicate_good.db"

    tests = {}
    conn = db.connect(db_file)
    cur = conn.cursor()
    configure_db(conn)
    create_tables(conn)
    _ = insert_site("TEST A", conn)
    _ = insert_device("TEST A", conn)
    with Dataset(example_netcdf, "r") as _nc:
        _ = insert_heights(
            nc=_nc,
            site="TEST A",
            device="TEST A",
            conn=conn
        )
        _ = insert_heights(
            nc=_nc,
            site="TEST A",
            device="TEST A",
            conn=conn
        )

    cur.execute("""SELECT COUNT(*) FROM dim_height;""")
    counts = cur.fetchone()[0]
    cur.close()
    conn.close()
    tests["Three rows"] = counts == 3

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_insert_heights_two_sites_good(db_path: Path, example_netcdf: Path):
    """"""
    db_file = db_path / "test_insert_heights_two_sites_good.db"

    tests = {}
    conn = db.connect(db_file)
    cur = conn.cursor()
    configure_db(conn)
    create_tables(conn)
    _ = insert_site("TEST A", conn)
    _ = insert_site("TEST B", conn)
    _ = insert_device("TEST A", conn)
    with Dataset(example_netcdf, "r") as _nc:
        _ = insert_heights(
            nc=_nc,
            site="TEST A",
            device="TEST A",
            conn=conn
        )
        _ = insert_heights(
            nc=_nc,
            site="TEST B",
            device="TEST A",
            conn=conn
        )

    cur.execute("""SELECT COUNT(*) FROM dim_height;""")
    counts = cur.fetchone()[0]
    cur.close()
    conn.close()
    tests["Six rows"] = counts == 6

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_insert_heights_two_devices_good(db_path: Path, example_netcdf: Path):
    """"""
    db_file = db_path / "test_insert_heights_two_devices_good.db"

    tests = {}
    conn = db.connect(db_file)
    cur = conn.cursor()
    configure_db(conn)
    create_tables(conn)
    _ = insert_site("TEST A", conn)
    _ = insert_device("TEST A", conn)
    _ = insert_device("TEST B", conn)
    with Dataset(example_netcdf, "r") as _nc:
        _ = insert_heights(
            nc=_nc,
            site="TEST A",
            device="TEST A",
            conn=conn
        )
        _ = insert_heights(
            nc=_nc,
            site="TEST A",
            device="TEST B",
            conn=conn
        )

    cur.execute("""SELECT COUNT(*) FROM dim_height;""")
    counts = cur.fetchone()[0]
    cur.close()
    conn.close()
    tests["Six rows"] = counts == 6
    print(counts)

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@pytest.mark.parametrize("species", ["CH4", "CO2", "CO"])
def test_insert_height_vars_good(
    db_path: Path,
    example_netcdf: Path,
    species: str
):
    """"""
    db_file = db_path / f"test_insert_height_vars_good_{species}.db"

    tests = {}
    conn = db.connect(db_file)
    cur = conn.cursor()
    configure_db(conn)
    create_tables(conn)
    _ = insert_site("TEST A", conn)
    _ = insert_device("TEST A", conn)
    with Dataset(example_netcdf, "r") as _nc:
        _ = insert_heights(
            nc=_nc,
            site="TEST A",
            device="TEST A",
            conn=conn
        )
        _ = insert_height_vars(
            nc=_nc,
            site="TEST A",
            device="TEST A",
            species=species,
            conn=conn
        )

    cur.execute("""SELECT COUNT(*) FROM fact_height_vars;""")
    counts = cur.fetchone()[0]
    cur.close()
    conn.close()
    print(counts)
    tests["Fifteen rows"] = counts == 15

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@pytest.mark.parametrize("species", ["CH4", "CO2", "CO"])
def test_insert_height_vars_duplicate_good(
    db_path: Path,
    example_netcdf: Path,
    species: str
):
    """"""
    db_file = db_path / f"test_insert_height_vars_duplicate_good_{species}.db"

    tests = {}
    conn = db.connect(db_file)
    cur = conn.cursor()
    configure_db(conn)
    create_tables(conn)
    _ = insert_site("TEST A", conn)
    _ = insert_device("TEST A", conn)
    with Dataset(example_netcdf, "r") as _nc:
        _ = insert_heights(
            nc=_nc,
            site="TEST A",
            device="TEST A",
            conn=conn
        )
        _ = insert_height_vars(
            nc=_nc,
            site="TEST A",
            device="TEST A",
            species=species,
            conn=conn
        )
        _ = insert_height_vars(
            nc=_nc,
            site="TEST A",
            device="TEST A",
            species=species,
            conn=conn
        )

    cur.execute("""SELECT COUNT(*) FROM fact_height_vars;""")
    counts = cur.fetchone()[0]
    cur.close()
    conn.close()
    print(counts)
    tests["Fifteen rows"] = counts == 15

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_insert_height_vars_all_species_good(
    db_path: Path,
    example_netcdf: Path,
):
    """"""
    db_file = db_path / "test_insert_height_vars_all_species_good.db"

    tests = {}
    conn = db.connect(db_file)
    cur = conn.cursor()
    configure_db(conn)
    create_tables(conn)
    _ = insert_site("TEST A", conn)
    _ = insert_device("TEST A", conn)
    with Dataset(example_netcdf, "r") as _nc:
        _ = insert_heights(
            nc=_nc,
            site="TEST A",
            device="TEST A",
            conn=conn
        )
        for s in ["CH4", "CO2", "CO"]:
            _ = insert_height_vars(
                nc=_nc,
                site="TEST A",
                device="TEST A",
                species=s,
                conn=conn
            )

    cur.execute("""SELECT COUNT(*) FROM fact_height_vars;""")
    counts = cur.fetchone()[0]
    cur.close()
    conn.close()
    tests["Fourtyfive rows"] = counts == 45

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("species", ["CH4", "CO2", "CO"])
def test_insert_height_vars_two_sites_good(
    db_path: Path,
    example_netcdf: Path,
    species: str
):
    """"""
    db_file = db_path / f"test_insert_height_vars_two_sites_good_{species}.db"

    tests = {}
    conn = db.connect(db_file)
    cur = conn.cursor()
    configure_db(conn)
    create_tables(conn)
    _ = insert_site("TEST A", conn)
    _ = insert_site("TEST B", conn)
    _ = insert_device("TEST A", conn)
    with Dataset(example_netcdf, "r") as _nc:
        _ = insert_heights(
            nc=_nc,
            site="TEST A",
            device="TEST A",
            conn=conn
        )
        _ = insert_heights(
            nc=_nc,
            site="TEST B",
            device="TEST A",
            conn=conn
        )
        _ = insert_height_vars(
            nc=_nc,
            site="TEST A",
            device="TEST A",
            species=species,
            conn=conn
        )
        _ = insert_height_vars(
            nc=_nc,
            site="TEST B",
            device="TEST A",
            species=species,
            conn=conn
        )

    cur.execute("""SELECT COUNT(*) FROM fact_height_vars;""")
    counts = cur.fetchone()[0]
    cur.close()
    conn.close()
    print(counts)
    tests["Thirty rows"] = counts == 30

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("species", ["CH4", "CO2", "CO"])
def test_insert_height_vars_two_devices_good(
    db_path: Path,
    example_netcdf: Path,
    species: str
):
    """"""
    db_file = db_path / f"test_insert_height_vars_two_devices_good_{species}.db"

    tests = {}
    conn = db.connect(db_file)
    cur = conn.cursor()
    configure_db(conn)
    create_tables(conn)
    _ = insert_site("TEST A", conn)
    _ = insert_device("TEST A", conn)
    _ = insert_device("TEST B", conn)
    with Dataset(example_netcdf, "r") as _nc:
        _ = insert_heights(
            nc=_nc,
            site="TEST A",
            device="TEST A",
            conn=conn
        )
        _ = insert_heights(
            nc=_nc,
            site="TEST A",
            device="TEST B",
            conn=conn
        )
        _ = insert_height_vars(
            nc=_nc,
            site="TEST A",
            device="TEST A",
            species=species,
            conn=conn
        )
        _ = insert_height_vars(
            nc=_nc,
            site="TEST A",
            device="TEST B",
            species=species,
            conn=conn
        )

    cur.execute("""SELECT COUNT(*) FROM fact_height_vars;""")
    counts = cur.fetchone()[0]
    cur.close()
    conn.close()
    print(counts)
    tests["Thirty rows"] = counts == 30

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_insert_surface_vars_good(
    db_path: Path,
    example_netcdf: Path,
):
    """"""
    db_file = db_path / "test_insert_surface_vars_good.db"

    tests = {}
    conn = db.connect(db_file)
    cur = conn.cursor()
    configure_db(conn)
    create_tables(conn)
    _ = insert_site("TEST A", conn)
    _ = insert_device("TEST A", conn)
    with Dataset(example_netcdf, "r") as _nc:
        _ = insert_heights(
            nc=_nc,
            site="TEST A",
            device="TEST A",
            conn=conn
        )
        _ = insert_surface_vars(
            nc=_nc,
            site="TEST A",
            device="TEST A",
            conn=conn
        )

    cur.execute("""SELECT COUNT(*) FROM fact_surface_vars;""")
    counts = cur.fetchone()[0]
    cur.close()
    conn.close()
    print(counts)
    tests["Five rows"] = counts == 5

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_insert_surface_vars_duplicate_good(
    db_path: Path,
    example_netcdf: Path,
):
    """"""
    db_file = db_path / "test_insert_surface_vars_duplicate_good.db"

    tests = {}
    conn = db.connect(db_file)
    cur = conn.cursor()
    configure_db(conn)
    create_tables(conn)
    _ = insert_site("TEST A", conn)
    _ = insert_device("TEST A", conn)
    with Dataset(example_netcdf, "r") as _nc:
        _ = insert_heights(
            nc=_nc,
            site="TEST A",
            device="TEST A",
            conn=conn
        )
        _ = insert_surface_vars(
            nc=_nc,
            site="TEST A",
            device="TEST A",
            conn=conn
        )
        _ = insert_surface_vars(
            nc=_nc,
            site="TEST A",
            device="TEST A",
            conn=conn
        )

    cur.execute("""SELECT COUNT(*) FROM fact_surface_vars;""")
    counts = cur.fetchone()[0]
    cur.close()
    conn.close()
    print(counts)
    tests["Five rows"] = counts == 5

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())



def test_insert_surface_vars_two_sites_good(
    db_path: Path,
    example_netcdf: Path,
):
    """"""
    db_file = db_path / "test_insert_surface_vars_two_sites_good.db"

    tests = {}
    conn = db.connect(db_file)
    cur = conn.cursor()
    configure_db(conn)
    create_tables(conn)
    _ = insert_site("TEST A", conn)
    _ = insert_site("TEST B", conn)
    _ = insert_device("TEST A", conn)
    with Dataset(example_netcdf, "r") as _nc:
        _ = insert_heights(
            nc=_nc,
            site="TEST A",
            device="TEST A",
            conn=conn
        )
        _ = insert_heights(
            nc=_nc,
            site="TEST B",
            device="TEST A",
            conn=conn
        )
        _ = insert_surface_vars(
            nc=_nc,
            site="TEST A",
            device="TEST A",
            conn=conn
        )
        _ = insert_surface_vars(
            nc=_nc,
            site="TEST B",
            device="TEST A",
            conn=conn
        )

    cur.execute("""SELECT COUNT(*) FROM fact_surface_vars;""")
    counts = cur.fetchone()[0]
    cur.close()
    conn.close()
    print(counts)
    tests["Ten rows"] = counts == 10

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_insert_surface_vars_two_devices_good(
    db_path: Path,
    example_netcdf: Path,
):
    """"""
    db_file = db_path / "test_insert_surface_vars_two_devices_good.db"

    tests = {}
    conn = db.connect(db_file)
    cur = conn.cursor()
    configure_db(conn)
    create_tables(conn)
    _ = insert_site("TEST A", conn)
    _ = insert_device("TEST A", conn)
    _ = insert_device("TEST B", conn)
    with Dataset(example_netcdf, "r") as _nc:
        _ = insert_heights(
            nc=_nc,
            site="TEST A",
            device="TEST A",
            conn=conn
        )
        _ = insert_heights(
            nc=_nc,
            site="TEST A",
            device="TEST B",
            conn=conn
        )
        _ = insert_surface_vars(
            nc=_nc,
            site="TEST A",
            device="TEST A",
            conn=conn
        )
        _ = insert_surface_vars(
            nc=_nc,
            site="TEST A",
            device="TEST B",
            conn=conn
        )

    cur.execute("""SELECT COUNT(*) FROM fact_surface_vars;""")
    counts = cur.fetchone()[0]
    cur.close()
    conn.close()
    print(counts)
    tests["Ten rows"] = counts == 10

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_insert_meta_files_good(db_path: Path):
    """"""
    db_file = db_path / "test_insert_meta_files.db"

    expected_files = {
        "1.file",
        "2.file",
        "3.file",
        "4.file",
        "5.file"
    }
    tests = {}
    conn = db.connect(db_file)
    cur = conn.cursor()
    configure_db(conn)
    create_tables(conn)
    _ = insert_meta_files(Path("1.file"), conn=conn)
    _ = insert_meta_files(Path("/2.file"), conn=conn)
    _ = insert_meta_files(Path("./3.file"), conn=conn)
    _ = insert_meta_files(Path("/path/to/4.file"), conn=conn)
    rowid = insert_meta_files(Path("path/to/5.file"), conn=conn)

    cur.execute("""SELECT COUNT(*) FROM meta_processed_files;""")
    counts = cur.fetchone()[0]

    cur.execute("SELECT file from meta_processed_files;")
    files = {f[0] for f in cur.fetchall()}

    cur.close()
    conn.close()

    tests["Correct files"] = files == expected_files
    tests["Correct count"] = counts == 5
    tests["Correct rowid"] = rowid == 5

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_select_all_meta_files_good(db_path: Path):
    """"""
    db_file = db_path / "test_select_all_meta_files.db"

    expected_files = {
        "1.file",
        "2.file",
        "3.file",
        "4.file",
        "5.file"
    }
    tests = {}
    conn = db.connect(db_file)
    configure_db(conn)
    create_tables(conn)
    for f in [
        Path("1.file"),
        Path("/2.file"),
        Path("./3.file"),
        Path("/path/to/4.file"),
        Path("path/to/5.file"),
    ]:
        insert_meta_files(f, conn)
    p_files = select_all_meta_processed_files(conn)
    conn.close()


    tests["Correct files"] = p_files == expected_files
    tests["Correct count"] = len(p_files) == 5

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())
