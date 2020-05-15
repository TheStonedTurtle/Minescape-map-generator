import json
from collections import namedtuple
from typing import Optional

from data import MinecraftBlock


class BlockManager:
    FILENAME = "./resources/block_data.json"

    def __init__(self):
        self.blocks = json.load(open(self.FILENAME))

    def get_block_data(self, block_name: str) -> Optional[MinecraftBlock]:
        if block_name not in self.blocks:
            return None

        json_dict = self.blocks[block_name]
        # noinspection PyTypeChecker,PyArgumentList
        return namedtuple('Block', json_dict.keys())(*json_dict.values())