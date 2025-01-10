import numpy as np
from scipy.signal import lfilter
from binary_utils import text_to_bits

def add_echo(signal, delay, alpha):
    if len(signal) == 0:
        raise ValueError("Signal is empty. Check frame processing in `embed_message`.")
    kernel = np.zeros(delay)
    kernel = np.append(kernel, [1]) * alpha
    return lfilter(kernel, [1.0], signal)


def embed_message(signal, message, d0=150, d1=200, alpha=0.5, frame_size=8192):
    bits = text_to_bits(message)
    num_frames = len(signal) // frame_size

    if len(bits) > num_frames:
        raise ValueError("Message too long for given audio signal")

    stego_signal = signal.copy()

    for i, bit in enumerate(bits):
        if i >= num_frames:
            break
        
        start = i * frame_size
        end = min((i + 1) * frame_size, len(signal))
        frame = signal[start:end]

        if len(frame) == 0:
            continue

        if bit == '0':
            frame = add_echo(frame, d0, alpha)
        elif bit == '1':
            frame = add_echo(frame, d1, alpha)
        else:
            raise ValueError(f"Unexpected bit value: {bit}")

        stego_signal[start:end] = frame

    return stego_signal

