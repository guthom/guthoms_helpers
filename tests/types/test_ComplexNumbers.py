import unittest
from unittest import TestCase
import numpy as np
from typing import List, Tuple
from guthoms_helpers.base_types.Complex import Complex
from guthoms_helpers.common_helpers.RandomHelper import RandomHelper
from math import pow, sqrt


class ComplexNumbersTests(TestCase):

    def GetRandomComplexPair(self):
        a = RandomHelper.RandomFloat(-200, 200)
        b = RandomHelper.RandomFloat(-200, 200)
        c = RandomHelper.RandomFloat(-200, 200)
        d = RandomHelper.RandomFloat(-200, 200)

        return Complex(a, b), Complex(c, d)

    def test_ComplexAddition(self):
        for i in range(0, 10):
            a, b = self.GetRandomComplexPair()
            res = a + b
            self.assertEqual(res.r, a.r + b.r)
            self.assertEqual(res.i, a.i + b.i)

    def test_ComplexSubstraction(self):
        for i in range(0, 10):
            a, b = self.GetRandomComplexPair()
            res = a - b
            self.assertEqual(res.r, a.r - b.r)
            self.assertEqual(res.i, a.i - b.i)

    def test_ComplexMultiplication(self):
        a = Complex(3, 2)
        b = Complex(1, 4)
        res = Complex(-5, 14)
        self.assertEqual(a*b, res)

        a = Complex(1, 1)
        b = Complex(1, 1)
        res = Complex(0, 2)
        res_ = a * b
        self.assertEqual(a * b, res)

    def test_ComplexDivision(self):
        a = Complex(3, 2)
        b = Complex(4, -3)
        res = Complex(6/25, 17/25)
        self.assertEqual(a / b, res)

        a = Complex(4, 5)
        b = Complex(2, 6)
        res = Complex(19/20, -7/20)
        self.assertEqual(a / b, res)

        a = Complex(-6, -3)
        b = Complex(4, 6)
        res = Complex(-21 / 26, 6 / 13)
        self.assertEqual(a / b, res)




