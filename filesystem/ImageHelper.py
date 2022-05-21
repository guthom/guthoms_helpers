import sys, os
import json
import pickle
import cv2
from typing import Dict

from guthoms_helpers.filesystem.FileHelper import FileHelper

class ImageHelper(object):

    @staticmethod
    def OpenImage(path, mode:str = "rgb"):
        if not FileHelper.FileExists(path):
            raise Exception("Image file does not Exist!")

        img = cv2.imread(path)

        if mode == "rgb" or "RGB":
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        elif mode == "bgr" or "BGR":
            pass
        else:
            raise Exception("Can't convert image to the given color format!")

        return img

