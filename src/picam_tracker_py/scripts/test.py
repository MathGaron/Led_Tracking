#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on August 05 12:34:50 2014

@author: Mathieu Garon
@email: mathieugaron91@gmail.com
"""


import numpy as np
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def norm_correlate(normalizedTemplate,signal):
    sumTemplate = normalizedTemplate.sum()

    signalMean = np.mean(signal)
    signalStd = np.std(signal)
    conv = np.convolve(normalizedTemplate[::-1],signal, mode='valid')
    result = (conv - sumTemplate * signalMean)/signalStd
    return result

def normalize_array(array):
    return (array - np.mean(array)/(np.std(array)*len(array)))

if __name__ == "__main__":
    data1 = np.array([1,0,0,0,1,10,0,0,0,10,40,1,0,0,40,1,0,0,0])
    data2 = np.array([1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1])
    data3 = np.array([0,1,1,1,0,0,1,1,1,0,0,1,1,0,1,0,1,1,1])
    data4 = np.array([1,0,0,0,1])
    
    normData = normalize_array(data3) 
    
    out = []
    start = time.time()
    i=0
    #for i in range(len(data1)-4):
    res = norm_correlate(normData,data1[i:i+5])
    #out = np.concatenate((out,res),axis=0)
    print time.time() - start
    #print data
    #print out
    plt.plot(np.real(out))
    plt.savefig('/home/CameraNetwork/July/plot.jpg')
    print "saved"
