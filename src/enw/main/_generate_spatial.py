from typing import TYPE_CHECKING

import enw.block as block

if TYPE_CHECKING:
    from enw.types import EnwConfig

def site(config: EnwConfig) -> str:
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


