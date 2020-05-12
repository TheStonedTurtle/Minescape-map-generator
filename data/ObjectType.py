from enum import Enum


class ObjectType(Enum):
    SINGLE_WALL = [0, 1]
    CORNER_WALL = [2]
    BOUNDARY_DECORATIVE = [4, 5, 6, 7, 8]
    WALL_DECORATIVE = [9]
    GROUND = [22]
    # empty list is a catch all
    GAME = []

    @staticmethod
    def get_by_object_type(obj_type: int):
        for objectType in ObjectType:
            types = objectType.value
            if obj_type in types or len(types) == 0:
                return objectType
