#!/usr/bin/env python3
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import rospy 
import time
#import scipy as sp

'''
mass[i][0] - max or min value (1 or 0)
mass[i][1] - degree of point (gradus)
mass[i][2] - value of point (range)
mass[i][3] - time of uppering and lowering
''' 


class Algorithm(object):
    _spdL = 0
    _spdR = 0
    _fMax = False
    _fMin = False
    _aCounter = 0 
    _tmp = 0
    _target = 0
    _targetPoint = 0
    _mass = np.empty((0,4), np.int32)
    _targets = np.array([])


    def __init__(self):
        return

    def clear(self):
        self._fMax = False
        self._fMin = False
        self._aCounter = 0
        self._tmp = 0
        self._target = 0
        self._targetPoint = 0
        self._mass = np.empty((0,4), np.int32)
        self._targets = np.array([], np.int32)
        
    def filter(self, array):
        if array[0] == 0:
            array[0] = array[359]
        for i in range(1,360):
            if array[i] == 0:
                array[i] = array[i-1]

        return array

    def pullingMass(self, array):
        for i in range (0,array.size):
            if array[i-1] < array[i] or self._fMax:
                self._fMax = True
                self._tmp += 1 
                if array[i-1] > array[i]:
                    self._mass =  np.append(self._mass, np.array([[1, i, array[i-1], self._tmp]],  np.int32), axis = 0)
                    self._tmp = 0
                    self._fMax = False
                    self._fMin = True
            if array[i-1] > array[i] or self._fMin:
                self._fMin = True
                self._tmp += 1 
                if array[i-1] < array[i]:
                    self._mass = np.append(self._mass, np.array([[0, i, array[i-1], self._tmp]],  np.int32), axis = 0)
                    self._tmp = 0
                    self._fMin = False
                    self._fMax = True
 
        """if self._fMax and array[359] > array[0]:
            self._mass = np.append(self._mass, np.array([[1, 359, array[359], self._tmp]],  np.int32), axis = 0)
            self._tmp = 0
        if self._fMin and array[359] < array[0]:
            self._mass = np.append(self._mass, np.array([[0, 359, array[359], self._tmp]], np.int32), axis = 0)"""

        self._fMin = False
        self._fMax = False

    def findDirection(self, middle):
        try:
            for i in range(0, self._mass.shape[0]): 
                if self._mass[i][0] == 0 and self._mass[i][2] > middle:
                    self._targets = np.append(self._targets, self._mass[i][1])

            for i in range(0,self._mass.shape[0]):
                if self._mass[i][0] == 0 and np.max(self._targets) == self._mass[i][1]:
                    self._targetPoint = np.max(self._targets)

            clearTargets = np.array([])
            tmp = 0
            counter = 0
            n = 15

            for i in range(0, self._targets.size-1):
                if self._targets[i+1] - self._targets[i] <= n:
                    tmp += self._targets[i]
                    counter += 1
                if self._targets[i+1] - self._targets[i] > n and tmp == 0:    
                    clearTargets = np.append(clearTargets, self._targets[i])
                if self._targets[i+1] - self._targets[i] > n and tmp != 0:
                    clearTargets = np.append(clearTargets, int(tmp/counter))
                    tmp = 0
                    counter = 0

            if self._targets[self._targets.size-1] - self._targets[0] <= n:
                    tmp += self._targets[self._targets.size-1]
                    counter += 1
                    clearTargets = np.append(clearTargets, int(tmp/counter))
                    tmp = 0
                    counter = 0
            if self._targets[self._targets.size-1] - self._targets[0] > n and tmp == 0:    
                    clearTargets = np.append(clearTargets, self._targets[self._targets.size-1])
            if self._targets[self._targets.size-1] - self._targets[0] > n and tmp != 0:    
                    clearTargets = np.append(clearTargets, int(tmp/counter))
                    tmp = 0
                    counter = 0
        except:
            pass
        return clearTargets                        

    def launch(self, msg_array):
        self.clear()
        calculatedArray = self.filter((np.array(msg_array) * 1000))
        self.pullingMass(calculatedArray)
        array = np.array((self.findDirection(calculatedArray.mean())), np.int32)
        
        """
        try: 
            if array[0] >= 350 or array[0] <= 10:
                self._spdL = 50
                self._spdR = 50
            else:
                self._spdL = -25
                self._spdR = 25
                   
        except:
            self._spdL = 20
            self._spdR = 20"""

        self._spdL = 20
        self._spdR = 20
        """for i in range (0, array.size):
            if array[i] >= 357 or array[i] <= 2:
                self._spdL = 50
                self._spdR = 50
                break
                #print(self._spdL)
                #print(self._spdR)
                time.sleep(1)
                self._spdL = 0
                self._spdR = 0
                #print(self._spdL)
                #print(self._spdR)
                #time.sleep(1)
            else:
                self._spdL = 25
                self._spdR = -25
                #print(self._spdL)
                #print(self._spdR)
                #time.sleep(1)
                #print(self._spdL)
                #print(self._spdR)
                #self._spdL = 0
                #self._spdR = 0
                #time.sleep(1)"""


        #self.show(array)


    def show(self, array):
        #print(self._mass)
        #print(self._mass.mean())
        #print(self._targets)
        print(array)
        #print(self._targetPoint)
        print(self._spdL)
        print(self._spdR)


    
    
    def getSpeed(self):
        return int(self._spdL), int(self._spdR)
        

    

        