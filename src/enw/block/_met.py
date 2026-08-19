from enw.utils import (
    check_type,
    check_time_interval,
    make_time_interval,
    make_switch,
    check_literal,
)
from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from ._base import NAMEIIIHeaderInputBlock
from enw.types import (
    BinaryFormatOpts,
    FieldQualifierOpts,
    FileTypeOpts, VerticalCoordSystems
)

if TYPE_CHECKING:
    from types import NotImplementedType
    from typing import Literal

    from enw.types import (
        TimeInterval,
        Switch
    )


@dataclass(kw_only=True)
class NWPMetDefinitions(NAMEIIIHeaderInputBlock):
    """"""
    rows: list[NWPMetDefinitionsRow]
    used_keys: dict[str, bool]

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        rows: dict[str, dict[str, str | bool | float | int]]
    ) -> NWPMetDefinitions:
        """"""
        converted_rows: list[NWPMetDefinitionsRow] = [
            NWPMetDefinitionsRow.setup(name=name, **row) #type: ignore[ty:invalid-argument-type]
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

        Passes the block configuration into the "nwpmetdefinitions.jinja" block
        template to get the appropriate configuration block.

        ``` jinja title="nwpmetdefinitions.jinja"
        --8<-- "./src/enw/files/block_templates/nwpmetdefinitions.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template("nwpmetdefinitions.jinja")
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
        repr_lines = ["[NWP Met Definitions]"]
        for row in self.rows:
            repr_lines.append(f"\t[[{row.name}]]")
            repr_lines.extend([
                f"\t\t{k:<32}: {v}"
                for k, v in row.__dict__.items()
                if k[0] != "_" and k != "name"
            ])
        return "\n".join(repr_lines)


@dataclass(kw_only=True)
class NWPMetDefinitionsRow:
    """"""

    name: str
    binary_format: BinaryFormatOpts
    file_type: FileTypeOpts
    time_interval: TimeInterval
    min_time: NotImplementedType | None = None #DateTime
    day_per_file: Switch
    prefix: str
    suffix: str
    next_heat_flux: Switch
    next_precipitation: Switch
    next_cloud: Switch
    mesoscale_sigu: float
    mesoscale_tauu: float
    met_file_structure_definition: str
    z_coord_w: VerticalCoordSystems
    z_coord_cloud_height: VerticalCoordSystems
    z_grid: str
    z_grid_u_v: str
    z_grid_w: str
    z_grid_p: str
    h_grid: str
    h_grid_u: str
    h_grid_v: str
    topography_file: str

    @classmethod
    def setup(
        cls,
        *,
        name: str,
        binary_format: str,
        file_type: str,
        time_interval: str,
        day_per_file: bool,
        prefix: str,
        suffix: str,
        next_heat_flux: bool,
        next_precipitation: bool,
        next_cloud: bool,
        mesoscale_sigu: float,
        mesoscale_tauu: float,
        met_file_structure_definition: str,
        z_coord_w: str,
        z_coord_cloud_height: str,
        z_grid: str,
        z_grid_u_v: str,
        z_grid_w: str,
        z_grid_p: str,
        h_grid: str,
        h_grid_u: str,
        h_grid_v: str,
        topography_file: str,
        min_time: None = None
    ) -> NWPMetDefinitionsRow:
        """"""
        _base_types = (
            ("name", name, str),
            ("prefix", prefix, str),
            ("suffix", suffix, str),
            ("mesoscale_sigu", mesoscale_sigu, float | int),
            ("mesoscale_tauu", mesoscale_tauu, float | int),
            (
                "met_file_structure_definition",
                met_file_structure_definition,
                str,
            ),
            ("z_grid", z_grid, str),
            ("z_grid_u_v", z_grid_u_v, str),
            ("z_grid_w", z_grid_w, str),
            ("z_grid_p", z_grid_p, str),
            ("h_grid", h_grid, str),
            ("h_grid_u", h_grid_u, str),
            ("h_grid_v", h_grid_v, str),
            ("topography_file", topography_file, str),
        )

        _switch_statements = (
            ("day_per_file", day_per_file),
            ("next_heat_flux", next_heat_flux),
            ("next_precipitation", next_precipitation),
            ("next_cloud", next_cloud),
        )

        _time_intervals = (
            ("time_interval", time_interval),
        )

        _literals =  (
            (
                "binary_format",
                binary_format,
                "BinaryFormatOpts",
                BinaryFormatOpts,
            ),
            (
                "file_type",
                file_type,
                "FileTypeOpts",
                FileTypeOpts,
            ),
            (
                "z_coord_w",
                z_coord_w,
                "VerticalCoordSystems",
                VerticalCoordSystems,
            ),
            (
                "z_coord_cloud_height",
                z_coord_cloud_height,
                "VerticalCoordSystems",
                VerticalCoordSystems,
            ),
        )

        _unimplemented = (
            ("min_time", min_time),
        )

        #INFO: Check time intervals
        time_intervals: dict[str, TimeInterval] = {}
        for val_name, val in _time_intervals:
            check_type(val_name, val, str)
            check_time_interval(val_name, val)
            time_intervals[val_name] = make_time_interval(val)

        #INFO: Check switch_statements
        switches: dict[str, Switch] = {}
        for val_name, val in _switch_statements:
            check_type(val_name, val, bool)
            switches[val_name] = make_switch(val)

        #INFO: Check standard types
        for val_name, val, type_to_check in _base_types:
            check_type(val_name, val, type_to_check)

        #INFO: Check literals
        literals = {}
        for val_name, val, lit_name, lit in _literals:
            check_type(val_name, val, str)
            check_literal(
                val_name,
                val,
                lit_name,
                lit
            )
        literals["binary_format"] = cast("BinaryFormatOpts", binary_format)
        literals["file_type"] = cast("FileTypeOpts", file_type)
        literals["z_coord_w"] = cast("VerticalCoordSystems", z_coord_w)
        literals["z_coord_cloud_height"] = cast(
            "VerticalCoordSystems",
            z_coord_cloud_height
        )

        #INFO: Check not implemented variables
        for k, v in _unimplemented:
            if v is not None:
                msg = (
                    f"{k} was specified but is not implemented for NWP Met "
                    "Definitions."
                )
                raise NotImplementedError(msg)

        return cls(
            name=name,
            binary_format=literals["binary_format"],
            file_type=literals["file_type"],
            time_interval=time_intervals["time_interval"],
            day_per_file=switches["day_per_file"],
            prefix=prefix,
            suffix=suffix,
            next_heat_flux=switches["next_heat_flux"],
            next_precipitation=switches["next_precipitation"],
            next_cloud=switches["next_cloud"],
            mesoscale_sigu=mesoscale_sigu,
            mesoscale_tauu=mesoscale_tauu,
            met_file_structure_definition=met_file_structure_definition,
            z_coord_w=literals["z_coord_w"],
            z_coord_cloud_height=literals["z_coord_cloud_height"],
            z_grid=z_grid,
            z_grid_u_v=z_grid_u_v,
            z_grid_w=z_grid_w,
            z_grid_p=z_grid_p,
            h_grid=h_grid,
            h_grid_u=h_grid_u,
            h_grid_v=h_grid_v,
            topography_file=topography_file,
            min_time=min_time,
        )

@dataclass(kw_only=True)
class NWPMetModuleInstances(NAMEIIIHeaderInputBlock):
    """"""
    rows: list[NWPMetModuleInstancesRow]
    used_keys: dict[str, bool]

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        rows: dict[str, dict[str, str | bool | float | int]]
    ) -> NWPMetModuleInstances:
        """"""
        converted_rows: list[NWPMetModuleInstancesRow] = [
            NWPMetModuleInstancesRow.setup(name=name, **row) #type: ignore[ty:invalid-argument-type]
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

        Passes the block configuration into the "nwpmetmoduleinstances.jinja"
        block template to get the appropriate configuration block.

        ``` jinja title="nwpmetmoduleinstances.jinja"
        --8<-- "./src/enw/files/block_templates/nwpmetmoduleinstances.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template(
            "nwpmetmoduleinstances.jinja"
        )
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
        repr_lines = ["[NWP Met Module Instances]"]
        for row in self.rows:
            repr_lines.append(f"\t[[{row.name}]]")
            repr_lines.extend([
                f"\t\t{k:<20}: {v}"
                for k, v in row.__dict__.items()
                if k[0] != "_" and k != "name"
            ])
        return "\n".join(repr_lines)


@dataclass(kw_only=True)
class NWPMetModuleInstancesRow:
    """"""
    name: str
    min_bl_depth: float
    max_bl_depth: float
    use_nwp_bl_depth: Switch
    mesoscale_sigu: NotImplementedType | None = None #float
    mesoscale_tauu: NotImplementedType | None = None #float
    free_trop_sigu: NotImplementedType | None = None #float
    free_trop_sigw: NotImplementedType | None = None #float
    free_trop_tauu: NotImplementedType | None = None #float
    free_trop_tauw: NotImplementedType | None = None #float
    restore_met_script: str
    delete_met: Switch
    met_folder: str
    ensemble_met_folder: NotImplementedType | None = None #str
    met_folder_stem: NotImplementedType | None = None #str
    met_folders: NotImplementedType | None = None #str
    topography_folder: str
    met_definition_name: str
    update_on_demand: Switch
    prefetch: NotImplementedType | None = None #Switch
    new_threaded_method: NotImplementedType | None = None #Switch

    @classmethod
    def setup(
        cls,
        *,
        name: str,
        min_bl_depth: float,
        max_bl_depth: float,
        use_nwp_bl_depth: bool,
        restore_met_script: str,
        delete_met: bool,
        met_folder: str,
        topography_folder: str,
        met_definition_name: str,
        update_on_demand: bool,
        mesoscale_sigu: None = None,
        mesoscale_tauu: None = None,
        free_trop_sigu: None = None,
        free_trop_sigw: None = None,
        free_trop_tauu: None = None,
        free_trop_tauw: None = None,
        ensemble_met_folder: None = None,
        met_folder_stem: None = None,
        met_folders: None = None,
        prefetch: None = None,
        new_threaded_method: None = None
    ) -> NWPMetModuleInstancesRow:
        """"""
        _unimplemented = (
            ("mesoscale_sigu", mesoscale_sigu),
            ("mesoscale_tauu", mesoscale_tauu),
            ("free_trop_sigu", free_trop_sigu),
            ("free_trop_sigw", free_trop_sigw),
            ("free_trop_tauu", free_trop_tauu),
            ("free_trop_tauw", free_trop_tauw),
            ("ensemble_met_folder", ensemble_met_folder),
            ("met_folder_stem", met_folder_stem),
            ("met_folders", met_folders),
            ("prefetch", prefetch),
            ("new_threaded_method", new_threaded_method)
        )
        _base_types = (
            ("name", name, str),
            ("min_bl_depth", min_bl_depth, float | int),
            ("max_bl_depth", max_bl_depth, float | int),
            ("restore_met_script", restore_met_script, str),
            ("met_folder", met_folder, str),
            ("topography_folder", topography_folder, str),
            ("met_definition_name", met_definition_name, str),

        )
        _switch_statements = (
            ("use_nwp_bl_depth", use_nwp_bl_depth),
            ("delete_met", delete_met),
            ("update_on_demand", update_on_demand),
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
                    f"{k} was specified but is not implemented for NWP Met "
                    "Module Instances."
                )
                raise NotImplementedError(msg)

        return cls(
            name=name,
            min_bl_depth=min_bl_depth,
            max_bl_depth=max_bl_depth,
            use_nwp_bl_depth=switches["use_nwp_bl_depth"],
            restore_met_script=restore_met_script,
            delete_met=switches["delete_met"],
            met_folder=met_folder,
            topography_folder=topography_folder,
            met_definition_name=met_definition_name,
            update_on_demand=switches["update_on_demand"],
            mesoscale_sigu=mesoscale_sigu,
            mesoscale_tauu=mesoscale_tauu,
            free_trop_sigu=free_trop_sigu,
            free_trop_sigw=free_trop_sigw,
            free_trop_tauu=free_trop_tauu,
            free_trop_tauw=free_trop_tauw,
            ensemble_met_folder=ensemble_met_folder,
            met_folder_stem=met_folder_stem,
            met_folders=met_folders,
            prefetch=prefetch,
            new_threaded_method=new_threaded_method,
        )


@dataclass(kw_only=True)
class NWPMetFileStructureDefinitions(NAMEIIIHeaderInputBlock):
    """"""
    name: str
    rows: list[NWPMetFileStructureDefinitionsRow]
    used_keys: dict[str, bool]

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        name: str,
        rows: dict[str, dict[str, str | bool | float | int]]
    ) -> NWPMetFileStructureDefinitions:
        """"""
        converted_rows: list[NWPMetFileStructureDefinitionsRow] = [
            NWPMetFileStructureDefinitionsRow.setup(
                field_name=field_name,
                **row #type: ignore[ty:invalid-argument-type]
            )
            for field_name, row in rows.items()
        ]
        used_keys = {"name": True}
        for row in converted_rows:
            used_keys = {
                k: v is not None or used_keys.get(k, False)
                for k, v in row.__dict__.items()
            }
        return cls(
            name=name,
            rows=converted_rows,
            used_keys=used_keys
        )

    def __str__(self) -> str:
        """Return the configuration block for the NAME input header file.

        Passes the block configuration into the
        "nwpmetfilestructuredefinitions.jinja" block
        template to get the appropriate configuration block.

        ``` jinja title="nwpmetfilestructuredefinitions.jinja"
        --8<-- "./src/enw/files/block_templates/\
nwpmetfilestructuredefinitions.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template(
            "nwpmetfilestructuredefinitions.jinja"
        )
        return template.render(
            name=self.name,
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
        repr_lines = ["[NWP Met File Structure Definitions]"]
        for row in self.rows:
            repr_lines.append(f"\t[[{row.field_name}]]")
            repr_lines.extend([
                f"\t\t{k:<20}: {v}"
                for k, v in row.__dict__.items()
                if k[0] != "_" and k != "name"
            ])
        return "\n".join(repr_lines)


@dataclass(kw_only=True)
class NWPMetFileStructureDefinitionsRow:
    """"""
    field_name: str
    lowest_level: int
    highest_level: int | Literal["Top"]
    field_code: int
    three_d: Switch
    field_qualifiers: FieldQualifierOpts | None
    nc_field_name: NotImplementedType | None = None#str


    @classmethod
    def setup(
        cls,
        *,
        field_name: str,
        lowest_level: int,
        highest_level: int | str,
        field_code: int,
        three_d: bool,
        field_qualifiers: str | None,
        nc_field_name: None = None
    ) -> NWPMetFileStructureDefinitionsRow:
        """"""
        _unimplemented = (
            ("nc_field_name", nc_field_name),
        )

        _base_types = (
            ("field_name", field_name, str),
            ("lowest_level", lowest_level, int),
            ("highest_level", highest_level, int | str),
            ("field_code", field_code, int),
        )

        _switch_statements = (
            ("three_d", three_d),
        )

        _literals = (
            (
                "field_qualifiers",
                field_qualifiers,
                "FieldQualifierOpts",
                FieldQualifierOpts,
                True
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

        #INFO: Check literals
        literals = {}
        for val_name, val, lit_name, lit, can_be_null in _literals:
            if can_be_null and val is None:
                continue
            check_type(val_name, val, str)
            check_literal(
                val_name,
                val,
                lit_name,
                lit
            )
        literals["field_qualifiers"] = cast(
            "FieldQualifierOpts",
            field_qualifiers
        )
        if isinstance(highest_level, str) and highest_level != "Top":
            msg = "highest_level is not an integer value or 'Top'."
            raise TypeError(msg)

        #INFO: Check not implemented variables
        for k, v in _unimplemented:
            if v is not None:
                msg = (
                    f"{k} was specified but is not implemented for NWP Met "
                    "File Structure Definition."
                )
                raise NotImplementedError(msg)

        return cls(
            field_name=field_name,
            lowest_level=lowest_level,
            highest_level=highest_level,
            field_code=field_code,
            three_d=switches["three_d"],
            field_qualifiers=literals["field_qualifiers"],
            nc_field_name=nc_field_name,
        )
