import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
 
plt.style.use("bmh")
 
 
class Chanks(object):
    _count = 0
    _scanArray = None
    _scanArray_first = None
    _scanArray_second = None
    _scanArray_third = None
    _scanArray_fourth = None
    _fig, _ax = plt.subplots()
 
    def __init__(self, scan=np.arange(0, 360)):
        self._createChanks(np.array(scan)*100)
        # for i in range(0, 360):
        # print(self._findXY(scan[i], i))
        

    def _createChanks(self, array):
        self._scanArray = np.array(array).reshape(4, 90)
        # print(self._scanArray)
        self._scanArray_first = pd.DataFrame(np.array(self._scanArray[0, :]).reshape(9, 10),
 
                                             index=["1y", "2y", "3y", "4y",
                                                    "5y", "6y", "7y", "8y", "9y"],
 
                                             columns=["1x", "2x", "3x", "4x", "5x",
                                                      "6x", "7x", "8x", "9x", "10x"])
        self._scanArray_second = pd.DataFrame(np.array(self._scanArray[1, :]).reshape(9, 10),
 
                                              index=["1y", "2y", "3y", "4y",
                                                     "5y", "6y", "7y", "8y", "9y"],
 
                                              columns=["-1x", "-2x", "-3x", "-4x", "-5x",
                                                       "-6x", "-7x", "-8x", "-9x", "-10x"])
        self._scanArray_third = pd.DataFrame(np.array(self._scanArray[2, :]).reshape(9, 10),
 
                                             index=["-1y", "-2y", "-3y", "-4y",
                                                    "-5y", "-6y", "-7y", "-8y", "-9y"],
 
                                             columns=["-1x", "-2x", "-3x", "-4x", "-5x",
                                                      "-6x", "-7x", "-8x", "-9x", "-10x"])
        self._scanArray_fourth = pd.DataFrame(np.array(self._scanArray[3, :]).reshape(9, 10),
 
                                              index=["-1y", "-2y", "-3y", "-4y",
                                                     "-5y", "-6y", "-7y", "-8y", "-9y"],
 
                                              columns=["1x", "2x", "3x", "4x", "5x",
                                                       "6x", "7x", "8x", "9x", "10x"])
 
    def _findXY(self, distance, index):
        return np.array([distance * math.cos((index * math.pi) / 180), 
                        distance * math.sin((index * math.pi) / 180)]
                        )
 
    def _showWithIndex(self, id):
        allChank = {
            1: self._scanArray_first,
            2: self._scanArray_second,
            3: self._scanArray_third,
            4: self._scanArray_fourth
        }
        print(allChank[id])
 
    def _showScatter(self, ScyOfPointsX, ScyOfPointsY=None):
        plt.ion()
        self._fig.canvas.draw()
        self._fig.canvas.flush_events()
        self._ax.plot(ScyOfPointsX, s=1)
        plt.pause(0.02)
        plt.show()
    