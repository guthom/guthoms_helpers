import unittest
from unittest import TestCase
import numpy as np
from typing import List, Tuple
from guthoms_helpers.base_types.Rotation3D import Rotation3D
from guthoms_helpers.base_types.Pose3D import Pose3D
from guthoms_helpers.base_types.Rotation2D import Rotation2D
from guthoms_helpers.base_types.Pose2D import Pose2D
from guthoms_helpers.base_types.Quaternion import Quaternion
from guthoms_helpers.base_types.RotationMatrix import RotationMatrix
from guthoms_helpers.base_types.EulerAngles import EulerAngles
from guthoms_helpers.base_types.Vector3D import Vector3D
from guthoms_helpers.base_types.Vector2D import Vector2D
from guthoms_helpers.base_types.AxisAngles import AxisAngles

from guthoms_helpers.common_helpers.RandomHelper import RandomHelper

from math import pow, sqrt

class TestCollection(object):

    def __init__(self, order: str="xyz"):
        self.order = None
        self.quats = []
        self.rpys = []
        self.rotMs = []
        self.axisAngles = []
        self.groups = []

        if order == "xyz":
            self.XYZ()
        else:
            raise Exception("No Golden model for this order!")

    def Normalize(self, quat: List[float]) -> List[float]:
        d = sqrt(pow(quat[0], 2) + pow(quat[1], 2) + pow(quat[2], 2) + pow(quat[3], 2))
        x = quat[0] / d
        y = quat[1] / d
        z = quat[2] / d
        w = quat[3] / d
        return [x, y, z, w]

    def XYZ(self):
        self.order = "xyz"
        self.quats = []
        # [x, y, z, w]
        self.quats.append(self.Normalize([0.500, -0.500, 0.5, 0.500]))
        self.quats.append(self.Normalize([0.500, 0.500, 0.500, 0.500]))
        self.quats.append(self.Normalize([0.707, 0, 0, 0.707]))
        self.quats.append(self.Normalize([0.270, 0.653, 0.270, 0.653]))
        self.quats.append(self.Normalize([0.2579252, 0.2579252, 0.0716607, 0.9283393]))

        self.rpys = []
        self.rpys.append([1.571, 0.0, 1.571])
        self.rpys.append([1.571, 1.571, 0.0])
        self.rpys.append([1.571, 0.0, 0.0])
        self.rpys.append([0.7841392, 1.5707963, 0.0])
        self.rpys.append([0.542, 0.542, 0.0])

        self.rotMs = []
        self.rotMs.append(np.array([
            [0.0000000, -1.0000000,  0.0000000],
            [0.0000000,  0.0000000, -1.0000000],
            [1.0000000,  0.0000000,  0.0000000]
        ]))
        self.rotMs.append(np.array([
            [0.0007963,  0.0000000,  0.9999997],
            [0.9999993,  0.0007963, -0.0007963],
            [-0.0007963,  0.9999997,  0.0000006]
        ]))
        self.rotMs.append(np.array([
            [1.0000000,  0.0000000,  0.0000000],
            [0.0000000,  0.0007963, -0.9999997],
            [0.0000000,  0.9999997,  0.0007963]
        ]))
        self.rotMs.append(np.array([
            [0.0000000,  0.0000000,  1.0000000],
            [0.7062160,  0.7079964,  0.0000000],
            [-0.7079964,  0.7062160,  0.0000000]
        ]))
        self.rotMs.append(np.array([
            [0.8566787,  0.0000000,  0.5158504],
            [0.2661016,  0.8566787, -0.4419180],
            [-0.4419180,  0.5158504,  0.7338984]
        ]))

        self.axisAngles = []
        self.axisAngles.append([[0.5773111, -0.5774287, 0.5773111], 2.0946303])
        self.axisAngles.append([[0.5773111, 0.5773111, 0.5774287], 2.0946303])
        self.axisAngles.append([[1, 0, 0], 1.571])
        self.axisAngles.append([[0.3569328, 0.8632485, 0.3569328], 1.7173218])
        self.axisAngles.append([[0.6938437, 0.6938437, 0.1927741], 0.761752])

        #add group representations
        self.groups.append([])


class GroupRepresentations(TestCase):

    def setUp(self):
        self.testCollections = []
        self.testCollections.append(TestCollection(order="xyz"))

    def test_So2Representation(self):

        #So2
        lastRotation = None
        for i in range(0, 30):

            randomAngle = RandomHelper.RandomFloat(-1.5, 1.5)
            rotation = Rotation2D(randomAngle)

            skew = rotation.GetSkewMatrix()
            skew2 = Rotation2D.Hat(randomAngle)

            self.assertTrue(np.array_equal(skew, skew2))

            self.assertTrue(np.array_equal([randomAngle], Rotation2D.Vee(skew)))

            mapped = Rotation2D.Exp(Rotation2D.Hat(randomAngle))
            recoverd = Rotation2D.Log(mapped)

            rot = Rotation2D.Exp(skew)
            rotM = rotation.GetRotM()
            self.assertTrue(np.array_equal(rotM, rot))
            self.assertTrue(np.array_equal(rotM, mapped))
            self.assertTrue(np.allclose(recoverd, skew))

            if lastRotation is not None:
                addRot = Rotation2D(angle=lastRotation)
                addSkew = addRot.GetSkewMatrix()

                res = skew + addSkew

                resRot = Rotation2D.ExpToElement(res)

                self.assertTrue(np.allclose(resRot.angle, lastRotation + randomAngle))

            lastRotation = randomAngle


    def test_SE2Representation(self):
        # SE2
        lastRotation = None
        for i in range(0, 30):

            transX = RandomHelper.RandomFloat(-100, 100)
            transY = RandomHelper.RandomFloat(-100, 100)
            randomAngle0 = RandomHelper.RandomFloat(-1.5, 1.5)
            elementArray = np.array([transX, transY, randomAngle0])

            pose = Pose2D(Vector2D(x=transX, y=transY), Rotation2D(angle=randomAngle0))

            skew = pose.GetSkewMatrix()
            skew2 = Pose2D.Hat(elementArray)

            self.assertTrue(np.array_equal(skew, skew2))


    def test_SE3Representation(self):
        # SE3
        lastRotation = None
        # Se3
        for i in range(0, 30):
            transX = RandomHelper.RandomFloat(-100, 100)
            transY = RandomHelper.RandomFloat(-100, 100)
            transZ = RandomHelper.RandomFloat(-100, 100)
            randomAngle0 = RandomHelper.RandomFloat(-1.5, 1.5)
            randomAngle1 = RandomHelper.RandomFloat(-1.5, 1.5)
            randomAngle2 = RandomHelper.RandomFloat(-1.5, 1.5)
            elementArray = np.array([transX, transY, transZ, randomAngle0, randomAngle1, randomAngle2])

            pose = Pose3D(Vector3D(x=transX, y=transY, z=transZ),
                          Rotation3D.fromEuler(EulerAngles.fromList([randomAngle0, randomAngle1, randomAngle2])))

            skew = pose.GetSkewMatrix()
            skew2 = Pose3D.Hat(elementArray)

            self.assertTrue(np.array_equal(skew, skew2))

            #self.assertEqual(pose, pose2)
            poseMat = Pose3D.Exp(skew)
            compareMat = pose.to4x4()
            # self.assertTrue(np.allclose(compareMat, poseMat))

            poseSkew = Pose3D.Log(poseMat)
            self.assertTrue(np.allclose(poseSkew, skew))








