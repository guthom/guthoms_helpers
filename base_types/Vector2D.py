from guthoms_helpers.base_types.VectorBase import VectorBase
from typing import List, Dict, Tuple
import math


class Vector2D(VectorBase):

    x: float = None
    y: float = None

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

        super().__init__()

    def __getitem__(self, item):

        if item == 0:
            return self.x

        if item == 1:
            return self.y

        if item > 1:
            raise Exception("Vector 2D only has x, -> 2 elements!")

    def __setitem__(self, item):

        if item == 0:
            self.x = item

        if item == 1:
            self.y = item

        if item > 1:
            raise Exception("Vector 2D only has x, -> 2 elements!")

    @classmethod
    def Zero(cls):
        return cls(0.0, 0.0)

    @classmethod
    def fromList(cls, list: List[float]):
        return cls(list[0], list[1])

    @classmethod
    def fromDict(cls, dict: Dict):
        return cls(float(dict["x"]), float(dict["y"]))

    def Normalized(self) -> 'Vector2D':
        d = math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))
        x = self.x / d
        y = self.y / d

        return Vector2D(x, y)

    def NormalizedToBaseSize(self, baseSize: Tuple[int, int]) -> 'Vector2D':
        x = self.x / baseSize[0]
        y = self.y / baseSize[1]

        return Vector2D(x, y)

    def toString(self) -> str:
        return "[" + str(self.x) + ", " + str(self.y) + "]"

    def toList(self) -> List[float]:
        return [self.x, self.y]

    def Rounded(self, decimals: int = 2):
        raise Exception("Not Implemented!")

    def AsType(self, type: type):
        raise Exception("Not Implemented!")