#put empty chunks everywhere just so we do not have to worry about world generation for now
from amulet import Block
from amulet.api.chunk import Chunk
from amulet.api.errors import ChunkDoesNotExist
from amulet.api.world import World
from amulet.utils import block_coords_to_chunk_coords

from data import MinecraftBlock


def initialize_world(world: World):
    minxcoord = -1000
    minzcoord = -1000
    maxxcoord = 5000
    maxzcoord = 7000
    minx, minz = block_coords_to_chunk_coords(minxcoord, minzcoord)
    maxx, maxz = block_coords_to_chunk_coords(maxxcoord, maxzcoord)
    for x in range(minx, maxx):
        for z in range(minz, maxz):
            world.put_chunk(Chunk(x, z))


def set_block(world: World, x: int, y: int, z: int, block: MinecraftBlock):
    if not (0 <= y <= 255):
        raise IndexError("The supplied Y coordinate must be between 0 and 255")

    cx, cz = block_coords_to_chunk_coords(x, z);

    try:
        chunk = world.get_chunk(cx, cz)
    except ChunkDoesNotExist:
        world.put_chunk(Chunk(cx, cz))
        chunk = world.get_chunk(cx, cz)

    offset_x, offset_z = x - 16 * cx, z - 16 * cz
    options = None
    if "material" in block:
        options = {"material": block.material.replace('"', "")}
    chunk.blocks[offset_x, y, offset_z] = world.palette.get_add_block(
        Block(namespace="universal_minecraft", base_name=block.name, properties=options)
    )
    chunk.changed = True


def set_blocks(world: World, x: int, y: int, z: int, block: MinecraftBlock, amount, downward=False):
    for i in range(0, amount):
        set_block(world, x, y + (-i if downward else i), z, block)
