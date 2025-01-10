from scipy.fftpack import fft, ifft
from binary_utils import bits_to_text
import numpy as np


def delayed_version_of(x, delay):
    out = np.zeros_like(x)
    if delay < len(x):
        out[delay:] = x[:-delay]
    return out


def detect_echo(signal, frame_size, d0, d1):
    num_frames = len(signal) // frame_size
    bits = ''
    
    for i in range(num_frames):
        frame = signal[i*frame_size:(i+1)*frame_size]
        
        corr0 = np.sum(frame * delayed_version_of(frame, d0))
        corr1 = np.sum(frame * delayed_version_of(frame, d1))

        if corr0 > corr1:
            bits += '0'
        else:
            bits += '1'

    return bits

def extract_message(signal, frame_size=8192, d0=150, d1=200):
    bits = detect_echo(signal, frame_size, d0, d1)
    return bits_to_text(bits)

