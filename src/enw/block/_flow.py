from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from enw.types import FlowAttributeOpts
from enw.utils import check_type, make_switch, check_literal
from ._base import NAMEIIIHeaderInputBlock


if TYPE_CHECKING:
    from types import NotImplementedType
    from enw.types import Switch

@dataclass(kw_only=True)
class NWPFlowModuleInstances(NAMEIIIHeaderInputBlock):
    """"""
    rows: list[NWPFlowModuleInstancesRow]
    used_keys: dict[str, bool]

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        rows: dict[str, dict[str, str]]
    ) -> NWPFlowModuleInstances:
        """"""
        converted_rows: list[NWPFlowModuleInstancesRow] = [
            NWPFlowModuleInstancesRow.setup(name=name, **row) #type: ignore[ty:invalid-argument-type]
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

        Passes the block configuration into the "nwpflowmoduleinstances.jinja"
        block  template to get the appropriate configuration block.

        ``` jinja title="nwpflowmoduleinstances.jinja"
        --8<-- "./src/enw/files/block_templates/nwpflowmoduleinstances.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template(
            "nwpflowmoduleinstances.jinja"
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
        repr_lines = ["[NWP Flow Module Instances]"]
        for row in self.rows:
            repr_lines.append(f"\t[[{row.name}]]")
            repr_lines.extend([
                f"\t\t{k:<32}: {v}"
                for k, v in row.__dict__.items()
                if k[0] != "_" and k != "name"
            ])
        return "\n".join(repr_lines)

@dataclass(kw_only=True)
class NWPFlowModuleInstancesRow:
    """"""
    name: str
    met_module: str
    met: str
    domain: str
    ancillary_met_module_instances: NotImplementedType | None = None#str
    radar_met_module_instances: NotImplementedType | None = None#str
    update_on_demand: Switch
    urban_canopy: NotImplementedType | None = None#Switch
    varying_free_trop_turb: NotImplementedType | None = None#Switch

    @classmethod
    def setup(
        cls,
        *,
        name: str,
        met_module: str,
        met: str,
        domain: str,
        update_on_demand: bool,
        ancillary_met_module_instances: None = None,
        radar_met_module_instances: None = None,
        urban_canopy: None = None,
        varying_free_trop_turb: None = None,
    ) -> NWPFlowModuleInstancesRow:
        """"""
        _base_types = (
            ("name", name, str),
            ("met_module", met_module, str),
            ("met", met, str),
            ("domain", domain, str),
        )

        _switch_statements = (
            ("update_on_demand", update_on_demand),
        )

        _unimplemented = (
            ("ancillary_met_module_instances", ancillary_met_module_instances),
            ("radar_met_module_instances", radar_met_module_instances),
            ("urban_canopy", urban_canopy),
            ("varying_free_trop_turb", varying_free_trop_turb),

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
                    f"{k} was specified but is not implemented for NWP Flow "
                    "Module Instances."
                )
                raise NotImplementedError(msg)

        return cls(
            name=name,
            met_module=met_module,
            met=met,
            domain=domain,
            update_on_demand=switches["update_on_demand"],
            ancillary_met_module_instances=ancillary_met_module_instances,
            radar_met_module_instances=radar_met_module_instances,
            urban_canopy=urban_canopy,
            varying_free_trop_turb=varying_free_trop_turb,
        )

@dataclass(kw_only=True)
class FlowOrder(NAMEIIIHeaderInputBlock):
    """"""
    name: str
    rows: list[FlowOrderRow]

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        name: str,
        rows: dict[str, str]
    ) -> FlowOrder:
        """"""
        converted_rows: list[FlowOrderRow] = [
            FlowOrderRow.setup(
                flow=k,
                flow_module=v,
            )
            for k, v in rows.items()
        ]
        return cls(
            name=name,
            rows=converted_rows
        )

    def __str__(self) -> str:
        """Return the configuration block for the NAME input header file.

        Passes the block configuration into the "floworder.jinja" block
        template to get the appropriate configuration block.

        ``` jinja title="floworder.jinja"
        --8<-- "./src/enw/files/block_templates/floworder.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template("floworder.jinja")
        return template.render(
            name=self.name,
            rows=[row.__dict__ for row in self.rows],
        )

    def __repr__(self) -> str:
        """Return representation of object to print to console.

        Returns
        -------
        str
            Representation of object.

        """
        repr_lines = ["[Flow Order]"]
        for row in self.rows:
            repr_lines.append(f"\t[[{row.flow}]]")
            repr_lines.extend([
                f"\t\t{k:<32}: {v}"
                for k, v in row.__dict__.items()
                if k[0] != "_" and k != "flow"
            ])
        return "\n".join(repr_lines)


@dataclass(kw_only=True)
class FlowOrderRow:
    """"""
    flow_module: str
    flow: str

    @classmethod
    def setup(
        cls,
        *,
        flow_module: str,
        flow: str
    ) -> FlowOrderRow:
        """"""
        _base_types = (
            ("flow_module", flow_module, str),
            ("flow", flow, str),
        )

        #INFO: Check standard types
        for val_name, val, type_to_check in _base_types:
            check_type(val_name, val, type_to_check)

        return cls(
            flow_module=flow_module,
            flow=flow
        )


@dataclass(kw_only=True)
class FlowAttributes(NAMEIIIHeaderInputBlock):
    """"""
    rows: list[FlowAttributesRow]
    used_keys: dict[str, bool]

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        rows: dict[str, str]
    ) -> FlowAttributes:
        """"""
        converted_rows: list[FlowAttributesRow] = [
            FlowAttributesRow.setup(name=k, flow_order=v)
            for k, v in rows.items()
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

        Passes the block configuration into the "flowattributes.jinja" block
        template to get the appropriate configuration block.

        ``` jinja title="flowattributes.jinja"
        --8<-- "./src/enw/files/block_templates/flowattributes.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template("flowattributes.jinja")
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
        repr_lines = ["[Flow Attributes]"]
        for row in self.rows:
            repr_lines.append(f"\t[[{row.name}]]")
            repr_lines.extend([
                f"\t\t{k:<32}: {v}"
                for k, v in row.__dict__.items()
                if k[0] != "_" and k != "name"
            ])
        return "\n".join(repr_lines)


@dataclass(kw_only=True)
class FlowAttributesRow(NAMEIIIHeaderInputBlock):
    """"""
    name: FlowAttributeOpts
    flow_order: FlowAttributeOpts

    @classmethod
    def setup(
        cls,
        *,
        name: str,
        flow_order: str
    ) -> FlowAttributesRow:
        """"""
        _literals =  (
            (
                "name",
                name,
                "FlowAttributeOpts",
                FlowAttributeOpts,
            ),
            (
                "flow_order",
                flow_order,
                "FlowAttributeOpts",
                FlowAttributeOpts,
            ),
        )
        #INFO: Check literals
        literals = {}
        for val_name, val, lit_name, lit in _literals:
            check_type(val_name, val, str)
            check_literal(
                name,
                val,
                lit_name,
                lit
            )
        literals["name"] = cast("FlowAttributeOpts", name)
        literals["flow_order"] = cast("FlowAttributeOpts", flow_order)

        return cls(
            name=literals["name"],
            flow_order=literals["flow_order"],
        )

