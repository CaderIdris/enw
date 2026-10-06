from pathlib import Path

import openghg_defs
import pytest

import enw.utils.openghg._defs as _defs

mp = pytest.MonkeyPatch()
mp.setattr(
    openghg_defs,
    "domain_info_file",
    Path("tests/test_utils/test_openghg/files/example_domains.json")
)
mp.setattr(
    openghg_defs,
    "site_info_file",
    Path("tests/test_utils/test_openghg/files/example_locations.json")
)
mp.setattr(
    openghg_defs,
    "species_info_file",
    Path("tests/test_utils/test_openghg/files/example_species.json")
)
mp.setattr(
    _defs,
    "openghg_defs_data",
    Path("tests/test_utils/test_openghg/files/")
)
