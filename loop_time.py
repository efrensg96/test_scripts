import serial
import time
import numpy as np
import matplotlib.pyplot as plt

t0 = time.time()
flag = False
while not flag:
    flag = True
    t1 = time.time()
print "time per loop", np.float(t0 - t1)
