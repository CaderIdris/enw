"""Generate output blocks."""
from typing import TYPE_CHECKING

import enw.block as block

if TYPE_CHECKING:
    from enw.types import EnwConfig

def site(config: EnwConfig) -> str:
    """Generate output blocks for site runs.

    Parameters
    ----------
    config : EnwConfig
        Complete config for Enw, including output blocks.

    Returns
    -------
    str
        NAME input header file with all output blocks.

    """
    output = block.Output.setup(
        **config["Output"]
    )

    for v in config["OutputRequirements"]["Global"].values():
        if "t_grid" not in v:
            v["t_grid"] = "TGrid"

    global_output_requirements = block.Fields.setup(
        rows=config["OutputRequirements"]["Global"]
    )
    #TODO: Finish pls
    pp_info = block.PPInfo.setup(
        rows=config["PPInfo"]
    )

    domain_name = next(iter(config["Domains"].keys()))

    sets_of_dispersion_options = block.DispersionOptions.setup(
        **config["DispersionOptions"],
        computational_domain=domain_name,
    )

    return "\n\n".join([
        str(output),
        str(global_output_requirements),
        str(pp_info),
        str(sets_of_dispersion_options)
    ])
