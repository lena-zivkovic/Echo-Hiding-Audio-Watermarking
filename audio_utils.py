import soundfile as sf
from pydub import AudioSegment

def load_audio(filepath):
    if filepath.endswith('.wav') or filepath.endswith('.flac'):
        data, samplerate = sf.read(filepath)
        return data, samplerate
    elif filepath.endswith('.mp3'):
        audio = AudioSegment.from_file(filepath)
        data = np.array(audio.get_array_of_samples())
        samplerate = audio.frame_rate
        return data, samplerate
    else:
        raise ValueError("Unsupported audio format.")

def save_audio(filepath, data, samplerate):
    sf.write(filepath, data, samplerate)
