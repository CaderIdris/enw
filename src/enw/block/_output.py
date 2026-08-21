"""Configuration objects for all the output NAME III Input Header Blocks.

Covers:

- Output Requirements - Fields: `Fields`

"""
from enw.types import (
    QuantityOpts,
    HorizontalCoordSystems,
    VerticalCoordSystems,
)
from enw.types._options import TAvOrIntOpts
from dataclasses import dataclass
from typing import cast, TYPE_CHECKING

from enw.types import (
    AcrossString,
    OutputFormatStringF,
    OutputRouteStringF,
    OutputRouteStringPP,
    SeparateFileString
)
from enw.utils import (
    check_type,
    check_literal,
    check_output_string_fields,
    check_output_string_pp,
    make_switch,
    check_time_interval,
    make_time_interval,
)

from ._base import NAMEIIIHeaderInputBlock

if TYPE_CHECKING:
    from enw.types import (
        TimeInterval,
        Switch,
    )
    from types import NotImplementedType

@dataclass(kw_only=True)
class Fields(NAMEIIIHeaderInputBlock):
    """Configuration for the Output Requirements - Fields block for NAME III.

    The `Output Requirements - Fields` block contains the following columns:
    ??? information "Columns"
        **Name**

        The name of the output requirement.

        _Accepted Values_

        Any valid string

        **Quantity**

        Type of field required.

        _Accepted Values_

        |Option|
        |------|
        |Air Concentration|
        |Mixing Ratio|
        |Dry Deposition Rate|
        |Wet Deposition Rate|
        |Deposition Rate|
        |Min Z|
        |# Particles|
        |# Puffs|
        |# Particle Steps|
        |# Puff Steps|
        |Mass|
        |Mean Z|
        |Sigma Z|
        |X Stats|
        |Mean Travel Time|
        |Puff Centres|
        |Sigma C|
        |Chemistry Field|
        |Eulerian Concentration|
        |E Mixing Ratio|
        |Concentration|
        |Sigma WW|
        |HSigma WW|
        |HSigma UU|
        |Tau WW|
        |Mean Flow U|
        |Mean Flow V|
        |Mean Flow W|
        |Temperature (K)|
        |Potential Temperature (K)|
        |Specific Humidity|
        |Pressure (Pa)|
        |Density|
        |Topography|
        |u-star|
        |Sensible Heat Flux|
        |Boundary Layer Depth|
        |Wind Speed|
        |Wind Direction (degrees)|
        |Precipitation Rate (mm/hr)|
        |Temperature (C)|
        |Cloud Amount (oktas)|
        |Relative Humidity (%)|
        |Pasquill Stability|
        |# Particles By Species|
        |Progress (%)|
        |Clock Time|
        |X|
        |Y|
        |Sigma VV|
        |Mesoscale Sigma VV|
        |Cloud Water (kg/kg)|
        |Cloud Ice (kg/kg)|
        |3d Cloud (Fraction)|
        |Roughness Length|
        |Sea Level Pressure (Pa)|
        |Photon Flux|
        |Adult Effective Cloud Gamma Dose|
        |Adult Lung Cloud Gamma Dose|
        |Adult Thyroid Cloud Gamma Dose|
        |Adult Bone Surface Cloud Gamma Dose|
        |Area at risk|
        |Land Use Fractions|
        |Canopy Water|
        |Leaf Area Index|
        |Canopy Height|
        |Stomatal Conductance|
        |Soil Moisture|
        |Land Fraction|
        |Convective Cloud Base|
        |Convective Cloud Top|
        |Eulerian Total Deposition Rate|
        |# Eulerian field|
        |Eulerian Dry Deposition Rate|
        |# Eulerian field|
        |Eulerian Wet Deposition Rate|
        |# Eulerian field|
        |Reference Source Strength|
        |Actual Source Strength|
        |Max Plume Rise Height|
        |Plume Depth|
        |Final volume flux|

        **Decay Deposition?**

        !!! warning
            Not currently implemented, will raise an error.

        **Species**

        Species that the field refers to.

        _Accepted Values_

        Previously specified species. Can be semicolon separated list.

        **Source**

        Source that the field refers to.

        _Accepted Values_

        Previously specified source, or blank for all sources.

        **Source Group**

        !!! warning
            Not currently implemented, will raise an error.

        **H-Grid**

        Horizontal grid.

        _Accepted Values_

        Previously specified horizontal grid.

        **Z-Grid**

        Vertical grid.

        _Accepted Values_

        Previously specified vertical grid.

        **T-Grid**

        Temporal grid.

        _Accepted Values_

        Previously specified temporal grid.

        **S-Grid**

        !!! warning
            Not currently implemented, will raise an error.

        **H-Coord**

        !!! warning
            Not currently implemented, will raise an error.

        **Z-Coord**

        !!! warning
            Not currently implemented, will raise an error.

        **BL Average?**

        Average results over boundary layer depth.

        _Accepted Values_

        `Yes` or `No`.

        **T Av Or Int**

        Average, integrate or neither over time.

        _Accepted Values_

        |Value|Description|
        |-----|-----------|
        |Av|Time averaging|
        |Int|Time integrating|
        |No|Do not average or integrate over time|

        **Av Time**

        Average/Integration time.

        _Accepted Values_

        Time interval string.

        **# Av Times**

        Number of instantaneous results used to form average.

        _Accepted Values_

        Positive integer value.

        **Ensemble Av?**

        !!! warning
            Not currently implemented, will raise an error.

        **Probabilities**

        !!! warning
            Not currently implemented, will raise an error.

        **Percentiles**

        !!! warning
            Not currently implemented, will raise an error.

        **P Time**

        !!! warning
            Not currently implemented, will raise an error.

        **P dT**

        !!! warning
            Not currently implemented, will raise an error.

        **Ensemble P?**

        !!! warning
            Not currently implemented, will raise an error.

        **Fluctuations?**

        !!! warning
            Not currently implemented, will raise an error.

        **Sync?**

        Calculate output when particles/puffs are synchronised?

        _Accepted Values_

        `Yes` or `No`.

        **X Scale**

        !!! warning
            Not currently implemented, will raise an error.

        **Y Scale**

        !!! warning
            Not currently implemented, will raise an error.

        **Across**

        A string of characters indicating whether variables are placed at the
        top of columns instead of the left of rows.

        _Accepted Values_

        A string comprised of the following characters:

        |Character|Description|
        |---------|-----------|
        |T|Time|
        |S|Travel Time|
        |X|X coordinate|
        |Y|Y coordinate|
        |Z|Z coordinate|

        **Separate File**

        A string of characters indicating which values to put in separate
        files.

        _Accepted Values_

        A string comprised of the following characters:

        |Character|Description|
        |---------|-----------|
        |T|Time|
        |S|Travel Time|
        |X|X coordinate|
        |Y|Y coordinate|
        |Z|Z coordinate|
        |N|Start output fresh after a restart|

        **Output Format**

        Define the output file format.

        _Accepted Values_

        A string comprised of the following characters:

        |Character|Description|
        |---------|-----------|
        |I|Include grid points indices|
        |A|Align columns|
        |Z|Output all grid points, including ones with zero values|
        |F|Flush buffer after writing to keep file up to date|
        |2|Format as NAME II (DEPRECATED)|

        **Output Route**

        Define the output route.

        _Accepted Values_

        A string comprised of the following characters:

        |Character|Description|
        |---------|-----------|
        |D|Output to disk|
        |S|Output to screen|
        |N|Output to NetCDF|

        **Output Group**

        Output group name. Output with same group name is placed in same file.

        _Accepted Values_

        Valid string.

        **Particle Size Distribution**

        !!! warning
            Not currently implemented, will raise an error.

        **Semi-Infinite Approx?**

        !!! warning
            Not currently implemented, will raise an error.

        **Material Unit**

        !!! warning
            Not currently implemented, will raise an error.

        **Masking Threshold**

        !!! warning
            Not currently implemented, will raise an error.

    """

    rows: list[FieldRow]
    used_keys: dict[str, bool]

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        rows: dict[str, dict[str, str | int]]
    ) -> Fields:
        """Set up the fields block.

        Parameters
        ----------
        rows : dict[str, dict[str, str | int]]
            Rows of temporal grid information.

        Returns
        -------
        Fields
            Fields block containing all rows.

        """
        converted_rows = [
            FieldRow.setup(name=name, **row) #type: ignore[ty:invalid-argument-type]
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

        Passes the block configuration into the "orfields.jinja" block
        template to get the appropriate configuration block.

        ``` jinja title="orfields.jinja"
        --8<-- "./src/enw/files/block_templates/orfields.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template("orfields.jinja")
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
        text = ["[Output Requirements - Fields]"]
        for row in self.rows:
            text.append(f"\t[[{row.name}]]")
            text.extend([
                f"\t\t{k:<30}: {v}"
                for k, v in row.__dict__.items()
                if k[0] != "_" and k != "name"
            ])
        return "\n".join(text)

@dataclass(kw_only=True)
class FieldRow:
    """A single row for the Output Requirements - Fields block."""

    name: str
    quantity: QuantityOpts
    species: str | None
    source: str | None
    h_grid: str | None
    z_grid: str | None
    t_grid: str
    bl_average: Switch | None
    t_av_or_int: TAvOrIntOpts
    av_time: TimeInterval | None
    num_av_times: int | None
    sync: Switch
    across: AcrossString | None
    separate_file: SeparateFileString | None
    output_format: OutputFormatStringF
    output_route: OutputRouteStringF
    output_group: str
    decay_deposition: NotImplementedType | None = None #Switch
    source_group: NotImplementedType | None = None #str
    s_grid: NotImplementedType | None = None #str
    h_coord: NotImplementedType | None = None #HorizontalCoordSystems
    z_coord: NotImplementedType | None = None #VerticalCoordSystems
    ensemble_av: NotImplementedType | None = None #Switch
    probabilities: NotImplementedType | None = None #str
    percentiles: NotImplementedType | None = None #str
    p_time: NotImplementedType | None = None #TimeInterval
    p_interval: NotImplementedType | None = None #TimeInterval
    ensemble_p: NotImplementedType | None = None #Switch
    fluctuations: NotImplementedType | None = None #Switch
    x_scale: NotImplementedType | None = None #float | int
    y_scale: NotImplementedType | None = None #float | int
    particle_size_distribution: NotImplementedType | None = None #str
    semi_infinite_approx: NotImplementedType | None = None #Switch
    material_unit: NotImplementedType | None = None #MaterialUnit
    masking_threshold: NotImplementedType | None = None #float | int

    @classmethod
    def setup(  #noqa: C901
        cls,
        *,
        name: str,
        quantity: str,
        t_grid: str,
        t_av_or_int: str,
        sync: bool,
        output_format: str,
        output_route: str,
        output_group: str,
        species: str | None = None,
        source: str | None = None,
        h_grid: str | None = None,
        z_grid: str | None = None,
        bl_average: bool | None = None,
        av_time: str | None = None,
        num_av_times: int | None = None,
        across: str | None = None,
        separate_file: str | None = None,
        decay_deposition: NotImplementedType | None = None, #Switch
        source_group: NotImplementedType | None = None, #str
        s_grid: NotImplementedType | None = None, #str
        h_coord: NotImplementedType | None = None, #HorizontalCoordSystems
        z_coord: NotImplementedType | None = None, #VerticalCoordSystems
        ensemble_av: NotImplementedType | None = None, #Switch
        probabilities: NotImplementedType | None = None, #str
        percentiles: NotImplementedType | None = None, #str
        p_time: NotImplementedType | None = None, #TimeInterval
        p_interval: NotImplementedType | None = None, #TimeInterval
        ensemble_p: NotImplementedType | None = None, #Switch
        fluctuations: NotImplementedType | None = None, #Switch
        x_scale: NotImplementedType | None = None, #float | int
        y_scale: NotImplementedType | None = None, #float | int
        particle_size_distribution: NotImplementedType | None = None, #str
        semi_infinite_approx: NotImplementedType | None = None, #Switch
        material_unit: NotImplementedType | None = None, #MaterialUnit
        masking_threshold: NotImplementedType | None = None, #float | int
    ) -> FieldRow:
        #INFO: I'm just ignoring C901 here because it'd be a massive hassle to
        # refactor
        """Configure a OR - Fields row with error checking and formatting.

        Parameters
        ----------
        name : str
            Name of the output requirement specification.

            Corresponds to **Name**.
        quantity : str
            Type of field required. Should be one of a list of options.
            (See `QuantityOpts`).

            Corresponds to **Quantity**
        decay_deposition : NotImplementedType | None, default=None
            **Not currently implemented.**

            Corresponds to **Decay Deposition?**
        species : str
            Species which the field corresponds to. Can be semicolon separated
            list.

            Corresponds to **Species**.
        source : str
            Source which the field corresponds to. If left blank, corresponds
            to all sources.

            Corresponds to **Source**.
        source_group : str
            Source group which the field corresponds to. If left blank,
            corresponds to all source groups.

            Corresponds to **Source Group**.
        h_grid : str
            Horizontal grid.

            Corresponds to **H_Grid**.
        z_grid : str
            Vertical grid.

            Corresponds to **Z-Grid**.
        t_grid : str
            Temporal grid.

            Corresponds to **T-Grid**.
        s_grid : NotImplementedType | None, default=None
            **Not currently implemented.**

            Corresponds to **S-Grid**.
        h_coord : NotImplementedType | None, default=None
            **Not currently implemented.**

            Corresponds to **H-Coord**.
        z_coord : NotImplementedType | None, default=None
            **Not currently implemented.**

            Corresponds to **Z-Coord**.
        bl_average : bool
            Average results over boundary layer depth?

            Corresponds to **BL Average?**.
        t_av_or_int : str
            Time averaging or integrating?

            Corresponds to **T Av Or Int**.
        av_time : str
            Averaging/Integration time.

            Corresponds to **Av Time**.
        num_av_times : int
            Number of instantaneous results used to form average.

            Corresponds to **# Av Times**.
        ensemble_av : NotImplementedType | None, default=None
            **Not currently implemented.**

            Corresponds to **Ensemble Av?**.
        probabilities : NotImplementedType | None, default=None
            **Not currently implemented.**

            Corresponds to **Probabilities**.
        percentiles : NotImplementedType | None, default=None
            **Not currently implemented.**

            Corresponds to **Percentiles**.
        p_time : NotImplementedType | None, default=None
            **Not currently implemented.**

            Corresponds to **P Time**.
        p_interval : NotImplementedType | None, default=None
            **Not currently implemented.**

            Corresponds to **p dT**.
        ensemble_p : NotImplementedType | None, default=None
            **Not currently implemented.**

            Corresponds to **Ensemble P?**.
        fluctuations : NotImplementedType | None, default=None
            **Not currently implemented.**

            Corresponds to **Fluctuations?**.
        sync : bool
            Calculate output when particles/puffs are synchronised?

            Corresponds to **Sync?**.
        x_scale : NotImplementedType | None, default=None
            **Not currently implemented.**

            Corresponds to **X Scale**.
        y_scale : NotImplementedType | None, default=None
            **Not currently implemented.**

            Corresponds to **Y Scale**.
        across : str
            Configuration of columns in output.

            Corresponds to **Across**.
        separate_file : str
            Which variables to separate.

            Corresponds to **Separate File**.
        output_format : str
            Format of the output file.

            Corresponds to **Output Format**.
        output_route : str
            How to save the output.

            Corresponds to **Output Route**.
        output_group : str
            Output with same group name is placed in same file.

            Corresponds to **Output Group**.
        particle_size_distribution : NotImplementedType | None, default=None
            **Not currently implemented.**

            Corresponds to **Particle Size Distribution**.
        semi_infinite_approx : NotImplementedType | None, default=None
            **Not currently implemented.**

            Corresponds to **Semi-Infinite Approx?**.
        material_unit : NotImplementedType | None, default=None
            **Not currently implemented.**

            Corresponds to **Material Unit**.
        masking_threshold : NotImplementedType | None, default=None
            **Not currently implemented.**

            Corresponds to **Masking Threshold**.

        Raises
        ------
        NotImplementedError
            A key that isn't implemented yet has a value other than None.

        Returns
        -------
        FieldRow
            Representation of a single row of the OR - Fields block.

        """
        _unimplemented = (
            ("decay_deposition", decay_deposition),
            ("source_group", source_group),
            ("s_grid", s_grid),
            ("h_coord", h_coord),
            ("z_coord", z_coord),
            ("ensemble_av", ensemble_av),
            ("probabilities", probabilities),
            ("percentiles", percentiles),
            ("p_time", p_time),
            ("p_interval", p_interval),
            ("ensemble_p", ensemble_p),
            ("fluctuations", fluctuations),
            ("x_scale", x_scale),
            ("y_scale", y_scale),
            ("particle_size_distribution", particle_size_distribution),
            ("semi_infinite_approx", semi_infinite_approx),
            ("material_unit", material_unit),
            ("masking_threshold", masking_threshold)
        )
        #INFO: Check name
        check_type(f"{name}.name", name, str)
        #INFO: Check quantity
        check_type(f"{name}.quantity", quantity, str)
        check_literal(
            f"{name}.quantity",
            quantity,
            "QuantityOpts",
            QuantityOpts
        )
        formatted_quantity = cast("QuantityOpts", quantity)
        #INFO: Check species
        if species is not None:
            check_type(f"{name}.species", species, str)
        #INFO: Check source
        if source is not None:
            check_type(f"{name}.source", source, str)
        #INFO: Check h_grid
        if h_grid is not None:
            check_type(f"{name}.h_grid", h_grid, str)
        #INFO: Check z_grid
        if z_grid is not None:
            check_type(f"{name}.z_grid", z_grid, str)
        #INFO: Check t_grid
        check_type(f"{name}.t_grid", t_grid, str)
        #INFO: Check bl_average
        formatted_bl_average = None
        if bl_average is not None:
            check_type(f"{name}.bl_average", bl_average, bool)
            formatted_bl_average = make_switch(bl_average)
        #INFO: Check t_av_or_int
        check_type(f"{name}.t_av_or_int", t_av_or_int, str)
        check_literal(
            f"{name}.t_av_or_int",
            t_av_or_int,
            "TAvOrIntOpts",
            TAvOrIntOpts
        )
        formatted_t_av_or_int = cast("TAvOrIntOpts", t_av_or_int)
        #INFO: Check av_time
        formatted_av_time = None
        if av_time is not None:
            check_type(f"{name}.av_time", av_time, str)
            check_time_interval(f"{name}.av_time", av_time)
            formatted_av_time = make_time_interval(av_time)
        #INFO: Check num_av_times
        if num_av_times is not None:
            check_type(f"{name}.num_av_times", num_av_times, int)
        #INFO: Check sync
        check_type(f"{name}.sync", sync, bool)
        formatted_sync = make_switch(sync)
        #INFO: Check across
        formatted_across = None
        if across is not None:
            check_type(f"{name}.across", across, str)
            check_output_string_fields(f"{name}.across", across, "across")
            formatted_across = AcrossString(across)
        #INFO: Check separate_file
        formatted_separate_file = None
        if separate_file is not None:
            check_type(f"{name}.separate_file", separate_file, str)
            check_output_string_fields(
                f"{name}.separate_file",
                separate_file,
                "separate_file"
            )
            formatted_separate_file = SeparateFileString(separate_file)
        #INFO: Check output_format
        check_type(f"{name}.output_format", output_format, str)
        check_output_string_fields(
            f"{name}.output_format",
            output_format,
            "output_format"
        )
        formatted_output_format = OutputFormatStringF(output_format)
        #INFO: Check output_route
        check_type(f"{name}.output_route", output_route, str)
        check_output_string_fields(
            f"{name}.output_route",
            output_route,
            "output_route"
        )
        formatted_output_route = OutputRouteStringF(output_route)
        #INFO: Check output_group
        check_type(f"{name}.output_group", output_group, str)

        for k, v in _unimplemented:
            msg = (
                f"{k} was specified but is not implemented for "
                "Output Requirements - Fields."
            )
            if v is not None:
                raise NotImplementedError(msg)

        return cls(
            name = name,
            quantity = formatted_quantity,
            species = species,
            source = source,
            h_grid = h_grid,
            z_grid = z_grid,
            t_grid = t_grid,
            bl_average = formatted_bl_average,
            t_av_or_int = formatted_t_av_or_int,
            av_time = formatted_av_time,
            num_av_times = num_av_times,
            sync = formatted_sync,
            across = formatted_across,
            separate_file = formatted_separate_file,
            output_format = formatted_output_format,
            output_route = formatted_output_route,
            output_group = output_group,
    )


@dataclass(kw_only=True)
class PPInfo(NAMEIIIHeaderInputBlock):
    """Config for the OR - Sets of Particle/Puff Info block for NAME III.

    `Output Requirements - Sets of Particle/Puff Information` has the following
    columns:

    ??? information Columns
        **Output Name**

        Name used for the output requirement.

        _Accepted Values_

        String.

        **Particles?**

        Include particle information in output?

        _Accepted Values_

        `Yes` or `No`.

        **Puffs?**

        Include puff information in output?

        _Accepted Values_

        `Yes` or `No`.

        **First Particle**

        First particle from each source to be included.

        _Accepted Values_

        Any integer greater than or equal to 0.

        **Last Particle**

        Last particle from each source to be included.

        _Accepted Values_

        Any integer greater than or equal to 0.

        **First Puff**

        First puff from each source to be included.

        _Accepted Values_

        Any integer greater than or equal to 0.

        **Last Puff**

        Last puff from each source to be included.

        _Accepted Values_

        Any integer greater than or equal to 0.

        **Source**

        Restrict output to this source, or use all sources if blank.

        _Accepted Values_

        Name of a source, or blank.

        **Met?**

        Include information on met?

        _Accepted Values_

        `Yes` or `No`.

        **Mass?**

        Include information on mass?

        _Accepted Values_

        `Yes` or `No`.

        **Plume Rise?**

        Include information on plume rise?

        _Accepted Values_

        `Yes` or `No`.

        **Dispersion Scheme?**

        Include information on dispersion scheme?

        _Accepted Values_

        `Yes` or `No`.

        **Puff Family?**

        Include information on puff family? (Puffs only)

        _Accepted Values_

        `Yes` or `No`.

        **Fate Info?**

        Include information on the particle or puff fate?

        _Accepted Values_

        `Yes` or `No`.

        **H-Coord**

        Horizontal coordinate system.

        _Accepted Values_

        Previously defined horizontal coordinate system.

        **Z-Coord**

        Vertical coordinate system.

        _Accepted Values_

        Previously defined vertical coordinate system.

        **T-Grid**

        Temporal grid.

        _Accepted Values_

        Previously defined temporal grid.

        **Sync?**

        Calculate output when particle/puffs are synchronised.

        _Accepted Values_

        `Yes` or `No`.

        **Output Format**

        A string of characters defining output file format.

        _Accepted Values_

        |Character|Description|
        |---------|-----------|
        |T|Separate time in separate files|
        |P|Separate particles in separate files|
        |F|Flush buffer after each sync time interval|

        **Output Route**

        A string of characters defining output route.

        _Accepted Values_

        |Character|Description|
        |---------|-----------|
        |D|Numerical output to disk|
        |S|Numerical output to screen|

    """

    rows: list[PPInfoRow]
    used_keys: dict[str, bool]

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        rows: dict[str, dict[str, str | int]]
    ) -> PPInfo:
        """Set up the fields block.

        Parameters
        ----------
        rows : dict[str, dict[str, str | int]]
            Rows of temporal grid information.

        Returns
        -------
        Fields
            Fields block containing all rows.

        """
        converted_rows = [
            PPInfoRow.setup(name=name, **row) #type: ignore[ty:invalid-argument-type]
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

        Passes the block configuration into the "orppinfo.jinja" block
        template to get the appropriate configuration block.

        ``` jinja title="orppinfo.jinja"
        --8<-- "./src/enw/files/block_templates/orppinfo.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template("orppinfo.jinja")
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
        text = ["[Output Requirements - Sets of Particle/Puff Information]"]
        for row in self.rows:
            text.append(f"\t[[{row.name}]]")
            text.extend([
                f"\t\t{k:<20}: {v}"
                for k, v in row.__dict__.items()
                if k[0] != "_" and k != "name"
            ])
        return "\n".join(text)

@dataclass(kw_only=True)
class PPInfoRow:
    """A single row for the Output Requirements - Set of P/P Info block."""

    name: str
    particles: Switch
    puffs: Switch
    first_particle: NotImplementedType | None = None #int | None
    last_particle: NotImplementedType | None = None #int | None
    first_puff: NotImplementedType | None = None #int | None
    last_puff: NotImplementedType | None = None #int | None
    source: NotImplementedType | None = None #str | None
    met: Switch
    mass: Switch
    plume_rise: Switch
    dispersion_scheme: Switch
    puff_family: Switch
    fate_info: Switch
    h_coord: HorizontalCoordSystems
    z_coord: VerticalCoordSystems
    t_grid: NotImplementedType | None = None #str | None
    sync: Switch
    output_format: NotImplementedType | None = None
    output_route: OutputRouteStringPP

    @classmethod
    def setup(
        cls,
        *,
        name: str,
        particles: bool,
        puffs: bool,
        met: bool,
        mass: bool,
        plume_rise: bool,
        dispersion_scheme: bool,
        puff_family: bool,
        fate_info: bool,
        h_coord: str,
        z_coord: str,
        sync: bool,
        output_route: str,
        first_particle: None = None,
        last_particle: None = None,
        first_puff: None = None,
        last_puff: None = None,
        source: None = None,
        t_grid: None = None,
        output_format: None = None
    ) -> PPInfoRow:
        """Configure a OR - PP Info row with type checking.

        Parameters
        ----------
        name : str
            Name of the output requirement.

            Corresponds to **Output Name**.
        particles : bool
            Include the particle puff information in the output?

            Corresponds to **Particles?**.
        puffs : bool
            Include the puff information in the output?

            Corresponds to **Puffs?**.
        met : bool
            Include information on the met?

            Corresponds to **Met?**.
        mass : bool
            Include information on mass?

            Corresponds to **Mass?**.
        plume_rise : bool
            Include information on plume rise?

            Corresponds to **Plume Rise?**
        dispersion_scheme : bool
            Include information on dispersion scheme?

            Corresponds to **Dispersion Scheme?**
        puff_family : bool
            Include information on puff family?

            Corresponds to **Puff Family?**.
        fate_info : bool
            Include information on particle/puff fate?

            Corresponds to **Fate Info?**.
        h_coord : str
            Horizontal coordinate system.

            Corresponds to **H-Coord**.
        z_coord : str
            Vertical coordinate system.

            Corresponds to **Z-Coord**.
        sync : bool
            Calculate output when particles/puffs are synchronised?

            Corresponds to **Sync?**.
        output_route : str
            String of characters defining output route.

            Corresponds to **Output Route**.
        first_particle : None = None
            Not currently implemented.

            Corresponds to **First Particle**.
        last_particle : None = None
            Not currently implemented.

            Corresponds to **Last Particle**.
        first_puff : None = None
            Not currently implemented.

            Corresponds to **First Puff**.
        last_puff : None = None
            Not currently implemented.

            Corresponds to **Last Puff**.
        source : None = None
            Not currently implemented.

            Corresponds to **Source**.
        t_grid : None = None
            Not currently implemented.

            Corresponds to **T-Grid**.
        output_format : None = None
            Not currently implemented.

            Corresponds to **Output Format**.

        Returns
        -------
        PPInfoRow
            Single row of `OR - Sets of Particle/Puff Information`

        Raises
        ------
        NotImplementedError
            Unimplemented argument is used.

        """
        _unimplemented = (
            ("first_particle", first_particle),
            ("last_particle", last_particle),
            ("first_puff", first_puff),
            ("last_puff", last_puff),
            ("source", source),
            ("t_grid", t_grid),
            ("output_format", output_format)
        )
        #INFO: Check name
        check_type(f"{name}.name", name, str)
        #INFO: Check particles
        check_type(f"{name}.particles", particles, bool)
        formatted_particles = make_switch(particles)
        #INFO: Check puffs
        check_type(f"{name}.puffs", puffs, bool)
        formatted_puffs = make_switch(puffs)
        #INFO: Check met
        check_type(f"{name}.met", met, bool)
        formatted_met = make_switch(met)
        #INFO: Check mass
        check_type(f"{name}.mass", mass, bool)
        formatted_mass = make_switch(mass)
        #INFO: Check plume_rise
        check_type(f"{name}.plume_rise", plume_rise, bool)
        formatted_plume_rise = make_switch(plume_rise)
        #INFO: Check dispersion_scheme
        check_type(f"{name}.dispersion_scheme", dispersion_scheme, bool)
        formatted_dispersion_scheme = make_switch(dispersion_scheme)
        #INFO: Check puff_family
        check_type(f"{name}.puff_family", puff_family, bool)
        formatted_puff_family = make_switch(puff_family)
        #INFO: Check fate_info
        check_type(f"{name}.fate_info", fate_info, bool)
        formatted_fate_info = make_switch(fate_info)
        #INFO: Check h_coord
        check_literal(
            f"{name}.h_coord",
            h_coord,
            "HorizontalCoordSystems",
            HorizontalCoordSystems
        )
        formatted_h_coord = cast("HorizontalCoordSystems", h_coord)
        #INFO: Check z_coord
        check_literal(
            f"{name}.z_coord",
            z_coord,
            "VerticalCoordSystems",
            VerticalCoordSystems
        )
        formatted_z_coord = cast("VerticalCoordSystems", z_coord)
        #INFO: Check sync
        check_type(f"{name}.sync", sync, bool)
        formatted_sync = make_switch(sync)
        #INFO: Check output_route
        check_type(f"{name}.output_route", output_route, str)
        check_output_string_pp(
            f"{name}.output_route",
            output_route,
            "output_route"
        )
        formatted_output_route = OutputRouteStringPP(output_route)

        for k, v in _unimplemented:
            msg = (
                f"{k} was specified but is not implemented for "
                "Output Requirements - Sets of PP Info."
            )
            if v is not None:
                raise NotImplementedError(msg)

        return cls(
            name=name,
            particles=formatted_particles,
            puffs=formatted_puffs,
            met=formatted_met,
            mass=formatted_mass,
            plume_rise=formatted_plume_rise,
            dispersion_scheme=formatted_dispersion_scheme,
            puff_family=formatted_puff_family,
            fate_info=formatted_fate_info,
            h_coord=formatted_h_coord,
            z_coord=formatted_z_coord,
            sync=formatted_sync,
            output_route=formatted_output_route
        )
