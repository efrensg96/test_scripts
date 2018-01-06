import serial
import time
import numpy as np
import matplotlib.pyplot as plt

arduinoPort = serial.Serial('COM1', 500000)
dataSerial01 = []
flag = False
time.sleep(3)
print "start time"
t0 = time.time()
while not flag:
    flag = True
    dataSerial01.append(arduinoPort.readline().strip())
    t1 = time.time()
print "time per loop", np.float(t1 - t0)
print "dataSerial01: ", dataSerial01
