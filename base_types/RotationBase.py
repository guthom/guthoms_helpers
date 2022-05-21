from abc import abstractmethod, abstractclassmethod
from guthoms_helpers.base_types.BaseType import BaseType
from guthoms_helpers.base_types.ILieGroupAssociated import ILieGroupAssociated
from guthoms_helpers.base_types.VectorBase import VectorBase
import numpy as np
from typing import List, Dict, Tuple

class RotationBase(BaseType):

    def __init__(self):
        super().__init__()

    def __len__(self):
        return len(self.toList())

    @abstractmethod
    def __add__(self, other: 'RotationBase') -> 'RotationBase':
        raise Exception("Not Implemented!")

    @abstractmethod
    def __sub__(self, other: 'RotationBase') -> 'RotationBase':
        raise Exception("Not Implemented!")

    @abstractmethod
    def Distance(self, other: 'RotationBase') -> 'RotationBase':
        raise Exception("Not Implemented!")

    @classmethod
    @abstractmethod
    def Empty(cls) -> 'RotationBase':
        raise Exception("Not Implemented!")

    @abstractmethod
    def DistanceNorm(self, other: 'RotationBase') -> float:
        raise Exception("Not Implemented!")

    @classmethod
    @abstractmethod
    def From2Vectors(cls, vec1: VectorBase, vec2: VectorBase, fullRange: bool = False) -> 'RotationBase':
        raise Exception("Not Implemented!")

    @staticmethod
    def DegToRad(deg: float):
        return deg * np.pi / 180

    @staticmethod
    def RadToDeg(rad: float):
        return rad * 180 / np.pi
