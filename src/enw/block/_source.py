"""Configuration objects for all of the misc NAME III Input Header Blocks.

Covers:

"""
from dataclasses import dataclass
from typing import cast, TYPE_CHECKING, Literal

from ._base import NAMEIIIHeaderInputBlock
from enw.types import (
    SourceShapeOpts,
    SourceStrength,
    HorizontalCoordSystems,
    VerticalCoordSystems,
    Switch,
    TimeInterval,
    DateTime,
)
from enw.utils import (
    check_type,
    check_time_interval,
    check_source_strength,
    make_time_interval,
    check_literal,
    make_switch,
    check_datetime,
    make_datetime
)

if TYPE_CHECKING:
    from types import NotImplementedType
    from typing import Literal

    from enw.types import TimeInterval


@dataclass(kw_only=True)
class Species(NAMEIIIHeaderInputBlock):
    """Configuration for the Species block for NAME III.

    The `Species:` block contains the following column:

    ??? information Columns
    **Name**

    Name to be used for the species.

    _Accepted Values_

    Any Valid String

    **Category**

    User defined category for the species.

    _Accepted Values_

    Any Valid String

    **Half Life**

    Half life of a radioactive species.

    _Accepted Values_

    - Valid time interval.
    - 'Stable'
    - Blank (Same as 'Stable')

    **Daughter**

    Name of the daughter product.

    _Accepted Values_

    Any valid string.

    **Cloud Gamma Parameters**

    Set of cloud gamma parameters.
    Not currently used.

    _Accepted Values_

    Name of a Cloud Gamma Parameters block.

    **UV Loss Rate**

    Rate of species destruction due to UV.

    _Accepted Values_

    - 'Stable'
    - Loss rate value

    **Surface Resistance**

    Surface resistance for deposition.

    _Accepted Values_

    Positive float value.

    **Deposition Velocity**

    Deposition velocity.

    _Accepted Values_

    Positive float value.

    **A rain - BC**

    Scavenging coefficient (A) for below-cloud wet deposition (washout)
    by rain.

    $ A = Ar^{B}$, r= $ precipitation rate (mm/hr)

    _Accepted Values_

    Positive float value.

    **B rain - BC**

    Scavenging coefficient (B) for below-cloud wet deposition (washout)
    by rain.

    $ A = Ar^{B}$, r= $ precipitation rate (mm/hr)

    _Accepted Values_

    Positive float value.

    **A snow - BC**

    Scavenging coefficient (A) for below-cloud wet deposition (washout)
    by snow.

    $ A = Ar^{B}$, r= $ precipitation rate (mm/hr)

    _Accepted Values_

    Positive float value.

    **B snow - BC**

    Scavenging coefficient (B) for below-cloud wet deposition (washout)
    by snow.

    $ A = Ar^{B}$, r= $ precipitation rate (mm/hr)

    _Accepted Values_

    Positive float value.

    **A rain - IC**

    Scavenging coefficient (A) for in-cloud wet deposition (rainout)
    by rain.

    $ A = Ar^{B}$, r= $ precipitation rate (mm/hr)

    _Accepted Values_

    Positive float value.

    **B rain - IC**

    Scavenging coefficient (B) for in-cloud wet deposition (rainout)
    by rain.

    $ A = Ar^{B}$, r= $ precipitation rate (mm/hr)

    _Accepted Values_

    Positive float value.

    **A snow - IC**

    Scavenging coefficient (A) for in-cloud wet deposition (rainout)
    by snow.

    $ A = Ar^{B}$, r= $ precipitation rate (mm/hr)

    _Accepted Values_

    Positive float value.

    **B snow - IC**

    Scavenging coefficient (B) for in-cloud wet deposition (rainout)
    by snow.

    $ A = Ar^{B}$, r= $ precipitation rate (mm/hr)

    _Accepted Values_

    Positive float value.

    **Molecular Weight**

    Molecular weight, only used for gases.

    _Accepted Values_

    Positive float value.

    **Material unit**

    Unit for weight.

    _Accepted Values_

    Valid unit.

    **Land use dependent dry dep**

    Whether to use the land use dependent dry deposition scheme.
    """

    rows: list[SpeciesRow]
    used_keys: dict[str, bool]

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        rows: dict[str, dict[str, str | int | float | None]]
    ) -> Species:
        """Configure a config block with error checking and formatting.

        Parameters
        ----------
        rows : list[dict[str, str | int | float | Nonw]]
            A list of species.

        """
        converted_rows: list[SpeciesRow] = [
            SpeciesRow.setup(name=name, **row) #type: ignore[ty:invalid-argument-type]
            for name, row in rows.items()
        ]
        used_keys = {"name": True, "half_life": True}
        for row in converted_rows:
            used_keys = {
                k: v is not None or used_keys.get(k, False)
                for k, v in row.__dict__.items()
            }
        return cls(
            rows=converted_rows,
            used_keys=used_keys
        )

    def __str__(self) -> str:
        """Return the configuration block for the NAME input header file.

        Passes the block configuration into the "species.jinja" block
        template to get the appropriate configuration block.

        ``` jinja title="species.jinja"
        --8<-- "./src/enw/files/block_templates/species.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template("species.jinja")
        return template.render(
            rows=[row.__dict__ for row in self.rows],
            used_keys=self.used_keys
        )

    def __repr__(self) -> str:
        """Return representation of object to print to console.

        Returns
        -------
        str
            Representation of object.

        """
        repr_lines = ["[Species]"]
        for row in self.rows:
            repr_lines.append(f"\t[[{row.name}]]")
            repr_lines.extend([
                f"\t\t{k:<20}: {v}"
                for k, v in row.__dict__.items()
                if k[0] != "_" and k != "name"
            ])
        return "\n".join(repr_lines)

@dataclass(kw_only=True)
class SpeciesRow:
    """A single row for the Species block in the input header file."""

    name: str
    category: str
    deposition_velocity: int | float
    molecular_weight: int | float
    material_unit: str
    half_life: TimeInterval | Literal["Stable"]
    surface_resistance: float | int | None
    uv_loss_rate: int | float
    daughter: str | None = None
    branching_ratio: NotImplementedType | None = None
    cloud_gamma_parameters: NotImplementedType | None = None
    below_cloud_rain_a: NotImplementedType | None = None
    below_cloud_rain_b: NotImplementedType | None = None
    in_cloud_rain_a: NotImplementedType | None = None
    in_cloud_rain_b: NotImplementedType | None = None
    below_cloud_snow_a: NotImplementedType | None = None
    below_cloud_snow_b: NotImplementedType | None = None
    in_cloud_snow_a: NotImplementedType | None = None
    in_cloud_snow_b: NotImplementedType | None = None
    land_use_dependent_dry_dep: NotImplementedType | None = None
    mean_aerosol_diameter: NotImplementedType | None = None

    @classmethod
    def setup(
        cls,
        name: str,
        category: str,
        deposition_velocity: int | float,
        molecular_weight: int | float,
        material_unit: str,
        uv_loss_rate: int | float,
        half_life: str | None = "Stable",
        surface_resistance: float | int | None = None,
        daughter: str | None = None,
        branching_ratio: None = None,
        cloud_gamma_parameters: None = None,
        below_cloud_rain_a: None = None,
        below_cloud_rain_b: None = None,
        in_cloud_rain_a: None = None,
        in_cloud_rain_b: None = None,
        below_cloud_snow_a: None = None,
        below_cloud_snow_b: None = None,
        in_cloud_snow_a: None = None,
        in_cloud_snow_b: None = None,
        land_use_dependent_dry_dep: None = None,
        mean_aerosol_diameter: None = None
    ) -> SpeciesRow:
        """Create the row for the Species block and type check.

        Parameters
        ----------
        name : str
            The name of the species
        category : str
            The user-defined category assigned to the species.
        deposition_velocity : int | float
            How quickly the species is deposited.
        molecular_weight : int | float
            The molecular weight of the species.
        material_unit : str
            The unit for the molecular weight (e.g. "g" for grams).
        uv_loss_rate : int | float
            The rate of loss of the species to UV light.
        half_life : str | None, default="Stable"
            The half life of the species.
        surface_resistance : float | int | None, default=None
            The surface resistance of the species.
        daughter : None, default=None
            Not implemented!
        branching_ratio : None, default=None
            Not implemented!
        cloud_gamma_parameters : None, default=None
            Not implemented!
        below_cloud_rain_a : None, default=None
            Not implemented!
        below_cloud_rain_b : None, default=None
            Not implemented!
        in_cloud_rain_a : None, default=None
            Not implemented!
        in_cloud_rain_b : None, default=None
            Not implemented!
        below_cloud_snow_a : None, default=None
            Not implemented!
        below_cloud_snow_b : None, default=None
            Not implemented!
        in_cloud_snow_a : None, default=None
            Not implemented!
        in_cloud_snow_b : None, default=None
            Not implemented!
        land_use_dependent_dry_dep : None, default=None
            Not implemented!
        mean_aerosol_diameter : None, default=None
            Not implemented!

        """
        _unimplemented = (
            ("branching_ratio", branching_ratio),
            ("cloud_gamma_parameters", cloud_gamma_parameters),
            ("below_cloud_rain_a", below_cloud_rain_a),
            ("below_cloud_rain_b", below_cloud_rain_b),
            ("in_cloud_rain_a", in_cloud_rain_a),
            ("in_cloud_rain_b", in_cloud_rain_b),
            ("below_cloud_snow_a", below_cloud_snow_a),
            ("below_cloud_snow_b", below_cloud_snow_b),
            ("in_cloud_snow_a", in_cloud_snow_a),
            ("in_cloud_snow_b", in_cloud_snow_b),
            ("land_use_dependent_dry_dep", land_use_dependent_dry_dep),
            ("mean_aerosol_diameter", mean_aerosol_diameter)
        )
        #INFO: Check name
        check_type(f"{name}.name", name, str)
        #INFO: Check category
        if category is not None:
            check_type(f"{name}.category", category, str)
        #INFO: Check half_life
        if half_life is None or half_life == "Stable":
            half_life_transformed: Literal["Stable"] = "Stable"
        else:
            if daughter is None:
                msg = "daughter must be specified with half_life."
                raise ValueError(msg)
            check_type(f"{name}.half_life", half_life, str)
            if half_life != "Stable":
                check_time_interval(f"{name}.half_life", half_life)
                half_life_transformed: TimeInterval = make_time_interval(
                    half_life
                )
        #INFO: Check daughter
        if daughter is not None:
            if half_life is None or half_life == "Stable":
                msg = "half_life must be specified with daughter."
                raise ValueError(msg)
            check_type(f"{name}.daughter", daughter, str)
        #INFO: Check surface_resistance
        if surface_resistance is not None:
            check_type(
                f"{name}.surface_resistance",
                surface_resistance,
                (int, float)
            )
        #INFO: Check deposition_velocity
        check_type(
            f"{name}.deposition_velocity",
            deposition_velocity,
            (int, float)
        )
        #INFO: Check molecular_weight
        check_type(
            f"{name}.molecular_weight",
            molecular_weight,
            (int, float)
        )
        #INFO: Check material_unit
        check_type(f"{name}.material_unit", material_unit, str)
        #INFO: Check not implemented variables
        for k, v in _unimplemented:
            if v is not None:
                msg = f"{k} was specified but is not implemented for Species."
                raise NotImplementedError(msg)
        #TODO: We need some +ve checks etc, do later
        return SpeciesRow(
            name=name,
            category=category,
            deposition_velocity=deposition_velocity,
            molecular_weight=molecular_weight,
            material_unit=material_unit,
            half_life=half_life_transformed,
            surface_resistance=surface_resistance,
            uv_loss_rate=uv_loss_rate,
            daughter=daughter,
            branching_ratio=branching_ratio,
            cloud_gamma_parameters=cloud_gamma_parameters,
            below_cloud_rain_a=below_cloud_rain_a,
            below_cloud_rain_b=below_cloud_rain_b,
            in_cloud_rain_a=in_cloud_rain_a,
            in_cloud_rain_b=in_cloud_rain_b,
            below_cloud_snow_a=below_cloud_snow_a,
            below_cloud_snow_b=below_cloud_snow_b,
            in_cloud_snow_a=in_cloud_snow_a,
            in_cloud_snow_b=in_cloud_snow_b,
            land_use_dependent_dry_dep=land_use_dependent_dry_dep,
            mean_aerosol_diameter=mean_aerosol_diameter
        )

@dataclass(kw_only=True)
class Sources(NAMEIIIHeaderInputBlock):
    """Configuration for the Sources block for NAME III.

    The `Sources:` block contains the following columns:

    ??? information Columns
        **Name**

        Name of the source.

        _Accepted Values_

        Any Valid String

        **Shape**

        Shape of the source.

        _Accepted Values_

        "Cuboid", "Ellipsoid", "Cylindroid" or "Suzuki".

        *Set of Locations**

        Name of the location block containing the source locations.

        _Accepted Values_

        Any specified Locations block.

        **H-Coord**

        Horizontal coordinate system to be used.

        _Accepted Values_

        Any valid horizontal coordinate system.

        **Z-Coord**

        Vertical coordinate system to be used.

        _Accepted Values_

        Any valid vertical coordinate system.

        **H-Grid**

        Horizontal grid to place the source on.

        _Accepted Values_

        Any previously specified horizontal grid.

        **Z-Grid**

        Vertical grid to place the source on.

        _Accepted Values_

        Any previously specified vertical grid.

        **X**

        X coordinate of source centre.

        _Accepted values_

        Any float value.

        **Y**

        Y coordinate of source centre.

        _Accepted values_

        Any float value.

        **Z**

        Z coordinate of source centre.

        _Accepted values_

        Any float value.

        **dH-Metres?

        Specify dX and dY in metres or in the specified coord system (H-Coord)

        _Accepted Values_

        "Yes" or "No"

        **dZ-Metres?

        Specify dZ in metres or in the specified coord system (Z-Coord)

        _Accepted Values_

        "Yes" or "No"

        **dX**

        Length of source.

        _Accepted Values_

        Positive float.

        **dY**

        Width of source.

        _Accepted Values_

        Positive float.

        **dZ**

        Height of rectangular source

        _Accepted Values_

        Positive float.

        **Angle**

        Angle of dX to the X axis. Measured anticlockwise.

        _Accapted Values_

        Float value.

        **Uniform Area?**

        Make the source uniform across horizontal area as opposed to being
        uniform in terms of the area dXdY as defined by H-Coord.

        _Accepted Values_

        "Yes" or "No".

        **No Reflect?**

        Delete any part of the source below the ground instead of reflecting
        it.

        _Accepted Values_

        "Yes" or "No".

        **Source Strength**

        Species and strength of source for the species.
        Strength is given as either total mass release or the release rate.

        _Accepted Values_

        Species name + Total mass released or release rate e.g.:
        - `SPECIES 1.0 g/s`
        - `SPECIES 40.0 g`

        **Time Dependency**

        Which source time dependency to use, if any.

        _Accepted Values_

        Not currently implemented

        **Plume Rise?**

        Whether or not to use plume rise

        _Accepted Values_

        "Yes" or "No".

        **Temperature**

        Temperature for buoyant release.

        _Accepted Values_

        Float value.

        **Volume Flow Rate**

        Volume flow rate of the emission.

        _Accepted Values_

        Positive float value.

        **Flow Velocity**

        Velocity of the emission.

        _Accepted Values_

        Positive float value.

        **# Particles**

        Lower limit on number of particles released, or particle release rate.

        _Accepted Values_

        Positive integer value, or positive float value.

        **Max Age**

        Maximum age of particles.

        _Accepted Values_

        Time interval, or "infinity"

        **Top Hat**

        Use the top hat distribution?

        _Accepted Values_

        "Yes" or "No".

        **Start Time**

        Start time of the release (Should be later than End Time for reverse
        modelling).

        _Accepted Values_

        Timestamp.

        **End Time**

        End time of the release (Should be earlier than Start Time for reverse
        modelling).

        _Accepted Values_

        Timestamp.

        **Particle Diameter**

        Diameter of the particulate.

        _Accepted Values_

        Positive float.

        **Particle Density**

        Density of particulate.

        _Accepted Values_

        Positive float.

        **Particle Size Distribution**

        Which distribution of particulate sizes to use, if any.

        _Accepted Values_

        Name of a particulate distribution.

        **Met-dependent Source Type**

        Source depends on Met data.

        _Accepted Values_

        "Yes" or "No".

        **Source Groups**

        Semicolon separated list of source groups this source belongs to.

        _Accepted Values_

        Semicolon separated strings.

    """

    rows: list[SourcesRow]
    used_keys: dict[str, bool]

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        rows: dict[str, dict[str, str | int | float | None]]
    ) -> Sources:
        """Configure a config block with error checking and formatting.

        Parameters
        ----------
        rows : list[dict[str, str | int | float | Nonw]]
            A list of sources.

        """
        converted_rows: list[SourcesRow] = [
            SourcesRow.setup(name=name, **row) #type: ignore[ty:invalid-argument-type]
            for name, row in rows.items()
        ]
        used_keys = {"name": True}
        for row in converted_rows:
            used_keys = {
                k: v is not None or used_keys.get(k, False)
                for k, v in row.__dict__.items()
            }
        return cls(
            rows=converted_rows,
            used_keys=used_keys
        )

    def __str__(self) -> str:
        """Return the configuration block for the NAME input header file.

        Passes the block configuration into the "sources.jinja" block
        template to get the appropriate configuration block.

        ``` jinja title="sources.jinja"
        --8<-- "./src/enw/files/block_templates/sources.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template("sources.jinja")
        return template.render(
            rows=[row.__dict__ for row in self.rows],
            used_keys=self.used_keys
        )

    def __repr__(self) -> str:
        """Return representation of object to print to console.

        Returns
        -------
        str
            Representation of object.

        """
        repr_lines = ["[Sources]"]
        for row in self.rows:
            repr_lines.append(f"\t[[{row.name}]]")
            repr_lines.extend([
                f"\t\t{k:<30}: {v}"
                for k, v in row.__dict__.items()
                if k[0] != "_" and k != "name"
            ])
        return "\n".join(repr_lines)

@dataclass(kw_only=True)
class SourcesRow:
    """Single row of the Sources config block in the input header file."""

    name: str
    shape: SourceShapeOpts
    set_of_locations: str
    location: str
    h_coord: HorizontalCoordSystems
    z_coord: VerticalCoordSystems
    z: float
    dh_metres: Switch
    dz_metres: Switch
    dx: float
    dy: float
    dz: float
    angle: float
    source_strength: SourceStrength
    plume_rise: Switch
    temperature: float
    volume_flow_rate: float
    num_particles: int | float
    max_age: TimeInterval | Literal["infinity"]
    top_hat: Switch
    start_time: DateTime
    stop_time: DateTime
    h_grid: NotImplementedType | None = None
    z_grid: NotImplementedType | None = None
    x: NotImplementedType | None = None
    y: NotImplementedType | None = None
    uniform_area: NotImplementedType | None = None
    no_reflect: NotImplementedType | None = None
    time_dependency: NotImplementedType | None = None
    flow_velocity: NotImplementedType | None = None
    particle_diameter: NotImplementedType | None = None
    particle_density: NotImplementedType | None = None
    particle_size_distribution: NotImplementedType | None = None
    met_dependent_source_type: NotImplementedType | None = None
    source_groups: NotImplementedType | None = None

    @classmethod
    def setup(
        cls,
        *,
        name: str,
        shape: str,
        set_of_locations: str,
        location: str,
        h_coord: str,
        z_coord: str,
        z: float,
        dh_metres: bool,
        dz_metres: bool,
        dx: float,
        dy: float,
        dz: float,
        angle: float,
        source_strength: str,
        plume_rise: bool,
        temperature: float,
        volume_flow_rate: float,
        num_particles: int | float,
        max_age: str,
        top_hat: bool,
        start_time: str,
        stop_time: str,
        h_grid: None = None,
        z_grid: None = None,
        x: None = None,
        y: None = None,
        uniform_area: None = None,
        no_reflect: None = None,
        time_dependency: None = None,
        flow_velocity: None = None,
        particle_diameter: None = None,
        particle_density: None = None,
        particle_size_distribution: None = None,
        met_dependent_source_type: None = None,
        source_groups: None = None
    ) -> SourcesRow:
        """Create a row for the sources block.

        Parameters
        ----------
        name : str
            The name of the source.
            Corresponds to **Name**.
        shape : str
            The shape of the source.
            Corresponds to **Shape**
            Can be "Cuboid", "Elipsoid" or "Cylindroid".
        set_of_locations : str
            Name of a Locations block.
            Corresponds to **Set of Locations**.
        location : str
            Specific location within the Locations block.
            Corresponds to **Location**.
        h_coord : str
            Horizontal coordinate system to use.
            Corresponds to **H-Coord**.
        z_coord : str
            Vertical coordinate system to used.
            Corresponds to **Z-Coord**.
        z : float
            Z coordinate of the source centre.
            Corresponds to **Z**.
        dh_metres : bool
            Specify dX and dY in metres instead of the coordinate system?
            Corresponds to **dH-Metres?**.
        dz_metres : bool
            Specify dZ in metres instead of the coordinate system?
            Corresponds to **dZ-Metres?**.
        dx : float
            Length of the source.
            Corresponds to **dX**.
        dy : float
            Width of the source.
            Corresponds to **dy**.
        dz : float
            Height of the source.
            Corresponds to **dZ**.
        angle : float
            Angle of dX to the x axis (anti clockwise).
            Corresponds to **Angle**.
        source_strength : bool
            Species released from source and its strength.
            Corresponds to **Uniform Area?**.
        plume_rise : bool
            Should a plume-rise scheme be used?
            Corresponds to **Plume Rise?**.
        temperature : float
            Temperature for buoyant release.
            Corresponds to **Temperature**.
        volume_flow_rate : float
            Volume flow rate of emission.
            Corresponds to **Volume Flow Rate**.
        num_particles : int | float
            Lower limit on number of particles released or particle release
            rate.
            Corresponds to **# Particles**.
        max_age : str
            Maximum age of particles. Should be timestamp or "infinity"
            Corresponds to **Max Age**.
        top_hat : bool
            Whether or not to use a top hat distribution.
            Corresponds to **Top Hat**.
        start_time : str
            The start time of the release.
            Corresponds to **Start Time**.
        stop_time : str
            The end time of the release.
            Corresponds to **Stop Time**.
        h_grid : None, default=None
            **Not implemented**
            Corresponds to **H-Grid**.
        z_grid : None, default=None
            **Not implemented**
            Corresponds to **Z-Grid**.
        x : None, default=None
            **Not implemented**
            Corresponds to **X**.
        y : None, default=None
            **Not implemented**
            Corresponds to **Y**.
        uniform_area : None, default=None
            **Not implemented**
            Corresponds to **Uniform Area?**.
        no_reflect : None, default=None
            **Not implemented**
            Corresponds to **No Reflect?**.
        time_dependency : None, default=None
            **Not implemented**
            Corresponds to **Time Dependency**.
        flow_velocity : None, default=None
            **Not implemented**
            Corresponds to **Flow Velocity**.
        particle_diameter : None, default=None
            **Not implemented**
            Corresponds to **Particle Diameter**.
        particle_density : None, default=None
            **Not implemented**
            Corresponds to **Particle Density**.
        particle_size_distribution : None, default=None
            **Not implemented**
            Corresponds to **Particle Size Distribution**.
        met_dependent_source_type : None, default=None
            **Not implemented**
            Corresponds to **Met-dependent Source Type**.
        source_groups : None, default=None
            **Not implemented**
            Corresponds to **Source Groups**.

        """
        #TODO: Some of these can be optional
        #INFO: Check name
        check_type("name", name, str)
        #INFO: Check shape
        check_literal("shape", shape, "SourceShapeOpts", SourceShapeOpts)
        shape_formatted = cast("SourceShapeOpts", shape)
        #INFO: Check set_of_locations
        check_type("set_of_locations", set_of_locations, str)
        #INFO: Check location
        check_type("location", location, str)
        #INFO: Check h_coord
        check_literal(
            "h_coord",
            h_coord,
            "HorizontalCoordSystems",
            HorizontalCoordSystems
        )
        h_coord_formatted = cast("HorizontalCoordSystems", h_coord)
        #INFO: Check z_coord
        check_literal(
            "z_coord",
            z_coord,
            "VerticalCoordSystems",
            VerticalCoordSystems
        )
        z_coord_formatted = cast("VerticalCoordSystems", z_coord)
        #INFO: Check z
        check_type("z", z, float | int)
        #INFO: Check dh_metres
        check_type("dh_metres", dh_metres, bool)
        dh_metres_formatted = make_switch(dh_metres)
        #INFO: Check dz_metres
        check_type("dz_metres", dz_metres, bool)
        dz_metres_formatted = make_switch(dz_metres)
        #INFO: Check dx
        check_type("dx", dx, float | int)
        #INFO: Check dy
        check_type("dy", dy, float | int)
        #INFO: Check dz
        check_type("dz", dz, float | int)
        #INFO: Check angle
        check_type("angle", angle, float | int)
        #INFO: Check source_strength
        check_type("source_strength", source_strength, str)
        check_source_strength("source_strength", source_strength)
        source_strength_formatted = SourceStrength(source_strength)
        #INFO: Check plume_rise
        check_type("plume_rise", plume_rise, bool)
        plume_rise_formatted = make_switch(plume_rise)
        #INFO: Check temperature
        check_type("temperature", temperature, float | int)
        #INFO: Check volume_flow_rate
        check_type("volume_flow_rate", volume_flow_rate, float | int)
        #INFO: Check num_particles
        check_type("num_particles", num_particles, float | int)
        #INFO: Check max_age
        check_type("max_age", max_age, str)
        if max_age != "infinity":
            check_time_interval("max_age", max_age)
            max_age_formatted = make_time_interval(max_age)
        else:
            max_age_formatted = "infinity"
        #INFO: Check top_hat
        check_type("top_hat", top_hat, bool)
        top_hat_formatted = make_switch(top_hat)
        #INFO: Check start_time
        check_type("start_time", start_time, str)
        check_datetime("start_time", start_time)
        start_time_formatted = make_datetime(start_time)
        #INFO: Check stop_time
        check_type("stop_time", stop_time, str)
        check_datetime("stop_time", stop_time)
        stop_time_formatted = make_datetime(stop_time)

        _unimplemented = (
            ("h_grid", h_grid),
            ("z_grid", z_grid),
            ("x", x),
            ("y", y),
            ("uniform_area", uniform_area),
            ("no_reflect", no_reflect),
            ("time_dependency", time_dependency),
            ("flow_velocity", flow_velocity),
            ("particle_diameter", particle_diameter),
            ("particle_density", particle_density),
            ("particle_size_distribution", particle_size_distribution),
            ("met_dependent_source_type", met_dependent_source_type),
            ("source_groups", source_groups),
        )

        #INFO: Check not implemented variables
        for k, v in _unimplemented:
            if v is not None:
                msg = f"{k} was specified but is not implemented for Sources."
                raise NotImplementedError(msg)

        return cls(
            name=name,
            shape=shape_formatted,
            set_of_locations=set_of_locations,
            location=location,
            h_coord=h_coord_formatted,
            z_coord=z_coord_formatted,
            z=z,
            dh_metres=dh_metres_formatted,
            dz_metres=dz_metres_formatted,
            dx=dx,
            dy=dy,
            dz=dz,
            angle=angle,
            source_strength=source_strength_formatted,
            plume_rise=plume_rise_formatted,
            temperature=temperature,
            volume_flow_rate=volume_flow_rate,
            num_particles=num_particles,
            max_age=max_age_formatted,
            top_hat=top_hat_formatted,
            start_time=start_time_formatted,
            stop_time=stop_time_formatted
        )


@dataclass(kw_only=True)
class SpeciesUses(NAMEIIIHeaderInputBlock):
    """"""
    name: str
    on_particles: Switch
    on_fields: Switch
    advect_field: Switch
    particle_size_distribution_for_fields: NotImplementedType | None = None#str

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        name: str,
        on_particles: bool,
        on_fields: bool,
        advect_field: bool,
        particle_size_distribution_for_fields: None = None
    ) -> SpeciesUses:
        """"""

        _base_types = (
            ("name", name, str),
        )

        _switch_statements = (
            ("on_particles", on_particles),
            ("on_fields", on_fields),
            ("advect_field", advect_field)
        )

        _unimplemented = (
            (
                "particle_size_distribution_for_fields",
                particle_size_distribution_for_fields,
            ),
        )

        #INFO: Check switch_statements
        switches: dict[str, Switch] = {}
        for val_name, val in _switch_statements:
            check_type(val_name, val, bool)
            switches[val_name] = make_switch(val)

        #INFO: Check standard types
        for val_name, val, type_to_check in _base_types:
            check_type(val_name, val, type_to_check)

        #INFO: Check not implemented variables
        for k, v in _unimplemented:
            if v is not None:
                msg = (
                    f"{k} was specified but is not implemented for Species "
                    "Uses."
                )
                raise NotImplementedError(msg)

        return cls(
            name=name,
            on_particles=switches["on_particles"],
            on_fields=switches["on_fields"],
            advect_field=switches["advect_field"],
            particle_size_distribution_for_fields=(
                particle_size_distribution_for_fields
            )
        )

    def __str__(self) -> str:
        """Return the configuration block for the NAME input header file.

        Passes the block configuration into the "speciesuses.jinja" block
        template to get the appropriate configuration block.

        ``` jinja title="speciesuses.jinja"
        --8<-- "./src/enw/files/block_templates/speciesuses.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template("speciesuses.jinja")
        return template.render(
            name=self.name,
            on_particles=self.on_particles,
            on_fields=self.on_fields,
            advect_field=self.advect_field,
            particle_size_distribution_for_fields=self.particle_size_distribution_for_fields,
        )


    def __repr__(self) -> str:
        """Return representation of object to print to console.

        Returns
        -------
        str
            Representation of object.

        """
        repr_lines = ["[Species Uses]"]
        repr_lines.extend([
            f"\t{k:<40}: {v}"
            for k, v in self.__dict__.items()
            if k[0] != "_"
        ])
        return "\n".join(repr_lines)


