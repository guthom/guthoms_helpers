from typing import List, Dict, Tuple, Optional
from guthoms_helpers.base_types.BaseType import BaseType
import math
import numpy as np

class RotationMatrix(BaseType):

    def __init__(self, rotM: np.array, order: str="xyz"):
        self.rotM = rotM
        self.order = order

        super().__init__()

    def __mul__(self, other: 'RotationMatrix'):
        retRotM = np.matmul(self.rotM, other.rotM)
        return RotationMatrix(retRotM, self.order)

    @classmethod
    def fromList(cls, list: List[float]):
        if list.__len__() != 9:
            raise Exception("List size is not correct! Should be 9 instead of : " + str(list.__len__()))

        return cls(np.array(list))

    @classmethod
    def fromQuat(cls, quat: 'Quaternion', order="xyz"):
        rotM = cls.RotMFromQuat(quat)
        return cls(rotM, order=order)

    @classmethod
    def fromEulerAngles(cls, eulerAng: 'EulerAngles', order="xyz"):
        rotM = cls.RotMFromEulerAngles(eulerAng, order)
        return cls(rotM, order=order)

    @classmethod
    def fromDict(cls, dict: Dict):
        raise Exception("Not Implemented!")

    @staticmethod
    def RotMFromQuat(quat: 'Quaternion') -> np.array:
        w = quat.w
        x = quat.x
        y = quat.y
        z = quat.z

        row0 = [w*w + x*x - y*y - z*z, 2*(x*y - w*z), 2*(z*x + w*y)]
        row1 = [2*(x*y + w*z), w*w - x*x + y*y - z*z, 2*(y*z - w*x)]
        row2 = [2*(z*x - w*y), 2*(y*z + w*x), w*w - x*x - y*y + z*z]

        rotM = []
        rotM.append(row0)
        rotM.append(row1)
        rotM.append(row2)

        return np.array(rotM)

    @staticmethod
    def RotMFromEulerAngles(eulerAng: 'EulerAngles', order: str="xyz") -> np.array:
        from math import cos, sin
        args = eulerAng.toList()
        Rs = []
        orderList = list(order)
        for i in range(0, orderList.__len__()):
            if order[i] == 'x':
                Rs.append(RotationMatrix.rotXAxis(args[0]))
            if order[i] == 'y':
                Rs.append(RotationMatrix.rotYAxis(args[1]))
            if order[i] == 'z':
                Rs.append(RotationMatrix.rotZAxis(args[2]))

        M = np.matmul(np.matmul(Rs[0], Rs[1]), Rs[2])

        return M

    def toString(self) -> str:
        return str(self.rotM)

    def toList(self) -> List[float]:
        return self.rotM.tolist()

    def get4x4(self) ->  np.array:
        tempMatrix = np.zeros((4, 4))
        tempMatrix[0:3, 0:3] = self.rotM
        tempMatrix[3, 3] = 1.0
        M = tempMatrix
        return np.array(M)

    @staticmethod
    def rotZAxis(angle: float) -> np.array:
        Rz =  np.array([
            [math.cos(angle), -math.sin(angle), 0],
            [math.sin(angle), math.cos(angle), 0],
            [0.0, 0.0, 1.0]
        ])
        return Rz

    @staticmethod
    def rotXAxis(angle: float) -> np.array:
        Rx =  np.array([
            [1.0, 0.0, 0.0],
            [0.0, math.cos(angle), -math.sin(angle)],
            [0.0, math.sin(angle), math.cos(angle)]
        ])
        return Rx

    @staticmethod
    def rotYAxis(angle: float) -> np.array:
        Ry =  np.array([
            [math.cos(angle), 0.0, math.sin(angle)],
            [0.0, 1.0, 0.0],
            [-math.sin(angle), 0.0, math.cos(angle)]
        ])
        return Ry

    def Rounded(self, decimals: int = 2):
        raise Exception("Not Implemented!")

    def AsType(self, type: type):
        raise Exception("Not Implemented!")