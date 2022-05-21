from abc import abstractmethod
from typing import List, Dict, Tuple
from guthoms_helpers.base_types.BaseType import BaseType
import math
import numpy as np

class Complex(BaseType):

    def __init__(self, r: float, i: float):
        self.r: float = r
        self.i: float = i

    def __add__(self, other: 'Complex') -> 'Complex':
       return Complex(self.r + other.r, self.i + other.i)

    def __sub__(self, other: 'Complex') -> 'Complex':
       return Complex(self.r - other.r, self.i - other.i)

    def __mul__(self, other: 'Complex') -> 'Complex':
        r = self.r * other.r - self.i * other.i
        i = self.r * other.i + self.i * other.r
        return Complex(r, i)

    def __truediv__(self, other: 'Complex') -> 'Complex':

        num_r = self.r * other.r + self.i * other.i
        num_i = self.i * other.r - self.r * other.i
        nom = math.pow(other.r, 2) + math.pow(other.i, 2)

        r = num_r / nom
        i = num_i / nom

        return Complex(r, i)

    def Abs(self) -> float:
        return math.sqrt(math.pow(self.r, 2) + math.pow(self.i, 2))

    def toList(self) -> List[float]:
        return [self.r, self.i]

    def toString(self) -> str:
        raise "r: " + str(self.r) + ", i: " + str(self.i) + "]"

    def Rounded(self, decimals: int = 2):
        raise Exception("Not Implemented!")

    def AsType(self, type: type):
        raise Exception("Not Implemented!")

    def fromList(cls, list: List[float]):
        raise Exception("Not Implemented!")

    def fromDict(cls, dict: Dict):
        raise Exception("Not Implemented!")


