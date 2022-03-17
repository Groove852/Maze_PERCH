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
    _scanArray_first = None
    _scanArray_second = None
    _scanArray_third = None
    _scanArray_fourth = None

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
            try:
                self._arrayXY.append([self.__findX(self._scanArray[i], i),self.__findY(self._scanArray[i], i)])
                self._scanArray_first[abs(self.__findX(self.__map(self._scanArray[i], 1, 7, self._scanArray[0:90].min(), self._scanArray[0:90].max()), i)),
                                    abs(self.__findY(self.__map(self._scanArray[i], 1, 7, self._scanArray[0:90].min(), self._scanArray[0:90].max()), i))] += 1 + int(self._scanArray[i])

                self._scanArray_second[(self.__findX(self.__map(self._scanArray[90 + i], 1, 7, self._scanArray[90:180].min(), self._scanArray[90:180].max()), 90 + i)),
                                    abs(self.__findY(self.__map(self._scanArray[90 + i], 1, 7, self._scanArray[90:180].min(), self._scanArray[90:180].max()), 90 + i))] += 1 + int(self._scanArray[90 + i])

                self._scanArray_third[(self.__findX(self.__map(self._scanArray[180 + i], 1, 7, self._scanArray[180:270].min(), self._scanArray[180:270].max()), 180 + i)),
                                    (self.__findY(self.__map(self._scanArray[180 + i], 1, 7, self._scanArray[180:270].min(), self._scanArray[180:270].max()), 180 + i))] += 1 + int(self._scanArray[i + 180])

                self._scanArray_fourth[abs(self.__findX(self.__map(self._scanArray[270 + i], 1, 7, self._scanArray[270:360].min(), self._scanArray[270:360].max()), 270 + i)),
                                    (self.__findY(self.__map(self._scanArray[270 + i], 1, 7, self._scanArray[270:360].min(), self._scanArray[270:360].max()), 270 + i))] += 1 + int(self._scanArray[i + 270])
            except:
                pass

            self._frstK = self._scanArray_first.mean() * 1000
            self._scndK = self._scanArray_second.mean() * 1000
            self._thrdK = self._scanArray_third.mean() * 1000
            self._frthK = self._scanArray_fourth.mean() * 1000

            self._leftCount = int(round((self._frstK - self._scndK) / 7))
            self._rightCount = int(round((self._thrdK - self._frthK) / 7))

            if ((self._leftCount== 0) and (self._rightCount == 0)): self._leftCount, self._rightCount = 50, 50

            self._spdR = self.__map(self._leftCount, 0, 255, 0, 150)
            self._spdL = self.__map(self._rightCount, 0, 255, 0, 150)

            #print(f'Left side :{self._leftCount}')
            #print(f'Right side :{self._rightCount}')

        #print(self._scanArray[0:90])
        #self.showAll()
        #print(np.array(self._arrayXY[0:90])/1000)

    def setScanArray(self, scan):
        self._scanArray = pd.Series(np.array(scan))

    def getSpeed(self):
        return self._spdL, self._spdR

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

    def showWithIndex(self, id):
        allChank = {
            1: df(self._scanArray_first, index=[1, 2, 3, 4, 5], columns=[1, 2, 3, 4, 5]),
            2: df(self._scanArray_second, index=[1, 2, 3, 4, 5], columns=[-1, -2, -3, -4, -5]),
            3: df(self._scanArray_third, index=[-1, -2, -3, -4, -5], columns=[-1, -2, -3, -4, -5]),
            4: df(self._scanArray_fourth, index=[-1, -2, -3, -4, -5], columns=[1, 2, 3, 4, 5])
        }
        print(allChank[id])

    def showAll(self):
        print(pd.concat([pd.concat([df(self._scanArray_second, index=[5, 4, 3, 2, 1], columns=[-5, -4, -3, -2, -1]),
                        df(self._scanArray_first, index=[5, 4, 3, 2, 1], columns=[1, 2, 3, 4, 5])],
                        axis=1),
                        
                        pd.concat([df(self._scanArray_third, index=[-1, -2, -3, -4, -5], columns=[-5, -4, -3, -2, -1]),
                        df(self._scanArray_fourth, index=[-1, -2, -3, -4, -5], columns=[1, 2, 3, 4, 5])],
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
        self._scanArray_first = np.array(self._scanChank[0, :]).reshape(5, 5)
        self._scanArray_second = np.array(self._scanChank[1, :]).reshape(5, 5)
        self._scanArray_third = np.array(self._scanChank[2, :]).reshape(5, 5)
        self._scanArray_fourth = np.array(self._scanChank[3, :]).reshape(5, 5)