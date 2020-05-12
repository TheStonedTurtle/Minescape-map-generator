import numpy

from data import Tile


class Region:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.tiles = numpy.empty((4, 64, 64), dtype=Tile)
