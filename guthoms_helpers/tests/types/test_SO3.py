from parameterized import parameterized
import unittest
from unittest import TestCase
import numpy as np
from guthoms_helpers.base_types.Rotation3D import Rotation3D
from guthoms_helpers.base_types.AxisAngles import AxisAngles

from math import pow, sqrt

class SO2Tests(TestCase):


    def setUp(self):
        pass

    @parameterized.expand([
        [
            [np.pi, np.pi/2, np.pi/4],
            np.array(
                [
                    [0,         -np.pi/4,   np.pi/2],
                    [np.pi/4,   0,          -np.pi],
                    [-np.pi/2,  np.pi,      0]
                ])
        ]
    ])
    def test_HatOperatorWorks(self, parameters, expected):
        ret = Rotation3D.Hat(parameters)
        self.assertTrue(np.array_equal(ret, expected))

    @parameterized.expand([
        [
            np.array(
                [
                    [0,         -np.pi/4,   np.pi/2],
                    [np.pi/4,   0,          -np.pi],
                    [-np.pi/2,  np.pi,      0]
                ]),
            np.array([np.pi, np.pi / 2, np.pi / 4])
        ]
    ])
    def test_VeeOperatorWorks(self, skew, expected):
        ret = Rotation3D.Vee(skew)
        self.assertTrue(np.array_equal(ret, expected))

    @parameterized.expand([
        [
            [-2.3428211, -1.17141054, -0.58570528],
            np.array(
                [
                    [0.54830101, 0.81911722, 0.16856154],
                    [0.62631956, -0.53577657, 0.56627491],
                    [0.55415685, -0.20491572, -0.80679597]
                ]
            ),
        ],
        [
            [np.pi, np.pi / 2, np.pi / 4],
            np.array(
                [
                    [0.54830101, 0.81911722, 0.16856154],
                    [0.62631956, -0.53577657, 0.56627491],
                    [0.55415685, -0.20491572, -0.80679597]
                ]
            )
        ]
    ])
    def test_ExponentialMapWorks(self, params, expected):
        skew = Rotation3D.Hat(params)
        ret = Rotation3D.Exp(skew)
        close = np.allclose(ret, expected)
        self.assertTrue(close)

    @parameterized.expand([
        [
            np.array(
                [
                    [0.54830101, 0.81911722, 0.16856154],
                    [0.62631956, -0.53577657, 0.56627491],
                    [0.55415685, -0.20491572, -0.80679597]
                ]
            ),
            np.array(
                [
                    [0, -np.pi / 4, np.pi / 2],
                    [np.pi / 4, 0, -np.pi],
                    [-np.pi / 2, np.pi, 0]
                ])
        ]
    ])
    def test_LogarithmicMapWorks(self, rotationMat, skew):
        ret = Rotation3D.Log(rotationMat)
        parmas = Rotation3D.Vee(skew)

        axisAngle = AxisAngles.fromAngleMagnitude(parmas)
        resRot = Rotation3D()
        resRot.setAxisAngles(axisAngle)
        resRot = resRot.rotM


        parmas2 = Rotation3D.Vee(ret)
        axisAngle2 = AxisAngles.fromAngleMagnitude(parmas2)
        resRot2 = Rotation3D()
        resRot2.setAxisAngles(axisAngle2)
        resRot2 = resRot2.rotM


        self.assertTrue(np.allclose(resRot.rotM, resRot2.rotM))
