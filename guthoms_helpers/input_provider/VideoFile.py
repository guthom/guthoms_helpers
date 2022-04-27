from typing import List

from guthoms_helpers.input_provider.Camera import Camera
from guthoms_helpers.filesystem.FileHelper import FileHelper

import cv2

class VideoFile(Camera):

    def __init__(self, path: str, fps: int = 30, resolution=None, preprocessFunction = None,
                 bufferLength: int = 30, autoStart: bool = True, loop: bool = False, useBuffer: bool=False):

        if not FileHelper.FileExists(path):
            raise Exception("Video File does not exist!")

        super(VideoFile, self).__init__(path, fps, resolution, preprocessFunction, bufferLength, autoStart=False,
                                        useBuffer=useBuffer)

        self.loop = loop

        if autoStart and useBuffer:
            self.Start()

