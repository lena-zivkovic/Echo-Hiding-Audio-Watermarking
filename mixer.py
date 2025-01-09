from scipy.signal.windows import hann

def create_mixer_signal(binary_sequence, frame_size, smoothing_window_size):
    repeated = np.repeat(list(map(int, binary_sequence)), frame_size)
    hann_window = hann(smoothing_window_size)
    smoothed_signal = np.convolve(repeated, hann_window, mode='same')
    return smoothed_signal / max(abs(smoothed_signal))

