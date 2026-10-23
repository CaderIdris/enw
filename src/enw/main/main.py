"""Entrypoint for enw."""
import argparse
import enum
import io
from pathlib import Path
import tarfile
from typing import TYPE_CHECKING

from enw.config import load_config
import enw.generate as gen

if TYPE_CHECKING:
    from enw.types import EnwConfig


class Subcommands(enum.StrEnum):
    """All valid subcommands."""

    build = "BUILD"

class BuildTypes(enum.StrEnum):
    """All valid build types."""

    site = "SITE"
    satellite = "SATELLITE"
    gemma = "GEMMA"

def parse_default_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns
    -------
    argparse.Namespace
        Parsed arguments.

    """
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
    build_subparser.set_defaults(func=Subcommands.build)
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

    return arg_parser.parse_args()


def enw() -> None:
    """Acts as the main entry point for enw.

    TODO: Description of different subcommands.
    """
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
    """Write provided contents to a file in a tar archive.

    Parameters
    ----------
    tar : tarfile.TarFile
        Opened context manager for tar archive.
    file_path : str
        Path to file within tar archive.
    contents : str
        Contents to write to the file

    """
    info = tarfile.TarInfo(file_path)
    contents_io = io.BytesIO(contents.encode("utf-8"))
    info.size = contents_io.getbuffer().nbytes
    tar.addfile(info, contents_io)


def build(config_file: Path, output: Path) -> None:
    """Subcommand of enw, creates input header files from config.

    TODO: Description of different build types.

    Parameters
    ----------
    config_file : Path
        Path to the config file.
    output : Path
        Where to save the archive to.

    """
    config = load_config(config_file)
    build_type = BuildTypes.site
    match build_type:
        case BuildTypes.site:
            build_site(config, output)
        case BuildTypes.satellite:
            raise NotImplementedError()
        case BuildTypes.gemma:
            raise NotImplementedError()


def build_site(config: EnwConfig, output: Path) -> None:
    """Create input header files for site runs.

    Parameters
    ----------
    config : EnwConfig
        Parsed and error checked config file.
    output : Path
        Where to save the header files.

    """
    tar_path = output / f"{config["Main"]["name"]}.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tar:
        #INFO: Run input file
        run_file = gen.main.base(config)
        write_to_tar(
            tar,
            "Input Files/Configuration/Run.txt",
            run_file
        )
        #INFO: Spatial input file
        spatial_file = gen.spatial.site(config)
        write_to_tar(
            tar,
            "Input Files/Configuration/Spatial.txt",
            spatial_file
        )
        #INFO: Output input file (isn't that a mouthful)
        output_file = gen.output.site(config)
        write_to_tar(
            tar,
            "Input Files/Configuration/Output.txt",
            output_file
        )
        #INFO: Temporal input file
        temporal_file = gen.time.site(config)
        write_to_tar(
            tar,
            "Input Files/Configuration/Temporal.txt",
            temporal_file
        )
        splits = gen.run.site(config)
        for split_date, split_contents in splits.items():
            write_to_tar(
                tar,
                f"Input Files/Splits/{split_date}.txt",
                split_contents
            )
        for met in ("MK4", "MK11"):
            write_to_tar(
                tar,
                f"Input Files/Met/{met}.txt",
                config[met]
            )
