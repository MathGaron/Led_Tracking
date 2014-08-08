#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on August 08:44:20 2014

@author: Mathieu Garon
@email: mathieugaron91@gmail.com
"""

import rospy
from cv_bridge import CvBridge, CvBridgeError

import cv2
import os
import io
import numpy as np
import threading
import time
import correlationBuffer as cbuff
import sharedGlobals as sg


class TimeCorrelation(threading.Thread):
    def __init__(self):
        super(TimeCorrelation,self).__init__()
        self.terminated = False
        self.start()

    def run(self):
        while not self.terminated:
            if sg.CORR_DATA.isReady():
                #start = time.time()
                with sg.VAR_LOCK:
                    out = sg.CORR_DATA.getImage()
                rect,buff = out[0]
                d,h,w = buff.shape
                sg.PLOT = buff[:,h/2,w/2]
                cv2.circle(buff[0],(h/2,h/2), 10, 255, -1)
                sg.PICTURE = buff[0]
                #print time.time() - start
            else:
                time.sleep(0)

class ImageProcessor(threading.Thread):
    def __init__(self):
        super(ImageProcessor,self).__init__()
        self.stream = io.BytesIO()
        self.frame_id = 0;
        self.event = threading.Event()
        self.terminated = False
        self.start()

    def close_thread(self):
        #reset stream
        self.stream.seek(0)
        self.stream.truncate()
        self.event.clear()
        with sg.VAR_LOCK:
            sg.POOL.append(self)

    def get_gray_image(self):
        self.stream.seek(0)
        return np.fromstring(self.stream.getvalue(),dtype=np.uint8,count=sg._WIDTH*sg._HEIGTH).reshape((sg._HEIGTH,sg._WIDTH))

    def get_foreground(self, img, tresh = 15):
        distance = abs(img.astype(np.float32)-sg.MU)
        return ((distance/np.sqrt(sg.SIG) > tresh).astype(np.uint8))

    def erode(self, img):
        kernel = np.array([[1,0,0,1],
                  [0,1,1,0],
                  [0,1,1,0],
                  [1,0,0,1]],np.uint8)
        return cv2.erode(img,kernel,iterations = 1)
    
    def dilate(self,img):
        kernel = np.array([[0,1,0,0],
                           [0,1,1,1],
                           [1,1,1,0],
                           [0,0,1,0]],np.uint8)
        return cv2.dilate(img,kernel,iterations = 1)

    def getBlobs(self,img):
        contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        rectangleList = []
        for h,cnt in enumerate(contours):
            area = cv2.contourArea(cnt)
            if area > 200:
                x,y,w,h = cv2.boundingRect(cnt)
                rectangleList.append([x,y,w,h])
                cv2.rectangle(img,(x,y),(x+w,y+h),125,2)
        return rectangleList

class GrayFrameCapture(ImageProcessor):
    def __init__(self):
        super(GrayFrameCapture,self).__init__()
    
    def run(self):
        while not self.terminated:
            if self.event.wait(1):
                try:
                    data = self.get_gray_image()
                    with sg.VAR_LOCK:
                        sg.VIDEO_MATRIX[FRAME_COUNT] = data
                        sg.FRAME_COUNT += 1
                        if sg.FRAME_COUNT == 15:
                            sg.DONE = True
                finally: 
                    self.close_thread();

class BackgroundSubstraction(ImageProcessor):
    def __init__(self):
        super(BackgroundSubstraction,self).__init__()

    def run(self):
        while not self.terminated:
            if self.event.wait(1):
                try:
                    startTime = rospy.get_rostime()
                    image = self.get_gray_image()
                    foreground = self.get_foreground(image)
                    data = self.erode(foreground)
                    data = self.dilate(data)
                    rectangles = self.getBlobs(data)
                    deltaTime = rospy.get_rostime() - startTime
                    with sg.VAR_LOCK:
                        sg.VIDEO_MATRIX[self.frame_id] = data*255
                        sg.FRAME_COUNT += 1
                        if sg.FRAME_COUNT == sg._DEPTH - 1:
                            sg.DONE = True
                        sg.TIME_LIST.append(deltaTime)
                finally:
                    self.close_thread()

class Correlation(ImageProcessor):
    def __init__(self):
        super(Correlation,self).__init__()

    def run(self):
        while not self.terminated:
            if self.event.wait(1):
                try:
                    image = self.get_gray_image()
                    startTime = rospy.get_rostime()
                    print startTime
                    with sg.VAR_LOCK:
                        #sg.VIDEO_MATRIX[self.frame_id] = mask
                        sg.FRAME_COUNT += 1
                        sg.CORR_DATA.addImage(image,self.frame_id)
                        if sg.FRAME_COUNT == sg._DEPTH - 1:
                            sg.DONE = True
                        deltaTime = rospy.get_rostime() - startTime
                        sg.TIME_LIST.append(deltaTime)
                finally:
                    self.close_thread()


class TestImageProcessor(ImageProcessor):
    def __init__(self):
        super(TestImageProcessor,self).__init__()

    def run(self):
        while not self.terminated:
            #wait for image:
            if self.event.wait(1):
                try:
                    data = self.get_gray_image();
                    startTime = rospy.get_rostime()
                    with sg.VAR_LOCK:
                        sg.VIDEO_MATRIX[self.frame_id] = data
                        sg.FRAME_COUNT += 1
                        if sg.FRAME_COUNT == sg._DEPTH:
                            sg.DONE = True
                        deltaTime = rospy.get_rostime() - startTime
                        sg.TIME_LIST.append(deltaTime)
                finally:
                    self.close_thread()
def streams():
    frame = 0
    while not sg.DONE:
        with sg.VAR_LOCK:
            if sg.POOL:
                processor = sg.POOL.pop()
            else:
                processor = None
        if processor:
            processor.frame_id = frame
            yield processor.stream
            processor.event.set()
            frame += 1
        else:
            time.sleep(0.1)

class rectangleBuffers:
    """
    Takes rectangles and create a correlation buffer with it, maintain buffers as rectangles
    rectangle = [x,y,w,h]
    """
    def __init__(self,bufferDepth,window,rectangleList = None):
        self.depth = bufferDepth
        self.window = window
        self.bufferList = []
        if rectangleList == None:
            rectangleList = []
        for rectangle in rectangleList:
            x,y,width,heigth = rectangle
            buff = cbuff.CorrelationBuffer(w=width,h=heigth,bufferSize=bufferDepth,windowSize=window)
            self.bufferList.append([rectangle,buff])

    def addRect(self,rectangleList = None):
        if rectangleList == None:
            rectangleList = []
        for rectangle in rectangleList:
            x,y,width,heigth = rectangle
            buff = cbuff.CorrelationBuffer(w=width,h=heigth,bufferSize=self.depth,windowSize=self.window)
            self.bufferList.append([rectangle,buff])

    def remRect(self,rectangleList = None):
        if rectangleList == None:
            rectangleList == []
        for rectangle in rectangleList:
            for index,data in enumerate(self.bufferList):
                rect,buff = data
                if rect == rectangle:
                    del self.bufferList[index]

    def addImage(self,image,index):
        for rect,buff in self.bufferList:
            x,y,w,h = rect
            buff.add(image[y:y+h,x:x+w],index)

    def getImage(self):
        ret = []
        for rect,buff in self.bufferList:
            ret.append([rect,buff.get()])
        return ret

    def isReady(self):
        for rect,buff in self.bufferList:
            return buff.isReady()
        return False

    def debugPrint(self):
        for rect,buff in self.bufferList:
            print rect
            print buff.debugPrint()
            print '\n'

            
if __name__ == "__main__":
    test = rectangleBuffers(20,5,[[2,2,3,3],[1,1,2,2]])
    #test.debugPrint()
    test.addRect([[4,4,1,1]])
    #test.debugPrint()
    test.remRect([[2,2,3,3]])
    #test.debugPrint()
    image = np.ones([5,5])
    test.addImage(image,0)
    #test.debugPrint()
    print test.getImage()
    test.addImage(image,1)
    test.addImage(image,2)
    test.addImage(image,3)
    test.addImage(image,4)
    test.debugPrint()
    test.getImage()
    test.debugPrint()

    empty = rectangleBuffers(20,5)
    empty.debugPrint()
