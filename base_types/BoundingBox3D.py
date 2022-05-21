from guthoms_helpers.base_types.BoundingBoxBase import BoundingBoxBase
from guthoms_helpers.base_types.Vector3D import Vector3D
from abc import abstractmethod, abstractclassmethod
from typing import List, Tuple, Dict
import sys
import numpy as np
import cv2
import matplotlib.patches as patches

class BoundingBox3D(BoundingBoxBase):

    def __getitem__(self, i):
        raise Exception("Not Implemented!")

    def FromPoints(cls, points: List[Vector3D]) -> "BoundingBoxBase":
        raise Exception("Not Implemented!")

    def FromMidAndRange(cls, mid: Vector3D, range: Vector3D) -> "BoundingBoxBase":
        raise Exception("Not Implemented!")

    def CreateBoundingBox(cls, keyPoints: List[List[Vector3D]], expandBox=True, max_x_val: int = sys.maxsize,
                          max_y_val: int = sys.maxsize) -> "BoundingBoxBase":
        raise Exception("Not Implemented!")

    def DiagLength(self):
        raise Exception("Not Implemented!")

    def FromList(cls, list: List[Vector3D]) -> "BoundingBoxBase":
        raise Exception("Not Implemented!")

    def GetEdgePoints(self) -> List[Vector3D]:
        raise Exception("Not Implemented!")

    def Clip(self, clipVal: float = 1.0):
        raise Exception("Not Implemented!")

    def SetScale(self):
        raise Exception("Not Implemented!")

    def SetMid(self):
        raise Exception("Not Implemented!")

    def ClipToShape(self, shape: Tuple[float]) -> "BoundingBoxBase":
        raise Exception("Not Implemented!")

    def AddPadding(self, padding: Tuple[float]) -> "BoundingBoxBase":
        raise Exception("Not Implemented!")

    def SubstractPadding(self, padding: Tuple[float]) -> "BoundingBoxBase":
        raise Exception("Not Implemented!")

    def ScaleBB(self, scale: Tuple[float]) -> "BoundingBoxBase":
        raise Exception("Not Implemented!")

    def ExtendBB(self, scale) -> "BoundingBoxBase":
        raise Exception("Not Implemented!")

    def Area(self) -> float:
        raise Exception("Not Implemented!")

    def CalculateOverlapp(self, target: "BoundingBoxBase") -> float:
        raise Exception("Not Implemented!")

    def CalculateIoU(self, target: "BoundingBoxBase") -> float:
        raise Exception("Not Implemented!")

    def toList(self) -> List[float]:
        raise Exception("Not Implemented!")

    def toString(self) -> str:
        raise Exception("Not Implemented!")

    def Rounded(self, decimals: int = 2):
        raise Exception("Not Implemented!")

    def AsType(self, type: type):
        raise Exception("Not Implemented!")

    @classmethod
    def fromList(cls, list: List[float]):
        raise Exception("Not Implemented!")

    @classmethod
    def fromDict(cls, dict: Dict):
        raise Exception("Not Implemented!")
