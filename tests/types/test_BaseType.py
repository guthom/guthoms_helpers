import unittest
from unittest import TestCase
import numpy as np
from typing import List, Tuple
from guthoms_helpers.base_types.Rotation2D import Rotation2D
from guthoms_helpers.base_types.Vector2D import Vector2D


class BaseTypeTests(TestCase):

    def test_Rotation2DFrom2Vectors(self):
        #yUp
        vec1 = Vector2D(0.0, 0.0)
        rot = Rotation2D.From2Vectors(vec1, vec2=Vector2D(1.0, 1.0))
        self.assertEqual(rot.Deg(), 45.0)

        rot = Rotation2D.From2Vectors(vec1, vec2=Vector2D(1.0, -1.0))
        self.assertEqual(rot.Deg(), -45.0)

        rot = Rotation2D.From2Vectors(vec1, vec2=Vector2D(-1.0, -1.0))
        self.assertEqual(rot.Deg(), -135.0)

        rot = Rotation2D.From2Vectors(vec1, vec2=Vector2D(-1.0, 1.0))
        self.assertEqual(rot.Deg(), 135.0)

        rot = Rotation2D.From2Vectors(vec1, vec2=Vector2D(0.0, 1.0))
        self.assertEqual(rot.Deg(), 90.0)

        rot = Rotation2D.From2Vectors(vec1, vec2=Vector2D(0.0, -1.0))
        self.assertEqual(rot.Deg(), -90.0)

        rot = Rotation2D.From2Vectors(vec1, vec2=Vector2D(1.0, 0.0))
        self.assertEqual(rot.Deg(), 0.0)

        rot = Rotation2D.From2Vectors(vec1, vec2=Vector2D(-1.0, 0.0))
        self.assertEqual(rot.Deg(), 180.0)

