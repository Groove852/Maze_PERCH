#!/usr/bin/env python3
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import rospy 
#import scipy as sp


class Algorithm:
    def __init__(self, msg_array):
        f_max = False
        f_min = False
        middle = 0
        tmp = 0
        aC = 0 #array counter
        #mass = np.zeros(30, 4)
        #mass=[[]*4]*30
        mass = np.zeros((30, 4), np.int32)
        array = np.array(msg_array)
        '''
        mass[i][0] - max or min value (1 or 0)
        mass[i][1] - degree of point (gradus)
        mass[i][2] - value of point (range)
        ''' 

        #filter
        if array[0] == 0:
            array[0] = array[359]
        array[0]=array[0]*1000    
        for i in range(1,360):
            array[i]=array[i]*1000 
            if array[i] == 0:
                array[i] = array[i-1]
            middle += array[i]
        middle = middle / 360 

        #sorting
          
        if array[359]<array[0] or f_max:
            f_max=True
            tmp+=1
        
        if array[359]>array[0] or f_min:
            f_min=True
            tmp+=1  

        for i in range (1,360):
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

            if array[i-1]<array[i] or f_max:
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

        #rospy.loginfo(mass)
        #rospy.loginfo(middle)

        #for i in range(0, )
        print(mass)
        print(middle)
        print()

        

        