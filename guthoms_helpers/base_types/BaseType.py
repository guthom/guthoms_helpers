from abc import ABC, abstractmethod
import numpy as np
from typing import List, Dict

class BaseType(ABC):

    @abstractmethod
    def toList(self) -> List[float]:
        raise Exception("Not Implemented!")

    @abstractmethod
    def toString(self) -> str:
        raise Exception("Not Implemented!")

    def __repr__(self):
        return self.toString()

    def __str__(self):
        return str(self.toList())

    def toNp(self) -> np.array:
        return np.array(np.array(self.toList()))

    def __eq__(self, other):
        return self.toList() == other.toList()

    @classmethod
    def FromInstance(cls, other: 'BaseType'):
        return cls.fromList(other.toList())

    @abstractmethod
    def Rounded(self, decimals: int = 2):
        raise Exception("Not Implemented!")

    @abstractmethod
    def AsType(self, type: type):
        raise Exception("Not Implemented!")

    @classmethod
    @abstractmethod
    def fromList(cls, list: List[float]):
        raise Exception("Not Implemented!")

    @classmethod
    @abstractmethod
    def fromDict(cls, dict: Dict):
        raise Exception("Not Implemented!")

