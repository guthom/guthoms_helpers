from typing import List
import time
import copy
import sys
from threading import Lock

if sys.version_info >= (3, 0):
    import _thread
else:
    import thread as _thread


class DataBuffer(object):

    def __init__(self, bufferLength: int):

        self.bufferLength = bufferLength
        self.lockObject = Lock()
        self.data = []

        return

    def __len__(self):
        self.lockObject.acquire()
        length = self.data.__len__()
        self.lockObject.release()
        return length

    def __getitem__(self, item):
        self.lockObject.acquire()
        if item in self.data:
            ret = self.data[item]
        else:
            return None
        self.lockObject.release()
        return ret

    def IsEmpty(self) -> bool:
        self.lockObject.acquire()
        bufferEmppty = self.data.__len__() <= 0
        self.lockObject.release()
        return bufferEmppty

    def append(self, item):

        self.lockObject.acquire()

        self.data.append(copy.deepcopy(item))

        if self.data.__len__() > self.bufferLength:
            self.data.__delitem__(0)

        self.lockObject.release()

    def GetBuffer(self) -> List:
        self.lockObject.acquire()
        data = self.data
        self.lockObject.release()
        return data

    def IsFull(self) -> bool:
        self.lockObject.acquire()
        full = self.data.__len__() >= self.bufferLength
        self.lockObject.release()
        return full

    def GetLastItem(self, delete: bool = True):

        if self.IsEmpty():
            return None

        self.lockObject.acquire()
        ret = copy.deepcopy(self.data[-1])
        if delete:
            del self.data[-1]

        #print(self.data.__len__())
        self.lockObject.release()
        return ret

    def GetLastItems(self, amount: int, delete: bool = True) -> List:
        self.lockObject.acquire()
        length = self.data.__len__()
        start = max(0, length-amount)
        end = max(0, start + length)

        ret = self.data[start:end]
        if delete:
            del self.data[start:end]
        self.lockObject.release()
        return ret
