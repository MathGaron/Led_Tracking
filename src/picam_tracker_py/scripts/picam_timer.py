#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on July 31 09:51:20 2014

@author: Mathieu Garon
@email: mathieugaron91@gmail.com
"""

import roslib; roslib.load_manifest('picam_tracker_py')
import rospy
from sensor_msgs.msg import Image
import std_srvs.srv

import cv2
import picamera
import wiringpi2 as gpio
import os
import io
import numpy as np
import threading
import time
import image_processor as proc
import sharedGlobals as sg
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class picam_tester:
    def __init__(self):
        try:
            self.picam = picamera.PiCamera()
        except:
            rospy.logfatal("Check if the Picam is free or installed")

        rospy.Service('test_camera',std_srvs.srv.Empty,self.test_cb)
        rospy.Service('gaussian_background_modeling',std_srvs.srv.Empty,self.gauss_BG_model_cb)
        rospy.Service('correlation',std_srvs.srv.Empty,self.correlation_cb)

        self._init_picamera()
        self._init_led()

        #datas:
        self.mu = []
        self.sig = []
        
        self._flash_led(nflash=4)
        rospy.loginfo("Picam_tester ready...")
        rospy.spin()

    def __del__(self):
        self.picam.close()

    def correlation_cb(self,req):
        rospy.loginfo("Correlation")
        w=1296
        h=730
        d=50
        template_signal =np.array([1,1,0,0,1,1,0,0,1,1,1,1,0,0,0,0])
        with sg.VAR_LOCK:
           sg.CORR_DATA = proc.rectangleBuffers(25,len(template_signal),[[250,200,200,200]])  #[[500,200,300,300]])
        corr_thread = proc.TimeCorrelation(template_signal)
        video_fps = self._process_video(proc.Correlation,w,h,d,processors = 3)
        self._get_chunk_time()
        with sg.VAR_LOCK:
            corr_thread.terminated = True
            corr_thread.join()
            self._empty_pool()
            self._reset_globals()
        #self._save_video(filename='correlation.avi',fps=video_fps)
        rospy.loginfo("Save Plot")
        plt.plot(sg.PLOT)
        plt.plot(sg.PLOT2)
        plt.savefig('/home/CameraNetwork/July/plot.jpg')
        cv2.imwrite('/home/CameraNetwork/July/image.jpg',sg.PICTURE)
        rospy.loginfo("Ending service.")
        return []

    def gauss_BG_model_cb(self,req):
        rospy.loginfo("Background Gaussian Modeling")
        self._process_video(proc.GrayFrameCapture)
        with sg.VAR_LOCK:
            self._empty_pool()
            self._reset_globals()
        Matrix = sg.VIDEO_MATRIX[0:15].astype(np.uint16)
        d,h,w = Matrix.shape
        rospy.loginfo("Starting modelisation")
        self.mu = sum(Matrix)/d
        std = Matrix-self.mu
        self.sig = np.sqrt(sum(std*std)/d)
        rospy.loginfo("normfit done...")
        sg.MU = self.mu.astype(np.float32)
        sg.SIG = self.sig.astype(np.float32)
        #substract part:
        rospy.loginfo("Starting background substraction...")
        video_fps = self._process_video(proc.BackgroundSubstraction,depth=30,processors=2)
        self._get_chunk_time()
        with sg.VAR_LOCK:
            self._empty_pool()
            self._reset_globals()
        self._save_video(filename='bg_substraction.avi',fps=video_fps)
        rospy.loginfo("Ending service.")
        return []


    def test_cb(self,req):
        rospy.loginfo("Begin Tests!")
        video_fps = self._process_video(proc.TestImageProcessor)
        totalTime = 0
        self._get_chunk_time()
        with sg.VAR_LOCK:
            self._empty_pool();
            self._reset_globals()
        self.save_video(fps=video_fps)
        rospy.loginfo("Ending service.")
        return []

    def _process_video(self,procClass,width=1296,heigth=730,depth=50, processors=4):
        gpio.digitalWrite(self.led,True)
        with sg.VAR_LOCK:
            #yuv : convert width and height to fit with yuv format
            sg._WIDTH = (width+31)//32*32
            sg._HEIGTH = (heigth+15)//16*16
            sg._DEPTH = depth
            sg.VIDEO_MATRIX = np.zeros([sg._DEPTH + 1,sg._HEIGTH,sg._WIDTH],np.uint8)
            sg.POOL = [procClass() for i in range(processors)]
        self.picam.resolution = (width,heigth)
        self.picam.framerate = 90
        rospy.sleep(1)
        startTime = rospy.get_rostime()
        self.picam.capture_sequence(proc.streams(),'yuv',use_video_port=True)
        gpio.digitalWrite(self.led,False)
        deltaTime = rospy.get_rostime() - startTime
        fps = depth/deltaTime.to_sec()
        rospy.loginfo("Capture : " + str(fps) + " fps.")
        return fps
   
    def _save_video(self,filename='test.avi',fps=20):
        rospy.loginfo("Saving Video...")
        filename = '/home/CameraNetwork/July/' + filename
        video =cv2.VideoWriter(filename,cv2.cv.CV_FOURCC('M','J','P','G'),fps,
                (sg._WIDTH,sg._HEIGTH),isColor = False)
        for i in sg.VIDEO_MATRIX:
            video.write(i)
        video.release()

    def _empty_pool(self):
        rospy.loginfo("Terminating Threads...")
        while sg.POOL:
            processor = sg.POOL.pop()
            processor.terminated = True
            processor.join()

    def _get_chunk_time(self):
        totalTime = 0
        for i in sg.TIME_LIST:
            totalTime += i.to_sec()
        rospy.loginfo("the chunk takes " + str(totalTime/len(sg.TIME_LIST)) + " sec")
            
    def _reset_globals(self):
        sg.POOL = []
        sg.FRAME_COUNT = 0
        sg.DONE = False
        sg.TIME_LIST = []
        #proc.VIDEO_MATRIX = np.zeros([_DEPTH + 1,_HEIGTH,_WIDTH],np.uint8)

    def _init_picamera(self):
        self.picam.exposure_mode = 'fixedfps'
        self.picam.awb_mode = 'off'
        self.picam.awb_gains = 1.4
        #self.picam.resolution = (1296,972)
        #self.picam.framerate = 40

    def _init_led(self):
        self.led = 5
        os.system("gpio export " + str(self.led) + " out")
        if gpio.wiringPiSetupSys() != 0:
            rospy.logfatal("Unable to setup gpio")
        gpio.digitalWrite(self.led,False)

    def _flash_led(self, nflash=1, delay=0.1):
        for n in range(nflash):
            gpio.digitalWrite(self.led,True)
            rospy.sleep(delay)
            gpio.digitalWrite(self.led,False)
            rospy.sleep(delay)

if __name__ == "__main__":
    rospy.init_node('picam_tester')
    server = picam_tester();
