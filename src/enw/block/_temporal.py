"""Configuration objects for all the temporal NAME III Input Header Blocks.

Covers:

- Temporal Grids: `TemporalGrids`

"""
from dataclasses import dataclass
from typing import TYPE_CHECKING

from enw.utils import (
    check_type,
    make_datetime,
    check_pos_int,
    check_time_interval,
    check_datetime,
    make_time_interval,
)

from ._base import NAMEIIIHeaderInputBlock

if TYPE_CHECKING:
    from enw.types import DateTime, TimeInterval
    from types import NotImplementedType

@dataclass(kw_only=True)
class TemporalGrids(NAMEIIIHeaderInputBlock):
    """Configuration for the TemporalGrids block for NAME III.

    This configures the temporal grid used in NAME.

    The `Temporal Grids:` block contains the following columns:

    ??? information "Columns"
        **Name**

        The name of the temporal grid.

        _Accepted Values_

        Any valid string.

        **nT**

        Number of grid points.

        _Accepted Values_

        Positive integer value.

        **dT**

        Grid spacing.

        _Accepted Values_

        String representing a time interval recognised by NAME.

        **T0**

        Initial time for the grid..

        _Accepted Values_

        String representing a datetime recognised by NAME.

        **T-Array**

        Name of an array giving coordinates of the grid.

        !!! warning "Not Implemented"
            Will currently raise a NotImplementedError.

        _Accepted Values_

        String representing the name of a valid array.

    The following combinations of keys are available:

    ??? example "A) Regular Grid"
        - **nT**
        - **dT**
        - **T0**

    ??? example "B) Irregular Grid"
        - **T-Array**

    """

    rows: list[TemporalGridRow]
    used_keys: dict[str, bool]

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        rows: dict[str, dict[str, str | int]]
    ) -> TemporalGrids:
        """Set up the temporal grids block.

        Parameters
        ----------
        rows : dict[str, dict[str, str | int]]
            Rows of temporal grid information.

        Returns
        -------
        TemporalGrids
            Temporal Grids block containing all rows.

        """
        converted_rows = [
            TemporalGridRow.setup(name=name, **row) #type: ignore[ty:invalid-argument-type]
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

        Passes the block configuration into the "temporalgrids.jinja" block
        template to get the appropriate configuration block.

        ``` jinja title="temporalgrids.jinja"
        --8<-- "./src/enw/files/block_templates/temporalgrids.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template("temporalgrids.jinja")
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
        text = ["[Temporal Grids]"]
        for row in self.rows:
            text.append(f"\t[[{row.name}]]")
            text.extend([
                f"\t\t{k:<20}: {v}"
                for k, v in row.__dict__.items()
                if k[0] != "_" and k != "name"
            ])
        return "\n".join(text)

@dataclass(kw_only=True)
class TemporalGridRow:
    """A single row for the Temporal Grids block in the input header file."""

    name: str
    t_num: int
    t_spacing: TimeInterval
    t_min: DateTime
    t_array: NotImplementedType | None = None

    @classmethod
    def setup(
        cls,
        *,
        name: str,
        t_num: int,
        t_spacing: str,
        t_min: str,
        t_array: None = None
    ) -> TemporalGridRow:
        """Configure a temporal grids row with error checking and formatting.

        Parameters
        ----------
        name : str
            Name of the grid.

            Corresponds to **Name**.

        t_num : int
            Number of grid points.

            Corresponds to **nT**.

        t_spacing : str
            Spacing between grid points.

            Corresponds to **dT**.

        t_min : str
            Smallest time value in the grid.

            Corresponds to **T0**.

        t_array : None, default=None
            Name of an array containing points in the grid.
            Not currently implemented.

            Corresponds to **T-Array**.

        Raises
        ------
        NotImplementedError
            If `t_array` it not None.
        TypeError
            If a type doesn't match.
        ValueError
            - If t_spacing is not a valid time interval.
            - If t_min is not a valid datetime.

        Returns
        -------
        TemporalGridRow
            Representation of a single row of the Temporal Grids block.

        """
        _unimplemented = (
            (
                "t_array", t_array
            ),
        )
        #INFO: Check name
        check_type(f"{name}.name", name, str)
        #INFO: Check t_num
        check_type(f"{name}.t_num", t_num, int)
        check_pos_int(f"{name}.t_num", t_num)
        #INFO: Check t_spacing
        check_type(f"{name}.t_spacing", t_spacing, str)
        check_time_interval(f"{name}.t_spacing", t_spacing)
        formatted_t_spacing = make_time_interval(t_spacing)
        #INFO: Check t_min
        check_type(f"{name}.t_min", t_min, str)
        check_datetime(f"{name}.t_min", t_min)
        formatted_t_min = make_datetime(t_min)
        #INFO: Check not implemented variables
        for k, v in _unimplemented:
            msg = (
                f"{k} was specified but is not implemented for TemporalGrids."
            )
            if v is not None:
                raise NotImplementedError(msg)

        return cls(
            name=name,
            t_num=t_num,
            t_spacing=formatted_t_spacing,
            t_min=formatted_t_min,
            t_array=t_array
        )

