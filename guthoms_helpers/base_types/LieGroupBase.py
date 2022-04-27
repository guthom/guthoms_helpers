from abc import abstractmethod
from typing import List, Dict, Tuple
from guthoms_helpers.base_types.BaseType import BaseType
import math
import numpy as np

class LieGroupBase(BaseType):

    def __init__(self):
        raise Exception("Not Implemented!")

    @abstractmethod
    def exp(self):
        raise Exception("Not Implemented!")

    @abstractmethod
    def log(self):
        raise Exception("Not Implemented!")

    @abstractmethod
    def hat(self):
        raise Exception("Not Implemented!")

    def toList(self) -> List[float]:
        raise Exception("Not Implemented!")

    def toString(self) -> str:
        raise Exception("Not Implemented!")

    def Rounded(self, decimals: int = 2):
        raise Exception("Not Implemented!")

    def AsType(self, type: type):
        raise Exception("Not Implemented!")

    def fromList(cls, list: List[float]):
        raise Exception("Not Implemented!")

    def fromDict(cls, dict: Dict):
        raise Exception("Not Implemented!")


