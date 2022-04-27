import os
from typing import Dict
import unittest
from unittest import TestCase
import numpy as np

from guthoms_helpers.common_stuff.DataPreloader import DataPreloader
from guthoms_helpers.filesystem.DirectoryHelper import DirectoryHelper
from guthoms_helpers.filesystem.FileHelper import FileHelper

class PreloaderTests(TestCase):

    def setUp(self):
        dirName = os.path.dirname(os.path.abspath(__file__))
        dirName = os.path.join(dirName, "test_data", "preloader")

        self.fileList = DirectoryHelper.ListDirectoryFiles(dirPath=dirName, fileEndings=[".json"])
        self.preloader = DataPreloader(samples=self.fileList, loadMethod=FileHelper.JsonToDict, maxPreloadCount=15,
                                       preprocessFunction=self.preProcessing, shuffleData=True)

    @staticmethod
    def preProcessing(stuff: Dict):
        stuff["preprocessed"] = True
        return stuff

    def test_Basictest(self):

        jsonData = []

        for i in range(0, self.fileList.__len__()):
            jsonData.append(self.preloader[i])

        self.assertEqual(jsonData.__len__(), self.fileList.__len__())

        for data in jsonData:
            self.assertTrue("preprocessed" in data)


    def tearDown(self):
        self.preloader.shutdown()



