from typing import List, Optional
import time
import sys
from threading import Lock
import threading
import random

class DataPreloader(object):

    def __init__(self, samples: List, loadMethod, maxPreloadCount: Optional[int] = None, preprocessFunction=None,
                 keepInMemory: bool = False, infinite: bool = False, shuffleData: bool = False,
                 waitForBuffer: bool = False):

        self.loadMethod = loadMethod
        self.infinite = infinite

        self.samples = samples

        self.shuffleData = shuffleData
        if self.shuffleData:
            random.shuffle(self.samples)

        self.maxIndex = self.samples.__len__() - 1

        if maxPreloadCount is None or maxPreloadCount > self.samples.__len__():
            self.maxPreloadCount = self.samples.__len__()
        else:
            self.maxPreloadCount = maxPreloadCount

        self.preprocessFunction = preprocessFunction
        self.keepInMemory = keepInMemory

        self.dataLock = Lock()
        self.data = None
        self.ResetData()

        self.waitItemLock = Lock()
        self.waitItems = []

        self.dataCountLock = Lock()
        self.dataCount = 0
        self.lastIndex = -1

        self.stop = False

        self.prealoadThread = threading.Thread(target=self.preloader, args=())
        self.prealoadThread.start()

        if waitForBuffer:
            while self.CheckDataCount() < self.maxPreloadCount:
                print("DataPreloader waiting for full buffer: " + str(self.CheckDataCount()) + "/" +
                      str(self.maxPreloadCount))
                time.sleep(0.25)

    def ResetData(self):
        self.data = [None] * self.samples.__len__()

    def __getitem__(self, item):
        if item > self.maxIndex:
            raise Exception("Index out of range!")

        while not self.CheckData(item):
            self.waitItemLock.acquire()
            try:
                if item not in self.waitItems:
                    self.waitItems.append(item)
            finally:
                self.waitItemLock.release()
            print("Wait for preloaded item: " + str(item))
            time.sleep(0.1)

        self.dataLock.acquire()
        try:
            ret = self.data[item]

            if not self.keepInMemory:
                self.data[item] = None

            self.dataCount -= 1
        finally:
            self.dataLock.release()

        return ret

    def Next(self):
        self.lastIndex += 1

        if self.lastIndex > self.maxIndex:
            self.lastIndex = self.maxIndex

        return self[self.lastIndex]

    def shutdown(self):
        self.stop = True
        if self.prealoadThread.is_alive():
            self.prealoadThread.join()

    def CheckData(self, index) -> bool:
        ret = False

        self.dataLock.acquire()
        try:
            if self.data[index] is not None:
                ret = True
        finally:
            self.dataLock.release()

        return ret

    def CheckDataCount(self) -> int:
        self.dataCountLock.acquire()
        try:
            ret = self.dataCount
        finally:
            self.dataCountLock.release()

        return ret

    def CheckWaitItem(self) -> bool:
        ret = False

        self.waitItemLock.acquire()
        try:
            if self.waitItems.__len__() > 0:
                ret = True
        finally:
            self.waitItemLock.release()

        return ret

    def preloader(self):

        while not self.stop:
            i = 0

            while i <= self.maxIndex:

                if self.stop:
                    break

                if self.CheckData(i):
                    continue

                #take care for maximum preload count but take also a wait item into account
                while self.CheckDataCount() >= self.maxPreloadCount and not self.CheckWaitItem():
                    if self.stop:
                        break

                    time.sleep(0.1)

                waitItem = None
                if self.CheckWaitItem():
                    self.waitItemLock.acquire()
                    try:
                        waitItem = self.waitItems[0]
                        storedIndex = i
                        i = waitItem
                        self.waitItems.__delitem__(0)
                    finally:
                        self.waitItemLock.release()
                try:
                    dataChunk = self.loadMethod(self.samples[i])
                except:
                    raise Exception("Load Method of preloader failed!")

                if self.preprocessFunction is not None:
                    dataChunk = self.preprocessFunction(dataChunk)

                if dataChunk is None:
                    raise Exception("Loaded Data is None!")

                self.dataLock.acquire()
                self.dataCountLock.acquire()
                try:
                    self.data[i] = dataChunk
                    self.dataCount += 1
                finally:
                    self.dataLock.release()
                    self.dataCountLock.release()

                if waitItem is not None:
                    i = storedIndex - 1

                i += 1
            #check if we want to preload infinite times
            if self.infinite and not self.stop:
                self.lastIndex = -1
                self.dataCount = 0
                if not self.keepInMemory:
                    self.ResetData()
                if self.shuffleData:
                    random.shuffle(self.samples)
            else:
                break
