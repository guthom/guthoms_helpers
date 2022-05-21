from typing import Dict, List

from guthoms_helpers.base_types.BaseType import BaseType

class OpticalFlow(BaseType):

    def __init__(self, direction: 'VectorBase', distance: float, speed: float):
        self.direction: 'VectorBase' = direction
        self.distance: float = distance
        self.speed: float = speed

    @classmethod
    def From2Vectors(cls, vec1: 'VectorBase', vec2: 'VectorBase', time: float = 1.0) -> 'OpticalFlow':
        dist = vec1.Distance(vec2)
        dir = (vec1 - vec2)

        if dist > 0:
            dir /= dist

        speed = dist / time
        return cls(dir, dist, speed)

    def Displacement(self) -> 'VectorBase':
        return self.direction*self.distance

    def __mul__(self, factor: float):
        self.distance *= factor
        self.speed *= factor
        return self

    def __add__(self, other: 'OpticalFlow'):
        self.distance += other.distance
        self.direction += other.direction
        self.speed += other.speed
        return self

    def __truediv__(self, other: float):
        self.distance /= other
        self.direction /= other
        self.speed /= other
        return self

    @classmethod
    def Mean(cls, flows: List['OpticalFlow'], weigths: List[float] = None) -> 'OpticalFlow':

        if weigths is None:
            meanFlow = flows[0]
            for i in range(1, flows.__len__()):
                meanFlow += flows[i]
        else:
            meanFlow = flows[0] * weigths[0]
            for i in range(1, flows.__len__()):
                meanFlow += flows[i] * weigths[i]

        return meanFlow / flows.__len__()


    def toList(self) -> List[float]:
        return [self.direction.toList(), self.distance, self.speed]

    def toString(self) -> str:
        return str(self.toList())

    def Rounded(self, decimals: int = 2):
        raise Exception("Not Implemented!")

    def AsType(self, type: type):
        raise Exception("Not Implemented!")

    def fromList(cls, list: List[float]):
        raise Exception("Not Implemented!")

    def fromDict(cls, dict: Dict):
        raise Exception("Not Implemented!")

