"""Generate main blocks."""
from typing import TYPE_CHECKING

import enw.block as block

if TYPE_CHECKING:
    from enw.types import EnwConfig


def base(config: EnwConfig) -> str:
    """Generate base config for main block."""
    main = block.Main.setup(
        name=config["Main"]["name"],
        backwards=config["Main"]["backwards"],
        max_num_sources=config["Main"]["max_num_sources"],
        max_num_field_reqs=config["Main"]["max_num_field_reqs"],
        max_num_field_output_groups=config["Main"]["max_num_field_output_groups"],
        absolute_or_relative=config["Main"]["absolute_or_relative"],
        fixed_met=config["Main"]["fixed_met"],
        flat_earth=config["Main"]["flat_earth"],
        random_seed=config["Main"]["random_seed"],
    )

    restart_file = block.Restart.setup(
        **config["Restart"]
    )

    multiple_case_file = block.MultipleCase.setup(
        **config["MultipleCase"]
    )

    openmp = block.OpenMP.setup(
        **config["OpenMP"]
    )

    return "\n\n".join([
        str(main),
        str(restart_file),
        str(multiple_case_file),
        str(openmp)
    ])


