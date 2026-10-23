"""Generate temporal blocks."""
from typing import TYPE_CHECKING

import enw.block as block
from enw.utils import get_timedelta, dt_to_name_string

if TYPE_CHECKING:
    from enw.types import EnwConfig

def site(config: EnwConfig) -> str:
    """Generate temporal blocks for site runs.

    Parameters
    ----------
    config : EnwConfig
        Complete config for Enw, including temporal blocks.

    Returns
    -------
    str
        NAME input header file with all temporal blocks.

    """
    duration = config["Main"]["end_time"] - config["Main"]["start_time"]
    time_step_td = get_timedelta(config["Main"]["time_step"])
    max_age_td = get_timedelta(config["Main"]["max_age"])

    #BUG: Calculating t_num wrong! Use max_age + duration of day!

    num_steps = (duration + max_age_td) // time_step_td
    grids = {
        "TGridEnd": {
            "t_num": 1,
            "t_spacing": config["Main"]["time_step"],
            "t_min": dt_to_name_string(config["Main"]["end_time"])
        },
        "TGridRun": {
            "t_num": num_steps,
            "t_spacing": config["Main"]["time_step"],
            "t_min": dt_to_name_string(config["Main"]["start_time"])
        }
    }

    temporal_grids = block.TemporalGrids.setup(rows=grids)

    return "\n\n".join([
        str(temporal_grids)
    ])

