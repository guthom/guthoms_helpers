from parameterized import parameterized
import unittest
from unittest import TestCase
import numpy as np
from guthoms_helpers.base_types.Rotation2D import Rotation2D

from math import pow, sqrt

class SO2Tests(TestCase):

    def setUp(self):
        pass

    @parameterized.expand([
        [np.pi/2, np.array([[0, -np.pi/2], [np.pi/2, 0]])]
    ])
    def test_HatOperatorWorks(self, alpha, expected):
        ret = Rotation2D.Hat(alpha)
        self.assertTrue(np.array_equal(ret, expected))

    @parameterized.expand([
        [np.array([[0, -np.pi/2], [np.pi/2, 0]]), np.pi/2]
    ])
    def test_VeeOperatorWorks(self, skew, expected):
        ret = Rotation2D.Vee(skew)
        self.assertEqual(ret, expected)

    @parameterized.expand([
        [
            np.array([[0, -np.pi/2], [np.pi/2, 0]]),
            np.array([
                [np.cos(np.pi / 2), -np.sin(np.pi / 2)],
                [np.sin(np.pi / 2), np.cos(np.pi / 2)]]
            )
        ]
    ])
    def test_ExponentialMapWorks(self, skew, expected):
        ret = Rotation2D.Exp(skew)
        self.assertTrue(np.array_equal(ret, expected))

    @parameterized.expand([
        [
            np.array([
                [np.cos(np.pi / 2), -np.sin(np.pi / 2)],
                [np.sin(np.pi / 2), np.cos(np.pi / 2)]]
            ),
            np.array([[0, -np.pi/2], [np.pi/2, 0]])
        ]
    ])
    def test_LogarithmicMapWorks(self, rotationMat, skew):
        ret = Rotation2D.Log(rotationMat)
        self.assertTrue(np.array_equal(ret, skew))










