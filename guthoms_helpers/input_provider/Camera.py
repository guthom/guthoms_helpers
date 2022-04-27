import sys
from guthoms_helpers.input_provider.InputProviderBase import InputProviderBase
from threading import Lock, Thread
import cv2
from datetime import datetime
import time
from typing import Union
if sys.version_info >= (3, 0):
    import _thread
else:
    import thread as _thread

class Camera(InputProviderBase):

    def __init__(self, cameraID: Union[str, int] = 0, fps: int = 30, resolution=None, preprocessFunction = None,
                 bufferLength: int = 30, autoStart: bool = True, useBuffer:bool = False):
        super(Camera, self).__init__(bufferLength, useBuffer=useBuffer)

        #locks
        self.camCapLock = Lock()

        self.cameraID = cameraID
        self.resolution = resolution
        self.camCap = self.InitCamCap()
        self.fps = fps
        self.preprocessFunction = preprocessFunction
        self.join = False

        #duration in [microseconds]
        self.duration = 1 / self.fps * 1e6
        self.preloadThread: Thread = None
        self.loop = False

        if autoStart and self.useBuffer:
            self.Start()

    def InitCamCap(self):
        self.camCapLock.acquire()
        camCap = cv2.VideoCapture(self.cameraID)

        if self.resolution is not None:
            camCap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            camCap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            print("[" + str(camCap.get(cv2.CAP_PROP_FRAME_WIDTH)) + "," + str(camCap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        self.camCapLock.release()
        return camCap

    def Start(self):
        self.join = False
        self.preloadThread = Thread(target=self._preloader)
        self.preloadThread.start()

    def Stop(self):
        self.join = True
        self.preloadThread.join()

    def GetData(self, index: int = None):
        if not self.useBuffer:
            return self.GetSingleData()

        if index is None:
            return self.dataBuffer.GetLastItem()
        else:
            return self.dataBuffer[index]

    def GetSingleData(self):

        if self.camCap.isOpened():
            self.camCapLock.acquire()
            ret, img = self.camCap.read()
            self.camCapLock.release()

            if img is None:
                # None image means emtpy file/framebuffer
                # restart if we want to loop
                if self.loop:
                    self.Reinit()
                else:
                    self.camCapLock.acquire()
                    self.camCap.release()
                    self.camCapLock.release()

            else:
                if self.preprocessFunction is not None:
                    img = self.preprocessFunction(img)

        return img

    def ReInit(self):
        self.camCapLock.acquire()
        self.camCap.release()
        self.camCap = cv2.VideoCapture(self.cameraID)
        self.camCapLock.release()


    def _preloader(self):
        while self.camCap.isOpened() and not self.join:

            if self.dataBuffer.IsFull():
                time.sleep(0.000001)
                continue

            startTime = datetime.now()

            img = self.GetSingleData()

            if self.preprocessFunction is not None:
                img = self.preprocessFunction(img)

            self.dataBuffer.append(img)


            # sleep time to fit in fps
            #TODO: Reimplement this better
            #duration = datetime.now() - startTime
            #timeleft = self.duration - duration.microseconds
            #if timeleft > 0:
            #    seconds = timeleft / 1e6
            #    print("sleep: " + str(seconds))
            #    time.sleep(seconds)



    def finished(self):
        self.camCapLock.acquire()
        opened = self.camCap.isOpened()
        self.camCapLock.release()

        return not opened

    def __len__(self):
        return -1

    def __iter__(self):
        raise Exception("Not Implemented!")

