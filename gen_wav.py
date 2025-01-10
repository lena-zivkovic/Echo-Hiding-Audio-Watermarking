import numpy as np
from scipy.io.wavfile import read, write


def gen_sine_wave(fname, dur, freq, samplerate=44100):
    t = np.linspace(0, dur, int(samplerate*dur), endpoint=False)
    wave = (np.sin(2*np.pi*freq*t)*32767).astype(np.int16)
    write(fname, samplerate, wave)


gen_sine_wave("test.wav", dur=20, freq=440)

