import serial
import time
import numpy as np
import matplotlib.pyplot as plt

arduinoPort = serial.Serial('COM1', 1000000)
counter = 0
t0 = time.time()
dataSerial01 = []
dataSerial02 = []
flag = True
while True:
    t1 = time.time()
    if (t1 - t0) >= 4:
        break
    elif (t1 - t0) >= 3:
        if flag:
            print "Start time: ", t1 - t0
            flag = False
        dataSerial01.append(arduinoPort.readline().strip())
        dataSerial02.append(arduinoPort.readline().strip())
print "Stop time: ", t1 - t0
# data = b''.join(data)
# data = map(np.int16, data[1])
print "dataSerial01 size: ", len(dataSerial01)
print "dataSerial02 size: ", len(dataSerial02)
# dataSerial01[0] = dataSerial01[1]
print "dataSerial01: ", dataSerial01
print "dataSerial02: ", dataSerial02
data01 = map(np.int16, dataSerial01[2::])
data02 = map(np.int16, dataSerial02[2::])
print "data01: ", data01
print "data02: ", data02
print "data01 lenght: ", len(data01)
print "data02 lenght: ", len(data02)
plt.figure()
plt.plot(data01)
plt.figure()
plt.plot(data02)
plt.show()




