#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on August 06 14:21:50 2014

@author: Mathieu Garon
@email: mathieugaron91@gmail.com
"""


import rospy
import numpy as np
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class CorrelationBuffer:
    """
    Special circular buffer that can get data in unordered manner.
    return depth datas when every data have been allocated in the window
    """
    def __init__(self,h=1,w=1,bufferSize=1,windowSize=1):
        self.heigth = h
        self.width = w
        self.depth = bufferSize
        self.windowSize = windowSize
        self.windowBegin = 0
        self.BUFFER = np.zeros([bufferSize,h,w])
        self.readyFlags = np.zeros(bufferSize,np.bool)

    def add(self,data,index):
        h,w = data.shape
        assert h == self.heigth,'Data heigth not matching with BUFFER'
        assert w == self.width,'Data width not matching with BUFFER'
        wrapIndex = index % self.depth
        if( self.readyFlags[wrapIndex]):
            print "Overwriting data warning"
        self.BUFFER[wrapIndex] = data
        self.readyFlags[wrapIndex] = True

    def get(self):
        if(self._windowIsReady()):
            begin = self.windowBegin
            end = begin + self.windowSize
            self.windowBegin = (begin+1)%self.depth
            self.readyFlags[begin] = False
            indices = np.mod(range(begin,end+1),self.depth) #wrap up indices
            return np.take(self.BUFFER,indices,axis=0)
        else:
            return None

    def debugPrint(self):
        print self.readyFlags

    def isReady(self):
        return self._windowIsReady()

    def _windowIsReady(self):
        return np.all(self.readyFlags[self.windowBegin:self.windowBegin+self.windowSize])
        
if __name__ == "__main__":
    buff = CorrelationBuffer(w=2,h=2,bufferSize=6,windowSize=5)
    buff.add(np.ones([2,2]),0)
    buff.add(np.zeros([2,2]),1)
    buff.add(np.ones([2,2]),2)
    buff.add(np.ones([2,2]),3)
    buff.add(np.ones([2,2]),4)
    buff.get()
    buff.add(np.ones([2,2]),5)
    buff.get()
    buff.add(np.zeros([2,2]),6)
    print buff.get()
    print buff.debugPrint()
