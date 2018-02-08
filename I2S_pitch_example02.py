import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import threading
import Queue
import struct
import madmom as mm
import pyaudio
import vamp
import wave

def audio_stream_thread():

    dataSerial_01 = []
    arduinoPort = serial.Serial('COM4', 1000000, timeout=3)

    t0 = time.time()
    while True:

        if len(dataSerial_01) >= CHUNK:
            stream_queue.put(dataSerial_01)
            dataChunk.append(dataSerial_01)
            dataSerial_01 = []
            # print "running time: ", time.time() - t0

            if stop_flag:
                arduinoPort.close()
                print("* stop recording")
                break

        dataSerial_01.append(struct.unpack("i", arduinoPort.read(4)))

def animate(i):

    #Reading from audio input stream into data with block length "CHUNK":
    global completeMelody, xAxis

    data = stream_queue.get()
    data01 = np.reshape(np.int32(data), (-1, 2))
    remixSamples = mm.audio.signal.remix(data01, 1)
    dataF0 = vamp.collect(remixSamples, RATE, "mtg-melodia:melodia")
    hop, melody = dataF0['vector']
    melody_pos = melody[:]
    melody_pos[melody <= 0] = None

    # print "melody_pos: ", len(melody_pos)

    medlodyChunk.append(melody_pos)

    completeMelody = np.concatenate(medlodyChunk)

    if len(completeMelody) >= 1218:
        completeMelody = completeMelody[-1218:]

    # print "completeMelody: ", len(completeMelody)

    ax1.clear()
    line, = ax1.plot(completeMelody)
    plt.ylim((100, 1600))
    plt.xlim((0, xAxis))
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    if xAxis <= 1200:
        xAxis += 200
    # xAxis += 200

    line.set_ydata(completeMelody)
    return line,


if __name__ == '__main__':

    # style.use('fivethirtyeight')

    dataChunk = []
    medlodyChunk = []
    CHUNK = 16000 #2 channels, 16khz of fs, time to be recorded (2*16000*time) = chunk size
    RATE = 16000

    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    xAxis = 200

    stop_flag = False

    stream_queue = Queue.Queue()
    audio_stream = threading.Thread(target=audio_stream_thread)

    print("* recording")
    audio_stream.start()

    ani = animation.FuncAnimation(fig, animate, interval=510, blit=True)
    plt.show()

    stop_flag = True

    waveData = np.int32(dataChunk)

    if (len(waveData) % 2) != 0:
        data01 = waveData[:-1]

    waveData = np.reshape(waveData, (-1, 2))

    # print "waveData shape: ", waveData.shape

    remixSamplesWav = mm.audio.signal.remix(waveData, 1)
    dataF0Wav = vamp.collect(remixSamplesWav, RATE, "mtg-melodia:melodia")
    hop, melodyWav = dataF0Wav['vector']
    timestamps = 8 * 128 / 44100.0 + np.arange(len(melodyWav)) * (128 / 44100.0)
    # # A clearer option is to get rid of the negative values before plotting
    melody_pos_wav = melodyWav[:]
    melody_pos_wav[melodyWav <= 0] = None
    plt.figure(figsize=(18, 6))
    plt.plot(timestamps, melody_pos_wav)
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.show()

    WAVE_OUTPUT_FILENAME = "I2S_pitch_example02.wav"
    CHANNELS = 1
    RATE = 32000
    FORMAT = pyaudio.paInt32

    p = pyaudio.PyAudio()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(waveData.tostring()))

    wf.close()


    print("* done")






