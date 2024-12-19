import datetime
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import scipy.signal as signal
import scipy.fftpack as fftpack
import scipy.io.wavfile as wav


RECORDING_DIR = "./recordings"
IMAGES_DIR = "./images"

def record_audio_to_file(duration, fs):
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    filepath = f"{RECORDING_DIR}/input_{timestamp}.wav"
    
    print("Recording Now...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    print("Done recording.")
    wav.write(filepath, fs, audio)
    print("Audio saved to", filepath)
    return audio


def plot_audio(audio, fs):
    time = np.arange(0, len(audio)/fs, 1/fs)
    plt.plot(time, audio)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Audio")
    plt.show()

def plot_audio_spectrum(audio, fs, show_negative=True):
    # Flatten the audio if it's 2D
    if audio.ndim > 1:
        audio = audio.flatten()
    
    N = len(audio)
    if show_negative:
        freq = np.fft.fftfreq(N, 1/fs)  # Both positive and negative frequencies
        audio_fft = np.fft.fft(audio)
    else:
        freq = np.fft.rfftfreq(N, 1/fs)  # Only positive frequencies
        audio_fft = np.fft.rfft(audio)  # real signals
    
    # Normalize magnitude 
    # regardless of the magnitude of the signal
    magnitude = np.abs(audio_fft) / N  

    plt.plot(freq, magnitude)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.title("Audio Spectrum")
    plt.grid()
    plt.show()
    
    # save the plot
    plt.savefig(f"{IMAGES_DIR}/audio_spectrum.png")


if __name__ == "__main__":
    duration = 5
    fs = 44100

    audio = record_audio_to_file(duration, fs)
    plot_audio(audio, fs)
    plot_audio_spectrum(audio, fs)
    
    # get audio spectrum
    # FFT: Converts the audio signal from the time domain to the frequency domain.
    audio_spectrum = np.fft.fft(audio)
    
    # FFT Shift: Centers the zero-frequency component for better visualization and analysis.
    audio_spectrum = np.fft.fftshift(audio_spectrum)
    
    # Magnitude: Extracts the amplitude of the frequency components, discarding phase information.
    audio_spectrum = np.abs(audio_spectrum)
    
    
    
    print("Done.")
