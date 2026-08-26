from importlib.resources import as_file, files
import logging
import tomllib
from typing import Any, cast, TYPE_CHECKING

from enw.utils.openghg import (
    get_location_info,
    get_domain_info,
    get_species_info,
)

from ._check import (
    check_coord_options,
    check_domain_options,
    check_location_options,
    check_main_options,
    check_openmp_options,
    check_output_options,
    check_restart_options,
    check_species_options,
)

if TYPE_CHECKING:
    from enw.types import (
        EnwConfig,
        OpenGHGPresets,
        OptionBlock,
    )
    from pathlib import Path


_logger = logging.getLogger("_enw")

#TODO: Need to separate this into individual blocks.
def load_config(path: Path) -> EnwConfig:
    """Load the config file, with error checking.

    Parameters
    ----------
    path : Path
        Path to the toml file.

    Returns
    -------
    EnwConfig
        Properly formatted config file.

    """
    raw_config = load_toml(path)
    config = {}

    #INFO: Check Main
    #TODO: Sort out whether main should be mandatory or not
    #BUG: Some of the main arguments aren't default now. Raise an error.
    if "Main" not in raw_config:
        _logger.warning("Main config not present, using defaults.")
    config_main = load_defaults(raw_config.get("Main", {}), "main")
    config["Main"] = check_main_options(config_main)
    #INFO: Check Output
    if "Output" not in raw_config:
        msg = "Mandatory section 'Output' not found in config."
        raise ValueError(msg)
    config_output = load_defaults(raw_config["Output"], "output")
    config["Output"] = check_output_options(config_output)
    #INFO: Check Restart
    if "Restart" in raw_config:
        config["Restart"] = check_restart_options(raw_config["Restart"])
    #INFO: Check Multiple Case NOT SET and then set default
    if "Multiple Case" in raw_config:
        msg = "Configuration for Multiple Case not enabled!"
        raise NotImplementedError(msg)
    config["Multiple Case"] = {
        "dispersion_options_ensemble_size": 1,
        "met_ensemble_size": 1
    }
    #INFO: Check OpenMP and set default
    if "OpenMP" not in raw_config:
        _logger.warning("OpenMP config not present, using defaults.")
    config_openmp = load_defaults(raw_config.get("OpenMP", {}), "openmp")
    config["OpenMP"] = check_openmp_options(config_openmp)
    #INFO: Check Coordinate Systems and set default
    if "Coordinate Systems" not in raw_config:
        _logger.warning(
            "Coordinate Systems config not present, using defaults."
        )
    config_coords = load_defaults(
        raw_config.get("Coordinate Systems", {}),
        "coords"
    )
    config["CoordinateSystems"] = check_coord_options(config_coords)
    #INFO: Import OpenGHG presets and test, along with any custom values
    openghg_presets = load_openghg(raw_config.get("OpenGHG Presets", {}))
    config["Locations"] = (
        check_location_options(openghg_presets["Locations"])
        if "Locations" in openghg_presets else {}
    )
    config["Locations"] = config["Locations"] | (
        check_location_options(raw_config.get("Locations", {}))
    )

    config["Domains"] = (
        check_domain_options(openghg_presets["Domains"])
        if "Domains" in openghg_presets else {}
    )
    config["Domains"] = config["Domains"] | (
        check_domain_options(raw_config.get("Domains", {}))
    )

    config["Species"] = (
        check_species_options(openghg_presets["Species"])
        if "Species" in openghg_presets else {}
    )
    config["Species"] = config["Species"] | (
        check_species_options(raw_config.get("Species", {}))
    )

    return cast("EnwConfig", config)


def load_toml(path: Path) -> dict[str, Any]:
    """Load in the toml file used to configure the NAME run.

    If the TOML file is misconfigured, the standard `TOMLDecodeError` will
    be raised as that should contain all necessary information about what
    has gone wrong.

    Parameters
    ----------
    path : Path
        Path to the toml file.

    Returns
    -------
    dict[str, Any]
        The contents of the config file. Note that normally an Any type would
        be bad practise but as the user could enter any toml file, it's valid
        here. Proper type checking will be done later.

    Raises
    ------
    FileNotFoundError
        If the toml file doesn't exist.

    """
    if not path.exists():
        msg = f"Could not find config file at {path.resolve()}"
        raise FileNotFoundError(msg)
    with path.open("rb") as toml:
        return tomllib.load(toml)


def load_defaults(
    configured_vals: dict[str, Any],
    block: OptionBlock,
) -> dict[str, Any]:
    """Set the expected defaults for a block, if a value isn't given.

    Parameters
    ----------
    configured_vals : dict[str, Any]
        User configured values.
    block : OptionBlock
        Name of block

    Returns
    -------
    dict[str, Any]
        User configured values with any defaults added.

    """
    default_path = files("enw.files.config.defaults").joinpath(f"{block}.toml")
    with as_file(default_path) as default_toml:
        defaults = load_toml(default_toml)
    return defaults | configured_vals


def load_openghg(
    config: dict[str, Any]
) -> OpenGHGPresets:
    """Load OpenGHG preset locations, species and domains.

    Parameters
    ----------
    config : dict[str, Any]
        OpenGHG presets within the config.

    Returns
    -------
    OpenGHGPresets
        Preset OpenGHG values

    """
    presets = {}

    if "Locations" in config:
        presets["Locations"] = {}
        for loc, overrides in config["Locations"].items():
            presets["Locations"][loc] = (
                get_location_info(loc, overrides.get("subset")) | overrides
            )
            if "subset" in presets["Locations"][loc]:
                presets["Locations"][loc].pop("subset")

    if "Species" in config:
        presets["Species"] = {}
        for loc, overrides in config["Species"].items():
            presets["Species"][loc] = (
                get_species_info(loc) | overrides
            )

    if "Domains" in config:
        presets["Domains"] = {}
        for loc, overrides in config["Domains"].items():
            presets["Domains"][loc] = (
                get_domain_info(loc) | overrides
            )

    return cast("OpenGHGPresets", presets)

