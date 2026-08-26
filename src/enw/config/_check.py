from types import NoneType, UnionType
import logging
from typing import (
    _LiteralGenericAlias, #type: ignore[ty:unresolved-import]
    cast,
    TYPE_CHECKING,
)

from enw.types import (
    AbsOrRelOpts,
    RandomSeedOpts,
    HorizontalCoordSystems,
    VerticalCoordSystems, MultipleCaseConfig,
)
from enw.utils import (
    check_pos_int,
    check_literal,
    check_type,
    check_path_like,
    check_mutually_exclusive,
    check_time_interval,
)

_logger = logging.getLogger("_enw")

if TYPE_CHECKING:
    from enw.types import (
        LocationConfig,
        SpeciesConfig,
        DomainConfig,
        CoordinateSystemsConfig,
        MainConfig,
        OutputConfig,
        RestartConfig,
        OpenMPConfig,
        DispersionOptionsConfig,
        VerticalGridsConfig
    )


def check_keys(actual: set[str], expected: set[str], block: str) -> None:
    """Check if there are unexpected keys in the configuration.

    Parameters
    ----------
    actual : set[str]
        The keys present in the configuration file.
    expected : set[str]
        The keys expected to be in the configuration file.
    block : str
        The name of the configuration block.

    """
    unexpected_keys = actual - expected
    for key in unexpected_keys:
        _logger.warning(
            "%s is not a valid configuration option for %s, ignoring.",
            key,
            block
        )
    # missing_keys = expected - actual
    # if missing_keys:
    #     msg = (
    #         f"Missing the following keys for {block}: "
    #         f"{", ".join(missing_keys)}"
    #     )
    #     raise ValueError(msg)


def check_main_options(config: dict[str, object]) -> MainConfig:
    """Check the main options portion of the config file.

    Parameters
    ----------
    config : dict[str, object]
        The "Main" section of the config.

    Returns
    -------
    MainConfig
        The Main options, after setting defaults and type checking.

    """
    #INFO: Check for unexpected keys
    expected_keys = {
        "name",
        "backwards",
        "max_num_sources",
        "max_num_field_reqs",
        "max_num_field_output_groups",
        "absolute_or_relative",
        "fixed_met",
        "flat_earth",
        "random_seed",
        "run_to",
        "same_results_with_update_on_demand"
    }
    check_keys(
        set(config.keys()),
        expected_keys,
        "Main"
    )
    #INFO: Check name
    if "name" not in config:
        msg = "Need to implement auto naming"
        raise NotImplementedError(msg)
    check_type("Main.name", config["name"], str)
    #INFO: Check max_num_sources
    check_type(
        "Main.max_num_sources",
        config["max_num_sources"],
        int
    )
    check_pos_int(
        "Main.max_num_sources",
        cast("int", config["max_num_sources"])
    )
    #INFO: Check max_num_field_reqs
    check_type(
        "Main.max_num_field_reqs",
        config["max_num_field_reqs"],
        int
    )
    check_pos_int(
        "Main.max_num_field_reqs",
        cast("int", config["max_num_field_reqs"])
    )
    #INFO: Check max_num_field_output_groups
    check_type(
        "Main.max_num_field_output_groups",
        config["max_num_field_output_groups"],
        int
    )
    check_pos_int(
        "Main.max_num_field_output_groups",
        cast("int", config["max_num_field_output_groups"])
    )
    #INFO: Check backwards
    check_type("Main.backwards", config["backwards"], bool)
    #INFO: Check fixed_met
    check_type("Main.fixed_met", config["fixed_met"], bool)
    #INFO: Check flat_earth
    check_type("Main.flat_earth", config["flat_earth"], bool)
    #INFO: Check absolute_or_relative
    check_literal(
        "Main.absolute_or_relative",
        cast("str", config["absolute_or_relative"]),
        "AbsOrRelOpts",
        AbsOrRelOpts
    )
    #INFO: Check random_seed
    check_literal(
        "Main.random_seed",
        cast("str", config["random_seed"]),
        "RandomSeedOpts",
        RandomSeedOpts
    )
    #WARN: Check run_to
    if "run_to" in config:
        msg = "run_to configuration is currently not implemented."
        raise NotImplementedError(msg)
    #WARN: Check same_results_with_update_on_demand
    if "same_results_with_update_on_demand" in config:
        msg = (
            "same_results_with_update_on_demand configuration is currently "
            "not implemented."
        )
        raise NotImplementedError(msg)

    return cast("MainConfig", config)


def check_output_options(config: dict[str, object]) -> OutputConfig:
    """Check the output options portion of the config file.

    Parameters
    ----------
    config : dict[str, object]
        The "output" section of the config.

    Returns
    -------
    OutputConfig
        The output options, after setting defaults and type checking.

    """
    #INFO: Check for unexpected keys
    expected_keys = {
        "folder",
        "seconds",
        "time_decimal_places"
    }
    check_keys(
        set(config.keys()),
        expected_keys,
        "Output"
    )
    #INFO: Check folder
    if "folder" not in config:
        msg = "Missing mandatory variable 'folder' in 'Output'."
        raise ValueError(msg)
    check_type("Output.folder", config["folder"], str)
    check_path_like(
        "Output.folder",
        cast("str", config["folder"]),
    )
    #INFO: Check seconds
    check_type("Output.seconds", config["seconds"], bool)
    #WARN: Check time_decimal_places
    if "time_decimal_places" in config:
        msg = (
            "time_decimal_places configuration is currently "
            "not implemented."
        )
        raise NotImplementedError(msg)

    return cast("OutputConfig", config)


def check_restart_options(config: dict[str, object]) -> RestartConfig:
    """Check the restart options portion of the config file.

    Parameters
    ----------
    config : dict[str, object]
        The "Restart" section of the config.

    Returns
    -------
    RestartConfig
        The restart options, after setting defaults and type checking.

    """
    #INFO: Check only one of cases_between_writes or time_between_writes
    check_mutually_exclusive(
        "Restart.cases_between_writes",
        cast("str", config.get("cases_between_writes")),
        "Restart.time_between_writes",
        cast("str", config.get("time_between_writes")),
    )
    #INFO: Check cases_between_writes
    if "cases_between_writes" in config:
        check_type(
            "Restart.cases_between_writes",
            config.get("cases_between_writes"),
            int
        )
        check_pos_int(
            "Restart.cases_between_writes",
            config.get("cases_between_writes")  # type: ignore[ty:invalid-argument-type]
        )
    #INFO: Check time_between_writes
    if "time_between_writes" in config:
        check_type(
            "Restart.time_between_writes",
            config.get("time_between_writes"),
            str
        )
        check_time_interval(
            "Restart.time_between_writes",
            cast("str", config.get("time_between_writes", ""))
        )
    #INFO: Check delete_old_files
    if "delete_old_files" in config:
        check_type(
            "Restart.delete_old_files",
            config.get("delete_old_files"),
            bool
        )
    #INFO: Check write_on_suspend
    if "write_on_suspend" in config:
        check_type(
            "Restart.write_on_suspend",
            config.get("write_on_suspend"),
            bool
        )
    return cast("RestartConfig", config)


def check_openmp_options(config: dict[str, object]) -> OpenMPConfig:
    """Check the openmp options portion of the config file.

    Parameters
    ----------
    config : dict[str, object]
        The "OpenMP" section of the config.

    Returns
    -------
    OpenMPConfig
        The OpenMP options, after setting defaults and type checking.

    """
    expected_keys = {
        "use_openmp",
        "threads",
        "particle_threads",
        "particle_update_threads",
        "chemistry_threads",
        "output_group_threads",
        "output_process_threads",
        "parallel_metread",
        "parallel_metprocess"
    }
    check_keys(
        set(config.keys()),
        expected_keys,
        "OpenMP"
    )
    #INFO: Check use_openmp
    check_type("OpenMP.use_openmp", config["use_openmp"], bool)
    #INFO: Check threads in config
    check_type("OpenMP.threads", config["threads"], int)
    check_pos_int(
        "OpenMP.threads",
        cast("int", config["threads"]),
    )
    #INFO: Check particle_threads
    if "particle_threads" in config:
        check_type("OpenMP.particle_threads", config["particle_threads"], int)
        check_pos_int(
            "OpenMP.particle_threads",
            cast("int", config["particle_threads"]),
        )
    #INFO: Check particle_update_threads
    if "particle_update_threads" in config:
        check_type(
            "OpenMP.particle_update_threads",
            config["particle_update_threads"],
            int
        )
        check_pos_int(
            "OpenMP.particle_update_threads",
            cast("int", config["particle_update_threads"]),
        )
    #INFO: Check chemistry_threads
    if "chemistry_threads" in config:
        check_type(
            "OpenMP.chemistry_threads",
            config["chemistry_threads"],
            int
        )
        check_pos_int(
            "OpenMP.chemistry_threads",
            cast("int", config["chemistry_threads"]),
        )
    #INFO: Check output_group_threads
    if "output_group_threads" in config:
        check_type(
            "OpenMP.output_group_threads",
            config["output_group_threads"],
            int
        )
        check_pos_int(
            "OpenMP.output_group_threads",
            cast("int", config["output_group_threads"]),
        )
    #INFO: Check output_process_threads
    if "output_process_threads" in config:
        check_type(
            "OpenMP.output_process_threads",
            config["output_process_threads"],
            int
        )
        check_pos_int(
            "OpenMP.output_process_threads",
            cast("int", config["output_process_threads"]),
        )
    #INFO: Check parallel_metread
    if "parallel_metread" in config:
        check_type(
            "OpenMP.parallel_metread",
            config["parallel_metread"],
            bool
        )
    #INFO: Check parallel_metprocess
    if "parallel_metprocess" in config:
        check_type(
            "OpenMP.parallel_metprocess",
            config["parallel_metprocess"],
            bool
        )
    return cast("OpenMPConfig", config)


def check_coord_options(
    config: dict[str, list[str] | str],
) -> CoordinateSystemsConfig:
    """Check the openmp options portion of the config file.

    Parameters
    ----------
    config : dict[str, object]
        The "Coordinate Systems" section of the config.

    Returns
    -------
    CoordinateSystemsConfig
        The CoordinateSystems options, after setting defaults and type
        checking.

    """
    expected_keys = {
        "name"
    }
    check_keys(
        set(config.keys()),
        expected_keys,
        "Coordinate Systems"
    )
    #INFO: Check horizontal
    hcoords = config["horizontal"]
    if isinstance(hcoords, str):
        hcoords = [hcoords]
    for i, h in enumerate(hcoords):
        check_literal(
            f"horizontal {i}",
            h,
            "HorizontalCoordSystems",
            HorizontalCoordSystems
        )
    #INFO: Check vertical
    vcoords = config["vertical"]
    if isinstance(vcoords, str):
        vcoords = [vcoords]
    for i, v in enumerate(vcoords):
        check_literal(
            f"vertical {i}",
            v,
            "VerticalCoordSystems",
            VerticalCoordSystems
        )
    return {
        "horizontal": hcoords,
        "vertical": vcoords
    }

def check_multiple_case_options(
    config: dict[str, object],
) -> MultipleCaseConfig: # pragma: no cover
    """Check the multiple case options portion of the config file.

    !!! warning
        Not currently implemented!

    Parameters
    ----------
    config : dict[str, object]
        The "Coordinate Systems" section of the config.

    Returns
    -------
    MultipleCaseConfig
        The MultipleCaseConfig options, after setting defaults and type
        checking.

    """
    expected_keys = {
        "dispersion_options_ensemble_size",
        "met_ensemble_size"
    }
    check_keys(
        set(config.keys()),
        expected_keys,
        "MultipleCaseConfig"
    )
    check_type(
        "dispersion_options_ensemble_size",
        config.get("dispersion_options_ensemble_size"),
        int
    )
    check_type(
        "met_ensemble_size",
        config.get("met_ensemble_size"),
        int
    )
    check_pos_int(
        "dispersion_options_ensemble_size",
        cast("int", config.get("dispersion_options_ensemble_size")),
    )
    check_pos_int(
        "met_ensemble_size",
        cast("int", config.get("met_ensemble_size")),
    )
    checked: MultipleCaseConfig = {
        "dispersion_options_ensemble_size": cast(
            "int",
            config.get(
                "dispersion_options_ensemble_size"
            )
        ),
        "met_ensemble_size": cast(
            "int",
            config.get("met_ensemble_size")
        )
    }
    if config.get("name") is not None:
        check_type("name", config.get("name"), str)
        checked["name"] = str(config.get("name"))

    return checked

def check_location_options(
    config: dict[str, dict[str, object]] | dict[str, LocationConfig]
) -> LocationConfig:
    """"""
    expected_keys = {
        "name",
        "x",
        "y",
        "inlet_height",
        "hcoord",
        "subset"
    }
    vals = (
        ("name", str),
        ("x", float | int),
        ("y", float | int),
        ("inlet_height", float | int),
        ("subset", str),
    )
    literals: tuple[tuple[str, str, _LiteralGenericAlias], ...] = (
        ("hcoord", "HorizontalCoordSystems", HorizontalCoordSystems),
    )
    for loc, loc_config in config.items():
        check_keys(
            set(loc_config.keys()),
            expected_keys,
            f"Locations ({loc}, OpenGHG)"
        )
        for val, expected_type in vals:
            check_type(f"{loc}.{val}", loc_config.get(val), expected_type)
        for val, literal_name, literal_type in literals:
            check_literal(
                f"{loc}.{val}",
                str(loc_config.get(val, "MISSING")),
                literal_name,
                literal_type
            )

    return cast("LocationConfig", config)


def check_species_options(
    config: dict[str, dict[str, object]] | dict[str, SpeciesConfig]
) -> SpeciesConfig:
    """"""
    expected_keys = {
        "name",
        "category",
        "molecular_weight",
        "deposition_velocity",
        "material_unit",
        "uv_loss_rate",
        "half_life",
        "surface_resistance",
        "on_particles",
        "on_fields",
        "advect_fields"
    }
    vals = (
        ("name", str),
        ("category", str),
        ("molecular_weight", float | int),
        ("deposition_velocity", float | int),
        ("material_unit", str),
        ("uv_loss_rate", float | int),
        ("half_life", float | int | str),
        ("surface_resistance", int | float | NoneType),
        ("on_particles", bool),
        ("on_fields", bool),
        ("advect_fields", bool)
    )
    for spc, spc_config in config.items():
        check_keys(
            set(spc_config.keys()),
            expected_keys,
            f"Species ({spc}, OpenGHG)"
        )
        for val, expected_type in vals:
            check_type(f"{spc}.{val}", spc_config.get(val), expected_type)

    return cast("SpeciesConfig", config)


def check_domain_options(
    config: dict[str, object | dict[str, object]] | dict[str, DomainConfig]
) -> DomainConfig:
    """"""
    expected_keys: dict[str, set[str]] = {
        "root": {"name", "hcoord", "zcoord", "x", "y", "z", "t"},
        "x": {"min", "max", "num", "unbounded"},
        "y": {"min", "max", "num", "unbounded"},
        "z": {"max", "unbounded"},
        "t": {"unbounded"}
    }
    vals: dict[str, tuple[tuple[str, type | UnionType], ...]] = {
        "root": (
            ("name", str),
        ),
        "x": (
            ("min", float | int),
            ("max", float | int),
            ("num", int),
            ("unbounded", bool)
        ),
        "y": (
            ("min", float | int),
            ("max", float | int),
            ("num", int),
            ("unbounded", bool)
        ),
        "z": (
            ("max", float | int),
            ("unbounded", bool)
        ),
        "t": (
            ("unbounded", bool),
        ),
    }
    literals: tuple[tuple[str, str, _LiteralGenericAlias], ...] = (
        ("hcoord", "HorizontalCoordSystems", HorizontalCoordSystems),
        ("zcoord", "VerticalCoordSystems", VerticalCoordSystems),
    )
    for dom, dom_config in config.items():
        dom_config = cast("dict[str, object | dict[str, object]]", dom_config)
        check_keys(
            set(dom_config.keys()),
            expected_keys["root"],
            f"Domains ({dom}, OpenGHG)"
        )
        for val, expected_type in vals["root"]:
            check_type(f"{dom}.{val}", dom_config.get(val), expected_type)
        for sub in ["x", "y", "z", "t"]:
            check_keys(
                set(cast("dict[str, object]", dom_config[sub]).keys()),
                expected_keys[sub],
                f"Domains ({dom}, {sub}, OpenGHG)"
            )
            for val, expected_type in vals[sub]:
                check_type(
                    f"{dom}.{sub}.{val}",
                    cast("dict[str, object]", dom_config[sub]).get(val),
                    expected_type
                )
        for val, literal_name, literal_type in literals:
            check_literal(
                f"{dom}.{val}",
                cast("str", dom_config.get(val, "MISSING")),
                literal_name,
                literal_type
            )

    return cast("DomainConfig", config)

def check_set_of_dispersion_options(
    config: dict[str, object]
) -> DispersionOptionsConfig:
    """"""
    expected_keys = {
        "max_num_particles",
        "max_num_full_particles",
        "max_num_puffs",
        "max_num_original_puffs",
        "skew_time",
        "velocity_memory_time",
        "mesoscale_velocity_memory_time",
        "inhomogeneous_time",
        "delta_opt",
        "puff_time",
        "sync_time",
        "puff_interval",
        "deep_convection",
        "radioactive_decay",
        "agent_decay",
        "dry_deposition",
        "wet_deposition",
        "turbulence",
        "mesoscale_motions",
        "chemistry"
    }
    vals = (
        ("max_num_particles", int),
        ("max_num_full_particles", int),
        ("max_num_puffs", int),
        ("max_num_original_puffs", int),
        ("skew_time", str),
        ("velocity_memory_time", str),
        ("mesoscale_velocity_memory_time", str),
        ("inhomogeneous_time", str),
        ("delta_opt", str),
        ("puff_time", str),
        ("sync_time", str),
        ("puff_interval", str),
        ("deep_convection", bool),
        ("radioactive_decay", bool),
        ("agent_decay", bool),
        ("dry_deposition", bool),
        ("wet_deposition", bool),
        ("turbulence", bool),
        ("mesoscale_motions", bool),
        ("chemistry", bool),
    )
    pos_ints = (
        "max_num_particles",
        "max_num_full_particles",
        "max_num_puffs",
        "max_num_original_puffs",
    )
    time_intervals = (
        "skew_time",
        "velocity_memory_time",
        "mesoscale_velocity_memory_time",
        "inhomogeneous_time",
        "puff_time",
        "sync_time",
        "puff_interval",
    )
    check_keys(
        set(config.keys()),
        expected_keys,
        "Dispersion Options"
    )
    for val, expected_type in vals:
        check_type(val, config.get(val), expected_type)
    for val in pos_ints:
        check_pos_int(val, cast("int", config.get(val)))
    for interval in time_intervals:
        check_time_interval(interval, cast("str", config.get(interval)))

    return cast("DispersionOptionsConfig", config)


def check_vertical_grids_options(
    config: dict[str, object]
) -> VerticalGridsConfig:
    """"""
    expected_keys: set[str] = {
        "zcoord",
        "num",
        "min",
        "spacing",
    }
    vals: tuple[tuple[str, type | UnionType], ...] = (
        ("num", int),
        ("min", int | float),
        ("spacing", int | float),
    )
    pos_ints: tuple[str, ...] = (
        "num",
    )
    literals: tuple[tuple[str, str, _LiteralGenericAlias], ...] = (
        ("zcoord", "VerticalCoordSystems", VerticalCoordSystems),
    )
    check_keys(
        set(config.keys()),
        expected_keys,
        "Vertical Grids"
    )
    for val, expected_type in vals:
        check_type(val, config.get(val), expected_type)
    for val in pos_ints:
        check_pos_int(val, cast("int", config.get(val)))
    for val, literal_name, literal_type in literals:
        check_literal(
            val,
            cast("str", config.get(val, "MISSING")),
            literal_name,
            literal_type
        )
    return cast("VerticalGridsConfig", config)
