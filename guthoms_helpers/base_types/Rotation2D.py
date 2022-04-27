from guthoms_helpers.base_types.RotationBase import RotationBase
from guthoms_helpers.base_types.Vector2D import Vector2D
from guthoms_helpers.base_types.Complex import Complex

from guthoms_helpers.base_types.ILieGroupAssociated import ILieGroupAssociated
import math
import numpy as np
from typing import List, Dict, Tuple, Optional


class Rotation2D(RotationBase, ILieGroupAssociated):
    pi1_4: float = np.pi / 4
    pi1_2: float = np.pi / 2
    pi3_4: float = 3 * pi1_4

    def __init__(self, angle: float):
        super().__init__()

        self.angle = angle

    def __add__(self, other: 'Rotation2D') -> 'Rotation2D':
        return Rotation2D(other.angle + self.angle)

    def __sub__(self, other: 'Rotation2D') -> 'Rotation2D':
        return Rotation2D(other.angle + self.angle)

    @staticmethod
    def GetGenerators():
        g0 = np.array([
            [0.0, -1.0],
            [1.0, 0.0]
        ])
        return [g0]

    def GetLieElements(self) -> np.array:
        """returns the elements used for the lie group representation"""
        return [self.angle]

    @staticmethod
    def Log(mat: np.array) -> np.array:
        """The logarithmic map maps a group element to the corresponding skew matrix (tangent space)"""
        omega = np.arctan2(mat[1, 0], mat[0, 0])
        return Rotation2D.Hat(omega)

    @staticmethod
    def LogFromElement(element: 'Rotation2D') -> np.array:
        """The logarithmic map maps a group element to the corresponding skew matrix (tangent space)"""
        rotM = element.GetRotM()
        return Rotation2D.Log(rotM)

    @staticmethod
    def Exp(skewMat: np.array) -> np.array:
        """The exponential map maps a skew symmetric matrix to a corresponding group element"""
        #tayler series expansion ends up in a simple rot matrix
        x = Rotation2D.Vee(skewMat)[0]
        return np.array(
            [
                [np.cos(x), - np.sin(x)],
                [np.sin(x), np.cos(x)]
            ])

    @staticmethod
    def ExpToElement(skewMat: np.array) -> 'Rotation2D':
        """The exponential map maps a skew symmetric matrix to a corresponding group element"""
        rotMat = Rotation2D.Exp(skewMat)
        return Rotation2D.fromRotM(rotMat)

    @staticmethod
    def Vee(mat: np.array) -> np.array:
        """The Vee operator maps the skew symmetric matrix to the its corresponding corresponding group
        element(~ the inverse of Hat)"""
        return np.array([mat[1, 0]])

    @staticmethod
    def VeeToElement(mat: np.array) -> 'Rotation2D':
        """The Vee operator maps the skew symmetric matrix to the its corresponding corresponding group
        element(~ the inverse of Hat)"""
        element = Rotation2D.Vee(mat)
        return Rotation2D(angle=float(element))

    @staticmethod
    def Hat(element: np.array) -> np.array:
        """The Hat operator maps an origin group element to the coresponding skew matrix"""
        return Rotation2D.GetGenerators()[0] * element

    def Adjoint(self, other: 'ILieGroupAssociated') -> np.array:
        """used to transform an element from one tangent space of an element into the tangent space of another """
        # in So2 we simply talk about the identity
        raise np.identity(2)

    def Jacobian(self) -> np.array:
        """gives the differentiation of the group element"""
        raise Exception("Not Implemented!")

    def ToComplex(self) -> Complex:
        # radius is set to 1.0 for the complex representation

        real = math.cos(self.angle)
        i = math.sin(self.angle)

        return Complex(real, i)

    def GetRotM(self) -> np.array:
        row0 = [math.cos(self.angle), -math.sin(self.angle)]
        row1 = [math.sin(self.angle), math.cos(self.angle)]

        rotM = []
        rotM.append(row0)
        rotM.append(row1)

        return np.array(rotM)

    def Distance(self, other: 'Rotation2D') -> float:
        diff = math.atan2(math.sin(self.angle - other.angle), math.cos(self.angle - other.angle))

        return diff

    def DistanceNorm(self, other: 'Rotation2D') -> float:
        return self.Distance(other)

    @classmethod
    def Empty(cls) -> 'Rotation2D':
        return Rotation2D(0.0)

    @classmethod
    def From2Vectors(cls, vec1: Vector2D, vec2: Vector2D, yUp:bool = False, fullRange: bool = False) -> 'Rotation2D':

        resVec = vec2 - vec1

        resAngle = math.atan2(resVec[1], resVec[0])

        if yUp:
            resAngle += cls.pi1_2

        if fullRange:
            raise Exception("Not Implemented!")

        return Rotation2D(resAngle)

    @classmethod
    def fromRotM(cls, rotM: np.array):
        return cls(math.atan2(rotM[1, 0], rotM[0, 0]))

    @classmethod
    def fromList(cls, newList: List[float]):
        return cls(newList[0])

    @classmethod
    def fromDict(cls, dict: Dict):
        return cls(dict["rotation"])



    def Deg(self):
        return self.RadToDeg(self.angle)

    def toString(self) -> str:
        return str(self.angle)

    def toList(self) -> List[float]:
        return [self.angle]

    def Rounded(self, decimals: int = 2):
        raise Exception("Not Implemented!")

    def AsType(self, type: type):
        raise Exception("Not Implemented!")
