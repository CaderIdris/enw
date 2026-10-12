from importlib.resources import as_file, files
import tomllib

preset_files = files("enw.files.config.presets")

def load_preset(
    preset_name: str,
    subfolder: str
) -> dict[str, float | int | str]:
    """Load in the specified preset."""
    preset_path = (
        preset_files
        .joinpath(f"{subfolder}/{preset_name.lower().replace(" ", "")}.toml")
    )

    with as_file(preset_path) as f:
        if not f.exists():
            return {}
        with f.open("rb") as toml:
            return tomllib.load(toml)
