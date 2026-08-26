from importlib.resources import files
import json

import openghg_defs as defs

openghg_defs_data = files("openghg_defs.data")

def get_location_keys() -> set[str]:
    """Get location keys stored in openghg-defs.

    Loads in the keys for all sites that have their location information
    stored in the [openghg-defs](https://pypi.org/project/openghg-defs/)
    package.

    Returns
    -------
    set[str]
        Set of all site keys.

    """
    with defs.site_info_file.open("rb") as sites:
        site_info = json.load(sites)
    return set(site_info.keys())


def get_location_info(
    key: str,
    subset: str | None = None,
) -> dict[str, str | float | None]:
    """Get location info stored in openghg-defs.

    Loads info for the specified site stored in the
    [openghg-defs](https://pypi.org/project/openghg-defs/) package.

    Parameters
    ----------
    key : str
        Site key.
    subset : str | None, default=None
        Which set of site info to use, if more than one present.

    Returns
    -------
    dict[str, str | float]
        Location information

    """
    with defs.site_info_file.open("rb") as sites:
        site_info = json.load(sites)
    if key not in site_info:
        msg = f"{key} is not a site specified in the openghg_defs package."
        raise KeyError(msg)
    all_info = site_info[key]
    if len(all_info) > 1 and subset is None:
        msg = (
            f"{key} has more than one definition. Need to define a subset "
            f"from: {", ".join(all_info.keys())}."
        )
        raise KeyError(msg)
    if subset is not None and subset not in all_info:
        msg = f"{subset} is not valid for {key}."
        raise KeyError(msg)
    if len(all_info) == 1:
        subset = str(next(iter(all_info.keys())))
    info = all_info[subset]
    return {
        "name": info.get("long_name", f"{key} - No long name"),
        "x": info.get("longitude"),
        "y": info.get("latitude"),
        "inlet_height": info.get("height_station_masl"),
        "hcoord": "Lat-Long",
        "subset": subset
    }


def get_domain_keys() -> set[str]:
    """Get domain keys stored in openghg-defs.

    Loads in the keys for all domains that have their domain information
    stored in the [openghg-defs](https://pypi.org/project/openghg-defs/)
    package.

    Returns
    -------
    set[str]
        Set of all domain keys.

    """
    with defs.domain_info_file.open("rb") as domains:
        domain_info = json.load(domains)
    return set(domain_info.keys())


def get_domain_info(key: str) -> dict[str, str | dict[str, float]]:
    """Get domain info stored in openghg-defs.

    Loads info for the specified domain stored in the
    [openghg-defs](https://pypi.org/project/openghg-defs) package.

    Parameters
    ----------
    key : str
        Domain key.

    Returns
    -------
    dict[str, str | float]
        Domain information.

    """
    with defs.domain_info_file.open("rb") as domains:
        domain_info = json.load(domains)


    if key not in domain_info:
        msg = f"{key} is not a domain specified in the openghg_defs package."
        raise KeyError(msg)
    all_info = domain_info[key]

    vals: dict[str, str | float]  = {"name": key}

    lats = openghg_defs_data / all_info["latitude_file"]
    with lats.open("rb") as latitude_file:
        latitudes = list(latitude_file.readlines())
        vals["y_min"] = float(latitudes[0])
        vals["y_max"] = float(latitudes[-1])
        vals["y_num"] = len(latitudes)
    lons = openghg_defs_data / all_info["longitude_file"]
    with lons.open("rb") as longitude_file:
        longitudes = list(longitude_file.readlines())
        vals["x_min"] = float(longitudes[0])
        vals["x_max"] = float(longitudes[-1])
        vals["x_num"] = len(longitudes)

    return {
        "name": vals["name"],
        "x": {
            "min": vals["x_min"],
            "max": vals["x_max"],
            "num": vals["x_num"],
            "unbounded": False
        },
        "y": {
            "min": vals["y_min"],
            "max": vals["y_max"],
            "num": vals["y_num"],
            "unbounded": False
        },
        "z": {
            "max": 20000,
            "unbounded": False
        },
        "t": {
            "unbounded": True
        },
        "hcoord": "Lat-Long",
        "zcoord": "m agl"
    }


def get_species_key_bridge() -> dict[str, str]:
    """Get a bridge for the species keys in openghg_defs.

    The species listed in openghg_defs have several alternate keys, stored
    in the "alt" key within the species information. This function returns a
    bridge table containing the original and all alternate keys as the
    dictionary keys and the original key as the values. This is used to
    translate between any alternate keys the user might use and the original
    key used in species_info.json.

    Returns
    -------
    dict[str, str]
        Bridge table.

    """
    with defs.species_info_file.open("rb") as species:
        species_info = json.load(species)
    bridge: dict[str, str] = {}
    for k, v in species_info.items():
        bridge[k] = k
        for alt in v.get("alt", []):
            bridge[alt] = k

    return bridge


def get_species_keys() -> set[str]:
    """Get species keys stored in openghg-defs.

    Loads in the keys for all species that have their species information
    stored in the [openghg-defs](https://pypi.org/project/openghg-defs/)
    package. This also includes all alternative keys.

    Returns
    -------
    set[str]
        Set of all species keys.

    """
    bridge = get_species_key_bridge()
    return set(bridge.keys())


def get_species_info(key: str) -> dict[str, str | float]:
    """Get species info stored in openghg-defs.

    Loads info for the specified species stored in the
    [openghg-defs](https://pypi.org/project/openghg-defs) package.

    Parameters
    ----------
    key : str
        Species key.

    Returns
    -------
    dict[str, str | float]
        Species information.

    """
    with defs.species_info_file.open("rb") as species:
        species_info = json.load(species)

    key_bridge = get_species_key_bridge()

    if key not in key_bridge:
        msg = f"{key} is not a species specified in the openghg_defs package."
        raise KeyError(msg)

    all_info = species_info[key_bridge[key]]

    return {
        "name": all_info.get("long_name", key),
        "category": all_info.get("group", "None"),
        "molecular_weight": all_info.get("mol_mass", 1),
        #INFO: Below not currently in species_info
        "deposition_velocity": all_info.get("deposition_velocity", 0),
        "material_unit": all_info.get("mass_unit", "g"),
        "uv_loss_rate": all_info.get("uv_loss_rate", 0),
        "half_life": all_info.get("half_life", "Stable"),
        "surface_resistance": all_info.get("surface_resistance"),
        "on_particles": True,
        "on_fields": False,
        "advect_fields": False
    }

