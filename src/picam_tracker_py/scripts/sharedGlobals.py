import numpy as np
import threading

#const
_WIDTH = 1296
_HEIGTH = 730
_DEPTH = 30


#algo datas:
MU = []
SIG = []
CORR_DATA = [] #rectangleBuffers(10,1) #default

VAR_LOCK = threading.Lock()
POOL = []
DONE = False
FRAME_COUNT = 0
TIME_LIST = []

VIDEO_MATRIX = np.zeros([_DEPTH + 1,_HEIGTH,_WIDTH],np.uint8)
PLOT = []
PLOT2 = []
PICTURE = []
PIXEL = [1,1]

