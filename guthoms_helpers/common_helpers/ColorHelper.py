from typing import List

import math

class ColorHelper(object):

    def __init__(self):
        pass

    @staticmethod
    def GetUniqueColors(count: int) -> List:

        colors = []

        if count <= 0:
            return colors

        maxValue = 255 * 3
        step = int(math.floor(maxValue/count))

        for i in range(1, count+1):
            r = min(step*i, 255)
            g = min(step*i - r, 255)
            b = step*i - r - g

            colors.append([r, g, b])

        return colors

    @staticmethod
    def GetUniqueColorsNormalized(count: int) -> List:
        colors = ColorHelper.GetUniqueColors(count)

        for i in range(0, len(colors)):
            for j in range(0, len(colors[i])):
                colors[i][j] /= 255

        return colors

    @staticmethod
    def GetUniqueRGBAColorsNormalized(count: int, alpha: int = 1) -> List:

        assert(0.0 <= alpha <= 1.0)

        colors = ColorHelper.GetUniqueColorsNormalized(count)

        for i in range(0, len(colors)):
            colors[i].append(alpha)

        return colors

    @staticmethod
    def GetUniqueRGBAColors(count: int, alpha: int = 255) -> List:

        colors = ColorHelper.GetUniqueColors(count)

        for i in range(0, len(colors)):
            colors[i].append(alpha)

        return colors