import numpy as np
from typing import Tuple, Optional
import cv2
import math


class VisionData(object):

    def __init__(self, data: np.array, paddingValue: float=0.0):
        self.data = data
        self.paddingValue = paddingValue
        self.originSize = data.shape
        self.addedPadding: Optional[Tuple] = None


    def ResizeData(self, target_size: Tuple):
        """If width or height of tuple (w, h) is None resize will be performed by respecting aspect ratio."""
        if self.addedPadding is not None:
            raise Exception("ResizeData: The data is padded and can not be resized. " + 
                                "Remove padding, resize and add desired padding afterwards again.")
        if target_size[0] is None and target_size[1] is None:
            raise Exception("ResizeData: Error: Width and height is None.")
        if target_size[0] is None:
            target_size = (self.data.shape[1] / self.data.shape[0] * target_size[1], target_size[1])
        if target_size[1] is None:
            target_size = (target_size[0], self.data.shape[0] / self.data.shape[1] * target_size[0])
        self.data = cv2.resize(self.data, tuple(np.rint(target_size).astype(np.int)))

    def PaddData(self, target_size: Tuple):
        padding_x = target_size[0] - self.data.shape[1]
        padding_y = target_size[1] - self.data.shape[0]
        if padding_x < 0 or padding_y < 0:
            raise Exception("PaddData: target_size " + str(target_size) + " is smaller than actual image size (" + 
                            str(self.data.shape[1]) + ", " + str(self.data.shape[1]) + ").")
        else:
            # Padding top, bottom, left, right
            self.addedPadding = (math.floor(padding_y / 2), math.ceil(padding_y / 2),
                                 math.floor(padding_x / 2), math.ceil(padding_x / 2))

            self.data = cv2.copyMakeBorder(src=self.data, dst=self.data,
                                           top=self.addedPadding[0], bottom=self.addedPadding[1],
                                           left=self.addedPadding[2], right=self.addedPadding[3],
                                           borderType=cv2.BORDER_CONSTANT, value=self.paddingValue)


    def UnpaddData(self):
        if self.addedPadding is None:
            raise Exception("UnpaddData: Not possible as the data is not padded.")
        self.data = self.data[self.addedPadding[0]:self.data.shape[0] - self.addedPadding[1],
                              self.addedPadding[2]:self.data.shape[1] - self.addedPadding[3]]
        self.addedPadding = None
