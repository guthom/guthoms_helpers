from parameterized import parameterized
import unittest
from unittest import TestCase
import numpy as np
from guthoms_helpers.base_types.Pose3D import Pose3D
from guthoms_helpers.base_types.Rotation3D import Rotation3D

from math import pow, sqrt

class SE3Tests(TestCase):

    def setUp(self):
        pass

    @parameterized.expand([
        [np.array([1.0, 2.0, 3.0, np.pi, np.pi/2, np.pi/4]),
         np.array([
             [0,            -np.pi/4,  np.pi/2, 1.0],
             [np.pi/4,      0.0,       -np.pi,  2.0],
             [-np.pi/2,     np.pi,     0.0,     3.0],
             [0.0,          0.0,       0.0,     0.0],
         ])]
    ])
    def test_HatOperatorWorks(self, params, expected):
        ret = Pose3D.Hat(params)
        self.assertTrue(np.array_equal(ret, expected))

    @parameterized.expand([
        [
            np.array(
                [
                    [0, -np.pi / 4, np.pi / 2, 1.0],
                    [np.pi / 4, 0.0, -np.pi, 2.0],
                    [-np.pi / 2, np.pi, 0.0, 3.0],
                    [0.0, 0.0, 0.0, 0.0],
                ]),
            np.array([1.0, 2.0, 3.0, np.pi, np.pi / 2, np.pi / 4])
        ]
    ])
    def test_VeeOperatorWorks(self, skew, expected):
        ret = Pose3D.Vee(skew)
        self.assertTrue(np.array_equal(ret, expected))

    @parameterized.expand([
        [
            [1.0, 2.0, 3.0, -2.3428211, -1.17141054, -0.58570528],
            np.array(
                [
                    [0.54830101,  0.81911722,  0.16856154, 1.29801315],
                    [0.62631956, - 0.53577657,  0.56627491, 2.9010191],
                    [0.55415685, - 0.20491572, - 0.80679597,  0.00590926],
                    [0.0,          0.0,          0.0,          1.0]
                ]),
        ]
    ])
    def test_ExponentialMapWorks(self, params, expected):
        skew = Pose3D.Hat(np.array(params))
        ret = Pose3D.Exp(skew)

        self.assertTrue(np.allclose(ret, expected))

    @parameterized.expand([
        [
            [1.0, 2.0, 3.0, -2.3428211, -1.17141054, -0.58570528],
            np.array(
                [
                    [0.0, 0.58570528, -1.17141054, 1.0],
                    [-0.58570528, 0.0, 2.3428211, 2.0],
                    [1.17141054, -2.3428211, 0.0, 3.0],
                    [0.0, 0.0, 0.0, 0.0],
                ]),
        ]
    ])
    def test_LogarithmicMapWorks(self, params, expected):
        skew = Pose3D.Hat(np.array(params))
        mat = Pose3D.Exp(skew)
        ret = Pose3D.Log(mat)
        params = Pose3D.Vee(ret)
        self.assertTrue(np.allclose(ret, expected))











