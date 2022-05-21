from typing import List, Dict
from guthoms_helpers.base_types.VectorBase import VectorBase
import math
import numpy as np

class Vector3D(VectorBase):

    x: float = None
    y: float = None
    z: float = None

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

        super().__init__()

    def __getitem__(self, item):

        if item == 0:
            return self.x

        if item == 1:
            return self.y

        if item == 2:
            return self.z

        if item > 2:
            raise Exception("Vector 3D only has x, y, z -> 3 elements!")

    def __setitem__(self, item):

        if item == 0:
            self.x = item

        if item == 1:
            self.y = item

        if item == 2:
            self.z = item

        if item > 2:
            raise Exception("Vector 3D only has x, y, z -> 3 elements!")

    @classmethod
    def Zero(cls):
        return cls(0.0, 0.0, 0.0)

    @classmethod
    def fromList(cls, list: List[float]):
        return cls(list[0], list[1], list[2])

    @classmethod
    def fromDict(cls, dict: Dict):
        return cls(float(dict["x"]), float(dict["y"]), float(dict["z"]))

    def toString(self) -> str:
        return "[" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + "]"

    def toList(self) -> List[float]:
        return [self.x, self.y, self.z]

    def toNp(self) -> np.array:
        return np.array([self.x, self.y, self.z])

    def toNp4(self) -> np.array:
        return np.array([[self.x], [self.y], [self.z], [1.0]])

    def Rounded(self, decimals: int = 2):
        raise Exception("Not Implemented!")

    def AsType(self, type: type):
        raise Exception("Not Implemented!")
