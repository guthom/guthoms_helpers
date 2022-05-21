from guthoms_helpers.base_types.BaseType import BaseType
from guthoms_helpers.base_types.Vector3D import Vector3D
from guthoms_helpers.base_types.Quaternion import Quaternion
from guthoms_helpers.base_types.RotationMatrix import RotationMatrix
from guthoms_helpers.base_types.EulerAngles import EulerAngles
from guthoms_helpers.base_types.AxisAngles import AxisAngles
from guthoms_helpers.base_types.ILieGroupAssociated import ILieGroupAssociated
import numpy as np
from typing import List, Dict, Tuple, Optional

class Rotation3D(BaseType, ILieGroupAssociated):


    def __init__(self, order: str = 'xyz'):
        super().__init__()

        self.quat: Optional[Quaternion] = None
        self.euler: Optional[EulerAngles] = None
        self.rotM: Optional[RotationMatrix] = None
        self.axiAngles: Optional[AxisAngles] = None

        if order not in ["xyz"]:
            raise Exception("This order is not supported yet!")

        self.order = order

    def __add__(self, other: 'Rotation3D') -> 'Rotation3D':
        resQuat = self.quat * other.quat
        return Rotation3D.fromQuat(resQuat)

    def __sub__(self, other: 'Rotation3D') -> 'Rotation3D':
        resQuat = self.quat * other.quat.Inverse()
        return Rotation3D.fromQuat(resQuat)

    @staticmethod
    def GetGenerators():
        g0 = np.array([
            [0.0, 0.0, 0.0],
            [0.0, 0.0, -1.0],
            [0.0, 1.0, 0.0]
        ])

        g1 = np.array([
            [0.0, 0.0, 1.0],
            [0.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0]
        ])

        g2 = np.array([
            [0.0, -1.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0]
        ])

        return [g0, g1, g2]

    def GetLieElements(self) -> np.array:
        """returns the elements used for the lie group representation"""
        return np.array(self.euler.toList())

    @staticmethod
    def Log(mat: np.array) -> np.array:
        """The logarithmic map maps a group element to the corresponding skew matrix (tangent space)"""
        trace = np.trace(mat)
        a = (trace - 1)/2
        omega = np.arccos(a)
        ret = omega/(2*np.sin(omega))*(mat - np.transpose(mat))
        return ret

    @staticmethod
    def LogFromElement(element: 'Rotation3D') -> np.array:
        """The logarithmic map maps a group element to the corresponding skew matrix (tangent space)"""
        return Rotation3D.Log(element.rotM.rotM)

    @staticmethod
    def ExpToElement(skewMat: np.array) -> 'Rotation3D':
        """The exponential map maps a skew symmetric matrix to a corresponding group element"""
        rotMat = Rotation3D.Exp(skewMat)
        return Rotation3D.fromRotationMatrix(RotationMatrix(rotM=rotMat))

    @staticmethod
    def Exp(skewMat: np.array) -> np.array:
        """The exponential map maps a skew symmetric matrix to a corresponding group element"""
        # taylor approx. of the matrix exponation will result in the famous rodriguez formula

        vectors = Rotation3D.Vee(skewMat)

        #omaga is the squared norm of the angle vectors
        omega = np.linalg.norm(vectors)

        i = np.identity(3)

        if omega == 0.0:
            return i

        a = np.sin(omega)/omega * skewMat
        w2 = np.linalg.matrix_power(skewMat, 2)
        b = (1.0 - np.cos(omega)) / np.power(omega, 2) * w2

        ret = i + a + b

        return ret

    @staticmethod
    def Vee(mat: np.array) -> np.array:
        """The Vee operator maps the skew symmetric matrix to the its corresponding corresponding group
        element(~ the inverse of Hat)"""
        return np.array([mat[2, 1], mat[0, 2], mat[1, 0]])

    @staticmethod
    def VeeToElement(mat: np.array) -> 'Rotation3D':
        """The Vee operator maps the skew symmetric matrix to the its corresponding corresponding group
        element(~ the inverse of Hat)"""
        vectors = Rotation3D.Vee(mat)
        return Rotation3D.fromEuler(EulerAngles.fromList(vectors.tolist()))

    @staticmethod
    def Hat(element: np.array) -> np.array:
        """The Hat operator maps an origin group element to the coresponding skew matrix"""
        gens = Rotation3D.GetGenerators()
        ret = np.zeros((3, 3))

        for i in range(0, gens.__len__()):
            ret += element[i] * gens[i]

        return ret

    def Adjoint(self, other: Optional['Rotation3D']) -> np.array:
        """used to transform an element from one tangent space of an element into another,
        in So3 we talk simply talk about the rotation matrix itsel"""
        return other.rotM

    def Jacobian(self) -> np.array:
        raise Exception("Not Implemented!")

    def Distance(self, other: 'Rotation3D') -> 'Rotation3D':
        #find rotation difference by finding the resulting quaternion
        diffQuat = self.quat * other.quat.Inverse()

        return Rotation3D.fromQuat(diffQuat)

    def DistanceNorm(self, other: 'Rotation3D') -> float:
        raise Exception("Not Implemented!")

    @classmethod
    def Empty(cls) -> 'Rotation3D':
        return Rotation3D.fromEuler(EulerAngles(0.0, 0.0, 0.0))

    @classmethod
    def From2Vectors(cls, vec1: Vector3D, vec2: Vector3D, fullRange: bool = False) -> 'Rotation3D':
        raise Exception("Not Implemented!")

    @classmethod
    def fromList(cls, newList: List[float], order="xyz"):
        raise Exception("Not implemented yet!")
        ret = Rotation3D(order=order)
        if len(newList) == 4:
            ret.setxyzw(newList[0], newList[1], newList[2], newList[3])
            return ret
        else:
            raise Exception("List shape is not correct!")

    @classmethod
    def fromQuat(cls, quat: Quaternion, order: str = 'xyz'):
        ret = Rotation3D(order=order)
        ret.setQuat(quat)
        return ret

    @classmethod
    def fromEuler(cls, eulerAng: EulerAngles):
        ret = Rotation3D(order=eulerAng.order)
        ret.setEuler(eulerAng)
        return ret

    @classmethod
    def fromAxisAngles(cls, axisAng: AxisAngles, order: str = 'xyz'):
        ret = Rotation3D(order=order)
        ret.setAxisAngles(axisAng)
        return ret

    @classmethod
    def fromRotationMatrix(cls, rotM: RotationMatrix):
        ret = Rotation3D(order=rotM.order)
        ret.setRotationMatrix(rotM)
        return ret

    @classmethod
    def fromAxisAngles(cls, axisAng: AxisAngles, order: str = 'xyz'):
        ret = Rotation3D(order=order)
        ret.setAxisAngles(axisAng)
        return ret

    @classmethod
    def fromDict(cls, dict: Dict, order: str = 'xyz'):
        ret = Rotation3D(order=order)

        if "x" and "y" and "z" and "w" in dict:
            ret.setQuat(Quaternion(float(dict["x"]), float(dict["y"]), float(dict["z"]), float(dict["w"])))
            return ret

        if "roll" and "pitch" and "yaw" in dict:
            ret.setEuler(EulerAngles(float(dict["roll"]), float(dict["pitch"]), float(dict["yaw"])))
            return ret

        if "rotM" in dict:
            ret.setRotationMatrix(RotationMatrix(dict["rotM"]))
            return ret

    def setAxisAngles(self, axisAng: AxisAngles):
        self.axiAngles = axisAng
        self.quat = Quaternion.fromAxisAngle(axisAng)
        self.rotM = RotationMatrix.fromQuat(self.quat, order=self.order)
        self.euler = EulerAngles.fromRotM(self.rotM, order=self.order)
        pass

    def setQuat(self, quat: Quaternion):
        self.quat = quat
        self.rotM = RotationMatrix.fromQuat(self.quat, order=self.order)
        self.euler = EulerAngles.fromRotM(self.rotM, order=self.order)
        self.axiAngles = AxisAngles.fromQuat(self.quat)

    def setEuler(self, euler: EulerAngles):
        self.euler = euler
        self.rotM = RotationMatrix.fromEulerAngles(euler, order=self.order)
        self.quat = Quaternion.fromEuler(self.euler, order=self.order)
        self.axiAngles = AxisAngles.fromQuat(self.quat)

    def setRotationMatrix(self, rotM: RotationMatrix):
        self.rotM = rotM
        self.euler = EulerAngles.fromRotM(self.rotM, order=self.order)
        self.quat = Quaternion.fromRotM(self.rotM)
        self.axiAngles = AxisAngles.fromQuat(self.quat)

    def toString(self) -> str:
        return self.quat.toString()

    def toList(self) -> List[float]:
        raise Exception("Not Implemented!")

    def distance(self, rotation: 'Rotation3D') -> float:
        raise Exception("Not Implemented!")

    def Rounded(self, decimals: int = 2):
        raise Exception("Not Implemented!")

    def AsType(self, type: type):
        raise Exception("Not Implemented!")