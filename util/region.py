import numpy

from util.xtea_util import ObjectType


class Region:
    def __init__(self, X: int, Y: int):
        self.X = X
        self.Y = Y
        self.tiles = numpy.empty((4, 64, 64), dtype=Tile)


class Tile:
    def __init__(self):
        self.height = None
        self.settings = 0
        self.overlay_id = 0
        self.overlay_path = 0
        self.overlay_rotation = 0
        self.underlay_id = 0
        self.attribute_opcode = 0
        self.objects = []

    # Checks if the 2nd bit is a 1
    def is_bridge(self):
        return (self.settings & 2) != 0

    # Checks if the 2nd, 4th, and 5th bits are 0
    def is_drawn(self):  # TODO rename this method pulled from MapImageDumper.java:L180
        return (self.settings & 26) == 0


class RsObject:
    def __init__(self, obj_id: int, obj_type: int, orientation: int):
        self.id = obj_id
        self.type = ObjectType.get_by_object_type(obj_type)
        self.orientation = orientation
