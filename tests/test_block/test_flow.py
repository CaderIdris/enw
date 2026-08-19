from jinja2 import Environment
import pytest

from enw.block import (
    FlowAttributes,
    FlowOrder,
    NWPFlowModuleInstances,
)
from enw.block._flow import (
    FlowAttributesRow,
    FlowOrderRow,
    NWPFlowModuleInstancesRow
)

pytestmark = [
    pytest.mark.block,
    pytest.mark.block_flow
]

@pytest.fixture
def preset_instances() -> dict[str, dict[str, str | int | float | None]]:
    """Preset rows for instances."""
    return {
        "A": {
            "met_module": "NWP Met",
            "met": "MetA",
            "domain": "DomainA",
            "update_on_demand": True
        },
        "B": {
            "met_module": "NWP Met",
            "met": "MetB",
            "domain": "DomainB",
            "update_on_demand": False
        },
    }

@pytest.fixture
def instances_expected_str() -> dict[str, str]:
    return {
        "Header": (
            "NWP Flow Module Instances:\n"
            "Name,Met Module,Met,Domain,Update on Demand?"
        ),
        "A": (
            "A,NWP Met,MetA,DomainA,Yes"
        ),
        "B": (
            "B,NWP Met,MetB,DomainB,No"
        )
    }

@pytest.fixture
def instances_expected_repr() -> str:
    return "\n".join([
        "[NWP Flow Module Instances]",
        "\t[[A]]",
        "\t\tmet_module                      : NWP Met",
        "\t\tmet                             : MetA",
        "\t\tdomain                          : DomainA",
        "\t\tancillary_met_module_instances  : None",
        "\t\tradar_met_module_instances      : None",
        "\t\tupdate_on_demand                : Yes",
        "\t\turban_canopy                    : None",
        "\t\tvarying_free_trop_turb          : None",
        "\t[[B]]",
        "\t\tmet_module                      : NWP Met",
        "\t\tmet                             : MetB",
        "\t\tdomain                          : DomainB",
        "\t\tancillary_met_module_instances  : None",
        "\t\tradar_met_module_instances      : None",
        "\t\tupdate_on_demand                : No",
        "\t\turban_canopy                    : None",
        "\t\tvarying_free_trop_turb          : None",
    ])

@pytest.mark.parametrize("row", ["A", "B"])
def test_init_instances_preset_single(
    row: str,
    preset_instances: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    tests = {}

    instances = NWPFlowModuleInstances.setup(
        rows={row: preset_instances[row]}
    )
    expected_used_cols = {
        "name": True,
        "met_module": True,
        "met": True,
        "domain": True,
        "ancillary_met_module_instances": False,
        "radar_met_module_instances": False,
        "update_on_demand": True,
        "urban_canopy": False,
        "varying_free_trop_turb": False
    }
    expected_rows = {
        "A": NWPFlowModuleInstancesRow(
            name="A",
            met_module="NWP Met",
            met="MetA",
            domain="DomainA",
            update_on_demand="Yes"
        ),
        "B": NWPFlowModuleInstancesRow(
            name="B",
            met_module="NWP Met",
            met="MetB",
            domain="DomainB",
            update_on_demand="No"
        )
    }
    vals = instances.__dict__
    tests["Correct row"] = vals["rows"] = expected_rows[row]
    tests["Correct used_keys"] = vals["used_keys"] == expected_used_cols
    print(vals["used_keys"])
    print(expected_used_cols)
    tests["Environment present"] = isinstance(
        instances._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_instances_preset_both(
    preset_instances: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    tests = {}

    expected_used_cols = {
        "name": True,
        "met_module": True,
        "met": True,
        "domain": True,
        "ancillary_met_module_instances": False,
        "radar_met_module_instances": False,
        "update_on_demand": True,
        "urban_canopy": False,
        "varying_free_trop_turb": False
    }
    expected_rows = {
        "A": NWPFlowModuleInstancesRow(
            name="A",
            met_module="NWP Met",
            met="MetA",
            domain="DomainA",
            update_on_demand=True
        ),
        "B": NWPFlowModuleInstancesRow(
            name="B",
            met_module="NWP Met",
            met="MetB",
            domain="DomainB",
            update_on_demand=False
        )
    }
    instances = NWPFlowModuleInstances.setup(
        rows=preset_instances
    )
    vals = instances.__dict__
    for i, r in enumerate(["A", "B"]):
        tests[f"{r}.Correct row"] = vals["rows"][i] = expected_rows[r]
    tests["Correct used_keys"] = vals["used_keys"] == expected_used_cols
    tests["Environment present"] = isinstance(
        instances._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@pytest.mark.parametrize("row", ["A", "B"])
def test_init_instances_single_str(
    row: str,
    preset_instances: dict[str, dict[str, object]],
    instances_expected_str: dict[str, str]
):
    """Does the Species class initialise?"""
    tests = {}

    instances = NWPFlowModuleInstances.setup(
        rows={row: preset_instances[row]}
    )

    expected = "\n".join([
        instances_expected_str["Header"],
        instances_expected_str[row],
    ])
    actual = str(instances)
    print(repr(expected))
    print(repr(actual))

    tests["Expected str"] = actual == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_instances_both_str(
    preset_instances: dict[str, dict[str, object]],
    instances_expected_str: dict[str, str]
):
    """Does the Species class initialise?"""
    tests = {}

    instances = NWPFlowModuleInstances.setup(
        rows=preset_instances
    )

    expected = "\n".join([
        instances_expected_str["Header"],
        instances_expected_str["A"],
        instances_expected_str["B"],
    ])
    actual = str(instances)

    tests["Expected str"] = actual == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_instances_both_repr(
    preset_instances: dict[str, dict[str, object]],
    instances_expected_repr: str
):
    """Does the Species class initialise?"""
    tests = {}

    instances = NWPFlowModuleInstances.setup(
        rows=preset_instances
    )

    actual = repr(instances)

    print(instances_expected_repr)
    print(actual)

    tests["Expected repr"] = actual == instances_expected_repr

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("bad_arg", [
        ("name", 0),
        ("met_module", 0),
        ("met", 0),
        ("domain", 0),
])
def test_init_instances_bad_base_type(
    bad_arg: tuple[str, str | int],
    preset_instances: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    rows = {"A": preset_instances["A"]}
    if bad_arg[0] != "name":
        rows["A"] = rows["A"] | {bad_arg[0]: bad_arg[1]}
    else:
        rows[0] = rows["A"]
        rows.pop("A")
    with pytest.raises(
        TypeError,
        match=r"is not.*str.*Is.*int|is not.*float.*Is.*str"
    ):
        _ = NWPFlowModuleInstances.setup(
            rows=rows
        )


@pytest.mark.parametrize("bad_key", [
    "update_on_demand",
])
def test_init_instances_bad_switch(
    bad_key: str,
    preset_instances: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    rows = {"A": preset_instances["A"]}
    rows["A"] = rows["A"] | {bad_key: "BAD VALUE"}
    with pytest.raises(
        TypeError,
        match=r"is not.*bool.*Is.*str"
    ):
        _ = NWPFlowModuleInstances.setup(
            rows=rows
        )


@pytest.mark.parametrize("bad_key", [
    "ancillary_met_module_instances",
    "radar_met_module_instances",
    "urban_canopy",
    "varying_free_trop_turb",
])
def test_init_instances_unimplemented(
    bad_key: str,
    preset_instances: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    rows = {"A": preset_instances["A"]}
    rows["A"] = rows["A"] | {bad_key: "BAD VALUE"}
    with pytest.raises(
        NotImplementedError,
        match=(
            f"{bad_key} was specified but is not implemented for NWP Flow "
            r"Module Instances\."
        )
    ):
        _ = NWPFlowModuleInstances.setup(
            rows=rows
        )

@pytest.fixture
def preset_order() -> dict[str, dict[str, str | int | float | None]]:
    """Preset rows for order."""
    return {
        "UKV_PT2_flow": "NWP Flow",
        "UKV_PT4_flow": "NWP Flow"
    }

@pytest.fixture
def order_expected_str() -> dict[str, str]:
    return {
        "Header": (
            "Flow Order: Test\n"
            "Flow Module,Flow"
        ),
        "UKV_PT2_flow": (
            "NWP Flow,UKV_PT2_flow"
        ),
        "UKV_PT4_flow": (
            "NWP Flow,UKV_PT4_flow"
        )
    }

@pytest.fixture
def order_expected_repr() -> str:
    return "\n".join([
        "[Flow Order]",
        "\t[[UKV_PT2_flow]]",
        "\t\tflow_module                     : NWP Flow",
        "\t[[UKV_PT4_flow]]",
        "\t\tflow_module                     : NWP Flow",
    ])

@pytest.mark.parametrize("row", ["UKV_PT2_flow", "UKV_PT4_flow"])
def test_init_order_preset_single(
    row: str,
    preset_order: dict[str, str],
):
    """Does the Species class initialise?"""
    tests = {}

    order = FlowOrder.setup(
        name="Test",
        rows={row: preset_order[row]}
    )
    expected_rows = {
        "UKV_PT2_flow": FlowOrderRow(
            flow_module="NWP Flow",
            flow="UKV_PT2_flow"
        ),
        "UKV_PT4_flow": FlowOrderRow(
            flow_module="NWP Flow",
            flow="UKV_PT4_flow"
        )
    }
    vals = order.__dict__
    tests["Correct row"] = vals["rows"] = expected_rows[row]
    tests["Environment present"] = isinstance(
        order._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_order_preset_both(
    preset_order: dict[str, str],
):
    """Does the Species class initialise?"""
    tests = {}

    expected_rows = {
        "UKV_PT2_flow": FlowOrderRow(
            flow_module="NWP Flow",
            flow="UKV_PT2_flow"
        ),
        "UKV_PT4_flow": FlowOrderRow(
            flow_module="NWP Flow",
            flow="UKV_PT4_flow"
        )
    }
    order = FlowOrder.setup(
        name="Test",
        rows=preset_order
    )
    vals = order.__dict__
    for i, r in enumerate(["UKV_PT2_flow", "UKV_PT4_flow"]):
        tests[f"{r}.Correct row"] = vals["rows"][i] = expected_rows[r]
    tests["Environment present"] = isinstance(
        order._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@pytest.mark.parametrize("row", ["UKV_PT2_flow", "UKV_PT4_flow"])
def test_init_order_single_str(
    row: str,
    preset_order: dict[str, str],
    order_expected_str: dict[str, str]
):
    """Does the Species class initialise?"""
    tests = {}

    order = FlowOrder.setup(
        name="Test",
        rows={row: preset_order[row]}
    )

    expected = "\n".join([
        order_expected_str["Header"],
        order_expected_str[row],
    ])
    actual = str(order)

    tests["Expected str"] = actual == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_order_both_str(
    preset_order: dict[str, str],
    order_expected_str: dict[str, str]
):
    """Does the Species class initialise?"""
    tests = {}

    order = FlowOrder.setup(
        name="Test",
        rows=preset_order
    )

    expected = "\n".join([
        order_expected_str["Header"],
        order_expected_str["UKV_PT2_flow"],
        order_expected_str["UKV_PT4_flow"],
    ])
    actual = str(order)

    tests["Expected str"] = actual == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_order_both_repr(
    preset_order: dict[str, str],
    order_expected_repr: str
):
    """Does the Species class initialise?"""
    tests = {}

    order = FlowOrder.setup(
        name="Test",
        rows=preset_order
    )

    actual = repr(order)

    print(order_expected_repr)
    print(actual)

    tests["Expected repr"] = actual == order_expected_repr

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("bad_arg", [
    "key",
    "val"
])
def test_init_order_bad_base_type(
    bad_arg: tuple[str, str | int],
    preset_order: dict[str, str],
):
    """Does the Species class initialise?"""
    rows = {0: "BAD VALUE"} if bad_arg == "key" else {"UKV_PT2_flow": 0}
    with pytest.raises(
        TypeError,
        match=r"is not.*str.*Is.*int"
    ):
        _ = FlowOrder.setup(
            name="Test",
            rows=rows
        )


@pytest.fixture
def preset_attributes() -> dict[str, dict[str, str | int | float | None]]:
    """Preset rows for attributes."""
    return {
        "Update": "Update",
        "Convert": "Convert"
    }

@pytest.fixture
def attributes_expected_str() -> dict[str, str]:
    return {
        "Header": (
            "Flow Attributes:\n"
            "Name,Flow Order"
        ),
        "Update": (
            "Update,Update"
        ),
        "Convert": (
            "Convert,Convert"
        )
    }

@pytest.fixture
def attributes_expected_repr() -> str:
    return "\n".join([
        "[Flow Attributes]",
        "\t[[Update]]",
        "\t\tflow_order                      : Update",
        "\t[[Convert]]",
        "\t\tflow_order                      : Convert",
    ])

@pytest.mark.parametrize("row", ["Update", "Convert"])
def test_init_attributes_preset_single(
    row: str,
    preset_attributes: dict[str, str],
):
    """Does the Species class initialise?"""
    tests = {}

    attributes = FlowAttributes.setup(
        rows={row: preset_attributes[row]}
    )
    expected_used_cols = {
        "name": True,
        "flow_order": True,
    }
    expected_rows = {
        "Update": FlowAttributesRow(name="Update", flow_order="Update"),
        "Convert": FlowAttributesRow(name="Convert", flow_order="Convert")
    }
    vals = attributes.__dict__
    tests["Correct row"] = vals["rows"] = expected_rows[row]
    tests["Correct used_keys"] = vals["used_keys"] == expected_used_cols
    print(vals["used_keys"])
    print(expected_used_cols)
    tests["Environment present"] = isinstance(
        attributes._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_attributes_preset_both(
    preset_attributes: dict[str, str],
):
    """Does the Species class initialise?"""
    tests = {}

    expected_used_cols = {
        "name": True,
        "flow_order": True,
    }
    expected_rows = {
        "Update": FlowAttributesRow(name="Update", flow_order="Update"),
        "Convert": FlowAttributesRow(name="Convert", flow_order="Convert")
    }
    attributes = FlowAttributes.setup(
        rows=preset_attributes
    )
    vals = attributes.__dict__
    for i, r in enumerate(["Update", "Convert"]):
        tests[f"{r}.Correct row"] = vals["rows"][i] = expected_rows[r]
    tests["Correct used_keys"] = vals["used_keys"] == expected_used_cols
    tests["Environment present"] = isinstance(
        attributes._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@pytest.mark.parametrize("row", ["Update", "Convert"])
def test_init_attributes_single_str(
    row: str,
    preset_attributes: dict[str, str],
    attributes_expected_str: dict[str, str]
):
    """Does the Species class initialise?"""
    tests = {}

    attributes = FlowAttributes.setup(
        rows={row: preset_attributes[row]}
    )

    expected = "\n".join([
        attributes_expected_str["Header"],
        attributes_expected_str[row],
    ])
    actual = str(attributes)
    print(expected)
    print(actual)

    tests["Expected str"] = actual == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_attributes_both_str(
    preset_attributes: dict[str, str],
    attributes_expected_str: dict[str, str]
):
    """Does the Species class initialise?"""
    tests = {}

    attributes = FlowAttributes.setup(
        rows=preset_attributes
    )

    expected = "\n".join([
        attributes_expected_str["Header"],
        attributes_expected_str["Update"],
        attributes_expected_str["Convert"],
    ])
    actual = str(attributes)
    print(expected)
    print(actual)

    tests["Expected str"] = actual == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_init_attributes_both_repr(
    preset_attributes: dict[str, str],
    attributes_expected_repr: str
):
    """Does the Species class initialise?"""
    tests = {}

    attributes = FlowAttributes.setup(
        rows=preset_attributes
    )

    actual = repr(attributes)

    print(attributes_expected_repr)
    print(actual)

    tests["Expected repr"] = actual == attributes_expected_repr

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("bad_arg", [
    "key",
    "val"
])
def test_init_attributes_bad_base_type(
    bad_arg: tuple[str, str | int],
    preset_attributes: dict[str, str],
):
    """Does the Species class initialise?"""
    rows = {0: "BAD VALUE"} if bad_arg == "key" else {"Update": 0}
    with pytest.raises(
        TypeError,
        match=r"is not.*str.*Is.*int"
    ):
        _ = FlowAttributes.setup(
                rows=rows
        )


@pytest.mark.parametrize("bad_arg", [
    "key",
    "val"
])
def test_init_attributes_bad_literal(
    bad_arg: tuple[str, str | int],
    preset_attributes: dict[str, str],
):
    """Does the Species class initialise?"""
    if bad_arg == "key":
        rows = {"BAD VALUE": "Update"}
    else:
        rows = {"Update": "BAD VALUE"}
    with pytest.raises(
        TypeError,
        match=r"is not a member of FlowAttributeOpts\."
    ):
        _ = FlowAttributes.setup(
                rows=rows
        )
