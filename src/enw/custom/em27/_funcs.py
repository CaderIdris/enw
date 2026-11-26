import datetime as dt
from typing import Literal, TYPE_CHECKING

from netCDF4 import Dataset

from enw.utils import check_literal, logger
from ._sql import (
    insert_device,
    insert_heights,
    insert_height_vars,
    insert_meta_files,
    insert_surface_vars,
    insert_site,
    configure_db,
    create_tables,
    select_all_meta_processed_files
)

if TYPE_CHECKING:
    from pathlib import Path
    from sqlite3 import Connection

ValidSpecies = Literal["CH4", "CO2", "CO"]
"""Species measured by EM27."""

def from_fs(
    path: Path,
    conn: Connection,
    species: ValidSpecies | list[ValidSpecies],
    locations: list[str] | None = None,
    start_date: dt.datetime = dt.datetime.min,
    end_date: dt.datetime = dt.datetime.max
) -> None:
    r"""Build the database from a filesystem.

    The filesystem should be structured as follows:

    - 📁 `path` - provided as a function argument
        - 📁 ==site names==
            - 🗒️ ==project name==\_==country==\_==device\_name==\_==site_name==
            \_==date==.nc

    Parameters
    ----------
    path : Path
        Path to the folder containing all the measurements.
    conn : Connection
        Connection to the sqlite3 database.
    species : ValidSpecies | list[ValidSpecies]
        Species(') to get averaging kernels for.
    locations : list[str] | None, default=None
        The locations to process.
    start_date : dt.datetime, default=dt.datetime.min
        Earliest date to search files from.
    end_date : dt.datetime, default=dt.datetime.max
        Latest date to search files until.

    """
    _globbed =  path.glob("**/*.nc")

    if isinstance(species, str):
        species = [species]

    if len(species) < 1:
        msg = "Expected at least one species."
        raise ValueError(msg)

    for s in species:
        check_literal(
            f"species.{s}",
            s,
            "ValidSpecies",
            ValidSpecies
        )

    configure_db(conn)
    create_tables(conn)

    p_files = select_all_meta_processed_files(conn)
    files = []
    for f in _globbed:
        if f.name in p_files:
            logger.debug("Skipping %s. Reason: Already processed", f.name)
            continue
        if locations is not None and f.parts[-2] not in locations:
            logger.debug(
                "Skipping %s. Reason: Not processing files from %s",
                f.name,
                f.parts[-2]
            )
            continue
        date_str = f.name[-9:-3]
        file_date = dt.datetime.strptime(date_str, "%y%m%d")
        if not end_date > file_date > start_date:
            logger.debug(
                "Skipping %s. Reason: Outside date range %s - %s",
                f.name,
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )
            continue
        files.append(f)

    for file_num, file in enumerate(files, start=1):
        site_name = file.parts[-2]
        device_name = file.parts[-1].split("_")[2]
        logger.info(
            "Processing EM27 file: %s (%s/%s) [%s, %s]",
            file.name,
            file_num,
            len(files),
            site_name,
            device_name
        )
        insert_site(site_name, conn)
        insert_device(device_name, conn)
        with Dataset(file, "r") as _nc:
            insert_heights(
                nc=_nc,
                site=site_name,
                device=device_name,
                conn=conn
            )
            insert_surface_vars(
                nc=_nc,
                site=site_name,
                device=device_name,
                conn=conn
            )
            for s in species:
                insert_height_vars(
                    nc=_nc,
                    site=site_name,
                    device=device_name,
                    species=s,
                    conn=conn
                )
        insert_meta_files(file, conn)


