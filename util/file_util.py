import os
import shutil
import json
from distutils.dir_util import copy_tree
from typing import TextIO


def handle_files(empty_world_path: str, output_world_path: str):
    if os.path.exists(output_world_path):
        shutil.rmtree(output_world_path)
    os.makedirs(output_world_path)
    copy_tree(empty_world_path, output_world_path)


def read_unsigned_byte(file: TextIO) -> int:
    return int.from_bytes(file.read(1), "little")


# Used for things like Objects and Models where caching the file results increases performance
class JsonFileCacheManager:
    def __init__(self, path: str):
        self.cache = {}
        self.path = path

    def get_file_data(self, filename: str):
        try:
            return self.cache[filename.lower()]
        except KeyError:
            pass

        file = os.path.join(self.path, filename)
        if not os.path.exists(file):
            print("Couldn't find file: " + file)
            return None

        with open(file, 'r') as f:
            data = json.loads(f.read())
            self.cache[filename.lower()] = data
            return data
