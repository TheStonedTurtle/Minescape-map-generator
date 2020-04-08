import os
import json
from typing import TextIO

from util.file_util import read_unsigned_byte
from util.region import Region, Tile, Location


def load_terrain(region: Region, file: TextIO):
    for z in range(4):
        for x in range(64):
            for y in range(64):
                tile = Tile()
                while True:
                    attribute = read_unsigned_byte(file)

                    if attribute == 0:
                        break
                    elif attribute == 1:
                        height = read_unsigned_byte(file)
                        tile.height = height
                        break
                    elif attribute <= 49:
                        tile.attribute_opcode = attribute
                        tile.overlay_id = read_unsigned_byte(file)
                        tile.overlay_path = (attribute - 2) / 4
                        tile.overlay_rotation = attribute - 2 & 3
                    elif attribute <= 81:
                        tile.settings = attribute - 49
                    else:
                        tile.underlay_id = attribute - 81

                region.tiles[z, x, y] = tile


def load_objects(region: Region, path: str):
    filename = os.path.join(path, "I%s_%s.json" % (region.X, region.Y))
    if not os.path.exists(filename):
        return

    with open(filename, 'r') as f:
        data = json.loads(f.read())
        locations = data['locations']
        for locationDict in locations:
            pos = locationDict['position']
            tile: Tile = region.tiles[pos['z'], pos['x'], pos['y']]
            location = Location(locationDict['id'], locationDict['type'], locationDict['orientation'])

            tile.objects.append(location)
