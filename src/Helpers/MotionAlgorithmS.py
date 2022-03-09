import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd

from PIDcontroller.PIDAutotune import PIDAutotune as autoPID
from PIDcontroller.PID import PID as mainPID


plt.style.use("bmh")


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
    _fig, _ax = plt.subplots()

    def __init__(self, kp, ki, kd):
        self._kp = kp
        self._ki = ki
        self._kd = kd

    def calculate(self):
        self.__createChanks()
        for i in range(0, 90):
            self._scanArray_first[[self.__map(self.__findY(self._scanArray[0 + i],  0 + i), 1, 10),
                                  self.__map(self.__findX(self._scanArray[0 + i],  0 + i), 1, 10)]] = self._scanArray[0 + i]
            
            self._scanArray_second[self.__map(self.__findY(self._scanArray[90 + i],  90 + i), 1, 10),
                                   self.__map(self.__findX(self._scanArray[90 + i],  90 + i), 1, 10)] = self._scanArray[90 + i]
            
            self._scanArray_third[[self.__map(self.__findY(self._scanArray[180 + i],  180 + i), 1, 10),
                                   self.__map(self.__findX(self._scanArray[180 + i],  180 + i), 1, 10)]] = self._scanArray[180 + i]
            
            self._scanArray_fourth[self.__map(self.__findY(self._scanArray[270 + i],  270 + i), 1, 10),
                                   self.__map(self.__findX(self._scanArray[270 + i],  270 + i), 1, 10)] = self._scanArray[270 + i]
        self.showWithIndex(1)

    def setScanArray(self, scan=np.arange(0, 360)):
        self._scanArray = np.array(scan)

    def getSpeed(self):
        return self._spdL, self._spdR

    def saveDataSet_to_Csv(self, value):
        if self._count < value:
            self._scanArray.to_csv("/home/perch/catkin_ws/src/maze_perch/src/Helpers/datasets/Data5/scanData" + str(self._count) + ".csv")
            print("/home/perch/catkin_ws/src/maze_perch/src/Helpers/datasets/Data5/scanData" + str(self._count) + ".csv")
            self._count+=1
        else:
            print("Done!")

    def __PID(target, current):
        mPID = mainPID(5, self._kp, self._ki, self._kd, 50, 265)
        return mPID.calc(current, target)

    def __findY(self, distance, index):
        return distance * math.cos((index * math.pi) / 180)

    def __findX(self, distance, index):
        return distance * math.sin((index * math.pi) / 180)

    def __map(self, value, new_min, new_max):
        return (((value - self._scanArray.min()) * (new_max - new_min)) / (self._scanArray.max() - self._scanArray.min())) + new_min

    def showWithIndex(self, id):
        allChank = {
            1: pd.DataFrame(self._scanArray_first,
                            index=[1, 2, 3, 4, 5, 6, 7, 8, 9],
                            columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
            2: self._scanArray_second,
            3: self._scanArray_third,
            4: self._scanArray_fourth
        }
        print(allChank[id])

    def showScatter(self, ScyOfPointsX, ScyOfPointsY=None):
        plt.ion()
        self._fig.canvas.draw()
        self._fig.canvas.flush_events()
        self._ax.plot(ScyOfPointsX, s=1)
        plt.pause(0.02)
        plt.show()

    def __createChanks(self):
        self._scanArray = self._scanArray.reshape(4, 90)
        """self._scanArray_first = pd.DataFrame(np.array(self._scanArray[0, :]).reshape(9, 10),
 
                                             index=[1, 2, 3, 4,
                                                    5, 6, 7, 8, 9],
 
                                             columns=[1, 2, 3, 4, 5,
                                                      6, 7, 8, 9, 10])
        self._scanArray_second = pd.DataFrame(np.array(self._scanArray[1, :]).reshape(9, 10),
 
                                              index=[1, 2, 3, 4,
                                                     5, 6, 7, 8, 9],
 
                                              columns=[-1, -2, -3, -4, -5,
                                                       -6, -7, -8, -9, -10])
        self._scanArray_third = pd.DataFrame(np.array(self._scanArray[2, :]).reshape(9, 10),
 
                                             index=[-1, -2, -3, -4,
                                                    -5, -6, -7, -8, -9],
 
                                             columns=[-1, -2, -3, -4, -5,
                                                      -6, -7, -8, -9, -10])
        self._scanArray_fourth = pd.DataFrame(np.array(self._scanArray[3, :]).reshape(9, 10),
 
                                              index=[-1, -2, -3, -4,
                                                     -5, -6, -7, -8, -9],
 
                                              columns=[1, 2, 3, 4, 5,
                                                       6, 7, 8, 9, 10])
        """
        self._scanArray_first = np.array(self._scanArray[0, :]).reshape(9, 10)
        self._scanArray_second = np.array(self._scanArray[1, :]).reshape(9, 10)
        self._scanArray_third = np.array(self._scanArray[2, :]).reshape(9, 10)
        self._scanArray_fourth = np.array(self._scanArray[3, :]).reshape(9, 10)