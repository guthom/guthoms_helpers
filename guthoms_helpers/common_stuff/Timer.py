import time
from typing import Optional

class Timer(object):

    def __init__(self, printTestTimers: bool=False):
        self.printTestTimers = printTestTimers
        self.startTime = time.time()
        self.text = ""

    def Start(self, text=""):
        self.text = text
        self.startTime = time.time()
        return

    def Stop(self, printLine: Optional[bool]=None):
        if printLine is None:
            printLine = self.printTestTimers

        elapsed = time.time() - self.startTime
        if printLine:
            print(self.text + " Elapsedtime: " + str(elapsed) + " sec, FPS: " + str(1/elapsed))

        return elapsed
