from guthoms_helpers.base_types.BaseType import BaseType
from guthoms_helpers.base_types.OpticalFlow import OpticalFlow
from typing import Tuple
from abc import abstractmethod
import math

class VectorBase(BaseType):

    @abstractmethod
    def __getitem__(self, item):
        raise Exception("Not Implemented!")

    def __len__(self):
        return len(self.toList())

    @classmethod
    @abstractmethod
    def Zero(cls):
        raise Exception("Not Implemented!")

    def CalculateFlow(self, other: 'VectorBase') -> OpticalFlow:
        return OpticalFlow.From2Vectors(self, other)

    def Distance(self, other: 'VectorBase') -> float:

        diff = other - self
        tempList = diff.toList()

        d = 0
        for entry in tempList:
            d += math.pow(entry, 2)

        return float(math.sqrt(d))

    def __add__(self, other: 'VectorBase'):

        tempList = []
        for i in range(0, self.__len__()):
            tempList.append(self[i] + other[i])

        return self.fromList(tempList)

    def __sub__(self, other: 'VectorBase'):
        tempList = []
        for i in range(0, self.__len__()):
            tempList.append(self[i] - other[i])

        return self.fromList(tempList)

    def __mul__(self, other: float):
        tempList = []
        for i in range(0, self.__len__()):
            tempList.append(self[i] * other)

        return self.fromList(tempList)

    def MultiplicateElementwise(self, other: 'VectorBase'):
        tempList = []
        for i in range(0, self.__len__()):
            tempList.append(self[i] * other[i])

        return self.fromList(tempList)

    def __truediv__(self, other: 'VectorBase'):
        tempList = []
        for i in range(0, self.__len__()):
            tempList.append(self[i] / other)

        return self.fromList(tempList)

    def Lengh(self):

        tempList = self.toList()
        d = 0
        for entry in tempList:
            d += math.pow(entry, 2)

        return float(math.sqrt(d))

    def Normalized(self):
        tempList = self.toList()
        length = self.Lengh()
        for i in range(0, len(tempList)):
            tempList[i] /= length

        return self.fromList(tempList)

    def NormalizedWithMax(self, position: 'VectorBase') -> 'VectorBase':

        newList = []
        for i in range(0, self.__len__()):
            newList.append(self[i] / position[i])

        return self.fromList(newList)

