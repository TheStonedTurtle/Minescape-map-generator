from typing import List, Optional, Tuple

from data import Tile


class Region:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.tiles: List[List[List[Optional[Tile]]]] = [[[None for k in range(64)] for j in range(64)] for i in range(4)]