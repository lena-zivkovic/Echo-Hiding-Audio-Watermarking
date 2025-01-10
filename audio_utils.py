import numpy as np
from scipy.io.wavfile import read as wav_read, write as wav_write
from pydub import AudioSegment

def load_audio(filepath):
    if filepath.endswith('.wav'):
        samplerate, data = wav_read(filepath)
        
        if data.dtype != np.float32:
            data = data.astype(np.float32) / np.iinfo(data.dtype).max
        return data, samplerate
    elif filepath.endswith('.mp3'):
        audio = AudioSegment.from_file(filepath)
        data = np.array(audio.get_array_of_samples(), dtype=np.float32)
        samplerate = audio.frame_rate
        
        if audio.sample_width == 2:  # 16-bit audio
            data /= 2**15
        elif audio.sample_width == 4:  # 32-bit audio
            data /= 2**31
        return data, samplerate
    else:
        raise ValueError("Unsupported audio format. Only WAV and MP3 are supported.")

def save_audio(filepath, data, samplerate):
    if filepath.endswith('.wav'):
        # Ensure data is int16 for WAV compatibility
        if data.dtype != np.int16:
            data = (data * np.iinfo(np.int16).max).astype(np.int16)
        wav_write(filepath, samplerate, data)
    else:
        raise ValueError("Unsupported audio format. Only WAV format is supported.")


