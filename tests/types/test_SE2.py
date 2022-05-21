from parameterized import parameterized
import unittest
from unittest import TestCase
import numpy as np
from guthoms_helpers.base_types.Pose2D import Pose2D
from guthoms_helpers.base_types.Rotation2D import Rotation2D

from math import pow, sqrt

class SE2Tests(TestCase):

    def setUp(self):
        pass

    @parameterized.expand([
        [np.array([1.0, 2.0, np.pi]),
         np.array([
             [0,        -np.pi,     1.0],
             [np.pi,     0.0,       2.0],
             [0.0,       0.0,       0.0]
         ])]
    ])
    def test_HatOperatorWorks(self, params, expected):
        ret = Pose2D.Hat(params)
        self.assertTrue(np.array_equal(ret, expected))

    @parameterized.expand([
        [
            np.array(
                [
                    [0, -np.pi, 1.0],
                    [np.pi, 0.0, 2.0],
                    [0.0, 0.0, 0.0]
                ]),
            np.array([1.0, 2.0, np.pi])
        ]
    ])
    def test_VeeOperatorWorks(self, skew, expected):
        ret = Pose2D.Vee(skew)
        self.assertTrue(np.array_equal(ret, expected))

    @parameterized.expand([
        [
            np.array(
                [
                    [0, -np.pi, 1.0],
                    [np.pi, 0.0, 2.0],
                    [0.0, 0.0, 0.0]
                ]),
                np.array([
                    [-1.00000000e+00, -1.22464680e-16, -1.27323954e+00],
                    [1.22464680e-16, -1.00000000e+00,  6.36619772e-01],
                    [0.00000000e+00,  0.00000000e+00,  1.00000000e+00]
                ])
        ]
    ])
    def test_ExponentialMapWorks(self, skew, expected):
        ret = Pose2D.Exp(skew)
        retRot, retTrans = Pose2D.SplitMats(ret)
        params = Pose2D.Vee(skew)

        expectedExp = Rotation2D.Exp(Rotation2D.Hat(params[2]))
        self.assertTrue(np.allclose(expectedExp, retRot))
        self.assertTrue(np.allclose(ret, expected))

    @parameterized.expand([
        [
            np.array([
                [-1.00000000e+00, -1.22464680e-16, -1.27323954e+00],
                [1.22464680e-16, -1.00000000e+00, 6.36619772e-01],
                [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]
            ]),
            np.array(
                [
                    [0, -np.pi, 1.0],
                    [np.pi, 0.0, 2.0],
                    [0.0, 0.0, 0.0]
                ]),
        ]
    ])
    def test_LogarithmicMapWorks(self, se2Mat, skew):
        ret = Pose2D.Log(se2Mat)
        self.assertTrue(np.allclose(ret, skew))










