from math import floor
from typing import Optional

from amulet.api.world import World
from amulet_nbt import TAG_String

from util.mc_util import set_blocks, set_block
from data import Tile, Region, RsObject, ObjectType


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

    if base_height is None:
        base_height = 0
        i = 0

    if base_height is not None:
        height = rs_height_to_mc(base_height) + PLANE_SIZE * (z - i)
    else:
        print("The basetile at this location does not have a height (" + str(baseX + x) + ", " + str(baseY + y) + ")")

    block = block_from_tile(tile.underlay_id, tile.overlay_id)

    if block is not None and height is not None:
        if tile.is_bridge():
            block = "glass"
        elif len(tile.objects) > 0:
            block = "granite"
        if z == 0:
            set_blocks(world, x + baseX, height, -(y + baseY), block, 7, None, True)

            if block == "water":
                set_blocks(world, x + baseX, height - 1, -(y + baseY), "dirt", 7, None, True)
        else:
            set_block(world, x + baseX, height, -(y + baseY), block)

    if len(tile.objects) > 0:
        obj: RsObject
        for obj in tile.objects:
            block = "bedrock"
            block_opts = None
            if obj.type == ObjectType.SINGLE_WALL:
                block = "fence"
                block_opts = {"material": TAG_String("oak")}
                set_blocks(world, x + baseX, height + 2, -(y + baseY), block, 2, block_opts)
                continue
            elif obj.type == ObjectType.CORNER_WALL:
                block = "fence"
                block_opts = {"material": TAG_String("dark_oak")}
                set_blocks(world, x + baseX, height + 2, -(y + baseY), block, 2, block_opts)
                continue
            elif obj.type == ObjectType.BOUNDARY_DECORATIVE:
                block = "sponge"
            elif obj.type == ObjectType.WALL_DECORATIVE:
                block = "sign"
                block_opts = {"material": TAG_String("oak")}
            elif obj.type == ObjectType.GROUND:
                block = "plant"
                block_opts = {"type": TAG_String("poppy")}
            elif obj.type == ObjectType.GAME:
                block = "wool"

            set_block(world, x + baseX, height + 1, -(y + baseY), block, block_opts)


def rs_height_to_mc(height: int) -> int:
    SCALE = 32  # how many RS units = 1 block for height
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

    return "grass_block"
