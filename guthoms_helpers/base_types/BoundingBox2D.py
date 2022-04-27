from guthoms_helpers.base_types.BoundingBoxBase import BoundingBoxBase
from guthoms_helpers.base_types.VectorBase import VectorBase
from guthoms_helpers.base_types.Pose2D import Pose2D
from guthoms_helpers.base_types.Vector2D import Vector2D
from typing import List, Dict, Union, Tuple
import sys
import copy
import numpy as np
import cv2
import matplotlib.patches as patches

import imgaug as ia


class BoundingBox2D(BoundingBoxBase):

    def __init__(self, p1: Vector2D, p2: Vector2D):
        super().__init__([p1, p2])

    def ToIaaBoundingBox(self) -> ia.BoundingBox:
        return ia.BoundingBox(x1=self.x1, y1=self.y1, x2=self.x2, y2=self.y2)

    @classmethod
    def FromIaaBB(self, iaaBB: ia.BoundingBox):
        return BoundingBox2D(Vector2D(x=iaaBB.x1, y=iaaBB.y1), Vector2D(x=iaaBB.x2, y=iaaBB.y2))

    @property
    def P1(self) -> Vector2D:
        return Vector2D.FromInstance(self.points[0])

    @property
    def P2(self) -> Vector2D:
        return Vector2D.FromInstance(self.points[1])

    @property
    def midX(self) -> float:
        return copy.copy(self.mid[0])

    @property
    def midY(self) -> float:
        return copy.copy(self.mid[1])

    @property
    def x1(self) -> float:
        return copy.copy(self.points[0][0])

    @property
    def y1(self) -> float:
        return copy.copy(self.points[0][1])

    @property
    def x2(self) -> float:
        return copy.copy(self.points[1][0])

    @property
    def y2(self) -> float:
        return copy.copy(self.points[1][1])

    @property
    def width(self) -> float:
        return copy.copy(self.size[0])

    @property
    def height(self) -> float:
        return copy.copy(self.size[1])

    @classmethod
    def FromTwoPoints(cls, p1: Vector2D, p2: Vector2D):

        if p1[0] < p2[0]:
            x1 = p1[0]
            x2 = p2[0]
        else:
            x1 = p2[0]
            x2 = p1[0]

        if p1[1] < p2[1]:
            y1 = p1[1]
            y2 = p2[1]
        else:
            y1 = p2[1]
            y2 = p1[1]

        return cls(Vector2D(x1, y1), Vector2D(x2, y2))

    @classmethod
    def FromMidAndRange(cls, mid: Vector2D, scale: Vector2D) -> 'BoundingBox2D':

        scale_2 = scale/2

        p1 = mid - scale_2
        p2 = mid + scale_2

        return cls(p1, p2)

    @classmethod
    def FromImage(cls, image: np.array) -> 'BoundingBox2D':

        p1 = Vector2D(x=0, y=0)
        p2 = Vector2D(x=image.shape[0], y=image.shape[1])

        return cls(p1, p2)

    @classmethod
    def CreateBoundingBox(cls, keyPoints: List[Union[Vector2D, Pose2D]], expandBox= False, max_x_val: int = sys.maxsize,
                          max_y_val: int = sys.maxsize, expandRatio: float = 0.2) -> 'BoundingBox2D':
        min_x = sys.maxsize
        min_y = sys.maxsize
        max_x = 0
        max_y = 0

        for joint in keyPoints:

            x = joint[0]
            y = joint[1]

            min_x = min_x if x > min_x else x
            min_y = min_y if y > min_y else y
            max_x = max_x if x < max_x else x
            max_y = max_y if y < max_y else y

        min_x = min_x if min_x > 0 else 0
        min_y = min_y if min_y > 0 else 0
        max_x = max_x if max_x < max_x_val else max_x_val
        max_y = max_y if max_y < max_y_val else max_y_val

        ret = BoundingBox2D(Vector2D(int(min_x), int(min_y)), Vector2D(int(max_x), int(max_y)))

        if expandBox:
            expandValue = ret.DiagLength() * expandRatio
            ret = ret.ExtendBB(Vector2D(expandValue, expandValue))

        return ret

    def DiagLength(self):
        return self.P1.Distance(self.P2)

    def SetNewMid(self, mid: Vector2D) -> 'BoundingBox2D':
        return BoundingBox2D.FromMidAndRange(mid, self.size)

    def GetEdgePoints(self) -> List[Vector2D]:

        #1 - 2
        #|   |
        #3 - 4
        size_2 = self.size/2
        p1 = Vector2D(self.mid[0] - size_2[0], self.mid[1] - size_2[1])
        p2 = Vector2D(self.mid[0] + size_2[0], self.mid[1] - size_2[1])
        p3 = Vector2D(self.mid[0] - size_2[0], self.mid[1] + size_2[1])
        p4 = Vector2D(self.mid[0] + size_2[0], self.mid[1] + size_2[1])

        return [p1, p2, p3, p4]

    @classmethod
    def fromList(cls, list: List[float]) -> "BoundingBox2D":
        return cls(Vector2D(list[0], list[1]), Vector2D(list[2], list[3]))

    def CalculateOpticalFlow(self, target: 'BoundingBox2D', normalized: bool = True) -> Vector2D:

        '''
        myPoints = self.GetEdgePoints()
        targetPoints = target.GetEdgePoints()

        flows = list()
        for i in range(0, myPoints.__len__()):
            flows.append(myPoints[i].CalculateFlow(targetPoints[i]))

        tempBox = BoundingBox2D.FromPoints()
        '''

        direction, distance = target.mid.CalculateFlow(self.mid)

        if normalized:
            meanBBSize = (self.DiagLength() + target.DiagLength())/2
            return direction / distance, meanBBSize
        else:
            return direction

    def NormWithImage(self, image: np.array):

        if image.shape.__len__() == 4:
            _, _, w, h = image.shape
        elif image.shape.__len__() == 3:
            w, h, _ = image.shape
        else:
            w, h = image.shape

        ret = BoundingBox2D(Vector2D(self.points[0][0] / w, self.points[0][1] / h),
                            Vector2D(self.points[1][0] / w, self.points[1][1] / h))
        return ret

    def NormWithSize(self, size: Tuple[int, int]):
        ret = BoundingBox2D(Vector2D(self.points[0][0] / size[0], self.points[0][1] / size[1]),
                            Vector2D(self.points[1][0] / size[0], self.points[1][1] / size[1]))
        return ret

    def Clip(self, clipVal=1.0):
        ret = BoundingBox2D(Vector2D(self._clip(self.points[0][0], clipVal), self._clip(self.points[0][1], clipVal)),
                            Vector2D(self._clip(self.points[1][0], clipVal), self._clip(self.points[1][1], clipVal)))
        return ret

    def ClipMin(self, clipVal=0.0):
        ret = BoundingBox2D(Vector2D(self._clipMin(self.points[0][0], clipVal),
                                     self._clipMin(self.points[0][1], clipVal)),
                            Vector2D(self._clipMin(self.points[1][0], clipVal),
                                     self._clipMin(self.points[1][1], clipVal)))
        return ret

    def ClipToShape(self, shape: Tuple[float, float]):
        x1 = self._clip(self.points[0][0], shape[0] - 1)
        y1 = self._clip(self.points[0][1], shape[1] - 1)
        x2 = self._clip(self.points[1][0], shape[0] - 1)
        y2 = self._clip(self.points[1][1], shape[1] - 1)

        return BoundingBox2D(Vector2D(x1, y1), Vector2D(x2, y2))

    def _clip(self, value, clipVal):
        return max(0, min(value, clipVal))

    def _clipMin(self, value, clipVal):
        return max(0, max(value, clipVal))

    def AddPadding(self, padX = 0.0, padY = 0.0):
        return BoundingBox2D(Vector2D(self.points[0][0] + padX, self.points[0][1] + padY),
                             Vector2D(self.points[1][0] + padX, self.points[1][1] + padY))

    def SubstractPadding(self,  padX = 0.0, padY = 0.0):
        return BoundingBox2D(Vector2D(self.points[0][0] - padX, self.points[0][1] - padY),
                             Vector2D(self.points[1][0] - padX, self.points[1][1] - padY))

    def ScaleBB(self, scale: Vector2D) -> 'BoundingBox2D':
        size_2 = self.size/2

        width = self.width*scale[0]
        heigth = self.height*scale[1]

        '''
        x1 = self.points[0][0] - (size_2[0] * scale[0])
        y1 = self.points[0][1] - (size_2[1] * scale[1])

        x2 = self.points[1][0] + (size_2[0] * scale[0])
        y2 = self.points[1][1] + (size_2[1] * scale[1])
        return BoundingBox2D(Vector2D(x1, y1), Vector2D(x2, y2))
        '''
        return BoundingBox2D.FromMidAndRange(self.mid, Vector2D(x=width, y=heigth))

    def ScaleCoordiantes(self, scale: Vector2D):
        return BoundingBox2D(Vector2D(self.points[0][0] * scale[0], self.points[0][1] * scale[1]),
                             Vector2D(self.points[1][0] * scale[0], self.points[1][1] * scale[1]))

    def ExtendBB(self, extension: Vector2D):
        x1 = self.points[0][0] - extension[0]
        y1 = self.points[0][1] - extension[1]

        x2 = self.points[1][0] + extension[0]
        y2 = self.points[1][1] + extension[1]

        return BoundingBox2D(Vector2D(x1, y1), Vector2D(x2, y2))

    def CropImage(self, image):
        #crop
        x1 = int(max(0.0, self.points[0][0]))
        y1 = int(max(0.0, self.points[0][1]))
        x2 = int(min(self.points[1][0], image.shape[1]-1))
        y2 = int(min(self.points[1][1], image.shape[0]-1))

        return np.array(image[y1:y2, x1:x2])

    def Draw(self, image, description=None, color=list([0.0, 0.0, 0.0])):

        bb = self.ClipToShape([image.shape[1], image.shape[0]])
        p1 = (int(bb.points[0][0]), int(bb.points[0][1]))
        p2 = (int(bb.points[1][0]), int(bb.points[1][1]))

        cv2.rectangle(image, p1, p2, color, thickness=2)

        if description is not None:
            cv2.putText(image, description, p1, fontScale=1, thickness=2,
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=color)
        return image

    def AddPatch(self, plt, ax, description=None, color=list([0.0, 0.0, 0.0, 1.0])):
        # Create a Rectangle patch
        bbox = patches.Rectangle((self.points[0][0], self.points[0][1]), self.size[0], self.size[1],
                                 linewidth=2, edgecolor=color, facecolor='none')

        # Add the bbox to the plot
        ax.add_patch(bbox)
        # Add label
        if description is not None:
            plt.text(self.points[0][0], self.points[0][1], s=description, color='white', verticalalignment='top',
                     bbox={'color': color, 'pad': 0})

        return plt

    def DrawImageInBoundingBox(self, image: np.array, drawImage: np.array, alpha=0.5) -> np.array:
        img = image

        xstart = max(0, int(self.x1))
        xend = xstart + drawImage.shape[1]
        heigth = xend - xstart


        ystart = max(0, int(self.y1))
        yend = ystart + drawImage.shape[0]
        width = yend - ystart
        try:
            img[ystart:yend, xstart:xend, :] = cv2.addWeighted(img[ystart:yend, xstart:xend, :], 1.0 - alpha, drawImage,
                                                               alpha, 0)
        except:
            print("Error Drawing IMG in BoundingBox: " + str(xstart) + "; " + str(xend) + "; " + str(ystart) + "; " + str(yend) + "; ")
            cv2.imwrite("/mnt/datastuff/TestExamples/tag_inpainter/error_image.png", image)
            cv2.imwrite("/mnt/datastuff/TestExamples/tag_inpainter/error_draw.png", drawImage)

        return img

    def ResizeImageToBoundingBox(self, image: np.array) -> np.array:
        return cv2.resize(image, dsize=(int(self.size[0]), int(self.size[1])))

    def Area(self) -> float:
        return self.height * self.width

    def CalculateOverlapp(self, target: "BoundingBox2D") -> float:

        x1 = max(self.x1, target.x1)
        y1 = max(self.y1, target.y1)
        x2 = min(self.x2, target.x2)
        y2 = min(self.y2, target.y2)

        width = (x2 - x1)
        height = (y2 - y1)
        # handle case where there is NO overlap
        if (width < 0) or (height < 0):
            interArea = 0.0
        else:
            interArea = width * height

        return interArea

    def CalculateIoU(self, target: "BoundingBox2D") -> float:
        overlap = self.CalculateOverlapp(target)
        union = self.Area() + target.Area() - overlap

        if union == 0.0:
            return 0
        iou = overlap/union
        return iou

    def toString(self) -> str:
        raise Exception("Not Implemented!")

    def Rounded(self, decimals: int = 2):
        raise Exception("Not Implemented!")

    def AsType(self, type: type):
        raise Exception("Not Implemented!")

    def SetSize(self):
        if self.size is None:
            width = self.P2[0] - self.P1[0]
            height = self.P2[1] - self.P1[1]

            self.size = Vector2D(width, height)

    def SetMid(self):
        if self.mid is None:
            self.mid = self.P1 + self.size/2

    @classmethod
    def fromDict(cls, dict: Dict):
        raise Exception("Not Implemented!")