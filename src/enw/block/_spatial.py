"""Configuration objects for all of the spatial NAME III Input Header Blocks.

Covers:

- Horizontal Coordinate Systems: `HorizontalCoords`
- Vertical Coordinate Systems: `VerticalCoords`
- Locations: `Locations`
- Horizontal Grids: `HorizontalGrids`
- Vertical Grids: `VerticalGrids`
- Domains: `Domains`

"""
from dataclasses import dataclass
from typing import cast, TYPE_CHECKING

from enw.types import (
    HorizontalCoordSystems,
    VerticalCoordSystems,
    Switch,
    TimeInterval,
)
from enw.utils import (
    check_literal,
    check_type,
    check_pos_float,
    check_pos_int,
    check_mutually_exclusive,
    make_switch,
    make_datetime,
    make_time_interval,
    parse_time_string
)

from ._base import NAMEIIIHeaderInputBlock

if TYPE_CHECKING:
    from enw.types import DateTime, DomainTimeBlock


@dataclass(kw_only=True)
class HorizontalCoords(NAMEIIIHeaderInputBlock):
    """Configuration for the Horizontal Coordinate Systems block for NAME III.

    This configures the horizontal coordinate systems used in NAME. Though this
    can be fully customised, for now it only accepts a predefined system
    from the following list:

    - "Lat-Long"
    - "EMEP 50km Grid"
    - "EMEP 150km Grid"
    - "UK National Grid (m)"
    - "UK National Grid (100m)"

    The `Horizontal Coordinate Systems` block currently contains a single
    column:

    **Name**

    The name of the grid.

    _Accepted Values_

    - "Lat-Long"
    - "EMEP 50km Grid"
    - "EMEP 150km Grid"
    - "UK National Grid (m)"
    - "UK National Grid (100m)"

    !!! warning
        If required, the ability to use custom coordinate systems can be added
        in the future.

    """

    names: tuple[HorizontalCoordSystems, ...]

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        names: list[str]
    ) -> HorizontalCoords:
        """Configure a config block with error checking and formatting.

        Parameters
        ----------
        names : list[str]
            The names of the coordinate systems.

        """
        for i, n in enumerate(names):
            check_literal(
                f"names index {i}",
                n,
                "HorizontalCoordSystems",
                HorizontalCoordSystems
            )
        return cls(
            names=tuple(cast("HorizontalCoordSystems", n) for n in names)
        )

    def __str__(self) -> str:
        """Return the configuration block for the NAME input header file.

        Passes the block configuration into the "hcoords.jinja" block
        template to get the appropriate configuration block.

        ``` jinja title="hcoords.jinja"
        --8<-- "./src/enw/files/block_templates/hcoords.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template("hcoords.jinja")
        return template.render(
            names=self.names
        )

    def __repr__(self) -> str:
        """Return representation of object to print to console.

        Returns
        -------
        str
            Representation of object.

        """
        return "\n".join(
            [
                "[Horizontal Coordinate Systems]"
            ] + [
                    f"\t{n}"
                    for n in self.names
            ]
        )


@dataclass(kw_only=True)
class VerticalCoords(NAMEIIIHeaderInputBlock):
    """Configuration for the Vertical Coordinate Systems block for NAME III.

    This configures the horizontal coordinate systems used in NAME. Though this
    can be fully customised, for now it only accepts a predefined system
    from the following list:

    - "m agl"
    - "m asl"
    - "FL"
    - "Pa"

    The `Vertical Coordinate Systems` block currently contains a single
    column:

    **Name**

    The name of the grid.

    _Accepted Values_

    - "m agl"
    - "m asl"
    - "FL"
    - "Pa"

    !!! warning
        If required, the ability to use custom coordinate systems can be added
        in the future.

    """

    names: tuple[VerticalCoordSystems, ...]

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        names: list[str]
    ) -> VerticalCoords:
        """Configure a config block with error checking and formatting.

        Parameters
        ----------
        names : list[str]
            The names of the coordinate systems.

        """
        for i, n in enumerate(names):
            check_literal(
                f"names index {i}",
                n,
                "VerticalCoordSystems",
                VerticalCoordSystems
            )
        return cls(
            names=tuple(cast("VerticalCoordSystems", n) for n in names)
        )

    def __str__(self) -> str:
        """Return the configuration block for the NAME input header file.

        Passes the block configuration into the "vcoords.jinja" block
        template to get the appropriate configuration block.

        ``` jinja title="vcoords.jinja"
        --8<-- "./src/enw/files/block_templates/vcoords.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template("vcoords.jinja")
        return template.render(
            names=self.names
        )

    def __repr__(self) -> str:
        """Return representation of object to print to console.

        Returns
        -------
        str
            Representation of object.

        """
        return "\n".join(
            [
                "[Vertical Coordinate Systems]"
            ] + [
                    f"\t{n}"
                    for n in self.names
            ]
        )


@dataclass(kw_only=True)
class Locations(NAMEIIIHeaderInputBlock):
    """Configuration for the Locations block for NAME III.

    The `Locations` block contains the following columns:

    **Name**

    The name of the location.

    _Accepted Values_

    Any valid string.

    **H-Coord**

    Coordinate system to be used for locations.

    _Accepted Values_

    Any horizontal coordinate system specified in the `Horizontal Coordinate
    Systems` block.

    **X**

    X coordinate representation of the location.

    _Accepted Values_

    Any float value lying within the x axis of the domain.

    **Y**

    Y coordinate representation of the location.

    _Accepted Values_

    Any float value lying within the y axis of the domain.

    """

    rows: tuple[LocationRow, ...]
    block_name: str

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        rows: dict[str, dict[str, float | str]],
        block_name: str
    ) -> Locations:
        """Configure a config block with error checking and formatting.

        Parameters
        ----------
        rows : dict[str, dict[str, float | str]]
            The names of the coordinate systems. The key represents **Name**,
            the value is a dict containing keys for "H-Coord", "X" and "Y":
            - "hcoord": **H-Coord**
            - "x": **X**
            - "y": **Y**
        block_name : str
            The name of the locations block

        """
        if not len(rows):
            msg = "No rows provided for locations block."
            raise ValueError(msg)
        for location, data in rows.items():
            #INFO: Check name
            check_type(f"{location}: name", location, str)
            #INFO: Check HCoord
            check_literal(
                f"{location}: hcoord",
                str(data["hcoord"]),
                "HorizontalCoordSystems",
                HorizontalCoordSystems
            )
            #INFO: Check X
            check_type(f"{location}: x", data["x"], (int, float))
            #INFO: Check Y
            check_type(f"{location}: y", data["y"], (int, float))
        #INFO: Check block name
        check_type("block_name", block_name, str)
        return cls(
            rows=tuple(
                LocationRow(
                    name=k,
                    hcoord=str(v["hcoord"]),
                    x=float(v["x"]),
                    y=float(v["y"]),
                ) for k, v in rows.items()
            ),
            block_name=block_name
        )

    def __str__(self) -> str:
        """Return the configuration block for the NAME input header file.

        Passes the block configuration into the "locations.jinja" block
        template to get the appropriate configuration block.

        ``` jinja title="locations.jinja"
        --8<-- "./src/enw/files/block_templates/locations.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template("locations.jinja")
        return template.render(
            rows=[d.__dict__ for d in self.rows],
            block_name=self.block_name
        )

    def __repr__(self) -> str:
        """Return representation of object to print to console.

        Returns
        -------
        str
            Representation of object.

        """
        parts = ["[Locations]"]
        for row in self.rows:
            parts.extend([
                f"\t[[{row.name}]]",
                f"\t\thcoord = {row.hcoord}",
                f"\t\tx      = {row.x}",
                f"\t\ty      = {row.y}",
            ])
        return "\n".join(parts)


@dataclass(kw_only=True)
class LocationRow:
    """A single row in the locations block."""

    name: str
    hcoord: str
    x: float
    y: float


@dataclass(kw_only=True)
class HorizontalGrids(NAMEIIIHeaderInputBlock):
    """Configuration for the Horizontal Grids block for NAME III.

    The `Horizontal Grids` block contains the following columns:
    ??? information "Columns"
        **Name**

        The name of the location.

        _Accepted Values_

        Any valid string.

        **H-Coord**

        Coordinate system to be used for locations.

        _Accepted Values_

        Any horizontal coordinate system specified in the `Horizontal
        Coordinate Systems` block.

        **nX**

        The number of grid points in the x direction.

        _Accepted Values_

        Any positive integer value.

        **nY**

        The number of grid points in the y direction.

        _Accepted Values_

        Any positive integer value.

        **dX**

        Grid spacing in the x direction.

        _Accepted Values_

        Any positive float value.

        **dY**

        Grid spacing in the y direction.

        _Accepted Values_

        Any positive float value.

        **X Min**

        X coordinate of the first grid point.

        _Accepted Values_

        Any float value.

        **X Max**

        X coordinate of the last grid point.

        _Accepted Values_

        Any float value.

        **X Centre**

        X coordinate of grid centre.

        _Accepted Values_

        Any float value.

        **X Range**

        Span of X coordinates (X Max - X Min)

        _Accepted Values_

        Any float value.

        **X Array**

        Name of the array giving the X coordinates of the grid.

        _Accepted Values_

        Name of any user defined array containing a series of float values.

        **Y Min**

        Y coordinate of the first grid point.

        _Accepted Values_

        Any float value.

        **Y Max**

        Y coordinate of the last grid point.

        _Accepted Values_

        Any float value.

        **Y Centre**

        Y coordinate of grid centre.

        _Accepted Values_

        Any float value.

        **Y Range**

        Span of Y coordinates (Y Max - Y Min)

        _Accepted Values_

        Any float value.

        **Y Array**

        Name of the array giving the Y coordinates of the grid.

        _Accepted Values_

        Name of any user defined array containing a series of float values.

        !!! warning "Extra Parameters"
            **Wrap**, **Set of locations** and **Location of centre** aren't
            currently accepted.

    The following combinations of keys are available:

    ??? example "A) Structured Grid i"
        - **H-Coord**
        - **nX**
        - **nY**
        - ==**TWO**== of
            - **X Min**
            - **X Max**
            - **X Centre**
            - **dX**, _mutually exclusive with **X Range**_
            - **X Range**, _mutually exclusive with **dX**_
        - ==**TWO**== of
            - **Y Min**
            - **Y Max**
            - **Y Centre**
            - **dY**, _mutually exclusive with **Y Range**_
            - **Y Range**, _mutually exclusive with **dY**_

    ??? example "B) Structured Grid ii"
        !!! warning
            **Set of locations** and **Location of centre** currently not
            implemented so this is not currently possible.

    ??? example "C) Irregularly Spaced Grid"
        !!! warning
            Arrays aren't fully implemented so this is not currently
            possible.

    ??? example "D) Unstructured Grid"
        !!! warning
            **Set of locations** isn't fully implemented so this won't
            work.

    """

    name: str
    hcoord: HorizontalCoordSystems
    x_count: int | None = None
    x_spacing: float | None = None
    x_min: float | None = None
    x_max: float | None = None
    x_centre: float | None = None
    x_range: float | None = None
    x_array: str | None = None
    y_count: int | None = None
    y_spacing: float | None = None
    y_min: float | None = None
    y_max: float | None = None
    y_centre: float | None = None
    y_range: float | None = None
    y_array: str | None = None

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        name: str,
        hcoord: str,
        x: dict[str, str | int | float | None],
        y: dict[str, str | int |  float | None]
    ) -> HorizontalGrids:
        """Configure a config block with error checking and formatting.

        Parameters
        ----------
        name : str
            Name of the grid.

            Corresponds to **Name**.

        hcoord : str
            Horizontal coordinate system to use when defining the grid.

            Corresponds to **H-Coord**.

        x : dict[str, str | int | float | None]
            Configuration for x axes, potentially containing one or more of
            the following keys:

            - "count" (int): Corresponds to **nX**
            - "spacing" (float): Corresponds to **dX**
            - "min" (float): Corresponds to **X Min**
            - "max" (float): Corresponds to **X Max**
            - "centre" (float): Corresponds to **X Centre**
            - "range" (float): Corresponds to **X Range**
            - "array" (str): Corresponds to **X Array**

            !!! information
                Valid combinations of keys can be found above.

        y : dict[str, str | float | int | None]
            Configuration for y axes, potentially containing one or more of
            the following keys:

            - "count" (int): Corresponds to **nY**
            - "spacing" (float): Corresponds to **dY**
            - "min" (float): Corresponds to **Y Min**
            - "max" (float): Corresponds to **Y Max**
            - "centre" (float): Corresponds to **Y Centre**
            - "range" (float): Corresponds to **Y Range**
            - "array" (str): Corresponds to **Y Array**

            !!! information
                Valid combinations of keys can be found above.

        """
        #INFO: Check name
        check_type("name", name, str)
        #INFO: Check hcoord
        check_literal(
            "hcoord",
            hcoord,
            "HorizontalCoordSystems",
            HorizontalCoordSystems
        )
        cls.check_axis("x", x)
        cls.check_axis("y", y)

        return cls(
            name=name,
            hcoord=cast("HorizontalCoordSystems", hcoord),
            **{f"x_{k}": v for k, v in x.items()},  #type: ignore[ty:invalid-argument-type]
            **{f"y_{k}": v for k, v in y.items()}
        )


    @classmethod
    def check_axis(
        cls,
        name: str,
        vals: dict[str, str | float | int | None],
    ) -> None:
        """Check the configuration of the X and Y axis.

        Parameters
        ----------
        name : str
            The name of the axis.
        vals : dict[str, str | float | int | None]
            The configuration of the specified axis.

        Raises
        ------
        ValueError
            - Unexpected keys
            - Incorrect number of configuration variables.
            - Mutually exclusive configuration variables specified.
            - Incorrect types for configuration variables.

        """
        expected_keys: set[str] = {
            "count",
            "spacing",
            "min",
            "max",
            "centre",
            "range",
            "array"
        }
        #INFO: Check max 3 values in vals
        #TODO: This needs more work when the other options are available
        if len(vals) != 3:
            msg = (
                f"Incorrect number of values provided for {name}."
                "Expected 3, including count."
            )
            raise ValueError(msg)
        #INFO: Check all vals keys are expected
        vals_extra_keys = set(vals.keys()) - expected_keys
        if vals_extra_keys:
            msg = f"Unexpected keys in {name}: {vals_extra_keys}"
            raise ValueError(msg)
        #INFO: Check vals.count
        if "count" in vals:
            check_type(f"{name}.count", vals["count"], int)
            check_pos_int(f"{name}.count", cast("int", vals["count"]))
        #INFO: Check vals.spacing
        if "spacing" in vals:
            check_type(f"{name}.spacing", vals["spacing"], (float, int))
            check_pos_float(f"{name}.spacing", cast("float", vals["spacing"]))
            check_mutually_exclusive(
                f"{name}.spacing",
                vals["spacing"],
                f"{name}.range",
                vals.get("range")
            )
        #INFO: Check vals.min
        if "min" in vals:
            check_type(f"{name}.min", vals["min"], (float, int))
        #INFO: Check vals.max
        if "max" in vals:
            check_type(f"{name}.max", vals["max"], (float, int))
        #INFO: Check vals.centre
        if "centre" in vals:
            check_type(f"{name}.centre", vals["centre"], (float, int))
        #INFO: Check vals.range
        if "range" in vals:
            check_type(f"{name}.range", vals["range"], (float, int))
            check_pos_float(f"{name}.range", cast("float", vals["range"]))
        #INFO: Check vals.array
        if "array" in vals:
            msg = "Array not implemented for HorizontalGrids."
            raise NotImplementedError(msg)
            # check_type(f"{name}.array", vals["array"], str)

    def __str__(self) -> str:
        """Return the configuration block for the NAME input header file.

        Passes the block configuration into the "hgrids.jinja" block
        template to get the appropriate configuration block.

        ``` jinja title="hgrids.jinja"
        --8<-- "./src/enw/files/block_templates/hgrids.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template("hgrids.jinja")
        return template.render(
            name=self.name,
            hcoord=self.hcoord,
            x_count=self.x_count,
            x_spacing=self.x_spacing,
            x_min=self.x_min,
            x_max=self.x_max,
            x_centre=self.x_centre,
            x_range=self.x_range,
            x_array=self.x_array,
            y_count=self.y_count,
            y_spacing=self.y_spacing,
            y_min=self.y_min,
            y_max=self.y_max,
            y_centre=self.y_centre,
            y_range=self.y_range,
            y_array=self.y_array
        )

    def __repr__(self) -> str:
        """Return representation of object to print to console.

        Returns
        -------
        str
            Representation of object.

        """
        return "\n".join([
            "[Horizontal Grids]",
        ] + [
            f"\t{k:<20}: {v}"
            for k, v in self.__dict__.items()
            if k[0] != "_"
        ])


@dataclass(kw_only=True)
class VerticalGrids(NAMEIIIHeaderInputBlock):
    """Configuration for the Vertical Grids block for NAME III.

    The `Vertical Grids` block contains the following columns:
    ??? information "Columns"
        **Name**

        The name of the location.

        _Accepted Values_

        Any valid string.

        **Z-Coord**

        Coordinate system to be used for height.

        _Accepted Values_

        Any vertical coordinate system specified in the `Vertical
        Coordinate Systems` block.

        **nZ**

        Number of vertical grid points.

        _Accepted Values_

        Any positive integer value.

        **dZ**

        How far apart the points should be spaced.

        _Accepted Values_

        Any positive float value.

        **Z0**

        Smallest value for vertical coordinate in grid.

        _Accepted Values_

        Any float value.

        **Z-Array**

        Name of the array giving the height (Z) of the grid points, with
        each entry in the array corresponding to a single grid point.

        _Accepted Values_

        | Option | Result |
        |--------|--------|
        |Name of array|Explicit heights for each grid point|
        |`Use Eta Levels`|Levels used when defining pressure based coord \
        system are also grid levels|

        **Av Z-Array**

        Name of the array giving the depth (dZ) of an explicit averaging region
        associated with each grid point.

        _Accepted Values_

        | Option | Result |
        |--------|--------|
        |Name of array|Explicit depths of averaging regions for each grid \
        point|
        |`Z On Boundaries`|**Z-Array** defines the boundaries of the averaging\
        regions|

        **Index-Array**

        Give the different levels indices other than the default 1,2,3 etc.

        _Accepted Values_

        n Positive integers where n is the size of **Z-Array**.

    The following combinations of keys are available:

    ??? example "A)"
        - **nZ**
        - **Z0**
        - **dZ**

    ??? example "B)"
        - **Z-Array** = `Use Eta Levels`
        !!! warning
            Custom coord systems aren't fully implemented so this is not
            currently possible.

    ??? example "C)"
        - **Z-Array** = A valid array name
        !!! warning
            Arrays aren't fully implemented so this is not currently
            possible.

    ??? example "D)"
        - **Z-Array** = A valid array name
        - **Av Z-Array** = `Z On Boundaries`
        !!! warning
            Arrays aren't fully implemented so this is not currently
            possible.

    ??? example "E)"
        - **Z-Array** = A valid array name
        - **Av Z-Array** = A valid array name
        !!! warning
            Arrays aren't fully implemented so this is not currently
            possible.

    """

    name: str
    zcoord: VerticalCoordSystems
    count: int | None
    spacing: float | None
    min_point: float | None
    array_name: str | None
    av_array_name: str | None
    index_array_name: str | None

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        name: str,
        zcoord: VerticalCoordSystems,
        count: int | None = None,
        spacing: float | None = None,
        min_point: float | None = None,
        array_name: str | None = None,
        av_array_name: str | None = None,
        index_array_name: str | None = None
    ) -> VerticalGrids:
        """Configure a config block with error checking and formatting.

        Parameters
        ----------
        name : str
            Name of the grid.

            Corresponds to **Name**.

        zcoord : str
            Vertical coordinate system to use when defining the grid.

            Corresponds to **Z-Coord**.

        count : int | None
            Number of vertical grid points.

            Corresponds to **nZ**.

        spacing : float | None
            Spacing between grid points.

            Corresponds to **dZ**.

        min_point : float | None
            Smallest Z coordinate.

            Corresponds to **Z0**.

        array_name : str | None
            Name of array giving heights (Z) of grid points.

            Corresponds to **Z-Array**.

        av_array_name : str | None
            Name of array giving depths (dZ) of averaging at grid points.

            Corresponds to **Z-Array**.

        index_array_name : str | None
            Name of array giving custom indices of grid points.

            Corresponds to **Z-Array**.


        """
        #INFO: Check name
        check_type("name", name, str)
        #INFO: Check zcoord
        check_literal(
            "zcoord",
            zcoord,
            "VerticalCoordSystems",
            VerticalCoordSystems
        )
        #TODO: Item count?
        #INFO: Check count
        if count is not None:
            check_type("count", count, (float, int))
            check_pos_int("count", count)
        #INFO: Check spacing
        if spacing is not None:
            check_type("spacing", spacing, (float, int))
            check_pos_float("spacing", spacing)
        #INFO: Check min_point
        if min_point is not None:
            check_type("min_point", min_point, (float, int))
        #INFO: Check array_name
        if array_name is not None:
            msg = "Array not implemented for VerticalGrids."
            raise NotImplementedError(msg)
            # check_type("array_name", array_name, str)
        #INFO: Check av_array_name
        if av_array_name is not None:
            msg = "Array not implemented for VerticalGrids."
            raise NotImplementedError(msg)
            # check_type("av_array_name", av_array_name, str)
        #INFO: Check index_array_name
        if index_array_name is not None:
            msg = "Array not implemented for VerticalGrids."
            raise NotImplementedError(msg)
            # check_type("index_array_name", index_array_name, str)

        return cls(
            name=name,
            zcoord=zcoord,
            count=count,
            spacing=spacing,
            min_point=min_point,
            array_name=array_name,
            av_array_name=av_array_name,
            index_array_name=index_array_name
        )

    def __str__(self) -> str:
        """Return the configuration block for the NAME input header file.

        Passes the block configuration into the "vgrids.jinja" block
        template to get the appropriate configuration block.

        ``` jinja title="vgrids.jinja"
        --8<-- "./src/enw/files/block_templates/vgrids.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template("vgrids.jinja")
        return template.render(
            name=self.name,
            zcoord=self.zcoord,
            count=self.count,
            spacing=self.spacing,
            min_point=self.min_point,
            array_name=self.array_name,
            av_array_name=self.av_array_name,
            index_array_name=self.index_array_name
        )

    def __repr__(self) -> str:
        """Return representation of object to print to console.

        Returns
        -------
        str
            Representation of object.

        """
        return "\n".join([
            "[Vertical Grids]",
        ] + [
            f"\t{k:<20}: {v}"
            for k, v in self.__dict__.items()
            if k[0] != "_"
        ])


@dataclass(kw_only=True)
class Domains(NAMEIIIHeaderInputBlock):
    """Configuration for the Domains block for NAME III.

    The `Domains` block contains the following columns:
    ??? information "Columns"
        **Name**

        The name of the domain.

        _Accepted Values_

        Any valid string.

        **H Unbounded?**

        Domain is horizontally unbounded in both X and Y directions.

        _Accepted Values_

        `Yes` or `No`.

        **X Unbounded?**

        Domain is horizontally unbounded in X direction.

        _Accepted Values_

        `Yes` or `No`.

        **Y Unbounded?**

        Domain is horizontally unbounded in Y direction.

        _Accepted Values_

        `Yes` or `No`.

        **H-Coord**

        Name of the horizontal coordinate system used.

        _Accepted Values_

        Any horizontal coordinate system specified in the `Horizontal
        Coordinate Systems` block.

        **X Min**

        X coordinate of domain start.

        _Accepted Values_

        **Y Min**

        Y coordinate of domain start.

        _Accepted Values_

        **X Max**

        X coordinate of domain end.

        _Accepted Values_

        **Y Max**

        Y coordinate of domain end.

        _Accepted Values_

        **X Centre**

        X coordinate of domain centre.

        _Accepted Values_

        **Y Centre**

        Y coordinate of domain centre.

        _Accepted Values_

        **X Range**

        Range of X coordinate values.

        _Accepted Values_

        **Y Range**

        Range of Y coordinate values.

        _Accepted Values_

        **Set of Locations**

        Name of the block containing relevant locations.

        _Accepted Values_

        The name of a location block.

        **Location of centre**

        Name of the location that defines the centre of the domain.

        _Accepted Values_

        The name of location contained inside the named location block.

        **Z Unbounded?**

        Domain is vertically unbounded.

        _Accepted Values_

        `Yes` or `No`.

        **Z-Coord**

        Name of the vertical coordinate system used.

        _Accepted Values_

        Any vertical coordinate system specified in the `Vertical
        Coordinate Systems` block.

        **Z Max**

        Maximum height of the domain.

        _Accepted Values_

        **T Unbounded?**

        Domain is unbounded in time?

        _Accepted Values_

        `Yes` or `No`.

        **Start Time**

        Domain is valid from this time.

        _Accepted Values_

        ==FIXME==

        **End Time**

        Domain not valid after this time.

        _Accepted Values_

        ==FIXME==

        **Duration*

        Total time domain is valid for.

        _Accepted Values_

        ==FIXME==

        **Max Travel Time**

        Maximum lifetime of particles in the domain.

        _Accepted Values_

        ==FIXME==


    The following combinations of keys are available:

    ??? example "A)"
        - **nZ**
        - **Z0**
        - **dZ**

    """

    rows: list[DomainRow]
    used_keys: dict[str, bool]

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        rows: list[dict[str, str | dict[str, str | float | int | bool]]]
    ) -> Domains:
        """Set up the domains block.

        Parameters
        ----------
        rows : list[dict[str, str | dict[str, str | float | int | bool]]]
            Rows of domain information.

        Returns
        -------
        Domains
            Domains block containing all rows.

        """
        converted_rows = [DomainRow.setup(**row) for row in rows]  #type: ignore[ty:invalid-argument-type]
        used_keys = {}
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

        Passes the block configuration into the "domains.jinja" block
        template to get the appropriate configuration block.

        ``` jinja title="domains.jinja"
        --8<-- "./src/enw/files/block_templates/domains.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template("domains.jinja")
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
        text = ["[Domains]"]
        for row in self.rows:
            text.append(f"\t[[{row.name}]]")
            text.extend([
                f"\t\t{k:<20}: {v}"
                for k, v in row.__dict__.items()
                if k[0] != "_" and k != "name"
            ])
        return "\n".join(text)


@dataclass(kw_only=True)
class DomainRow:

    name: str
    hcoord: HorizontalCoordSystems | None
    zcoord: VerticalCoordSystems | None
    max_travel_time: TimeInterval
    h_unbounded: Switch | None = None
    x_unbounded: Switch | None = None
    y_unbounded: Switch | None = None
    z_unbounded: Switch | None = None
    t_unbounded: Switch | None = None
    start_time: DateTime | TimeInterval | None = None
    end_time: DateTime | TimeInterval | None = None
    duration: TimeInterval | None = None
    x_min: float | None = None
    x_max: float | None = None
    x_centre: float | None = None
    x_range: float | None = None
    y_min: float | None = None
    y_max: float | None = None
    y_centre: float | None = None
    y_range: float | None = None
    z_max: float | None = None
    location_block_name: str | None = None
    location: str | None = None

    @classmethod
    def setup(
        cls,
        *,
        name: str,
        h_unbounded: bool | None = None,
        x: dict[str, bool | float | None] | None = None,
        y: dict[str, bool | float | None] | None = None,
        z: dict[str, bool | float | None],
        t: dict[str, bool | float | str | None],
        hcoord: str | None,
        zcoord: str | None,
        location_block_name: str | None = None,
        location: str | None = None
    ) -> DomainRow:
        """Configure a config block with error checking and formatting.

        Parameters
        ----------
        name : str
            Name of the grid.

            Corresponds to **Name**.

        h_unbounded : bool | None
            Should the horizontal domain be unbounded on both x and y axes?

            Corresponds to **H Unbounded?**.

        x : dict[str, bool | float | None] | None
            Configuration for x axes, potentially containing one or more of
            the following keys:
            - "unbounded" (bool): Corresponds to **X Unbounded?**
            - "min" (float): Corresponds to **X Min**
            - "max" (float): Corresponds to **X Max**
            - "centre" (float): Corresponds to **X Centre**
            - "range" (float): Corresponds to **X Range**

        y : dict[str, bool | float | None] | None
            Configuration for y axes, potentially containing one or more of
            the following keys:
            - "unbounded" (bool): Corresponds to **Y Unbounded?**
            - "min" (float): Corresponds to **Y Min**
            - "max" (float): Corresponds to **Y Max**
            - "centre" (float): Corresponds to **Y Centre**
            - "range" (float): Corresponds to **Y Range**

        z : dict[str, bool | float | None]
            Configuration for z axes, potentially containing one or more of
            the following keys:
            - "unbounded" (bool): Corresponds to **Z Unbounded?**
            - "max" (float): Corresponds to **Z Max**

        t : dict[str, bool | float | None]
            - "unbounded" (bool): Corresponds to **Z Unbounded?**
            - "start" (str): Corresponds to **Start Time**
            - "end" (str): Corresponds to **End Time**
            - "duration" (str): Corresponds to **Duration**
            - "max_travel_time" (str): Corresponds to **Max Travel Time**

        hcoord : HorizontalCoordSystems
            Horizontal coordinate system to use when defining the domain.

            Corresponds to **H-Coord**.

        zcoord : VerticalCoordSystems
            Vertical coordinate system to use when defining the domain.

            Corresponds to **Z-Coord**.

        location_block_name : str | None
            Name of the block containing relevant locations.

            Corresponds to **Set of Locations**.

        location : str | None
            Name of the location which represents the centre of the domain.

            Corresponds to **Location of centre**.

        """
        #INFO: Check name
        check_type("name", name, str)
        #INFO: Check h_unbounded
        if h_unbounded is not None:
            check_type("h_unbounded", h_unbounded, bool)
            h_unbounded_switch = make_switch(h_unbounded)
            check_mutually_exclusive("h_unbounded", h_unbounded, "x", x)
            check_mutually_exclusive("h_unbounded", h_unbounded, "y", y)
        else:
            h_unbounded_switch = None
        #INFO: Check hcoord
        if hcoord is not None:
            check_literal(
                "hcoord",
                hcoord,
                "HorizontalCoordSystems",
                HorizontalCoordSystems
            )
            hcoord = cast("HorizontalCoordSystems", hcoord)
        #INFO: Check zcoord
        if zcoord is not None:
            check_literal(
                "zcoord",
                zcoord,
                "VerticalCoordSystems",
                VerticalCoordSystems
            )
            zcoord = cast("VerticalCoordSystems", zcoord)
        #INFO: Check x
        if x is not None:
            cls.check_h_axis("x", x)
            x_typed: dict[str, bool | float | Switch | None] = cast(
                "dict[str, bool | float | Switch | None]",
                x.copy()
            )
            if "unbounded" in x:
                x_typed["unbounded"] = make_switch(
                    cast("bool", x.get("unbounded"))
                )
        else:
            x_typed = {}
        #INFO: Check y
        if y is not None:
            cls.check_h_axis("y", y)
            y_typed: dict[str, bool | float | Switch | None] = cast(
                "dict[str, bool | float | Switch | None]",
                y.copy()
            )
            if "unbounded" in y:
                y_typed["unbounded"] = make_switch(
                    cast("bool", y.get("unbounded"))
                )
        else:
            y_typed = {}
        #INFO: Check z
        cls.check_z_axis(z)
        z_typed: dict[str, bool | float | Switch | None] = cast(
            "dict[str, bool | float | Switch | None]",
            z.copy()
        )
        if "unbounded" in z:
            z_typed["unbounded"] = make_switch(
                cast("bool", z.get("unbounded"))
            )
        #INFO: Check t
        cls.check_t_axis(t)
        t_vals = cls.cast_t_types(t)
        #INFO: Check location_block_name and location
        if location_block_name is not None or location is not None:
            msg = "Specific location not implemented for Domains."
            raise NotImplementedError(msg)
            # check_type("location_block_name", location_block_name, str)

        return cls(
            name=name,
            h_unbounded=h_unbounded_switch,
            t_unbounded=t_vals["t_unbounded"],
            start_time=t_vals["start_time"],
            end_time=t_vals["end_time"],
            duration=t_vals["duration"],
            max_travel_time=t_vals["max_travel_time"],
            **{f"x_{k}": v for k, v in x_typed.items()}, # type: ignore[ty:invalid-argument-type]
            **{f"y_{k}": v for k, v in y_typed.items()},
            **{f"z_{k}": v for k, v in z_typed.items()},
            hcoord=hcoord,
            zcoord=zcoord,
            location_block_name=location_block_name,
            location=location
        )

    @classmethod
    def check_h_axis(
        cls,
        name: str,
        vals: dict[str, bool | float | None],
    ) -> None:
        """Check the configuration of the X and Y axis.

        Parameters
        ----------
        name : str
            The name of the axis.
        vals : dict[str, bool | float | None]
            The configuration of the specified axis.

        Raises
        ------
        ValueError
            - Other configuration given when unbounded.
            - Unexpected keys.
            - Incorrect number of configuration variables.
            - Incorrect types for configuration variables.

        """
        expected_keys: set[str] = {
            "unbounded",
            "min",
            "max",
            "centre",
            "range"
        }
        #INFO: Check max 1 value in vals if unbounded
        if "unbounded" in vals and len(vals) > 1:
            msg = f"Specific values provided for {name} when unbounded."
            raise ValueError(msg)
        #INFO: Check max 2 values in vals if neither are unbounded
        #TODO: This needs more work when the other options are available
        if "unbounded" not in vals and len(vals) != 2:
            msg = (
                f"Incorrect number of values provided for {name}. "
                "Expected 2."
            )
            raise ValueError(msg)
        #INFO: Check all vals keys are expected
        vals_extra_keys = set(vals.keys()) - expected_keys
        if vals_extra_keys:
            msg = f"Unexpected keys in {name}: {"\n".join(vals_extra_keys)}"
            raise ValueError(msg)
        #INFO: Check vals.unbounded
        if "unbounded" in vals:
            check_type(f"{name}.unbounded", vals["unbounded"], bool)
        #INFO: Check vals.min
        if "min" in vals:
            check_type(f"{name}.min", vals["min"], (float, int))
        #INFO: Check vals.max
        if "max" in vals:
            check_type(f"{name}.max", vals["max"], (float, int))
        #INFO: Check vals.centre
        if "centre" in vals:
            check_type(f"{name}.centre", vals["centre"], (float, int))
        #INFO: Check vals.range
        if "range" in vals:
            check_pos_float(f"{name}.range", cast("float", vals["range"]))

    @classmethod
    def check_z_axis(
        cls,
        vals: dict[str, bool | float | None],
    ) -> None:
        """Check the configuration of the Z axis.

        Parameters
        ----------
        vals : dict[str, bool | float | None]
            The configuration of the temporal axis.

        Raises
        ------
        ValueError
            - Other configuration given when unbounded.
            - Unexpected keys.
            - Incorrect number of configuration variables.
            - Incorrect types for configuration variables.

        """
        expected_keys: set[str] = {
            "unbounded",
            "max",
        }
        #INFO: Check max 1 value in vals if unbounded
        if "unbounded" in vals and len(vals) > 1:
            msg = "Specific values provided for z when unbounded."
            raise ValueError(msg)
        #INFO: Check all vals keys are expected
        vals_extra_keys = set(vals.keys()) - expected_keys
        if vals_extra_keys:
            msg = f"Unexpected keys in z: {"\n".join(vals_extra_keys)}"
            raise ValueError(msg)
        #INFO: Check vals.unbounded
        if "unbounded" in vals:
            check_type("z.unbounded", vals["unbounded"], bool)
        #INFO: Check vals.max
        if "max" in vals:
            check_type("z.max", vals["max"], (float, int))

    @classmethod
    def check_t_axis(
        cls,
        vals: dict[str, bool | float | str | None],
    ) -> None:
        """Check the configuration of the temporal axis.

        Parameters
        ----------
        vals : dict[str, bool | float | None]
            The configuration of the temporal axis.

        Raises
        ------
        ValueError
            - Other configuration given when unbounded.
            - Unexpected keys.
            - Incorrect types for configuration variables.
            - max_travel_time not present

        """
        expected_keys: set[str] = {
            "unbounded",
            "start",
            "end",
            "duration",
            "max_travel_time"
        }
        #FIXME: Check for timestamps
        #INFO: Check max 1 value in vals if unbounded
        if "unbounded" in vals and len(vals) > 2:
            msg = "Specific values provided for t when unbounded."
            raise ValueError(msg)
        #INFO: Check all vals keys are expected
        vals_extra_keys = set(vals.keys()) - expected_keys
        if vals_extra_keys:
            msg = f"Unexpected keys in t: {"\n".join(vals_extra_keys)}"
            raise ValueError(msg)
        #INFO: Check vals.unbounded
        if "unbounded" in vals:
            check_type("t.unbounded", vals["unbounded"], bool)
        #INFO: Check vals.start
        if "start" in vals:
            check_type("t.start", vals["start"], str)
        #INFO: Check vals.end
        if "end" in vals:
            check_type("t.end", vals["end"], str)
        #INFO: Check vals.duration
        if "duration" in vals:
            check_type("t.duration", vals["duration"], str)
        #INFO: Check vals.max_travel_time
        if "max_travel_time" not in vals:
            msg = "max_travel_time not provided for t."
            raise ValueError(msg)
        check_type("t.max_travel_time", vals["max_travel_time"], str)

    @classmethod
    def cast_t_types(
        cls,
        t: dict[str, float | bool | str | Switch | None],
    ) -> DomainTimeBlock:
        """Cast the time values to their appropriate types.

        Parameters
        ----------
        t : dict[str, float | bool | str | None]
            Time related parameters.

        Returns
        -------
        DomainTimeBlock
            Values of `t` cast to their appropriate types.

        Raises
        ------
        ValueError
            start_time isn't in the appropriate format.

        ValueError
            end_time isn't in the appropriate format.

        """
        start_time = t.get("start")
        if start_time is not None:
            start_type = parse_time_string(cast("str", start_time))
            if start_type == "DateTime":
                start_time = make_datetime(cast("str", start_time))
            elif start_type in ("Descriptive", "NonDescriptive"):
                start_time = make_time_interval(cast("str", start_time))
            else:
                msg = "start_time is not in datetime or time interval format."
                raise ValueError(msg)
        end_time = t.get("end")
        if end_time is not None:
            end_type = parse_time_string(cast("str", end_time))
            if end_type == "DateTime":
                end_time = make_datetime(cast("str", end_time))
            elif end_type in ("Descriptive", "NonDescriptive"):
                end_time = make_time_interval(cast("str", end_time))
            else:
                msg = "end_time is not in datetime or time interval format."
                raise ValueError(msg)
        duration = t.get("duration")
        if duration is not None:
            duration = make_time_interval(cast("str", duration))
        max_travel_time = make_time_interval(cast("str", t["max_travel_time"]))
        unbounded = t.get("unbounded")
        if unbounded is not None:
            unbounded = make_switch(cast("bool", unbounded))
        return {
            "start_time": start_time,
            "end_time": end_time,
            "duration": duration,
            "max_travel_time": max_travel_time,
            "t_unbounded": unbounded
        }
