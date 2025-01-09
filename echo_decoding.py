from scipy.fftpack import fft, ifft

def detect_echo(signal, frame_size, d0, d1):
    num_frames = len(signal) // frame_size
    bits = ''
    
    for i in range(num_frames):
        frame = signal[i*frame_size:(i+1)*frame_size]
        rceps = np.abs(ifft(np.log(np.abs(fft(frame)))))
        if rceps[d0] > rceps[d1]:
            bits += '0'
        else:
            bits += '1'

    return bits

def extract_message(signal, frame_size=8192, d0=150, d1=200):
    bits = detect_echo(signal, frame_size, d0, d1)
    return bits_to_text(bits)

