import sys, os, shutil
from typing import Dict, List

class DirectoryHelper(object):

    @staticmethod
    def GetHomeDir() -> str:
        return os.environ['HOME']

    @staticmethod
    def GetCurrentDir() -> str:
        return os.path.dirname(os.path.realpath(__file__))

    @staticmethod
    def DirExists(dirPath: str) -> str:
        return os.path.isdir(dirPath)

    @staticmethod
    def CreateDirs(dirPath: str):
        os.makedirs(dirPath, exist_ok=True)

    @staticmethod
    def CreateIfNotExist(dirPath: str):
        if not DirectoryHelper.DirExists(dirPath):
            DirectoryHelper.CreateDirs(dirPath)

    @staticmethod
    def ClearDir(dirPath: str):
        shutil.rmtree(dirPath)
        DirectoryHelper.CreateIfNotExist(dirPath)

    @staticmethod
    def ListDirectories(dirPath: str, level: int = 1) -> List[str]:

        ret = []


        dirs = os.walk(dirPath)

        levelCounter = 1
        for dir in dirs:
            if levelCounter > level:
                #break for loop if we reached the max level we want to list
                break

            for subdir in dir[1]:
                ret.append(os.path.join(dir[0], subdir))

            levelCounter += 1

        return ret

    @staticmethod
    def ListDirectoryFiles(dirPath: str, fileEndings: List[str] = None, sort: bool=False, sortKey = None) -> List[str]:
        fileNames = []

        for file in os.listdir(dirPath):
            for ending in fileEndings:
                if file.endswith(ending):
                    fileNames.append(os.path.join(dirPath, file))

        if sort:
            if sortKey is None:
                fileNames = sorted(fileNames)
            else:
                fileNames = sorted(fileNames, key=sortKey)


        return fileNames
