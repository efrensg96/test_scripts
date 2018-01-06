import serial
import time
import numpy as np
import matplotlib.pyplot as plt

arduinoPort = serial.Serial('/dev/ttyUSB0', 500000)
dataSerial01 = []
flag = False
time.sleep(3)
counter = 0
print "start time"
t0 = time.time()
while True:
    if counter >= 8000:
        break
    dataSerial01.append(arduinoPort.readline().strip())
    counter += 1
print "time per loop", np.float(time.time() - t0)
print "counter: ", counter
print "dataSerial01 lenght: ", len(dataSerial01)
