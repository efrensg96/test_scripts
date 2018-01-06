import serial
import time
import numpy as np
import matplotlib.pyplot as plt

arduinoPort = serial.Serial('/dev/ttyUSB0', 500000) # to read
dataSerial01 = []
flag = False
time.sleep(3)
print "start time"
t0 = time.time()
while not flag:
    flag = True
    dataSerial01.append(arduinoPort.readline().strip())
print "time per loop", np.float(time.time() - t0)
print "dataSerial01: ", dataSerial01
