from abc import ABC, abstractmethod
from guthoms_helpers.common_stuff.DataBuffer import DataBuffer
import cv2
import numpy as np
from typing import Tuple
class InputProviderBase(ABC):

    def __init__(self, bufferLength: int, useBuffer: bool = False):
        self.useBuffer = useBuffer
        if useBuffer:
            print("Warning! Buffer functionality is still experimental!")

        self.dataBuffer = DataBuffer(bufferLength)

    def __getitem__(self, item):
        return self.GetData(index=item)

    @staticmethod
    def BGRToRGB(image: np.array, targetSize: Tuple[int, int] = None) -> np.array:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if targetSize is not None:
            image = cv2.resize(image, targetSize)

        return image

    @abstractmethod
    def ReInit(self):
        raise Exception("Not Implemented!")

    @abstractmethod
    def __iter__(self):
        raise Exception("Not Implemented!")

    @abstractmethod
    def __len__(self):
        raise Exception("Not Implemented!")

    @abstractmethod
    def finished(self):
        raise Exception("Not Implemented!")

    @abstractmethod
    def GetData(self, index: int = None) -> any:
        raise Exception("Not Implemented!")



