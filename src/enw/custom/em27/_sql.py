import datetime as dt
from importlib.resources import files
import json
from typing import cast, TYPE_CHECKING, Literal

from enw.utils._misc import get_hash
from enw.utils import logger

if TYPE_CHECKING:
    from pathlib import Path
    import sqlite3 as sql
    from typing import Literal

    from netCDF4 import Dataset

_av_kernels: dict[str, tuple[str, str | None]] = {
    "CO2": ("XCO2_AK", "XCO2_STR_AK"),
    "CH4": ("XCH4_AK", "XCH4_S5P_AK"),
    "CO": ("XCO_AK", None)
}
"Standard and alternative names for the averaging kernels."

def configure_db(conn: sql.Connection) -> None:
    """Configure the database.

    Runs the `configure_db.sql` script.
    ``` sql title="configure_db.sql"
    --8<-- "./src/enw/files/sql/em27/configure_db.sql"
    ```

    Parameters
    ----------
    conn : sql.Connection
        Connection to the sqlite db.

    Returns
    -------
        None

    """
    logger.debug("Executing configure_db.sql")
    cur = conn.cursor()
    with files(
        "enw.files.sql.em27"
    ).joinpath("configure_db.sql").open("r") as sql_file:
        stmt = sql_file.read()
        cur.executescript(stmt)
    cur.close()


def create_tables(conn: sql.Connection) -> None:
    """Create all em27 tables in sqlite.

    Runs the following sql statements:
    ??? information "create_dim_site.sql"
        ``` sql title="create_dim_site.sql"
        --8<-- "./src/enw/files/sql/em27/create_dim_site.sql"
        ```
    ??? information "create_dim_device.sql"
        ``` sql title="create_dim_device.sql"
        --8<-- "./src/enw/files/sql/em27/create_dim_device.sql"
        ```
    ??? information "create_dim_height.sql"
        ``` sql title="create_dim_height.sql"
        --8<-- "./src/enw/files/sql/em27/create_dim_height.sql"
        ```
    ??? information "create_fact_height_vars.sql"
        ``` sql title="create_fact_height_vars.sql"
        --8<-- "./src/enw/files/sql/em27/create_fact_height_vars.sql"
        ```
    ??? information "create_fact_surface_vars.sql"
        ``` sql title="create_fact_surface_vars.sql"
        --8<-- "./src/enw/files/sql/em27/create_fact_surface_vars.sql"
        ```
    ??? information "create_meta_processed_files.sql"
        ``` sql title="create_meta_processed_files.sql"
        --8<-- "./src/enw/files/sql/em27/create_meta_processed_files.sql"
        ```

    Parameters
    ----------
    conn : sql.Connection
        Connection to the sqlite db.

    Returns
    -------
        None

    """
    sql_create_files = (
        "create_dim_site.sql",
        "create_dim_device.sql",
        "create_dim_height.sql",
        "create_fact_height_vars.sql",
        "create_fact_surface_vars.sql",
        "create_meta_processed_files.sql"
    )
    cur = conn.cursor()
    for file in sql_create_files:
        logger.debug("Executing %s", file)
        with (
            files("enw.files.sql.em27").joinpath(file).open("r")
        ) as sql_file:
            create_stmt = sql_file.read()
            cur.execute(create_stmt)
    cur.close()


def insert_device(device: str, conn: sql.Connection) -> int | None:
    """Insert a device into dim_device.

    Runs the `insert_dim_device.sql` script.
    ``` sql title="insert_dim_device.sql"
    --8<-- "./src/enw/files/sql/em27/insert_dim_device.sql"
    ```

    Parameters
    ----------
    device : str
        The device to add to the dim_device table.
    conn : sql.Connection
        Connection to the sqlite db.

    Returns
    -------
    int | None
        The rowid of the last inserted row.

    """
    with (
        files("enw.files.sql.em27").joinpath("insert_dim_device.sql").open("r")
    ) as sql_file:
        device_insert_stmt = sql_file.read()
    logger.debug("Inserting device: %s", device)
    device_hash = get_hash(device)
    result = conn.execute(
        device_insert_stmt,
        (device_hash, device)
    )
    conn.commit()
    return result.lastrowid


def insert_site(site: str, conn: sql.Connection) -> int | None:
    """Insert a site into dim_site.

    Runs the `insert_dim_site.sql` script.
    ``` sql title="insert_dim_site.sql"
    --8<-- "./src/enw/files/sql/em27/insert_dim_site.sql"
    ```

    Parameters
    ----------
    site : str
        The site the site is located at.
    site : str
        The site to add to the dim_site table.
    conn : sql.Connection
        Connection to the sqlite db.

    Returns
    -------
    int | None
        The rowid of the last inserted row.

    """
    with (
        files("enw.files.sql.em27").joinpath("insert_dim_site.sql").open("r")
    ) as sql_file:
        site_insert_stmt = sql_file.read()
    logger.debug("Inserting site: %s", site)
    site_hash = get_hash(site)
    result = conn.execute(
        site_insert_stmt,
        (site_hash, site)
    )
    conn.commit()
    return result.lastrowid


def insert_heights(
    nc: Dataset,
    site: str,
    device: str,
    conn: sql.Connection,
) -> int | None:
    """Insert height data into dim_height.

    Runs the `insert_dim_height.sql` script.
    ``` sql title="insert_dim_height.sql"
    --8<-- "./src/enw/files/sql/em27/insert_dim_height.sql"
    ```

    Parameters
    ----------
    nc : Dataset
        The EM27 data file.
    site : str
        The site the sensor is located at.
    device : str
        The device the EM27 data represents.
    conn : sql.Connection
        Connection to the sqlite db.

    Returns
    -------
    int | None
        The rowid of the last inserted row.

    """
    with (
        files("enw.files.sql.em27")
        .joinpath("insert_dim_height.sql")
        .open("r")
    ) as sql_file:
        height_insert_stmt = sql_file.read()
    vals = []
    site_hash = get_hash(site)
    device_hash = get_hash(device)
    for (height_b, height_t, pressure_b, pressure_t) in zip(
        nc.variables["height_grid"][:-1],
        nc.variables["height_grid"][1:],
        nc.variables["pressure_grid"][:-1],
        nc.variables["pressure_grid"][1:],
        strict=True
    ):
        height_hash = get_hash(f"{site_hash}{device_hash}{height_b}")
        vals.append((
            height_hash,
            site_hash,
            device_hash,
            height_b.ravel().data[0],
            height_t.ravel().data[0],
            pressure_b.ravel().data[0],
            pressure_t.ravel().data[0],
        ))
    logger.debug(
        "Inserting %s rows into dim_height for site %s, device %s",
        len(vals),
        site,
        device
    )
    result = conn.executemany(height_insert_stmt, vals)
    conn.commit()
    return result.lastrowid

def insert_height_vars(
    nc: Dataset,
    site: str,
    device: str,
    species: Literal["CH4", "CO2", "CO"],
    conn: sql.Connection,
) -> int | None:
    """Insert height data into fact_height_vars.

    Runs the `insert_fact_height_vars.sql` script.
    ``` sql title="insert_fact_height_vars.sql"
    --8<-- "./src/enw/files/sql/em27/insert_fact_height_vars.sql"
    ```

    Stores the following height variables:

    - Averaging kernel
        - The averaging kernel at that specific height at that specific time.
    - Alternative averaging kernel
        - An alternative averaging kernel value for CO2 or CH4 at that specific
        height at that specific time.
            - CO2: STR kernel
            - CH4: S5P kernel

    Parameters
    ----------
    nc : Dataset
        The EM27 data file.
    site : str
        The site the sensor is located at.
    device : str
        The device the EM27 data represents.
    species : Literal["CH4", "CO2", "CO"]
        The species to get the averaging kernels for.
    conn : sql.Connection
        Connection to the sqlite db.

    Returns
    -------
    int | None
        The rowid of the last inserted row.

    """
    with (
        files("enw.files.sql.em27")
        .joinpath("insert_fact_height_vars.sql")
        .open("r")
    ) as sql_file:
        pressure_insert_stmt = sql_file.read()
    vals = []
    site_hash = get_hash(site)
    device_hash = get_hash(device)
    last_rowid = None
    for i, time in enumerate(nc.variables["time"][:]):
        for j, height_b in enumerate(nc.variables["height_grid"][:-1]):
            height_hash = get_hash(f"{site_hash}{device_hash}{height_b}")
            height_var_hash = get_hash(f"{height_hash}{int(time)}{species}")
            ak = nc.variables[_av_kernels[species][0]][i,j].ravel().data[0]
            if _av_kernels[species][1] is not None:
                ak_alt = nc.variables[
                    cast("str", _av_kernels[species][1])
                ][i,j].ravel().data[0]
            else:
                ak_alt = None
            vals.append(
                (height_var_hash, height_hash, int(time), species, ak, ak_alt)
            )
    logger.debug(
        "Inserting %s rows into fact_height_vars for site %s, device %s",
        len(vals),
        site,
        device
    )
    result = conn.executemany(pressure_insert_stmt, vals)
    last_rowid = result.lastrowid
    conn.commit()
    return last_rowid


def insert_surface_vars(
    nc: Dataset,
    site: str,
    device: str,
    conn: sql.Connection,
) -> int | None:
    """Insert surface data into fact_surface_vars.

    Runs the `insert_fact_surface_vars.sql` script.
    ``` sql title="insert_fact_surface_vars.sql"
    --8<-- "./src/enw/files/sql/em27/insert_fact_surface_vars.sql"
    ```

    Stores the following surface variables:

    - Pressure (hPa)
        - The surface pressure.
    - Temperature (K)
        - The surface temperature.
    - Latitude (°N)
        - The latitude of the device
    - Longitude (°E)
        - The longitude of the device
    - Altitude (m)
        - The altitude of the device
    - Azimuth (°)
        - The angle of the sunlight relative to the surface.
    - appSZA
        - 🤷
    - qual_flag
        - The flag that determines whether a measurement is valid or not.

    Parameters
    ----------
    nc : Dataset
        The EM27 data file.
    site : str
        The site the sensor is located at.
    device : str
        The device the EM27 data represents.
    conn : sql.Connection
        Connection to the sqlite db.

    Returns
    -------
    int | None
        The rowid of the last inserted row.

    """
    with (
        files("enw.files.sql.em27")
        .joinpath("insert_fact_surface_vars.sql")
        .open("r")
    ) as sql_file:
        surface_insert_stmt = sql_file.read()
    vals = []
    site_hash = get_hash(site)
    device_hash = get_hash(device)
    latitude = float(nc.variables["latitude"][0])
    longitude = float(nc.variables["longitude"][0])
    altitude = float(nc.variables["obs_height"][0])
    for i, time in enumerate(nc.variables["time"][:]):
        surface_hash = get_hash(f"{site_hash}{device_hash}{int(time)}")
        pressure = nc.variables["gndP"][i].ravel().data[0]
        temp = nc.variables["gndT"][i].ravel().data[0]
        azimuth = nc.variables["azimuth"][i].ravel().data[0]
        app_sza = nc.variables["appSZA"][i].ravel().data[0]
        qual_flag = int(nc.variables["qual_flag"][i].ravel().data[0])
        vals.append(
            (
                surface_hash,
                site_hash,
                device_hash,
                int(time),
                pressure,
                temp,
                latitude,
                longitude,
                altitude,
                azimuth,
                app_sza,
                qual_flag,
            )
        )
    logger.debug(
        "Inserting %s rows into fact_surface_vars for site %s, device %s",
        len(vals),
        site,
        device
    )
    result = conn.executemany(surface_insert_stmt, vals)
    conn.commit()
    return result.lastrowid


def insert_meta_files(file_path: Path, conn: sql.Connection) -> int | None:
    """Insert a record of a processed file into meta_processed_files.

    Runs the `insert_meta_processed_files.sql` script.
    ``` sql title="insert_meta_processed_files.sql"
    --8<-- "./src/enw/files/sql/em27/insert_meta_processed_files.sql"
    ```

    Parameters
    ----------
    file_path : Path
        The path to the file.
    conn : sql.Connection
        Connection to the sqlite db.

    Returns
    -------
    int | None
        The rowid of the last inserted row.

    """
    with (
        files("enw.files.sql.em27")
        .joinpath("insert_meta_processed_files.sql")
        .open("r")
    ) as sql_file:
        meta_insert_stmt = sql_file.read()
    logger.debug("Inserting meta_file: %s", file_path.name)
    result = conn.execute(
        meta_insert_stmt,
        (
            str(file_path.name),
            round(dt.datetime.now().timestamp())
        )
    )
    conn.commit()
    return result.lastrowid


def select_all_meta_processed_files(conn: sql.Connection) -> set[str]:
    """Select all processed files logged in the db.

    Runs the `select_all_meta_processed_files.sql` script.
    ``` sql title="select_all_meta_processed_files.sql"
    --8<-- "./src/enw/files/sql/em27/select_all_meta_processed_files.sql"
    ```

    Parameters
    ----------
    conn : sql.Connection
        Connection to the sqlite db.

    Returns
    -------
    set[str]
        All files that have been processed.

    """
    with (
        files("enw.files.sql.em27")
        .joinpath("select_all_meta_processed_files.sql")
        .open("r")
    ) as sql_file:
        select_stmt = sql_file.read()
    cursor = conn.cursor()
    result = cursor.execute(select_stmt)
    p_files: set[str] = {f[0] for f in result.fetchall()}
    cursor.close()
    logger.debug("Returned %s processed files", len(p_files))
    return p_files


def _dict_factory(cursor: sql.Cursor, row: sql.Row) -> dict[str, object]:
    fields = [column[0] for column in cursor.description]
    return dict(zip(fields, row, strict=True))


def select_data(
    conn: sql.Connection,
    start_time: dt.datetime,
    end_time: dt.datetime,
    height_limit: int | float,
    time_agg: dt.timedelta,
    sites: list[str],
    species: Literal["CO2", "CH4", "CO"]
) -> list[dict[str, str | float | None]]:
    """"""
    num_seconds = time_agg.total_seconds()

    conn.row_factory = _dict_factory

    with (
        files("enw.files.sql.em27").joinpath("select_data.sql").open("r")
    ) as sql_file:
        select_stmt = sql_file.read()

    cursor = conn.cursor()
    result = cursor.execute(
        select_stmt,
        {
            "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "height_limit": height_limit,
            "num_seconds": num_seconds,
            "species": species,
            "sites": json.dumps(sites)
        }
    )
    return result.fetchall()
