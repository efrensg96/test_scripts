import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading
import multiprocessing
import Queue
import struct
import madmom as mm
import pyaudio
import vamp
import wave
import pdb


def audio_stream_process(time_limit, audio_queue):

    microphonePort = serial.Serial('COM10', 1000000, timeout=3)
    dataSerial_audio = []
    init_time_process_audio = time.time()

    while True:

        if (time.time() - init_time_process_audio) >= time_limit:
            audio_queue.put(dataSerial_audio)
            print "* stop audio serial port at:", time.time() - init_time_process_audio
            dataSerial_audio = []
            microphonePort.close()
            break

        dataSerial_audio.append(struct.unpack("i", microphonePort.read(4)))


def vibration_stream_process(time_limit, vib_queue):

    arduinoPort = serial.Serial('COM1', 1000000, timeout=3)
    dataSerial_vibration = []
    init_time_process_vibration = time.time()

    while True:

        if (time.time() - init_time_process_vibration) >= time_limit:
            vib_queue.put(dataSerial_vibration)
            print "* stop vibration serial port at:", time.time() - init_time_process_vibration
            dataSerial_vibration = []
            arduinoPort.close()
            break

        dataSerial_vibration.append(arduinoPort.readline().strip())


if __name__ == '__main__':

    # style.use('fivethirtyeight')

    dataChunk = []
    medlodyChunk = []
    CHUNK = 16000 #2 channels, 16khz of fs, time to be recorded (2*16000*time) = chunk size
    RATE = 16000

    RECORDING_TIME = 5.0 #in seconds
    N16 = 2 ** 16
    N10 = 2 ** 10
    N8 = 2 ** 8

    # pdb.set_trace()

    t0 = time.time()

    stream_queue = multiprocessing.Queue()
    audio_stream = multiprocessing.Process(target=audio_stream_process, args=(RECORDING_TIME, stream_queue))

    vibration_queue = multiprocessing.Queue()
    vibration_stream = multiprocessing.Process(target=vibration_stream_process, args=(RECORDING_TIME, vibration_queue))

    audio_stream.start()
    vibration_stream.start()

    print "* recording at: ", time.time() - t0

    while True:
        if (stream_queue.empty() is False) and (vibration_queue.empty() is False):
            print "* Total running time: ", time.time() - t0
            time.sleep(.5)
            print "* STOP recording"
            break

    vibration_data_8bits = vibration_queue.get()
    # print "vibration_data_8bits: ", vibration_data_8bits[0:20]
    vibration_data_16bits = np.int16(vibration_data_8bits[2::])
    # vibration_data_16bits = np.round((vibration_data_16bits * N16) / N8)
    vibration_spectrogram = mm.audio.spectrogram.Spectrogram(vibration_data_16bits)

    print "* Vibration_data_16bits lenght: ", len(vibration_data_16bits)

    audio_data = stream_queue.get()
    audio_data_32bits = np.int32(audio_data)

    if (len(audio_data_32bits) % 2) != 0:
        audio_data_32bits = audio_data_32bits[:-1]

    audio_data_32bits = np.reshape(audio_data_32bits, (-1, 2))
    audio_remix_samples = mm.audio.signal.remix(audio_data_32bits, 1)
    audio_spectrogram = mm.audio.spectrogram.Spectrogram(audio_remix_samples)

    print "* Audio_remix_samples shape: ", audio_data_32bits.shape

    plt.figure()
    plt.plot(vibration_data_16bits)
    plt.title("Vibration Raw Data")

    plt.figure()
    plt.imshow(vibration_spectrogram[:, :200].T, origin='lower', aspect='auto')
    plt.title("Vibration Spectrogram")

    plt.figure()
    plt.plot(audio_remix_samples)
    plt.title("Audio Raw Data")

    plt.figure()
    plt.imshow(audio_spectrogram[:, :200].T, origin='lower', aspect='auto')
    plt.title("Audio Spectrogram")

    plt.show()

    WAVE_OUTPUT_FILENAME = "audio_vibration_serial.wav"
    CHANNELS = 1
    RATE = 16000
    FORMAT = pyaudio.paInt32

    p = pyaudio.PyAudio()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(audio_data_32bits.tostring()))
    wf.close()

    print "* done"






