from typing import List, Tuple, Dict

import cv2

from blocks import MinecraftBlocks

IMAGE_SIZE = 16


class SpriteManager:
    FILENAME = "./resources/sprites.png"

    def __init__(self, auto_generate=False):
        self.master_img = cv2.imread(self.FILENAME, cv2.IMREAD_UNCHANGED)
        if auto_generate:
            self.color_map = self.averageMinecraftBlockColors()

    def getSprite(self, position: int):
        idx = position - 1
        rows, cols, channels = self.master_img.shape
        # Calculate where in the image this index is located
        image_cols = int(cols / IMAGE_SIZE)
        row = int(idx / image_cols)
        col = int(idx - (row * image_cols))

        x_start = row * IMAGE_SIZE
        x_end = (row + 1) * IMAGE_SIZE
        y_start = col * IMAGE_SIZE
        y_end = (col + 1) * IMAGE_SIZE
        return self.master_img[x_start:x_end, y_start:y_end]

    def averageSpriteRgbColor(self, position: int, ignore_transparent=True) -> Tuple[int, int, int]:
        r, g, b = 0, 0, 0
        pixels = self.getSprite(position)
        rows, cols, channels = pixels.shape
        transparent_count = 0
        for row in range(rows):
            for col in range(cols):
                pixel = pixels[row][col]
                if ignore_transparent and pixel[3] == 0:
                    transparent_count += 1
                    continue
                # BGR order not RGB
                b += pixel[0]
                g += pixel[1]
                r += pixel[2]

        pixel_count = (rows * cols) - transparent_count
        rgb = int(r / pixel_count), int(g / pixel_count), int(b / pixel_count)
        return rgb

    def averageMinecraftBlockColors(self, blocks: List[Tuple[str, int]] = MinecraftBlocks.MinecraftBlocks)\
            -> Dict[str, Tuple[int, int, int]]:
        color_map = {}
        for block_data in blocks:
            color = self.averageSpriteRgbColor(block_data[1])
            color_map[block_data[0]] = color

        return color_map

    @staticmethod
    def rgbColorToInt(rgb: Tuple[int, int, int]) -> int:
        return rgb[0] << 16 | rgb[1] << 8 | rgb[2]
