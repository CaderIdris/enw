import datetime as dt
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
        RunConfig,
        SpatialConfig
    )
    from pathlib import Path


_logger = logging.getLogger("_enw")

def load_config_run(raw_config: dict[str, dict[str, object]]) -> RunConfig:
    """Load the run relevant items from the config file, with error checking.

    Parameters
    ----------
    raw_config : dict[str, object | dict[str, object]]
        The raw config.

    Returns
    -------
    RunConfig
        The run elements of the config file

    """
    config = {}

    #INFO: Check Main
    #TODO: Sort out whether main should be mandatory or not
    #BUG: Some of the main arguments aren't default now. Raise an error.
    if "Main" not in raw_config:
        msg = "Mandatory section 'Main' not found in config."
        raise ValueError(msg)
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

    return cast("RunConfig", config)


def load_config_spatial(
    raw_config: dict[str, dict[str, object]],
) -> SpatialConfig:
    """Load the run relevant items from the config file, with error checking.

    Parameters
    ----------
    raw_config : dict[str, object | dict[str, object]]
        The raw config.

    Returns
    -------
    RunConfig
        The run elements of the config file

    """
    #BUG: No HGRID OR VGRID 😢
    config = {}
    #INFO: Check Coordinate Systems and set default
    if "Coordinate Systems" not in raw_config:
        _logger.warning(
            "Coordinate Systems config not present, using defaults."
        )
    config_coords = load_defaults(
        raw_config.get("Coordinate Systems", {}),
        "coords"
    )
    config["Coordinate Systems"] = check_coord_options(config_coords)
    #INFO: Import OpenGHG presets and test, along with any custom values
    openghg_presets = load_openghg(raw_config.get("OpenGHG Presets", {}))
    config["Locations"] = (
        check_location_options(openghg_presets["Locations"])
        if "Locations" in openghg_presets else {}
    )
    config["Locations"] = config["Locations"] | (
        check_location_options(
            cast(
                "dict[str, dict[str, object]]",
                raw_config.get("Locations", {})
            )
        )
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
        check_species_options(
            cast(
                "dict[str, dict[str, object]]",
                raw_config.get("Species", {})
            )
        )
    )
    return cast("SpatialConfig", config)


def load_config_temp(
    raw_config: dict[str, dict[str, object]],
) -> dict[str, object]:
    """Check the temporary limits on the options.

    Parameters
    ----------
    raw_config : dict[str, dict[str, object]]
        The raw config.

    Raises
    ------
    ValueError
        - If ukv is not selected
        - If domain is not Europe
        - Error if date is outside if 04/05/2022 - 20/01/2026

    """
    config = {}
    main = raw_config["Main"]
    start_time: dt.datetime = cast("dt.datetime", main["start_time"])
    end_time: dt.datetime = cast("dt.datetime", main["end_time"])
    if any(
        (
            start_time > dt.datetime(2026, 1, 20),
            end_time > dt.datetime(2026, 1, 20),
            start_time < dt.datetime(2022, 5, 4),
            end_time < dt.datetime(2022, 5, 4)
        )
    ):
        msg = "Message lying outside of MK11 range."
        raise ValueError(msg)
    if not main["use_ukv"]:
        msg = "UKV should be selected, for now."
        raise ValueError(msg)
    if all((
        "OpenGHG" in raw_config,
        "Lat-Long" not in cast(
            "list[str]",
            raw_config["Coordinate Systems"]["horizontal"]
        )
    )):
        msg = (
            "Lat-Long must be a selected coordinate system if OpenGHG presets "
            "are used."
        )
        raise ValueError(msg)

    mk4_path = files("enw.files.temp").joinpath("Mk4.txt")
    with as_file(mk4_path) as mk4, mk4.open("r") as file:
        config["MK4"] = file.read()
    mk11_path = files("enw.files.temp").joinpath("Mk11.txt")
    with as_file(mk11_path) as mk11, mk11.open("r") as file:
        config["MK11"] = file.read()

    return config


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

    config = (
        config |
        load_config_run(raw_config) |
        load_config_spatial(raw_config)
    )

    config = (
        config |
        load_config_temp(
            cast("dict[str, dict[str, object]]", config)
        )
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

