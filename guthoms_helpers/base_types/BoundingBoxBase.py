from guthoms_helpers.base_types.BaseType import BaseType
from guthoms_helpers.base_types.VectorBase import VectorBase
from abc import abstractmethod, abstractclassmethod
from typing import List, Tuple
import sys
import numpy as np
import cv2
import matplotlib.patches as patches

class BoundingBoxBase(BaseType):

    def __init__(self, points: List[VectorBase]):
        self.points = points

        self.vectorSize = self.points[0].__len__()
        self.maxIndex = self.points.__len__()*self.vectorSize

        self.size: VectorBase = None
        self.mid: VectorBase = None

        self.SetSize()
        self.SetMid()


    def __getitem__(self, i):
        if i > self.maxIndex:
            raise Exception("Index not supported! Max index is: " + str(self.maxIndex))

        pointIndex = int(i / self.vectorSize)
        restIndex = int(i % self.vectorSize)

        return self.points[pointIndex][restIndex]

    def Move(self, displacement: VectorBase):
        return self.FromMidAndRange(self.mid + displacement, self.size)

    def toList(self) -> List[float]:
        ret = []
        for point in self.points:
            ret.append(point.toList())
        return ret

    @classmethod
    def FromPoints(cls, points: List[VectorBase]) -> "BoundingBoxBase":
        tempList = []

        for vec in points:
            tempList.extend(vec.toList())

        return cls.fromList(tempList)

    def _clip(self, value, clipVal):
        return max(0, min(value, clipVal))

    @abstractmethod
    def DiagLength(self):
        raise Exception("Not Implemented!")

    @abstractclassmethod
    def FromMidAndRange(cls, mid: VectorBase, range: VectorBase) -> "BoundingBoxBase":
        raise Exception("Not Implemented!")

    @abstractclassmethod
    def CreateBoundingBox(cls, keyPoints: List[VectorBase], expandBox= True,
                          max_x_val: int = sys.maxsize, max_y_val: int = sys.maxsize) -> "BoundingBoxBase":
        raise Exception("Not Implemented!")

    @abstractmethod
    def CalculateOpticalFlow(self, target: 'BoundingBoxBase', normalized: bool = True) -> VectorBase:
        raise Exception("Not Implemented!")

    @abstractmethod
    def  GetEdgePoints(self) -> List[VectorBase]:
        raise Exception("Not Implemented!")

    @abstractmethod
    def Clip(self, clipVal: float=1.0):
        raise Exception("Not Implemented!")

    @abstractmethod
    def SetSize(self):
        raise Exception("Not Implemented!")

    @abstractmethod
    def SetMid(self):
        raise Exception("Not Implemented!")

    @abstractmethod
    def ClipToShape(self, shape: Tuple[float]) -> "BoundingBoxBase":
        raise Exception("Not Implemented!")

    @abstractmethod
    def AddPadding(self, padding: Tuple[float]) -> "BoundingBoxBase":
        raise Exception("Not Implemented!")

    @abstractmethod
    def SubstractPadding(self, padding: Tuple[float]) -> "BoundingBoxBase":
        raise Exception("Not Implemented!")

    @abstractmethod
    def ScaleBB(self, scale: VectorBase) -> "BoundingBoxBase":
        raise Exception("Not Implemented!")

    @abstractmethod
    def ExtendBB(self, extension: VectorBase) -> "BoundingBoxBase":
        raise Exception("Not Implemented!")

    @abstractmethod
    def Area(self) -> float:
        raise Exception("Not Implemented!")

    @abstractmethod
    def CalculateOverlapp(self, target: "BoundingBoxBase") -> float:
        raise Exception("Not Implemented!")

    @abstractmethod
    def CalculateIoU(self, target: "BoundingBoxBase") -> float:
        raise Exception("Not Implemented!")