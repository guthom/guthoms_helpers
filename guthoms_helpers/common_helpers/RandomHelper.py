import random
import os
from typing import Optional
import string

class RandomHelper(object):

    @staticmethod
    def RandomInt(lowerRange: int, upperRange: Optional[int]=None, ignoreVal=None) -> int:
        rand = ignoreVal

        if upperRange is None:
            while rand == ignoreVal:
                rand = random.randrange(-lowerRange, lowerRange)
        else:
            while rand == ignoreVal:
                rand = random.randrange(lowerRange, upperRange)

        return rand

    @staticmethod
    def RandomFloat(lowerRange: float, upperRange: Optional[float]=None) -> float:
        if upperRange is None:
            rand = random.uniform(-lowerRange, lowerRange)
        else:
            rand = random.uniform(lowerRange, upperRange)

        return rand


    @staticmethod
    def DecideByProb(prob: float = 0.5):
        return random.random() < prob

    @staticmethod
    def RandomBytes(length:int) -> bytearray:
        return bytearray(os.urandom(length))

    @staticmethod
    def RandomString(length:int):
        chars = string.ascii_lowercase
        ret = ""
        for i in range(0, length):
            ret += random.choice(chars)
        return ret
