"""Functionality specific to EM27 measurements.

Read the EM27 data and:

- Store averaging kernels, pressure and other values to use to configure NAME\
 runs.
"""
from ._sql import (
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

from ._funcs import (
    from_fs
)

__all__ = [
    "configure_db",
    "create_tables",
    "from_fs",
    "insert_device",
    "insert_height_vars",
    "insert_heights",
    "insert_meta_files",
    "insert_site",
    "insert_surface_vars",
    "select_all_meta_processed_files"
]
