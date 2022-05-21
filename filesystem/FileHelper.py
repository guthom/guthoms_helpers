import sys, os
import json
import pickle
import imagesize
from typing import Dict, List, Union, Tuple

class FileHelper(object):

    @staticmethod
    def FileExists(filePath: str):
        return os.path.isfile(filePath)

    @staticmethod
    def DeleteFile(filePath: str):
        os.remove(filePath)

    @staticmethod
    def DumpDictToFile(jsonDict: Union[Dict, List], filePath: str, append: bool=False):
        jsonString = json.dumps(jsonDict)

        with open(filePath, "w") as text_file:
            if append:
                content = text_file.readlines()
                content += jsonString
            else:
                content = jsonString

            text_file.write(content)

    @staticmethod
    def ReadRawFile(filePath: str) -> str:
        ret = ""

        with open(filePath) as file:
            ret = file.read()

        return ret

    @staticmethod
    def GetFileName(path: str, includeEnding: bool = True) -> str:

        filename = os.path.basename(path)

        if not includeEnding:
            splitname = filename.split(".")
            filename = ""
            for i in range(0, splitname.__len__() - 1):
                filename += splitname[i]

        return filename

    @staticmethod
    def GetFilePath(path: str) -> str:
        return os.path.dirname(path)

    @staticmethod
    def JsonToDict(filePath: str) -> Dict:
        with open(filePath) as file:
            return json.load(file)

    @staticmethod
    def PickleData(data, filePath: str):
        pickle.dump(data, open(filePath, "wb"))

    @staticmethod
    def DePickleData(filePath: str):
        return pickle.load(open(filePath, "rb"))

    @staticmethod
    def GetImageSize(path: str) -> Tuple[int, int]:
        ret = imagesize.get(path)
        return ret