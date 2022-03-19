import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame as df

from PIDcontroller.PIDAutotune import PIDAutotune as autoPID
from PIDcontroller.PID import PID as mainPID


plt.style.use("bmh")
#from findXY send none if 5 < value or -5 > value
#create 10 on 10 chanks
#buffer on 5 values for any 

class Chanks(object):
    _count = 0

    _spdL = 0
    _spdR = 0

    _kp = 0
    _ki = 0
    _kd = 0 

    _scanArray = None
    _scanArray_back = None
    _scanArray_left = None
    _scanArray_forward = None
    _scanArray_right = None

    _scanSTDleft = None
    _scanSTDright = None

    _scanChank = None

    _frstK = 0
    _scndK = 0
    _thrdK = 0
    _frthK = 0

    _leftCount = 0
    _rightCount = 0

    _arrayXY = []
    _fig, _ax = plt.subplots()

    def __init__(self, kp, ki, kd):
        self._kp = kp
        self._ki = ki
        self._kd = kd

    def calculate(self):
        self._arrayXY = []
        self.__createChanks()
        for i in range(0, 90):
            self._arrayXY.append([self.__findX(self._scanArray[i], i),self.__findY(self._scanArray[i], i)])
            self._scanArray_back[abs(self.__findX(self.__map(self._scanArray[i if (i < 46) else 270 + i], 1, 4, np.concatenate((self._scanArray[0:45], self._scanArray[315:359]), axis=0).min(), np.concatenate((self._scanArray[0:45], self._scanArray[315:359]), axis=0).max()), i if (i < 46) else 270 + i)),
                                abs(self.__findY(self.__map(self._scanArray[i if (i < 46) else 270 + i], 1, 4, np.concatenate((self._scanArray[0:45], self._scanArray[315:359]), axis=0).min(),  np.concatenate((self._scanArray[0:45], self._scanArray[315:359]), axis=0).max()), i if (i < 46) else 270 + i))] += self._scanArray[i if (i < 46) else 270 + i] * 100

            self._scanArray_left[(self.__findX(self.__map(self._scanArray[45 + i], 1, 4, self._scanArray[45:135].min(), self._scanArray[45:135].max()), 45 + i)),
                                abs(self.__findY(self.__map(self._scanArray[45 + i], 1, 4, self._scanArray[45:135].min(), self._scanArray[45:135].max()), 45 + i))] += self._scanArray[45 + i] * 100

            self._scanArray_forward[(self.__findX(self.__map(self._scanArray[135 + i], 1, 4, self._scanArray[135:225].min(), self._scanArray[135:225].max()), 135 + i)),
                                (self.__findY(self.__map(self._scanArray[135 + i], 1, 4, self._scanArray[135:225].min(), self._scanArray[135:225].max()), 135 + i))] += self._scanArray[i + 135] * 100

            self._scanArray_right[abs(self.__findX(self.__map(self._scanArray[225 + i], 1, 4, self._scanArray[225:315].min(), self._scanArray[225:315].max()), 225 + i)),
                                (self.__findY(self.__map(self._scanArray[225 + i], 1, 4, self._scanArray[225:315].min(), self._scanArray[225:315].max()), 225 + i))] += self._scanArray[i + 225] * 100

        # print(f'Cov with left and right: {round(np.cov(self._scanArray_left, self._scanArray_right).sum()/1000)}')
        # print(f'Cov with left and forward: {round(np.cov(self._scanArray_left, self._scanArray_forward).sum()/1000)}')
        # print(f'Cov with left and back: {round(np.cov(self._scanArray_left, self._scanArray_back).sum()/1000)}')
        # print(f'Cov with right and forward: {round(np.cov(self._scanArray_right, self._scanArray_forward).sum()/1000)}')
        # print(f'Cov with right and back: {round(np.cov(self._scanArray_right, self._scanArray_back).sum()/1000)}')
        # print(f'Cov with forward and back: {round(np.cov(self._scanArray_forward, self._scanArray_back).sum()/1000)}')


        # print(f'Left sum = {self._scanArray_left.sum()}')
        # print(f'Right sum = {self._scanArray_right.sum()}')
        # print(f'Left std = {np.std(self._scanArray_left, dtype=np.int32)}')
        # print(f'Right std = {np.std(self._scanArray_right, dtype=np.int32)}')
        # print(f'Back std = {np.std(self._scanArray_back, dtype=np.int32)}')
        # print(f'Forward std = {np.std(self._scanArray_forward, dtype=np.int32)}')

        self._scanSTDleft = np.std(self._scanArray_left, dtype=np.int32) - (np.std(self._scanArray_back, dtype=np.int32) + np.std(self._scanArray_forward, dtype=np.int32)) / 2
        self._scanSTDright = np.std(self._scanArray_right, dtype=np.int32) - (np.std(self._scanArray_back, dtype=np.int32) + np.std(self._scanArray_forward, dtype=np.int32)) / 2

        self._leftCount = int((np.cov(self._scanArray_left, self._scanArray_forward).sum() + np.cov(self._scanArray_left, self._scanArray_back).sum()) / 2000)
        self._rightCount = int((np.cov(self._scanArray_right, self._scanArray_forward).sum() + np.cov(self._scanArray_right, self._scanArray_back).sum()) / 2000)

        self._leftCountTest = int((np.cov(self._scanArray_left, self._scanArray_forward, bias=True).sum() + np.cov(self._scanArray_left, self._scanArray_back, bias=True).sum()) / 2000)
        self._rightCountTest = int((np.cov(self._scanArray_right, self._scanArray_forward, bias=True).sum() + np.cov(self._scanArray_right, self._scanArray_back, bias=True).sum()) / 2000)

        self._spdR = self.__map(self._rightCountTest - self._leftCountTest, -10 * self._leftCount/self._leftCountTest, 10 * self._rightCount / self._rightCountTest, self._leftCount, self._rightCount)
        self._spdL = self.__map(self._leftCountTest - self._rightCountTest, -10 * self._leftCount/self._leftCountTest, 10 * self._rightCount / self._rightCountTest, self._leftCount, self._rightCount)

        # print(f'Left count = {self._leftCount}, Right count = {self._rightCount}')
        # print(f'Left count test = {self._leftCountTest}, Right count test = {self._rightCountTest}')
        # print(f'Attitude left = {self._leftCount/self._leftCountTest}, Attitude right = {self._rightCount/self._rightCountTest}')

        #print(self._scanArray[0:90])
        #self.showAll()
        #print(np.array(self._arrayXY[0:90])/1000)
        #print()

    def setScanArray(self, scan):
        self._scanArray = np.array(scan)

    def getSpeed(self):
        return int(self._spdL) if self._spdL > self._spdR else int(self._spdL * (-0.1)), int(self._spdR) if self._spdR > self._spdL else int(self._spdR * (-0.1))

    def covariance(self, a, b):
        
        if len(a) != len(b):
            return

        a_mean = np.mean(a)
        b_mean = np.mean(b)

        sum = 0

        for i in range(0, len(a)):
            sum += ((a[i] - a_mean) * (b[i] - b_mean))

        return sum/(len(a)-1)

    def saveDataSet_to_Csv(self, value):
        if self._count < value:
            self._scanArray.to_json("/home/perch/catkin_ws/src/maze_perch/src/Helpers/datasets/Data1/scanData" + str(self._count) + ".json")
            print("/home/perch/catkin_ws/src/maze_perch/src/Helpers/datasets/Data5/scanData" + str(self._count) + ".json")
            self._count+=1
        else:
            print("Done!")

    def __PID(self, target, current):
        mPID = mainPID(5, self._kp, self._ki, self._kd, 50, 265)
        return mPID.calc(current, target)

    def __findY(self, distance, index):
        return int(distance * math.cos((index * math.pi) / 180))

    def __findX(self, distance, index):
        return int(distance * math.sin((index * math.pi) / 180))

    def __map(self, value, new_min, new_max, old_min, old_max):
        return ((value - old_min) * (new_max - new_min)) / (old_max - old_min) + new_min

    def __ABCmap(self, value, new_min, new_max, old_min, old_max):
        return abs(((value - old_min) * (new_max - new_min)) / (old_max - old_min) + new_min)

    def showWithIndex(self, id):
        allChank = {
            1: df(self._scanArray_back, index=[1, 2, 3, 4, 5], columns=[1, 2, 3, 4, 5]),
            2: df(self._scanArray_left, index=[1, 2, 3, 4, 5], columns=[-1, -2, -3, -4, -5]),
            3: df(self._scanArray_forward, index=[-1, -2, -3, -4, -5], columns=[-1, -2, -3, -4, -5]),
            4: df(self._scanArray_right, index=[-1, -2, -3, -4, -5], columns=[1, 2, 3, 4, 5])
        }
        print(allChank[id])

    def showAll(self):
        print(pd.concat([pd.concat([df(self._scanArray_left, index=[5, 4, 3, 2, 1], columns=[-5, -4, -3, -2, -1]),
                        df(self._scanArray_back, index=[5, 4, 3, 2, 1], columns=[1, 2, 3, 4, 5])],
                        axis=1),
                        
                        pd.concat([df(self._scanArray_forward, index=[-1, -2, -3, -4, -5], columns=[-5, -4, -3, -2, -1]),
                        df(self._scanArray_right, index=[-1, -2, -3, -4, -5], columns=[1, 2, 3, 4, 5])],
                        axis=1)],
                        axis=0))

    def showScatter(self, ScyOfPointsX, ScyOfPointsY=None):
        plt.ion()
        self._fig.canvas.draw()
        self._fig.canvas.flush_events()
        self._ax.plot(ScyOfPointsX, s=1)
        plt.pause(0.02)
        plt.show()

    def __createChanks(self):
        self._scanChank = np.zeros((4,25))
        self._scanArray_back = np.array(self._scanChank[0, :]).reshape(5, 5)
        self._scanArray_left = np.array(self._scanChank[1, :]).reshape(5, 5)
        self._scanArray_forward = np.array(self._scanChank[2, :]).reshape(5, 5)
        self._scanArray_right = np.array(self._scanChank[3, :]).reshape(5, 5)