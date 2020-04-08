import os
import re
import argparse
parser = argparse.ArgumentParser(description="Generates an RuneScape themed MineCraft world from the OSRS map data")
parser.add_argument("--test", action="store_true",
                    help="Limits the data used for generating the map to the testdata directory")
args = parser.parse_args()

from amulet.world_interface import load_world

from util.color_util import block_from_tile, process_tile
from util.file_util import handle_files
from util.map_loader import load_terrain, load_objects
from util.mc_util import set_block, initialize_world
from util.region import Region

if __name__ == "__main__":
    empty_world_path = "resources/emptymap"
    # WARNING ANY DIRECTORY AT THE OUTPUT PATH WILL BE DELETED
    output_world_path = "output/testworld1"

    handle_files(empty_world_path, output_world_path)
    world = load_world(output_world_path)
    initialize_world(world)
    # set_block(world, 0, 64, 0)
    # world.save()
    path = "rscachedump/"
    if args.test:
        path = "testdata/"
    mapPath = os.path.join(path, "tiledata")
    xteaPath = os.path.join(path, "xtea")
    regions = []
    pattern = re.compile("m(\d+)_(\d+).dat")
    for filename in os.listdir(mapPath):
        with open(os.path.join(mapPath, filename), 'rb') as f:
            match = pattern.match(filename)
            regionX = match.group(1)
            regionY = match.group(2)
            region = Region(int(regionX), int(regionY))
            load_terrain(region, f)
            load_objects(region, xteaPath)
            regions.append(region)
            f.close()

    for region in regions:
        for z in range(len(region.tiles)):
            for x in range(len(region.tiles[z])):
                for y in range(len(region.tiles[z][x])):
                    tile = region.tiles[z][x][y]
                    process_tile(world, z, x, y, regions, region)

    world.save()
