from abc import abstractmethod
from typing import List
from guthoms_helpers.base_types.BaseType import BaseType
import numpy as np

#the final implementation of all LieGrouAssociated are following Ethan Eades technical Report published in
# http://ethaneade.com/lie.pdf

class ILieGroupAssociated(object):


    def GetSkewMatrix(self) -> np.array:
        elements = self.GetLieElements()
        return self.Hat(elements)

    @staticmethod
    @abstractmethod
    def GetGenerators() -> List[np.array]:
        raise Exception("Not Implemented!")

    @abstractmethod
    def GetLieElements(self) -> np.array:
        """returns the elements used for the lie group representation"""
        raise Exception("Not Implemented!")

    @staticmethod
    @abstractmethod
    def Log(mat: np.array) -> np.array:
        """The logarithmic map maps a group element to the corresponding skew matrix (tangent space)"""
        raise Exception("Not Implemented!")

    @staticmethod
    def LogFromElement(element: 'ILieGroupAssociated') -> np.array:
        """The logarithmic map maps a group element to the corresponding skew matrix (tangent space)"""
        raise Exception("Not Implemented!")

    @staticmethod
    @abstractmethod
    def Exp(skewMat: np.array) -> np.array:
        """The exponential map maps a skew symmetric matrix to a corresponding group element"""
        raise Exception("Not Implemented!")

    @staticmethod
    @abstractmethod
    def ExpToElement(skewMat: np.array) -> 'ILieGroupAssociated':
        """The exponential map maps a skew symmetric matrix to a corresponding group element"""
        raise Exception("Not Implemented!")

    @staticmethod
    @abstractmethod
    def Vee(mat: np.array) -> np.array:
        """The Vee operator maps the skew symmetric matrix to the its corresponding corresponding group
        element(~ the inverse of Hat)"""
        raise Exception("Not Implemented!")

    @staticmethod
    @abstractmethod
    def VeeToElement(mat: np.array) -> 'ILieGroupAssociated':
        """The Vee operator maps the skew symmetric matrix to the its corresponding corresponding group
        element(~ the inverse of Hat)"""
        raise Exception("Not Implemented!")

    @staticmethod
    @abstractmethod
    def Hat(element: np.array) -> np.array:
        """The Hat operator maps an origin group element to the coresponding skew matrix"""
        raise Exception("Not Implemented!")

    @abstractmethod
    def Adjoint(self, other: 'ILieGroupAssociated') -> np.array:
        """used to transform an element from one tangent space of an element into the tangent space of another """
        raise Exception("Not Implemented!")

    @abstractmethod
    def Jacobian(self) -> np.array:
        """gives the differentiation of the group element"""
        raise Exception("Not Implemented!")


