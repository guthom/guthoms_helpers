from guthoms_helpers.input_provider.InputProviderBase import InputProviderBase
from guthoms_helpers.filesystem.DirectoryHelper import DirectoryHelper
from guthoms_helpers.common_stuff.DataPreloader import DataPreloader

import cv2
import os
from typing import List

class ImageDirectory(InputProviderBase):

    def __init__(self, dirPath: str, sort: bool = True, fileEnding: List[str] = list([".png", ".jpg"]),
                 preprocessingFunction = None, loop: bool = False, bufferLength: int = 30, useBuffer: bool=False):

        super(ImageDirectory, self).__init__(bufferLength, useBuffer=useBuffer)

        self.dirPath = dirPath
        self.preprocessingFunction = preprocessingFunction
        self.fileList = DirectoryHelper.ListDirectoryFiles(dirPath=dirPath, fileEndings=fileEnding, sort=sort,
                                                           sortKey=lambda f: int(os.path.basename(f).split(".")[0]))
        self.loop = loop
        self.lastIndex = -1

        if self.useBuffer:
            self.dataPreloader = DataPreloader(samples=self.fileList, loadMethod=self.OpenImage,
                                               preprocessFunction=self.preprocessingFunction, keepInMemory=loop)

    def ReInit(self):
        self.lastIndex = -1


    def finished(self):
        if self.lastIndex != self.fileList.__len__()-1:
            return False
        else:
            return True

    @staticmethod
    def OpenImage(path: str):
        img = cv2.imread(path)
        return img

    def GetData(self, index: int = None):

        self.lastIndex += 1

        if index is None:
            index = self.lastIndex

        if self.useBuffer:
            img = self.dataPreloader[index]
        else:
            img = self.OpenImage(self.fileList[index])

        if self.loop:
            if self.lastIndex + 1 >= self.fileList.__len__():
                self.lastIndex = -1

        if self.preprocessingFunction is not None:
            img = self.preprocessingFunction(img)

        return img

    def __len__(self):
        return self.fileList.__len__()

    def __iter__(self):
        raise Exception("Not Implemented!")

