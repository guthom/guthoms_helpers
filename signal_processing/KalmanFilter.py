import numpy as np
from typing import Optional

from guthoms_helpers.common_stuff.DataBuffer import DataBuffer


class KalmanState(object):

    def __init__(self, Y_m: np.array = np.array([[0.0]]), Y_err: np.array = 0.0, X_state: np.array = np.array([[0.0]]),
                 Xp_state: np.array = np.array([[0.0]]), K: np.array = np.array([[0.0]]),
                 P_state: np.array = np.array([[0.0]]), Pp_state: np.array = np.array([[0.0]])):
        self.Y_m = Y_m
        self.Y_err = Y_err

        self.X_state = X_state
        self.Xp_state = Xp_state

        # Kalman Gain
        self.K = K

        self.P_state = P_state
        self.Pp_state = Pp_state

    @property
    def Y_state(self):
        return self.Y_m + self.Y_err

class KalmanFilter(object):

    def __init__(self, varCount: int = 1, dependencyMat: Optional[np.array] = None, R: np.array=np.array([[0.0]]),
                 X_0: Optional[np.array] = None, u: Optional[np.array] = None, P_0: Optional[np.array] = None,
                 maxBufferSize: int = 100):

        self.varCount = varCount

        # contains buffer of KalmanState objects
        # TODO: Needs to be garbage sensitive -> This is currently a known memory leak!!
        self.stateBuffer: DataBuffer = DataBuffer(maxBufferSize)
        # TODO: Needs to be garbage sensitive -> This is currently a known memory leak!!
        self.states: DataBuffer = DataBuffer(maxBufferSize)
        # Contains the most recent state of the kalman system
        self.currentState = None

        # the needed Helper/Transformations matrices
        self.matA = np.identity(varCount)
        self.matB = np.transpose(np.ones(varCount))
        self.matC = np.identity(varCount)
        self.matH = np.identity(varCount)

        # The process noise covariance matrix
        self.matQ = np.zeros((varCount, varCount))

        #controll variable matrix -> prediction model
        if u is not None:
            self.u = u
        else:
            self.u = np.zeros(varCount)
        self.matw = np.zeros(varCount)

        # the "trust" for the measurements
        if R is not None:
            assert(R.shape[0] == varCount)
            self.R = R
        else:
            self.R = np.zeros(varCount)

        if X_0 is not None:
            assert (X_0.shape[0] == varCount)
        else:
            X_0 = np.zeros(varCount)

        if dependencyMat is not None:
            self.matA = dependencyMat

        # init Filter
        self.SetInitialState(X_0, P_0)

    @property
    def prevState(self):
        return self.stateBuffer.GetLastItem(False)

    def SetInitialState(self, X_0: np.array, P_0: Optional[np.array]=None):
        self.currentState = KalmanState()
        self.currentState.X_state = X_0

        if P_0 is None:
            self.currentState.P_state = np.identity(self.varCount)
        else:
            assert (X_0.shape[0] == self.varCount)
            self.currentState.P_state = P_0

        #append X_state for better use of the filtered row
        self.states.append(self.currentState.X_state)

    def AddMeasurement(self, Y_m: np.array, Y_err: Optional[np.array]=None):

        self.stateBuffer.append(self.currentState)

        self.currentState = KalmanState()

        self.currentState.Y_m = Y_m

        if Y_err is None:
            Y_err = np.zeros(self.varCount)
        self.currentState.Y_err = Y_err

        self.RunIteration()
        return self.currentState

    def RunIteration(self):

        self.Calc_PredState()
        self.Calc_PredCovMat()
        self.Calc_Gain()
        self.Calc_CurrentState()
        self.Calc_CovMatrix()


        #append X_state for better use of the filtered row
        self.states.append(self.currentState.X_state)


    def Calc_PredState(self):
        first = np.matmul(self.matA, self.prevState.X_state)
        if self.u.shape[0] == 1:
            second = self.matB * self.u + self.matw
        else:
            second = np.matmul(self.matB, self.u) + self.matw
        predState = first + second
        self.currentState.Xp_state = predState

    def Calc_PredCovMat(self):
        first = np.matmul(self.matA, self.prevState.P_state)
        second = np.matmul(first, np.transpose(self.matA))
        state = second + self.matQ
        self.currentState.Pp_state = state

    def Calc_Gain(self):
        num = np.matmul(self.currentState.Pp_state, np.transpose(self.matH))
        first = np.matmul(self.matH, self.currentState.Pp_state)
        denum = np.matmul(first, np.transpose(self.matH) + self.R)

        if np.array_equal(first, denum):
            gain = np.identity(num.shape[0])
        else:
            #prevent zero deviding with where statement
            gain = np.divide(num, denum, where=denum != 0)

        self.currentState.K = gain

    def Calc_CurrentState(self):
        first = np.matmul(self.matH, np.transpose(self.currentState.Xp_state))
        third = self.currentState.Y_state - np.transpose(first)
        second = np.matmul(self.currentState.K, np.transpose(third))
        state = self.currentState.Xp_state + np.transpose(second)

        self.currentState.X_state = state

    def Calc_CovMatrix(self):
        I = np.identity(self.varCount)
        second = np.matmul(self.currentState.K, self.matH)
        third = I - second
        pState = np.matmul(third, self.currentState.Pp_state)
        self.currentState.P_state = pState