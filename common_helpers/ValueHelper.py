import math
from typing import List

class ValueHelper(object):

    def GetExponentialWeights(self, weightCount: int, weigthFactor: float = 0.5) -> List[float]:
        ret = [math.exp(-weigthFactor * x) for x in range(0, weightCount)]
        return ret