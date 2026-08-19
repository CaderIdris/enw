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
    dispersion_options_ensemble_size: NotRequired[int]
    met_ensemble_size: NotRequired[int]


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
    """"""

    num: int
    min: float
    max: float

class DomainVDimension(TypedDict):
    """"""

    max: int

class DomainTDimension(TypedDict):
    """"""

    unbounded: bool
    max_travel_time: str


class DomainConfig(TypedDict):
    """"""

    hcoord: str
    zcoord: str
    x: DomainHDimension
    y: DomainHDimension
    z: DomainVDimension
    t: DomainTDimension


class TemporalGridConfig(TypedDict):
    """"""
    num: int
    spacing: str
    min: dt.datetime

class SpeciesConfig(TypedDict):
    """"""

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
    TemporalGrid: TemporalGridConfig
    Domain: dict[str, DomainConfig]
    Species: dict[str, SpeciesConfig]


class DomainTimeBlock(TypedDict):
    """Schema of the time options in the Domain block."""

    t_unbounded: Switch | None
    start_time: DateTime | TimeInterval | None
    end_time: DateTime | TimeInterval | None
    duration: TimeInterval | None
    max_travel_time: TimeInterval

OptionBlock = Literal[
    "main",
    "output",
    "restart",
    "multiple_case",
    "openmp",
    "coords"
]
"""A camel case set of all NAME III config blocks with defaults in enw.

This is used for tyoe hinting during development, to minimise bugs.
This will likely not be required if you are using enw as a base to
build your own tool.
"""

