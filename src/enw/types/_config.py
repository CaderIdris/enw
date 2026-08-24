"""Custom types used when configuring enw."""
from typing import Literal, TypedDict, NotRequired, TYPE_CHECKING

if TYPE_CHECKING:
    import datetime as dt

    from ._options import Switch
    from ._strings import DateTime, TimeInterval

class MainConfig(TypedDict):
    """Configuration variables for the Main Options input block.

    This TypedDict represents all of the configuration variables of the `Main
    Options` block in the NAME III Input Header files, using pure Python types.
    In the case of boolean variables, they are cast to `Switch` variables when
    the `Main` dataclass is set up. In the case of values with a fixed set of
    options, such as `Absolute or Relative?`, they are cast to their respective
    Literal type when the `Main` dataclass is set up.
    """

    name: str
    backwards: bool
    start_time: dt.datetime
    end_time: dt.datetime
    time_step: str


class MainExtraConfig(TypedDict):
    """Additional configuration variables for the Main Options input block.

    This TypedDict represents all of the additional configuration variables of
    the `Main Options` block in the NAME III Input Header files, using pure
    Python types. In the case of boolean variables, they are cast to `Switch`
    variables when the `Main` dataclass is set up. In the case of values with
    a fixed set of options, such as `Absolute or Relative?`, they are cast to
    their respective Literal type when the `Main` dataclass is set up.
    """

    max_num_sources: int
    max_num_field_reqs: int
    max_num_field_output_groups: int
    absolute_or_relative: str
    fixed_met: bool
    flat_earth: bool
    random_seed: str
    use_ukv: bool


class OutputConfig(TypedDict):
    """Configuration variables for the Output Options input block.

    This TypedDict represents all the configuration variables of the `Output
    Options` block in the NAME III Input Header files, using pure Python types.
    `Seconds?` is cast to a `Switch` type when the `Output` dataclass is set
    up.
    """

    folder: str
    seconds: bool


class RestartConfig(TypedDict):
    """Configuration variables for the Restart Options input block.

    This TypedDict represents all the configuration variables of the `Restart
    Options` block in the NAME III Input Header files, using pure Python types.
    `Write on Suspend?` and `Delete Old Files?` are cast to a `Switch` type
    when the `Output` dataclass is set up. `Time Between Writes` is cast to
    either a `DescriptiveTimeInterval` or `NonDescriptiveTimeInterval` type.

    """

    cases_between_writes: NotRequired[int]
    time_between_writes: NotRequired[str]
    delete_old_files: NotRequired[bool]
    write_on_suspend: NotRequired[bool]


class MultipleCaseConfig(TypedDict):
    """Configuration variables for the MultipleCase Options input block.

    This TypedDict represents all of the configuration variables of the
    `Multiple Case Options` block in the NAME III Input Header files, using
    pure Python types.
    """

    name: NotRequired[str]
    dispersion_options_ensemble_size: int
    met_ensemble_size: int


class OpenMPConfig(TypedDict):
    """Configuration variables for the OpenMP Options input block.

    This TypedDict represents all of the configuration variables of the `OpenMP
    Options` block in the NAME III Input Header files, using pure Python types.
    """

    use_openmp: bool
    threads: NotRequired[int]
    particle_threads: NotRequired[int]
    particle_update_threads: NotRequired[int]
    chemistry_threads: NotRequired[int]
    output_group_threads: NotRequired[int]
    output_process_threads: NotRequired[int]
    parallel_metread: NotRequired[bool]
    parallel_metprocess: NotRequired[bool]


class CoordinateSystemsConfig(TypedDict):
    """Configuration variables for the Coordinate Systems input blocks.

    Covers both horizontal and vertical.

    This TypedDict represents all of the configuration variables of the
    `Horizontal Coordinate Systems` and `Vertical Coordinate Systems` blocks
    in the NAME III Input Header files, using pure Python types.
    """

    horizontal: list[str]
    vertical: list[str]


class LocationConfig(TypedDict):
    """Configuration variables for the Locations input blocks.

    This TypedDict represents all of the configuration variables for the
    `Locations` block in the NAME III Input Header files, using pure Python
    types.
    """

    hcoord: str
    x: float
    y: float


class HorizontalGridDimension(TypedDict):
    """Nested dictionary for x/y dimensions in HorizontalGrids TypedDict."""

    num: int
    min: float
    max: float

class HorizontalGridsConfig(TypedDict):
    """Configuration variables for the Horizontal Grids input blocks.

    This TypedDict represents all of the configuration variables for the
    `Horizontal Grids` block in the NAME III Input Header files, using pure
    Python types.
    """

    #INFO: Take from location leftovers
    name: str
    hcoord: str
    x: HorizontalGridDimension
    y: HorizontalGridDimension


class VerticalGridsConfig(TypedDict):
    """Configuration variables for the VerticalGrids input blocks.

    This TypedDict represents all the configuration variables for the
    `Vertical Grids` block in the NAME III Input Header files, using pure
    Python types.
    """

    name: str
    zcoord: str
    count: int
    spacing: float
    min_point: float


class DomainHDimension(TypedDict):
    """Horizontal subdict for Domain input blocks."""

    num: int
    min: float
    max: float

class DomainVDimension(TypedDict):
    """Vertical subdict for Domain input blocks."""

    max: int

class DomainTDimension(TypedDict):
    """Temporal subdict for Domain input blocks."""

    unbounded: bool
    max_travel_time: str


class DomainConfig(TypedDict):
    """Configuration variables for the Domains input blocks.

    This TypedDict represents all the configuration variables for the
    `Domains` block in the NAME III Input Header files, using pure
    Python types.
    """

    hcoord: str
    zcoord: str
    x: DomainHDimension
    y: DomainHDimension
    z: DomainVDimension
    t: DomainTDimension


class SpeciesConfig(TypedDict):
    """Configuration variables for the Species input block.

    This TypedDict represents all the configuration variables for the
    `Species` block in the NAME III Input Header files, using pure
    Python types.
    """

    category: str
    molecular_weight: float
    deposition_velocity: float
    material_unit: str
    uv_loss_rate: float
    half_life: str
    surface_resistance: float | None
    on_particles: bool
    on_fields: bool
    advect_fields: bool

class OutputRequirementsConfig(TypedDict):
    """"""
    fields: dict[str, ORFields]
    ppinfo: dict[str, ORPPInfo]

class ORFields(TypedDict):
    """"""
    quantity: str
    species: NotRequired[str]
    source: NotRequired[str]
    h_grid: NotRequired[str]
    z_grid: NotRequired[str]
    t_grid: str
    bl_average: NotRequired[bool]
    t_av_or_int: str
    av_time: NotRequired[str]
    num_av_times: NotRequired[int]
    sync: bool
    across: NotRequired[str]
    separate_file: NotRequired[str]
    output_format: str
    output_route: str
    output_group: str

class ORPPInfo(TypedDict):
    """"""
    particles: bool
    puffs: bool
    met: bool
    mass: bool
    plume_rise: bool
    dispersion_scheme: bool
    puff_family: bool
    fate_info: bool
    h_coord: str
    z_coord: str
    sync: bool
    output_route: str


class DispersionOptionsConfig(TypedDict):
    """"""
    max_num_particles: int
    max_num_full_particles: int
    max_num_puffs: int
    max_num_original_puffs: int
    skew_time: str
    velocity_memory_time: str
    inhomogeneous_time: str
    mesoscale_velocity_memory_time: str
    puff_time: str
    sync_time: str
    computational_domain: str
    puff_interval: str
    delta_opt: str
    time_of_fixed_met: dt.datetime
    deep_convection: str
    radioactive_decay: bool
    agent_decay: bool
    dry_deposition: bool
    wet_deposition: bool
    mesoscale_motions: bool
    chemistry: bool
    turbulence: bool


class EnwConfig(TypedDict):
    """Configuration schema of enw.

    This TypedDict represents all of the configuration variables of enw, once
    type checking and formatting has been performed. It contains all the
    required and optional keys, with each configuration block separated out
    into its own TypedDict.
    """

    Main: MainConfig
    MainExtra: MainExtraConfig
    Output: OutputConfig
    Restart: NotRequired[RestartConfig]
    OpenMP: OpenMPConfig
    MultipleCase: MultipleCaseConfig
    CoordinateSystems: CoordinateSystemsConfig
    Locations: dict[str, LocationConfig]
    HorizontalGrid: HorizontalGridsConfig
    VerticalGrid: VerticalGridsConfig
    Domain: dict[str, DomainConfig]
    Species: dict[str, SpeciesConfig]
    OutputRequirements: OutputRequirementsConfig
    SetsOfDispersionOptions: DispersionOptionsConfig


class DomainTimeBlock(TypedDict):
    """Schema of the time options in the Domain block."""

    t_unbounded: Switch | None
    start_time: DateTime | TimeInterval | None
    end_time: DateTime | TimeInterval | None
    duration: TimeInterval | None
    max_travel_time: TimeInterval

class OpenGHGPresets(TypedDict):
    """Return type for preset locations, species and domains from OpenGHG."""

    Locations: dict[str, LocationConfig]
    Species: dict[str, SpeciesConfig]
    Domains: dict[str, DomainConfig]

OptionBlock = Literal[
    "main",
    "output",
    "restart",
    "multiple_case",
    "openmp",
    "coords"
]
"""A camel case set of all NAME III config blocks with defaults in enw.

This is used for type hinting during development, to minimise bugs.
This will likely not be required if you are using enw as a base to
build your own tool.
"""

