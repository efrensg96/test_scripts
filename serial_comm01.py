import serial
import time
import numpy as np
import matplotlib.pyplot as plt

# arduinoPort = serial.Serial('COM1', 230400)
arduinoPort = serial.Serial('/dev/ttyS0', 500000) # to read
# arduinoPort = serial.Serial('/dev/ttyAMA0', 230400) # to write
counter = 0
t0 = time.time()
dataSerial01 = []
flag = True

time.sleep(3)
t1 = time.time()
print "Start time: ", t1 - t0
while True:
    t1 = time.time()
    if (t1 - t0) >= 4.0:
        break
    dataSerial01.append(arduinoPort.readline().strip())

print "Stop time: ", t1 - t0
# data = b''.join(data)
# data = map(np.int16, data[1])
print "dataSerial01 size: ", len(dataSerial01)

# dataSerial01[0] = dataSerial01[1]
# print "dataSerial01: ", dataSerial01

data01 = map(np.int16, dataSerial01[2::])

# print "data01: ", data01

print "data01 lenght: ", len(data01)

plt.figure()
plt.plot(data01)
plt.show()




