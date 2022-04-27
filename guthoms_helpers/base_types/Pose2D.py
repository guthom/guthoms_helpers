from guthoms_helpers.base_types.PoseBase import PoseBase
from guthoms_helpers.base_types.Vector2D import Vector2D
from guthoms_helpers.base_types.Rotation2D import Rotation2D
from guthoms_helpers.base_types.Quaternion import Quaternion
from guthoms_helpers.base_types.ILieGroupAssociated import ILieGroupAssociated

from typing import List, Dict, Tuple

import numpy as np

class Pose2D(PoseBase, ILieGroupAssociated):
    def __init__(self, trans: Vector2D, angle: Rotation2D = Rotation2D(0.0), visible: bool = True):
        super().__init__(trans, angle, visible)

    def __getitem__(self, item):

        if item == 0:
            return self.trans.x

        if item == 1:
            return self.trans.y

        if item == 2:
            return self.rotation.angle

        if item > 2:
            raise Exception("Pose 2D only has x, y, angle -> 3 elements!")

    def __setitem__(self, item):

        if item == 0:
            self.trans.x = item

        if item == 1:
            self.trans.y = item

        if item == 2:
            self.rotation = item

        if item > 2:
            raise Exception("Pose 2D only has x, y, angle -> 3 elements!")

    @staticmethod
    def GetGenerators():
        g0 = np.array([
            [0.0, 0.0, 1.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0]
        ])

        g1 = np.array([
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 0.0, 0.0]
        ])

        g2 = np.array([
            [0.0, -1.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0]
        ])

        return [g0, g1, g2]

    def GetLieElements(self) -> np.array:
        """returns the elements used for the lie group representation"""
        return [self.trans.x, self.trans.y, self.rotation.angle]

    @staticmethod
    def SplitMats(mat: np.array) -> Tuple[np.array, np.array]:
        rot = mat[:2, :2]
        trans = np.array([mat[0, 2], mat[1, 2]])
        return rot, trans

    @staticmethod
    def Log(mat: np.array) -> np.array:
        """The logarithmic map maps a group element to the corresponding skew matrix (tangent space)"""
        rotMat, transVec = Pose2D.SplitMats(mat)
        theta = Rotation2D.Vee(Rotation2D.Log(rotMat))[0]
        Vinv = theta / (np.power(np.sin(theta), 2) + (np.power(1 - np.cos(theta), 2)))

        Vinv *= np.array(
            [
                [np.sin(theta), 1 - np.cos(theta)],
                [-1 + np.cos(theta), np.sin(theta)]
            ])

        t = np.matmul(Vinv, transVec)

        return Pose2D.Hat(np.array([t[0], t[1], theta]))


    @staticmethod
    def LogFromElement(element: 'ILieGroupAssociated') -> np.array:
        """The logarithmic map maps a group element to the corresponding skew matrix (tangent space)"""
        raise Exception("Not Implemented!")

    @staticmethod
    def Exp(skewMat: np.array) -> np.array:
        """The exponential map maps a skew symmetric matrix to a corresponding group element"""
        # handle skew of so2 seperate
        rotSkew, transSkew = Pose2D.SplitMats(skewMat)

        # handle Translation part
        theta = Rotation2D.Vee(Rotation2D.Log(Rotation2D.Exp(rotSkew)))[0]

        V = np.array([
            [np.sin(theta), -1 + np.cos(theta)],
            [1 - np.cos(theta), np.sin(theta)]
        ]) / theta

        #transSkew = np.matmul(V, transSkew)
        transSkew = np.matmul(V, transSkew.transpose())

        rotExp = Rotation2D.Exp(rotSkew)

        mat = np.array([
            [rotExp[0, 0], rotExp[0, 1], transSkew[0]],
            [rotExp[1, 0], rotExp[1, 1], transSkew[1]],
            [0.0, 0.0, 1.0]
        ])
        return mat

    @staticmethod
    def ExpToElement(skewMat: np.array) -> 'ILieGroupAssociated':
        """The exponential map maps a skew symmetric matrix to a corresponding group element"""
        vector = Pose2D.Vee(skewMat)
        return


    @staticmethod
    def Vee(mat: np.array) -> np.array:
        """The Vee operator maps the skew symmetric matrix to the its corresponding corresponding group
        element(~ the inverse of Hat)"""
        return np.array([mat[0, 2], mat[1, 2], mat[1, 0]])

    @staticmethod
    def VeeToElement(mat: np.array) -> 'ILieGroupAssociated':
        """The Vee operator maps the skew symmetric matrix to the its corresponding corresponding group
        element(~ the inverse of Hat)"""
        params = Pose2D.Vee(mat)
        raise Pose2D(Vector2D(params[0], params[1]), Rotation2D(angle=params[2]))

    @staticmethod
    def Hat(element: np.array) -> np.array:
        """The Hat operator maps an origin group element to the corresponding skew matrix"""
        gens = Pose2D.GetGenerators()
        ret = np.zeros((3, 3))

        for i in range(0, gens.__len__()):
            ret += element[i] * gens[i]

        return ret

    def Adjoint(self, other: 'ILieGroupAssociated') -> np.array:
        """used to transform an element from one tangent space of an element into the tangent space of another """
        raise Exception("Not Implemented!")

    def Jacobian(self) -> np.array:
        """gives the differentiation of the group element"""
        raise Exception("Not Implemented!")

    @classmethod
    def fromDict(cls, data: Dict[str, Dict], visible: bool = True):
        trans = Vector2D.fromDict(data["translation"])
        rotation = Rotation2D.fromDict(data["rotation"])
        return cls(trans, rotation, visible=visible)

    @classmethod
    def fromData(cls, x: float, y: float, angle: float, visible: bool = True):
        trans = Vector2D(x=x, y=y)
        rotation = Rotation2D(angle)
        return cls(trans=trans, angle=rotation, visible=visible)

    @classmethod
    def fromList(cls, list: List[List[float]], visible: bool = True):
        trans = Vector2D.fromList(list[0])
        rotation = Rotation2D.fromList(list[1])
        return cls(trans=trans, angle=rotation, visible=visible)

    def Rounded(self, decimals: int = 2):
        return Pose2D.fromData(x=round(self.trans[0], decimals), y=round(self.trans[1], decimals),
                               angle=round(self.rotation.angle, decimals))

    def AsType(self, type: type):
        if type == float:
            return self

        if type == int:
            pose = self.Rounded(decimals=0)
            return Pose2D.fromData(int(self.trans.x), int(self.trans.y), int(self.rotation.angle))

        raise Exception("Type is not yet supported!")

    def IsVisible(self):
        if not self.visible or self.trans[0] == -1 or self.trans[1] == -1:
            return False
        else:
            return True

    def toString(self) -> str:
        return "[" + self.trans.toString() + str(self.rotation.toString()) + "]"

    def toList(self) -> List[List[float]]:
        return [self.trans.toList(), self.rotation.toList()]

    def toNp(self) -> np.array:
        return np.array([self.trans.toNp(), self.rotation.toNp()])

    def to3x3(self) -> np.matrix:
        R = self.rotation.GetRotM()
        t = self.trans.toNp()

        M = np.array([
            [R[0, 0], R[0, 1], t[0]],
            [R[1, 0], R[1, 1], t[1]],
            [0.0, 0.0, 1.0]
        ])

        return M


