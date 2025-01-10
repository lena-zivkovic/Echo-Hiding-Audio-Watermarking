import numpy as np
from scipy.signal import lfilter
from binary_utils import text_to_bits

def add_echo(signal, delay, alpha):
    if len(signal) == 0:
        raise ValueError("Signal is empty. Check frame processing in `embed_message`.")
    kernel = np.zeros(delay + 1)
    kernel[0] = 1.0
    kernel[-1] = alpha
    return lfilter(kernel, [1.0], signal)


def embed_message(signal, message, d0=150, d1=200, alpha=0.5, frame_size=8192):
    bits = text_to_bits(message)
    num_bits = len(bits)
    # num_frames = len(signal) // frame_size

    hop_size = frame_size // 2

    stego_len = (num_bits - 1) * hop_size + frame_size

    if stego_len > len(signal):
        raise ValueError("Message too long for given audio signal")


    stego_signal = np.zeros(len(signal) , dtype=signal.dtype)

    for i, bit in enumerate(bits):
        #if i >= num_frames:
        #    break
        
        start_ola = i * hop_size
        end_ola = start_ola + frame_size

        #start = i * frame_size
        #end = min((i + 1) * frame_size, len(signal))
        frame = signal[start_ola:end_ola].copy()

        if len(frame) < frame_size:
            pad_len = frame_size - len(frame)
            frame = np.concatenate([frame, np.zeros(pad_len, dtype=frame.dtype)])

        window = np.hanning(frame_size)
        frame_win = frame * window

        if bit == '0':
            echoed_frame_win = add_echo(frame_win, d0, alpha)
        elif bit == '1':
            echoed_frame_win = add_echo(frame_win, d1, alpha)
        else:
            raise ValueError(f"Unexpected bit value: {bit}")

        actual_end = min(end_ola, len(stego_signal))
        stego_signal[start_ola:actual_end] += echoed_frame_win[:(actual_end - start_ola)]

        if stego_len < len(signal):
            stego_signal[stego_len:] = signal[stego_len:]

    return stego_signal

