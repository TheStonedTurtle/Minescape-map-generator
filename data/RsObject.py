from data import ObjectType


class RsObject:
    def __init__(self, obj_id: int, obj_type: int, orientation: int):
        self.id = obj_id
        self.type = ObjectType.get_by_object_type(obj_type)
        self.orientation = orientation
