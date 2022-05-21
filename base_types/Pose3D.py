from guthoms_helpers.base_types.PoseBase import PoseBase
from guthoms_helpers.base_types.Vector3D import Vector3D
from guthoms_helpers.base_types.Rotation3D import Rotation3D
from guthoms_helpers.base_types.EulerAngles import EulerAngles
from guthoms_helpers.base_types.Quaternion import Quaternion
from guthoms_helpers.base_types.ILieGroupAssociated import ILieGroupAssociated

from typing import List, Dict, Tuple

import numpy as np

class Pose3D(PoseBase, ILieGroupAssociated):

    def __init__(self, trans: Vector3D, quat: Rotation3D, visible: bool = True):
        super().__init__(trans, quat, visible)

    def __getitem__(self, item):

        if item == 0:
            return self.trans.x
        if item == 1:
            return self.trans.y
        if item == 2:
            return self.trans.z

        if item == 3:
            return self.rotation.quat.x
        if item == 4:
            return self.rotation.quat.y
        if item == 5:
            return self.rotation.quat.z
        if item == 6:
            return self.rotation.quat.w

        if item > 2:
            raise Exception("Pose 3D only has x, y, z, qx, qy, qz, qw -> 7 elements!")

    def __getitem__(self, item):

        if item == 0:
            self.trans.x = item
        if item == 1:
            self.trans.y = item
        if item == 2:
            self.trans.z = item

        if item == 3:
            self.rotation.quat.x = item
        if item == 4:
            self.rotation.quat.y = item
        if item == 5:
            self.rotation.quat.z = item
        if item == 6:
            self.rotation.quat.w = item

        if item > 2:
            raise Exception("Pose 3D only has x, y, z, qx, qy, qz, qw -> 7 elements!")

    @classmethod
    def fromDict(cls, data: Dict[str, Dict], visible: bool = True):
        trans = Vector3D.fromDict(data["translation"])
        quat = Rotation3D.fromDict(data["rotation"])
        return cls(trans, quat, visible=visible)

    @staticmethod
    def GetGenerators():
        g0 = np.array([
            [0.0, 0.0, 0.0, 1.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0]
        ])

        g1 = np.array([
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0]
        ])

        g2 = np.array([
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
            [0.0, 0.0, 0.0, 0.0]
        ])


        g3 = np.array([
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, -1.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0]
        ])


        g4 = np.array([
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0]
        ])


        g5 = np.array([
            [0.0, -1.0, 0.0, 0.0],
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0]
        ])

        return [g0, g1, g2, g3, g4, g5]

    def GetLieElements(self) -> np.array:
        """returns the elements used for the lie group representation"""
        euler = self.rotation.euler.toList()
        return np.array([self.trans[0], self.trans[1], self.trans[2], euler[0], euler[1], euler[2]])

    @staticmethod
    def Log(mat: np.array) -> np.array:
        """The logarithmic map maps a group element to the corresponding skew matrix (tangent space)"""
        rotMat, transVec = Pose3D.SplitMats(mat)

        rotSkew = Rotation3D.Log(rotMat)
        # theta is the squared norm of the angle vectors of rotSkew
        rotParams = Rotation3D.Vee(rotSkew)
        theta = np.linalg.norm(rotParams)

        w2 = np.linalg.matrix_power(rotSkew, 2) # omaga_x²
        theta_2 = theta/2

        i_3 = np.identity(3)
        A = 1 - (theta*(np.cos(theta_2)) / (2*np.sin(theta_2)))
        # alternative equation
        #A = 1 - ((theta * np.sin(theta)) / (2*(1 - np.cos(theta))))

        Vinv = i_3 - 0.5*rotSkew + (1/np.power(theta, 2)) * A * w2
        transSkew = np.matmul(Vinv, transVec)

        ret = np.zeros((4, 4))
        ret[:3, :3] = rotSkew
        ret[0:3, 3] = transSkew
        return ret

    @staticmethod
    def LogFromElement(element: 'Pose3D') -> np.array:
        """The logarithmic map maps a group element to the corresponding skew matrix (tangent space)"""


    @staticmethod
    def SplitMats(mat: np.array) -> Tuple[np.array, np.array]:
        rot = mat[:3, :3]
        trans = np.array([mat[0, 3], mat[1, 3], mat[2, 3]])
        return rot, trans

    @staticmethod
    def Exp(skewMat: np.array) -> np.array:
        """The exponential map maps a skew symmetric matrix to a corresponding group element"""
        rotSkew, transSkew = Pose3D.SplitMats(skewMat)
        rotParams = Rotation3D.Vee(rotSkew)
        theta = np.linalg.norm(rotParams)

        i_3 = np.identity(3)
        A = (1 - np.cos(theta)) / np.power(theta, 2)
        B = (theta - np.sin(theta)) / np.power(theta, 3)
        V = i_3 + A * rotSkew + B * np.linalg.matrix_power(rotSkew, 2)

        ret = np.zeros((4, 4))
        expRot = Rotation3D.Exp(rotSkew)
        expT = np.matmul(V, transSkew)
        ret[:3, :3] = expRot
        ret[0:3, 3] = expT
        ret[3, 3] = 1.0
        return ret

    @staticmethod
    def ExpToElement(skewMat: np.array) -> 'Pose3D':
        """The exponential map maps a skew symmetric matrix to a corresponding group element"""
        transMat = Pose3D.Log(skewMat)
        rot, trans = Pose3D.SplitMats(transMat)
        rotation = Rotation3D.fromRotationMatrix(rot)
        translation = Vector3D.fromList(trans)
        return Pose3D(trans=translation, quat=rotation)

    @staticmethod
    def Vee(mat: np.array) -> np.array:
        """The Vee operator maps the skew symmetric matrix to the its corresponding corresponding group
        element(~ the inverse of Hat)"""
        return np.array([mat[0, 3], mat[1, 3], mat[2, 3], mat[2, 1], mat[0, 2], mat[1, 0]])

    @staticmethod
    def VeeToElement(mat: np.array) -> 'Pose3D':
        """The Vee operator maps the skew symmetric matrix to the its corresponding corresponding group
        element(~ the inverse of Hat)"""
        raise Exception("Not Implemented!")

    @staticmethod
    def Hat(element: np.array) -> np.array:
        """The Hat operator maps an origin group element to the coresponding skew matrix"""
        gens = Pose3D.GetGenerators()
        ret = np.zeros((4, 4))

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
    def fromList(cls, list: List[List[float]], visible: bool = True):
        trans = Vector3D.fromList(list[0])
        quat = Rotation3D.fromQuat(Quaternion.fromList(list[1]))
        return cls(trans=trans, quat=quat, visible=visible)

    def toOpenCvTvecRvec(self) -> Tuple[np.array, np.array]:
        raise Exception("Not Implemented!")
        rvec = None
        tvec = None
        return rvec, tvec

    def toString(self) -> str:
        return "[" + self.trans.toString() + self.rotation.toString() + "]"

    def toList(self) -> List[List[float]]:
        return [self.trans.toList(), self.rotation.quat.toList()]

    def toNp(self) -> np.array:
        return np.array(self.trans.toNp(), self.rotation.toNp())

    def to4x4(self) -> np.array:
        R = self.rotation.rotM.rotM
        t = self.trans.toNp()

        ret = np.zeros((4, 4))
        ret[:3, :3] = R
        ret[0:3, 3] = t
        ret[3, 3] = 1.0

        return ret

    def Rounded(self, decimals: int = 2):
        raise Exception("Not Implemented!")

    def AsType(self, type: type):
        raise Exception("Not Implemented!")
