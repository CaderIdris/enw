""""""
import argparse
import enum
import gzip
import io
from pathlib import Path
import tarfile
from typing import TYPE_CHECKING

import enw.block as block
from enw.config import load_config

if TYPE_CHECKING:
    from enw.types import EnwConfig


class Subcommands(enum.StrEnum):
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

    output = block.Output.setup(
        **config["Output"]
    )

    return "\n\n".join([
        str(main),
        str(restart_file),
        str(multiple_case_file),
        str(openmp),
        str(output)
    ])


def generate_spatial(config: EnwConfig) -> str:
    """"""
    horizontal = block.HorizontalCoords.setup(
        names=config["CoordinateSystems"]["horizontal"]
    )
    vertical = block.VerticalCoords.setup(
        names=config["CoordinateSystems"]["vertical"]
    )

    locations = block.Locations.setup(
        block_name="Receptor Locations",
        rows=config["Locations"]
    )

    hgrids = block.HorizontalGrids.setup(
        **config["HorizontalGrid"]["EUROPE"]
    )
    #BUG: Make hgrids accept multiple AAAAAAA

    vgrids = block.VerticalGrids.setup(
        name="VGrid1",
        **config["VerticalGrid"]
    )

    domains = block.Domains.setup(
        rows=config["Domains"]
    )

    return "\n\n".join([
        str(horizontal),
        str(vertical),
        str(locations),
        str(hgrids),
        str(vgrids),
        str(domains)
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
        spatial_file = generate_spatial(config)
        spatial_io = io.BytesIO(spatial_file.encode("utf-8"))
        spatial_info.size = spatial_io.getbuffer().nbytes
        tar.addfile(spatial_info, spatial_io)
