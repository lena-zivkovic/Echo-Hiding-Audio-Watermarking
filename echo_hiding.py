import numpy as np
from scipy.signal import lfilter

def add_echo(signal, delay, alpha):
    kernel = np.zeros(delay)
    kernel = np.append(kernel, [1]) * alpha
    return lfilter(kernel, [1.0], signal)

def embed_message(signal, message, d0=150, d1=200, alpha=0.5, frame_size=8192):
    bits = text_to_bits(message)
    num_frames = len(signal) // frame_size
    stego_signal = signal.copy()

    for i, bit in enumerate(bits):
        if i >= num_frames:
            break
        frame = signal[i*frame_size:(i+1)*frame_size]
        if bit == '0':
            frame = add_echo(frame, d0, alpha)
        else:
            frame = add_echo(frame, d1, alpha)
        stego_signal[i*frame_size:(i+1)*frame_size] = frame

    return stego_signal

