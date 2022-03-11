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


class Algorithm:
    _spdL = 0
    _spdR = 0
    _fMax = False
    _fMin = False
    _aCounter = 0 
    _tmp = 0
    _target = 0
    _targetPoint = 0
    _mass = np.zeros((60, 4), np.int32)
    

    def __init__(self):
        return

    def clear(self):
        self._fMax = False
        self._fMin = False
        self._aCounter = 0
        self._tmp = 0
        self._target = 0
        self._targetPoint = 0
        self._mass = np.zeros((60, 4), np.int32)

    def filter(self, array):
        if array[0] == 0:
            array[0] = array[359]
        for i in range(1,360):
            if array[i] == 0:
                array[i] = array[i-1]

        return array

    def findSMTH(self, array, i, f_value):
        if array[i-1] < array[i] or f_value:
            f_value = True
            self._tmp += 1 
            if array[i-1] > array[i]:
                self.mass[self._aCounter, 0] = 1
                self.mass[self._aCounter, 1] = i 
                self.mass[self._aCounter, 2] = array[i-1] 
                self.mass[self._aCounter, 3] = self._tmp
                self._tmp = 0
                self._aCounter += 1
                f_value = False

    def calculate(self, msg_array):
        calculatedArray = self.filter(np.array(msg_array) * 1000)

        for i in range (1,360):
            self.findSMTH(calculatedArray, i, self._fMax)
            self.findSMTH(calculatedArray, i, self._fMin)
            if calculatedArray[i-1] < calculatedArray[i] or self._fMax:
                f_max=True
                tmp+=1
        
        if mass[0,0]==1:
            for i in range(0,int(mass[0,1])):
                if array[i-1]<array[i] or f_max:
                    f_max=True
                    tmp+=1
                    if array[i-1]>array[i]:
                        mass[aC,0]=1 #max
                        mass[aC,1]=i #degree
                        mass[aC,2]=array[i-1] #value
                        mass[aC,3]=tmp #rangee of area
                        tmp=0
                        aC+=1
                        f_max=False

                if array[i-1]>array[i] or f_min:
                    f_min=True
                    tmp+=1
                    if array[i-1]<array[i]:
                        mass[aC,0]=0 #min
                        mass[aC,1]=i #degree
                        mass[aC,2]=array[i-1] #value
                        mass[aC,3]=tmp #rangee of area
                        tmp=0
                        aC+=1
                        f_min=False

        for i in range(0, 60):
            if mass[i][0] == 0 and mass[i][2]>target: 
                target = mass[i][1] 

        if targetPoint == (mass[0][1] or mass[1][1] or mass[359][1]):
                self._spdL = 50
                self._spdR = 50
                time.sleep(5)
        else:
            if targetPoint <= 180:
                self._spdL = 0
                self._spdR = 50
            else:
                self._spdL = 0
                self._spdR = 50     
        #print(mass)
        #print(middle)
        #print(targetPoint)
        #print(self._spdL)
        #print(self._spdR)


    
    
    def getSpeed(self):
        return self._spdL, self._spdR
        

    

        