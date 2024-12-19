import numpy as np
import matplotlib.pyplot as plt
from constants import IMAGES_DIR

def plot_time_domain(audio, fs, chart_title="Audio Signal in Time Domain", save=False):
    time = np.arange(0, len(audio)/fs, 1/fs)
    plt.figure(figsize=(12, 6), dpi=100)
    plt.plot(time, audio)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title(chart_title)
    if save:
        plt.savefig(f"{IMAGES_DIR}/{chart_title}.png", dpi=100)
    plt.show()
    

def plot_magnitude_spectrum(audio, fs, show_negative=True, chart_title="Audio Spectrum in Frequency Domain", save=False):
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

    plt.figure(figsize=(12, 6), dpi=100)
    plt.plot(freq, magnitude)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.title(chart_title)
    plt.grid()
    if save:
        plt.savefig(f"{IMAGES_DIR}/{chart_title}.png", dpi=100)
    plt.show()
    
