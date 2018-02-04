import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import struct
import madmom as mm
import pyaudio
import wave


def main():

    arduinoPort = serial.Serial('/dev/ttyACM0', 1000000, timeout=3)
    dataSerial_01 = []    
    CHUNK = 96000 #2 channels, 16khz of fs, time to be recorded (2*16000*time) = chunk size
    N = 2**16

    t0 = time.time()
#     time.sleep(3)    
    t1 = time.time()
    print "Start time: ", t1 - t0  

    while True:
        t1 = time.time()
        if (t1 - t0) >= 4.0:
            break
        dataSerial_01.append(struct.unpack("i", arduinoPort.read(4)))

    print "time per loop", np.float(time.time() - t0)
    print "dataSerial_01 lenght: ", len(dataSerial_01)
    print "dataSerial_01: ", dataSerial_01[0:20]

    data01 = np.int32(dataSerial_01)
    data01 = np.int16(np.round(data01/N))

    print "data01 shape: ", data01.shape

    remixSamples = mm.audio.signal.remix(data01, 1)
    spec = mm.audio.spectrogram.Spectrogram(remixSamples)

    plt.figure()
    plt.plot(data01)
    plt.title("Raw Data")

    plt.figure()
    plt.imshow(spec[:, :200].T, origin='lower', aspect='auto')
    plt.title("Spectogram")

    plt.show()

    WAVE_OUTPUT_FILENAME = "I2S_example_01.wav"
    CHANNELS = 2
    RATE = 16000
    FORMAT = pyaudio.paInt16

    p = pyaudio.PyAudio()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(data01.tostring()))
    wf.close()

    arduinoPort.close()


if __name__ == '__main__':
    main()




