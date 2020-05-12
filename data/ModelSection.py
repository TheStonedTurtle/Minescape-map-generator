from typing import List

from data import FaceData


class ModelSection:
    def __init__(self, x: int, y: int, faces: List[FaceData]):
        self.x = x
        self.y = y
        self.faces = faces
