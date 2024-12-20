import datetime
import time
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import soundfile as sf
from constants import INTMAX_16_BIT_SIGNED, RECORDING_DIR, \
    INPUT_RECORDING_DIR, OUTPUT_RECORDING_DIR
from filtering import custom_hilbert

def read_audio_file(filename):
    filepath = f"{INPUT_RECORDING_DIR}/{filename}"
    audio, fs = sf.read(filepath)
    return audio, fs


def save_signal_to_file(signal, fs, filename):
    filepath = f"{OUTPUT_RECORDING_DIR}/{filename}"
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



def ssb_modulate(signal, carrier_freq, sample_rate):

    t = np.arange(len(signal)) / sample_rate
    carrier = np.cos(2 * np.pi * carrier_freq * t)
    
    # Compute the analytic signal
    analytic_signal = custom_hilbert(signal)
    
    # SSB modulation (upper sideband)
    ssb_signal = np.real(analytic_signal * np.exp(1j * 2 * np.pi * carrier_freq * t))
    
    return ssb_signal

def combine_signals(signals):
    return np.sum(signals, axis=0)

def ssb_demodulate(ssb_signal, carrier_freq, sample_rate):
    t = np.arange(len(ssb_signal)) / sample_rate
    carrier = np.cos(2 * np.pi * carrier_freq * t)
    
    # Multiply by the carrier signal to shift the spectrum back to baseband
    demodulated = ssb_signal * carrier
    
    return demodulated
