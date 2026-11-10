"""Generate input files block."""
import enw.block as block

def input_files(files: list[str]) -> str:
    """Generate input files block."""
    input_files = block.InputFiles.setup(files=files)
    return str(input_files)
