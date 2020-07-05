import colorsys
from collections import namedtuple
from typing import Tuple, List

from data import ObjectData, ModelData, ModelSection
from managers import SpriteManager
from managers import BlockManager
from util.file_util import JsonFileCacheManager
from util.model_util import ModelUtil

OBJECTS = JsonFileCacheManager("testdata/object_defs")
MODELS = JsonFileCacheManager("testdata/models")
# Stores the ModelSection with the calculate Block type for this model
MODEL_BLOCK_CACHE = dict()
SPRITE_MANAGER = SpriteManager(True)
BLOCK_MANAGER = BlockManager()


class Mappings:
    block_manager = BLOCK_MANAGER
    @staticmethod
    def get_object_data(id: int) -> ObjectData:
        return Mappings.convert_object_json(OBJECTS.get_file_data("%s.json" % id))

    @staticmethod
    def convert_object_json(json_dict: dict) -> ObjectData:
        # noinspection PyTypeChecker,PyArgumentList
        return namedtuple('ObjectData', json_dict.keys())(*json_dict.values())

    @staticmethod
    def get_model_data(id: int) -> ModelData:
        return Mappings.convert_model_json(MODELS.get_file_data("%s.json" % id))

    @staticmethod
    def convert_model_json(json_dict: dict) -> ModelData:
        # noinspection PyTypeChecker,PyArgumentList
        return namedtuple('ModelData', json_dict.keys())(*json_dict.values())

    @staticmethod
    def map_object_to_model_sections(id: int) -> List[ModelSection]:
        data: ObjectData = Mappings.get_object_data(id)

        sections = []

        try:
            for model_id in data.objectModels:
                if MODEL_BLOCK_CACHE.get(model_id) is not None:
                    sections.append(MODEL_BLOCK_CACHE.get(model_id))
                    continue

                model: ModelData = Mappings.get_model_data(model_id)

                face_sections = ModelUtil.getScaledFaceSections(data, model, 1)
                for i in range(len(face_sections)):
                    section = face_sections[i]
                    section_color = ModelUtil.averageColorInSection(model, section)

                    # Find the block that matches the above color
                    block_name = None
                    distance = 0
                    for block in SPRITE_MANAGER.color_map.keys():
                        color = SPRITE_MANAGER.color_map.get(block)
                        d = Mappings.colorDistance(section_color, color)
                        if d < distance or block_name is None:
                            #print(distance, block_name, d, block)
                            block_name = block
                            distance = d

                    section.block = BLOCK_MANAGER.get_block_data(block_name)
                    MODEL_BLOCK_CACHE[model_id] = section
                    sections.append(section)
        except AttributeError:
            pass
        return sections

    @staticmethod
    def colorDistance(rgb_a: Tuple[int, int, int], rgb_b: Tuple[int, int, int]):
        # Convert to HSL and compare by hue
        a = colorsys.rgb_to_hls(rgb_a[0], rgb_a[1], rgb_a[2])
        b = colorsys.rgb_to_hls(rgb_b[0], rgb_b[1], rgb_b[2])
        return abs(a[0] - b[0])
