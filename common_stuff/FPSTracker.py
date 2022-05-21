from typing import List
import numpy as np
from guthoms_helpers.common_stuff.Timer import Timer
from guthoms_helpers.common_stuff.DataBuffer import DataBuffer


class FPSTracker(object):

    def __init__(self, selfTracking: bool = True, meanCount: int = 30):
        self.fps: List[float] = []
        self.elapsed: List[float] = []
        self.meanCount = meanCount

        self.timer = Timer()

        self.meanBuffer = DataBuffer(5)

        if selfTracking:
            self.timer.Start("FPSTracker")

    def FinishRun(self) -> float:
        elapsed = self.timer.Stop(False)
        self.TrackElapsed(elapsed)
        self.timer.Start("FPSTracker")

        return self.MeanFPS()

    def TrackElapsed(self, elapsed):
        self.elapsed.append(elapsed)
        self.fps.append(1/elapsed)

    def TrackFPS(self, fps):
        self.fps.append(fps)
        self.elapsed.append(1/fps)

    def MeanFPS(self) -> float:
        mean = float(np.mean(self.fps))

        if self.fps.__len__() >= self.meanCount:
            self.fps.clear()
            #print("-----------------" + str(mean))
            self.meanBuffer.append(mean)

        return float(np.mean(self.meanBuffer.GetBuffer()))

