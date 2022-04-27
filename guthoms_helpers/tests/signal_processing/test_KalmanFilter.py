import unittest

from guthoms_helpers.signal_processing.KalmanFilter import KalmanFilter, KalmanState
import numpy as np
from unittest import TestCase

from typing import List

class KalmanFilterTests(TestCase):

    def setUp(self):
        pass

    def test_singleDimensionRisingOperationWorks(self):
        initialState = [0.0]
        kalmanFilter = KalmanFilter(1, R=np.array([[0.1]]), X_0=np.array(initialState), u=np.array([0]))
        results: List[KalmanState] = []
        for i in range(1, 200):
            result = kalmanFilter.AddMeasurement(np.array([i]))
            results.append(result)

            for j in range(0, result.X_state.shape[0]):
                self.assertTrue(result.X_state[j] < [i])

    def test_singleDimensionFallingOperationWorks(self):
        initialState = [201.0]
        kalmanFilter = KalmanFilter(1, R=np.array([[0.1]]), X_0=np.array(initialState), u=np.array([0]))
        results: List[KalmanState] = []
        for i in range(200, 1, -1):
            result = kalmanFilter.AddMeasurement(np.array([i]))
            results.append(result)

            for j in range(0, result.X_state.shape[0]):
                self.assertTrue(result.X_state[j] > [i])

    def test_multiDimensionOperationWorks(self):
        initialState = [0.0, 0.0]
        kalmanFilter = KalmanFilter(2, R=np.array([[0.1], [0.1]]), X_0=np.array(initialState), u=np.array([0]))
        results: List[KalmanState] = []
        for i in range(1, 200):
            x = np.array([i, i+1])
            result = kalmanFilter.AddMeasurement(x)
            results.append(result)

            for j in range(0, result.X_state.shape[0]):
                self.assertTrue(result.X_state[j] < [i + j])
