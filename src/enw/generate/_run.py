"""Generate run blocks."""
from typing import TYPE_CHECKING

import enw.block as block
from enw.utils import get_timedelta, dt_to_name_string

if TYPE_CHECKING:
    from enw.types import EnwConfig

def site(config: EnwConfig) -> dict[str, str]:
    """Generate run blocks for site runs.

    Parameters
    ----------
    config : EnwConfig
        Complete config for Enw.

    Returns
    -------
    dict[str, str]
        NAME input header files split by date.

    """
    splits = {}
    duration = config["Main"]["end_time"] - config["Main"]["start_time"]
    split_by_td = get_timedelta(config["Main"]["split_by"])
    time_step_td = get_timedelta(config["Main"]["time_step"])

    num_splits = duration // split_by_td
    num_steps = split_by_td // time_step_td

    species_uses = {
        k: v["uses"] for k, v in config["Species"].items()
    }
    species = config["Species"].copy()
    for v in species.values():
        if "uses" in v:
            v.pop("uses")

    num_digits_steps = len(str(num_steps))

    for split in range(num_splits):
        time = config["Main"]["start_time"] + (split_by_td * split)
        species_step = {}
        species_uses_step = {}
        sources = {}
        for step in range(num_steps):
            start_time = time + (time_step_td * step)
            end_time = time + (time_step_td * (step - 1))
            species_step = species_step | {
                f"{k}_{step:0{num_digits_steps}}": v
                for k, v in species.items()
            }
            species_uses_step = species_uses_step | {
                f"{k}_{step:0{num_digits_steps}}": v
                for k, v in species_uses.items()
            }
            sources = sources | {
                f"{species_name}_{location}_{step}": {
                    "shape": "Cuboid",
                    "set_of_locations": "Receptor Locations",
                    "location": location,
                    "h_coord": config["CoordinateSystems"]["horizontal"][0],
                    "z_coord": config["CoordinateSystems"]["vertical"][0],
                    "z": float(config["Locations"][location]["inlet_height"]),
                    "dh_metres": True,
                    "dz_metres": True,
                    "dx": 0,
                    "dy": 0,
                    "dz": 20,
                    "angle": 0,
                    "source_strength": f"{species_name} 1.0 g/s",
                    "plume_rise": False,
                    "temperature": 0,
                    "volume_flow_rate": 0,
                    "num_particles": 20000,
                    "max_age": "infinity",
                    "top_hat": True,
                    "start_time": dt_to_name_string(start_time),
                    "stop_time": dt_to_name_string(end_time)
                }
                for location in config["Locations"]
                for species_name in species
            }
        _species = block.Species.setup(rows=species_step)
        _species_uses = block.SpeciesUses.setup(rows=species_uses_step)
        _sources = block.Sources.setup(rows=sources)
        splits[time.strftime("%Y%m%d%H%M%S")] = "\n\n".join([
            str(_species),
            str(_species_uses),
            str(_sources)
        ])
    return splits


