from math import floor
from typing import Optional

from amulet.api.world import World

from util.mc_util import set_blocks, set_block
from util.region import Tile, Region


def process_tile(world: World, z: int, x: int, y: int, regions: Region, region: Region):
    PLANE_SIZE = 4  # how how many blocks should separate floors

    tile = region.tiles[z][x][y]
    baseX = region.X << 6
    baseY = region.Y << 6
    height = None
    base_height = None
    for i in range(z, -1, -1):
        basetile: Tile = region.tiles[i][x][y]
        if basetile.height is not None:
            base_height = basetile.height
            break

    if (base_height is None):
        base_height = 0
        i = 0

    if base_height is not None:
        height = rs_height_to_mc(base_height) + PLANE_SIZE * (z - i)
    else:
        print("The basetile at this location does not have a height (" + str(baseX + x) + ", " + str(baseY + y) + ")")

    block = block_from_tile(tile.underlay_id, tile.overlay_id)

    if block is not None and height is not None:
        if z is 0:
            set_blocks(world, x + baseX, height, -(y + baseY), block)

            if block is "water":
                set_blocks(world, x + baseX, height - 1, -(y + baseY), "dirt")
        else:
            set_block(world, x + baseX, height, -(y + baseY), block)


def rs_height_to_mc(height: int) -> int:
    SCALE = 30  # how many RS units = 1 block for height
    BASE_MINECRAFT_FLOOR_SIZE = 64  # what block height = 0 should be at

    return BASE_MINECRAFT_FLOOR_SIZE + floor(height / SCALE)

# todo: this is def just jank to test with, will be replaced
def block_from_tile(underlay_id: int, overlay_id: int) -> Optional[str]:
    overlay_switcher = {
        5: "planks",  # todo dark oak or different type
        6: "water",
        10: "stone",
        14: "dirt",
        22: "dirt"
    }

    result = overlay_switcher.get(overlay_id, None)
    if result is not None:
        return result

    if overlay_id != 0:
        print("Overlay id not handled: " + str(overlay_id))
        return "stone"

    if underlay_id == 0:
        return None

    underlay_switcher = {
        48: "grass_block",
        50: "grass_block",
        63: "grass_block",
        64: "grass_block",
        65: "grass_block"
    }

    result = underlay_switcher.get(underlay_id, None)
    if result is not None:
        return result

    print("Underlay id not handled: " + str(underlay_id))
    return "grass_block"
