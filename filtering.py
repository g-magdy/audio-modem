import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, firwin, lfilter


# newer functions for filtering

def apply_lpf(signal, sample_rate, cutoff):
    nyquist = sample_rate / 2
    b, a = butter(4, cutoff / nyquist, btype='low')
    filtered_signal = filtfilt(b, a, signal)
    return filtered_signal


def apply_bandpass(signal, sample_rate, lowcut, highcut):
    nyquist = sample_rate / 2
    b, a = butter(4, [lowcut / nyquist, highcut / nyquist], btype='band')
    bandpassed_signal = filtfilt(b, a, signal)
    return bandpassed_signal


def custom_hilbert(signal):

    N = len(signal)
    signal_fft = np.fft.fft(signal)
    
    # Create a frequency mask
    h = np.zeros(N)
    if N % 2 == 0:
        h[0] = 1
        h[1:N//2] = 2
        h[N//2] = 1
    else:
        h[0] = 1
        h[1:(N+1)//2] = 2
    
    analytic_signal = np.fft.ifft(signal_fft * h)
    return analytic_signal

