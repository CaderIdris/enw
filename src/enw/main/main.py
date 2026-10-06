""""""
import argparse
import enum
import io
from pathlib import Path
import tarfile
from typing import TYPE_CHECKING

import enw.block as block
from enw.config import load_config

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


def generate_species(config: EnwConfig) -> str:
    """"""
    species = block.Species.setup(
        rows=config["Species"]
    )

    return "\n\n".join([
        str(species)
    ])


def generate_output(config: EnwConfig) -> str:
    """"""

    output = block.Output.setup(
        **config["Output"]
    )

    #TODO: Finish pls

    return "\n\n".join([
        str(output)
    ])


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


def build(config_file: Path, output: Path) -> int:
    """"""
    config = load_config(config_file)
    # print(config)
    # assert 0
    tar_path = output / f"{config["Main"]["name"]}.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tar:
        #INFO: Run input file
        run_info = tarfile.TarInfo("Input Files/Configuration/Run.txt")
        run_file = generate_run(config)
        run_io = io.BytesIO(run_file.encode("utf-8"))
        run_info.size = run_io.getbuffer().nbytes
        tar.addfile(run_info, run_io)
        #INFO: Spatial input file
        spatial_info = tarfile.TarInfo("Input Files/Configuration/Spatial.txt")
        spatial_file = site(config)
        spatial_io = io.BytesIO(spatial_file.encode("utf-8"))
        spatial_info.size = spatial_io.getbuffer().nbytes
        tar.addfile(spatial_info, spatial_io)
        #INFO: Species input file
        species_info = tarfile.TarInfo("Input Files/Configuration/Species.txt")
        species_file = generate_species(config)
        species_io = io.BytesIO(species_file.encode("utf-8"))
        species_info.size = species_io.getbuffer().nbytes
        tar.addfile(species_info, species_io)
        #INFO: Output input file (isn't that a mouthful)
        output_info = tarfile.TarInfo("Input Files/Configuration/Output.txt")
        output_file = generate_output(config)
        output_io = io.BytesIO(output_file.encode("utf-8"))
        output_info.size = output_io.getbuffer().nbytes
        tar.addfile(output_info, output_io)
