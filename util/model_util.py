from typing import Tuple, List

from data import ObjectData, ModelData, FaceData, ModelSection


class Matrix:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        # noinspection PyTypeChecker
        self.array: List[List[FaceData]] = [[None for x in range(rows)] for y in range(cols)]

    def __getitem__(self, key: Tuple[int, int]) -> FaceData:
        if key[0] >= self.rows or key[1] >= self.cols:
            raise IndexError()
        return self.array[key[0]][key[1]]

    def __setitem__(self, key: Tuple[int, int], value: FaceData):
        if key[0] >= self.rows or key[1] >= self.cols:
            return IndexError()
        self.array[key[0]][key[1]] = value


class ModelUtil:
    HUE_OFFSET = (.5 / 64.0)
    SATURATION_OFFSET = (.5 / 8.0)
    # base x/y values for a 1:1 ratio
    BASE_SIZE = (128, 128)

    @staticmethod
    def rgbIntToColor(color: int) -> Tuple[int, int, int]:
        red = (color & 0xff0000) >> 16
        green = (color & 0x00ff00) >> 8
        blue = color & 0x0000ff
    
        return red, green, blue
    
    @staticmethod
    def hslIntToColor(color: int) -> Tuple[int, int, int]:
        return ModelUtil.rgbIntToColor(ModelUtil.hslIntToRgbInt(color))
    
    @staticmethod
    def rgbFloatsToRgbInt(r: float, g: float, b: float):
        return int(r * 256) << 16 | int(g * 256) << 8 | int(b * 256)
    
    @staticmethod
    def unpackHue(hsl: int):
        return (hsl >> 10) & 63
    
    @staticmethod
    def unpackSaturation(hsl: int):
        return (hsl >> 7) & 7
    
    @staticmethod
    def unpackLuminance(hsl: int):
        return hsl & 127
    
    @staticmethod
    def hslIntToRgbInt(hsl: int):
        hue = ModelUtil.unpackHue(hsl) / 64 + ModelUtil.HUE_OFFSET
        saturation = ModelUtil.unpackSaturation(hsl) / 8 + ModelUtil.SATURATION_OFFSET
        luminance = ModelUtil.unpackLuminance(hsl) / 128
    
        chroma = (1.0 - abs((2.0 * luminance) - 1.0)) * saturation
        x = chroma * (1 - abs(((hue * 6.0) % 2.0) - 1.0))
        lightness = luminance - (chroma / 2)
    
        r = lightness
        g = lightness
        b = lightness
        switcher = int(hue * 6.0)
        if switcher == 0:
            r += chroma
            g += x
        elif switcher == 1:
            g += chroma
            r += x
        elif switcher == 2:
            g += chroma
            b += x
        elif switcher == 3:
            b += chroma
            g += x
        elif switcher == 4:
            b += chroma
            r += x
        else:
            r += chroma
            b += x
    
        rgb = ModelUtil.rgbFloatsToRgbInt(r, g, b)
    
        if rgb == 0:
            rgb = 1
    
        return rgb

    @staticmethod
    def getFacesBetweenPoints(min_points: Tuple[int, int], max_points: Tuple[int, int], face_matrix: Matrix) -> List[FaceData]:
        faces = []
        for x in range(min_points[0], max_points[0] + 1):
            for y in range(min_points[1], max_points[1] + 1):
                if face_matrix[x, y] is not None:
                    faces.append(face_matrix[x, y])
        return faces

    @staticmethod
    def getScaledFaceSections(object_data: ObjectData, model_data: ModelData, scale_factor: int = 1) -> List[ModelSection]:
        size = (ModelUtil.BASE_SIZE[0] / scale_factor, ModelUtil.BASE_SIZE[1] / scale_factor)
        # How many blocks will be required for this block based on the scaled size
        blocks_x = int(object_data.modelSizeX / size[0])
        blocks_y = int(object_data.modelSizeY / size[1])
        sections = []

        # Store all the faces in a matrix so we don't have to loop each time
        faces = Matrix(object_data.modelSizeX + 1, object_data.modelSizeY + 1)
        for i in range(model_data.faceCount):
            # abs as inward facing faces aren't useful
            idx = abs(model_data.faceVertexIndices1[i])
            idy = abs(model_data.faceVertexIndices2[i])
            x = model_data.vertexPositionsX[idx]
            y = model_data.vertexPositionsY[idy]
            face_data = faces[x, y]
            priority = model_data.faceRenderPriorities[i]
            if face_data is not None and face_data.priority <= priority:
                continue
            faces[x, y] = FaceData(priority, idx)

        for x in range(blocks_x):
            for y in range(blocks_y):
                section_mins = (int(size[0] * x), int(size[1] * y))
                max_x = int(min(section_mins[0] + size[0], object_data.modelSizeX))
                max_y = int(min(section_mins[1] + size[1], object_data.modelSizeY))
                section = ModelSection(x, y, ModelUtil.getFacesBetweenPoints(section_mins, (max_x, max_y), faces))
                sections.append(section)

        return sections

    @staticmethod
    def averageColorInSection(model: ModelData, section: ModelSection) -> Tuple[int, int, int]:
        face_count = len(section.faces)
        r, g, b = 0, 0, 0

        if face_count <= 0:
            return r, g, b

        for idx in range(face_count):
            hsl_color = model.faceColors[section.faces[idx].idx]
            rgb_tuple = ModelUtil.hslIntToColor(hsl_color)
            r += rgb_tuple[0]
            g += rgb_tuple[1]
            b += rgb_tuple[2]

        return max(int(r / face_count), 0), max(int(g / face_count), 0), max(int(b / face_count), 0)
