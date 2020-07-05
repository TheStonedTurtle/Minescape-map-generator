from math import floor
from typing import Optional

from amulet.api.world import World
from amulet_nbt import TAG_String

from data import MinecraftBlock
from util.mappings import Mappings
from util.mc_util import set_blocks, set_block
from data import Tile, Region, RsObject, ObjectType, ModelSection

PLANE_SIZE = 4  # how how many blocks should separate floors
BLOCK_MANAGER = Mappings().block_manager


def process_tile(world: World, z: int, x: int, y: int, region: Region):
    tile = region.tiles[z][x][y]
    base_x = region.x << 6
    base_y = region.y << 6
    height = None
    base_height = 0
    for i in range(z, -1, -1):
        base_tile: Tile = region.tiles[i][x][y]
        if base_tile.height is not None:
            base_height = base_tile.height
            break

    if base_height is not None:
        height = rs_height_to_mc(base_height) + PLANE_SIZE * z
    else:
        print("The basetile at this location does not have a height (" + str(base_x + x) + ", " + str(base_y + y) + ")")
        height = rs_height_to_mc(0) + PLANE_SIZE * z

    block_name: str = block_from_tile(tile.underlay_id, tile.overlay_id)

    if block_name is not None and height is not None:
        block: MinecraftBlock = BLOCK_MANAGER.get_block_data(block_name)
        if block is None:
            print("Unknown block: %s" % block_name)
            return

        # Pad the flooring so it isn't directly above the void
        if z == 0:
            set_blocks(world, x + base_x, height, -(y + base_y), block, 7)

            # Put 3 blocks of dirt under water
            if block == "water":
                set_blocks(world, x + base_x, height - 1, -(y + base_y), BLOCK_MANAGER.get_block_data("dirt"), 3, True)
        else:
            set_block(world, x + base_x, height, -(y + base_y), block)

    if len(tile.objects) > 0:
        obj: RsObject
        for obj in tile.objects:
            sections = Mappings.map_object_to_model_sections(obj.id)
            section: ModelSection
            for section in sections:
                block: MinecraftBlock = section.block
                if section.block is None:
                    print("Skipping model section with no block type")
                    continue
                amount = 1
                if obj.type == ObjectType.SINGLE_WALL or obj.type == ObjectType.CORNER_WALL:
                    amount = 2

                if block.name == "air":
                    print("Skipping adding air")
                    continue

                set_blocks(world, x + base_x, height + 1, -(y + base_y), block, amount)
                print(x + base_x, height + 1, -(y + base_y), block.name, amount)


def rs_height_to_mc(height: int) -> int:
    SCALE = 32  # how many RS units = 1 block for height
    BASE_MINECRAFT_FLOOR_SIZE = 64  # what block height = 0 should be at

    return BASE_MINECRAFT_FLOOR_SIZE + floor(height / SCALE)


# todo: this is def just jank to test with, will be replaced
def block_from_tile(underlay_id: int, overlay_id: int) -> Optional[str]:
    overlay_switcher = {
        5: "oak_planks",  # todo dark oak or different type
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
