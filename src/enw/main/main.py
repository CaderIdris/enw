""""""
import argparse
from copy import deepcopy
import datetime as dt
import enum
import io
from pathlib import Path
import tarfile
from typing import TYPE_CHECKING

import enw.block as block
from enw.config import load_config
from enw.utils import get_timedelta, dt_to_name_string

from ._generate_spatial import site

if TYPE_CHECKING:
    from enw.types import EnwConfig


class Subcommands(enum.StrEnum):
    """All valid subcommands"""
    build = "BUILD"


def generate_run(config: EnwConfig) -> str:
    """"""
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


def generate_output(config: EnwConfig) -> str:
    """"""

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


def generate_time(config: EnwConfig) -> str:
    """"""
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


def generate_run_blocks(config: EnwConfig) -> dict[str, str]:
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
        

def parse_default_args() -> argparse.Namespace:
    """"""
    arg_parser = argparse.ArgumentParser(
        prog="Enw - Easy Name Wizard",
        description=(
            "Run and process NAME Input header files."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    subparsers = arg_parser.add_subparsers(
        title="subcommands",
        description="Enw functions",
        required=True
    )

    build_subparser = subparsers.add_parser(
        "build",
        help="Create NAME Input header files from a config file."
    )
    build_subparser.add_argument(
        "config",
        type=Path,
        help="Path to the config file.",
        metavar="path/to/config.toml",
    )

    build_subparser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Folder to save output header files to.",
        default="./",
        metavar="DIRECTORY",
        dest="output"
    )
    build_subparser.set_defaults(func=Subcommands.build)

    return arg_parser.parse_args()


def enw() -> None:
    """"""
    args = parse_default_args()

    match args.func:
        case Subcommands.build:
            build(
                config_file=args.config,
                output=args.output
            )


def write_to_tar(
    tar: tarfile.TarFile,
    file_path: str,
    contents: str,
) -> None:
    """"""
    info = tarfile.TarInfo(file_path)
    contents_io = io.BytesIO(contents.encode("utf-8"))
    info.size = contents_io.getbuffer().nbytes
    tar.addfile(info, contents_io)


def build(config_file: Path, output: Path) -> None:
    """"""
    config = load_config(config_file)
    # assert 0

    tar_path = output / f"{config["Main"]["name"]}.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tar:
        #INFO: Run input file
        run_file = generate_run(config)
        write_to_tar(
            tar,
            "Input Files/Configuration/Run.txt",
            run_file
        )
        #INFO: Spatial input file
        spatial_file = site(config)
        write_to_tar(
            tar,
            "Input Files/Configuration/Spatial.txt",
            spatial_file
        )
        #INFO: Output input file (isn't that a mouthful)
        output_file = generate_output(config)
        write_to_tar(
            tar,
            "Input Files/Configuration/Output.txt",
            output_file
        )
        #INFO: Temporal input file
        temporal_file = generate_time(config)
        write_to_tar(
            tar,
            "Input Files/Configuration/Temporal.txt",
            temporal_file
        )
        splits = generate_run_blocks(config)
        for split_date, split_contents in splits.items():
            write_to_tar(
                tar,
                f"Input Files/Splits/{split_date}.txt",
                split_contents
            )

