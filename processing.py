import datetime
import time
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
from constants import INTMAX_16_BIT_SIGNED, RECORDING_DIR

def read_audio_file(filepath):
    fs, audio = wav.read(filepath)
    return fs, audio


def save_signal_to_file(signal, fs, filepath):
    # Normalize the signal to the range of int16
    # this solves the problem of having a really loud volume
    signal = np.int16(signal / np.max(np.abs(signal)) * INTMAX_16_BIT_SIGNED)
    wav.write(filepath, fs, signal)
    print("Signal saved to", filepath)


def record_audio_to_file(duration, fs):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    filepath = f"{RECORDING_DIR}/input_{timestamp}.wav"
    print("Recording Now...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    
    # to show the remaining seconds while recording
    for remaining in range(duration, 0, -1):
        print(f"Remaining seconds: {remaining} ", end="\r", flush=True)
        time.sleep(1)
    
    sd.wait()
    print("\nRecording finished.")
    wav.write(filepath, fs, audio)
    print("Audio saved to", filepath)
    return audio


def modulate(message_signal, carrier_freq, fs):

    # Time vector based on sampling frequency
    t = np.arange(len(message_signal)) / fs
    
    # Carrier signal with frequency w_c
    carrier = np.cos(2 * np.pi * carrier_freq * t)
    
    # Modulated signal = m(t) * cos(w_c * t)
    modulated_signal = message_signal * carrier
    
    return modulated_signal


def demodulate(modulated_signal, carrier_freq, fs):
    # Demodulation is done by multiplying the modulated signal by the carrier signal
    # and then applying a low-pass filter to remove the high-frequency components
    # but in this case, we will just multiply by the carrier signal
    # and leave the low-pass filter out of this function to be more flexible
    return modulate(modulated_signal, carrier_freq, fs)
