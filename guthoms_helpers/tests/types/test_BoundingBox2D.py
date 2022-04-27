import unittest
from unittest import TestCase
import numpy as np
from typing import List, Tuple
from guthoms_helpers.base_types.Rotation2D import Rotation2D
from guthoms_helpers.base_types.Vector2D import Vector2D
from guthoms_helpers.common_helpers.RandomHelper import RandomHelper
import math
from guthoms_helpers.base_types.BoundingBox2D import BoundingBox2D

class BoundingBox2DTests(TestCase):
    
    def setUp(self) -> None:
        self.numTries = 200

    @staticmethod
    def _random2Points(lowerRange: int = 1, upperRange: int = 100, asFloat: bool=False) -> Tuple[Vector2D, Vector2D]:

        if not asFloat:
            p1 = Vector2D(RandomHelper.RandomInt(lowerRange=lowerRange, upperRange=upperRange),
                          RandomHelper.RandomInt(lowerRange=lowerRange, upperRange=upperRange))

            p2 = Vector2D(RandomHelper.RandomInt(lowerRange=lowerRange, upperRange=upperRange),
                          RandomHelper.RandomInt(lowerRange=lowerRange, upperRange=upperRange))
        else:
            p1 = Vector2D(RandomHelper.RandomFloat(lowerRange=lowerRange, upperRange=upperRange),
                          RandomHelper.RandomFloat(lowerRange=lowerRange, upperRange=upperRange))

            p2 = Vector2D(RandomHelper.RandomFloat(lowerRange=lowerRange, upperRange=upperRange),
                          RandomHelper.RandomFloat(lowerRange=lowerRange, upperRange=upperRange))
        return p1, p2

    def _checkBBwith2Points(self, p1: Vector2D, p2: Vector2D, bb: BoundingBox2D):

        if p1.x > p2.x:
            self.assertTrue(p1.x == bb.P2.x)
            self.assertTrue(p2.x == bb.P1.x)
        else:
            self.assertTrue(p1.x == bb.P1.x)
            self.assertTrue(p2.x == bb.P2.x)

        if p1.y > p2.y:
            self.assertTrue(p1.y == bb.P2.y)
            self.assertTrue(p2.y == bb.P1.y)
        else:
            self.assertTrue(p1.y == bb.P1.y)
            self.assertTrue(p2.y == bb.P2.y)

    def test_sizeCalculationWorks(self):
        for i in range(0, self.numTries):
            p1, _ = self._random2Points(0, 20)
            p2,  _ = self._random2Points(30, 50)

            size = Vector2D(p2[0] - p1[0], p2[1] - p1[1])

            bb = BoundingBox2D.FromTwoPoints(p1, p2)

            self.assertTrue(size == bb.size)

    def test_iouCalculationWorks(self):

        bb1 = BoundingBox2D.fromList([0.0, 0.0, 10.0, 10.0])
        bb2 = BoundingBox2D.fromList([0.0, 0.0, 20.0, 20.0])

        self.assertEqual(bb1.CalculateIoU(bb1), 1.0)
        self.assertEqual(bb2.CalculateIoU(bb2), 1.0)
        self.assertEqual(bb1.CalculateIoU(bb2), 0.25)
        self.assertEqual(bb2.CalculateIoU(bb1), 0.25)

        bb3 = BoundingBox2D.fromList([40.0, 40.0, 20.0, 20.0])

        self.assertEqual(bb3.CalculateIoU(bb2), 0.0)

        for i in range(0, self.numTries):

            p1, p2 = self._random2Points(5, 20, asFloat=True)
            p3, p4 = self._random2Points(30, 50, asFloat=True)

            bb1 = BoundingBox2D.FromTwoPoints(p1, p3)
            bb2 = BoundingBox2D.FromTwoPoints(p2, p4)
            self.assertEqual(bb1.CalculateIoU(bb1), 1.0)
            self.assertEqual(bb2.CalculateIoU(bb2), 1.0)

            iou = bb2.CalculateIoU(bb1)
            self.assertTrue(iou < 1.0 and iou >= 0.0)
            self.assertEqual(iou, bb1.CalculateIoU(bb2))


    def test_PaddingWorks(self):
        for i in range(0, self.numTries):
            p1, _ = self._random2Points(5, 20)
            p2,  _ = self._random2Points(30, 50)

            padX = RandomHelper.RandomInt(10, 20)
            padY = RandomHelper.RandomInt(10, 20)

            bb = BoundingBox2D.FromTwoPoints(p1, p2)

            padded = bb.AddPadding(padX, padY)

            self.assertTrue(padded.P1.x == (p1.x + padX))
            self.assertTrue(padded.P1.y == (p1.y + padY))

            unpadded = padded.SubstractPadding(padX, padY)

            self.assertTrue(unpadded == bb)

    def test_ClipMinWorks(self):
        for i in range(0, self.numTries):
            p1, _ = self._random2Points(-20, -10)
            p2,  _ = self._random2Points(20, 50)

            clipVal = RandomHelper.RandomInt(0, 10)

            bb = BoundingBox2D.FromTwoPoints(p1, p2)
            bb = bb.ClipMin(clipVal)

            self.assertTrue(bb.P1.x >= clipVal)
            self.assertTrue(bb.P1.y >= clipVal)

    def test_ClipMaxWorks(self):
        for i in range(0, self.numTries):
            p1, _ = self._random2Points(20, 50)
            p2,  _ = self._random2Points(80, 200)

            clipVal = RandomHelper.RandomInt(60, 150)

            bb = BoundingBox2D.FromTwoPoints(p1, p2)
            bb = bb.Clip(clipVal)

            self.assertTrue(bb.P2.x <= clipVal)
            self.assertTrue(bb.P2.y <= clipVal)

    def test_ClipShapeWorks(self):
        for i in range(0, self.numTries):
            p1, _ = self._random2Points(20, 50)
            p2,  _ = self._random2Points(80, 200)

            clipValX = RandomHelper.RandomInt(50, 60)
            clipValY = RandomHelper.RandomInt(100, 150)

            bb = BoundingBox2D.FromTwoPoints(p1, p2)
            bb = bb.ClipToShape((clipValX, clipValY))

            self.assertTrue(bb.P2.x <= clipValX)
            self.assertTrue(bb.P2.y <= clipValY)

    def test_IndexingWorks(self):
        for i in range(0, self.numTries):
            p1, _ = self._random2Points(0, 20)
            p2,  _ = self._random2Points(30, 50)

            bb = BoundingBox2D.FromTwoPoints(p1, p2)

            self.assertTrue(bb[0] == p1[0])
            self.assertTrue(bb[1] == p1[1])
            self.assertTrue(bb[2] == p2[0])
            self.assertTrue(bb[3] == p2[1])


    def test_FromTwoPointsWorks(self):
        for i in range(0, self.numTries):
            p1, p2 = self._random2Points()

            bb = BoundingBox2D.FromTwoPoints(p1, p2)

            width = p1.Distance(p2)

            self._checkBBwith2Points(p1, p2, bb)

    def test_BoundingBoxScallingWorks(self):
        for i in range(0, self.numTries):
            p1, p2 = self._random2Points(50, 100)
            xWidth = abs(p1.x - p2.x) / 2
            yHeigth = abs(p1.y - p2.y) / 2

            scaleFactorX = RandomHelper.RandomFloat(1.1, 1.3)
            scaleFactorY = RandomHelper.RandomFloat(1.1, 1.3)

            bbBase = BoundingBox2D.FromTwoPoints(p1, p2)

            p1 = bbBase.P1
            p2 = bbBase.P2

            p1.x -= xWidth * scaleFactorX
            p1.y -= yHeigth * scaleFactorY
            p2.x += xWidth * scaleFactorX
            p2.y += yHeigth * scaleFactorY

            bbScaled = BoundingBox2D.FromTwoPoints(p1, p2)

            bb2 = bbBase.ScaleBB(Vector2D(scaleFactorX, scaleFactorY))

            self.assertTrue(bb2 == bbScaled)

    def test_BoundingBoxCoordinateScallingWorks(self):
        for i in range(0, self.numTries):
            p1, p2 = self._random2Points(50, 100)
            scaleFactorX = RandomHelper.RandomFloat(1.1, 1.3)
            scaleFactorY = RandomHelper.RandomFloat(1.1, 1.3)

            bbBase = BoundingBox2D.FromTwoPoints(p1, p2)

            p1 = bbBase.P1
            p2 = bbBase.P2

            p1.x *= scaleFactorX
            p1.y *= scaleFactorY
            p2.x *= scaleFactorX
            p2.y *= scaleFactorY

            bbScaled = BoundingBox2D.FromTwoPoints(p1, p2)

            bb2 = bbBase.ScaleCoordiantes(Vector2D(scaleFactorX, scaleFactorY))

            self.assertTrue(bb2 == bbScaled)

    def test_BoundingBoxExtendingWorks(self):
        for i in range(0, self.numTries):
            p1, p2 = self._random2Points(50, 100)
            xWidth = abs(p1.x - p2.x) / 2
            yHeigth = abs(p1.y - p2.y) / 2

            extensionX = RandomHelper.RandomInt(5, 20)
            extensionY = RandomHelper.RandomInt(5, 20)

            bbBase = BoundingBox2D.FromTwoPoints(p1, p2)

            p1 = bbBase.P1
            p2 = bbBase.P2

            p1.x -= extensionX
            p1.y -= extensionY
            p2.x += extensionX
            p2.y += extensionY

            bbScaled = BoundingBox2D.FromTwoPoints(p1, p2)

            bb2 = bbBase.ExtendBB(Vector2D(extensionX, extensionY))

            self.assertTrue(bb2 == bbScaled)

    def test_CreateBoundingBoxFromKeypointsWorks(self):
        for i in range(0, self.numTries):
            p0, _ = self._random2Points(0, 10)
            p1, p2 = self._random2Points(20, 50)
            p3, p4 = self._random2Points(20, 50)
            p5, p6 = self._random2Points(20, 50)
            p7, p8 = self._random2Points(20, 50)
            p9, _ = self._random2Points(60, 80)

            points = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9]

            bb = BoundingBox2D.CreateBoundingBox(points, expandBox=False)

            self._checkBBwith2Points(p0, p9, bb)

        for i in range(0, self.numTries):
            p0, _ = self._random2Points(0, 10)
            p1, p2 = self._random2Points(20, 50)
            p3, p4 = self._random2Points(20, 50)
            p5, p6 = self._random2Points(20, 50)
            p7 = Vector2D(-1, -1)
            p8 = Vector2D(-1, -1)
            p9, _ = self._random2Points(60, 80)

            points = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9]

            bb = BoundingBox2D.CreateBoundingBox(points, expandBox=False)

            self._checkBBwith2Points(p0, p9, bb)

    def test_DiagLengthWorks(self):
        for i in range (0, self.numTries):
            p1, p2 = self._random2Points()
            bb = BoundingBox2D.FromTwoPoints(p1, p2)

            dist = p1.Distance(p2)
            self.assertTrue(dist == bb.DiagLength())

    def test_GetEdgePointsWorks(self):
        for i in range(0, self.numTries):
            p1, p2 = self._random2Points()
            bb = BoundingBox2D.FromTwoPoints(p1, p2)
            edgePoints = bb.GetEdgePoints()

            self._checkBBwith2Points(edgePoints[0], edgePoints[3], bb)

    def test_FromMidAndRangeWorks(self):
        for i in range(0, self.numTries):
            p1, p2 = self._random2Points(lowerRange=1, upperRange=50)

            xWidth = abs(p1.x - p2.x)
            yHeigth = abs(p1.y - p2.y)

            if p1.y < p2.y:
                yMid = p1.y + yHeigth / 2
            else:
                yMid = p2.y + yHeigth / 2

            if p1.x < p2.x:
                xMid = p1.x + xWidth / 2
            else:
                xMid = p2.x + xWidth / 2

            bb = BoundingBox2D.FromMidAndRange(Vector2D(xMid, yMid), Vector2D(xWidth, yHeigth))

            self._checkBBwith2Points(p1, p2, bb)

