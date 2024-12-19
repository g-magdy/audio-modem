import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, firwin, lfilter

def low_pass_filter_2(audio, cutoff, fs, filter_order=50):
    lpf = firwin(filter_order, cutoff, fs=fs)
    filtered_audio = lfilter(lpf, 1.0, audio)
    return filtered_audio


def band_pass_filter_2(audio, low_cutoff, high_cutoff, fs, filter_order=50):
    bpf = firwin(
        filter_order, [low_cutoff, high_cutoff], pass_zero=False, fs=fs)
    return lfilter(bpf, 1.0, audio)



def low_pass_filter(signal, cutoff, fs, order=6):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, signal)


def band_pass_filter(signal ,lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band', analog=False)
    return  filtfilt(b, a, signal)


def band_pass_filter_Custom(signal, lowcut, highcut, fs, filter_length=51):
    # Normalize the cutoff 
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist

    # shift to center
    n = np.arange(filter_length) - (filter_length - 1) / 2
    # generate sinc filter and apply smoothing
    h_low = np.sinc(2 * high * n) * np.hamming(filter_length)
    h_high = np.sinc(2 * low * n) * np.hamming(filter_length)

    # Band-pass kernel = low-pass - high-pass
    h_band = h_high - h_low
    h_band = h_band / np.sum(h_band)  # Normalize filter

    # Apply the filter to the signal
    filtered_signal = np.convolve(signal, h_band, mode='same')

    return filtered_signal


def low_pass_filter_custom(signal, cutoff, fs, filter_length=51):
    # Normalize the cutoff 
    nyquist = 0.5 * fs
    normalized_cutoff = cutoff / nyquist

    # shift to center
    n = np.arange(filter_length) - (filter_length - 1) / 2
    # generate sinc filter
    h = np.sinc(2 * normalized_cutoff * n)

    # reduce ripples by smoothing the edges
    window = np.hamming(filter_length)
    h = h * window

    # Normalize filter 
    h = h / np.sum(h)

    # Apply the filter to the signal using convolution
    filtered_signal = np.convolve(signal, h, mode='same')

    return filtered_signal, h


def ideal_lowpass_filter(signal, cutoff, fs, filter_length=101):
    
    # Frequency Domain: Create an ideal rectangular frequency response
    nyquist = fs / 2
    normalized_cutoff = cutoff / nyquist

    freq_response = np.zeros(filter_length)
    half_length = filter_length // 2

    # Set the rectangular response to 1 below the cutoff frequency
    for i in range(filter_length):
        freq = abs(i - half_length) / half_length  # Normalize frequency [-1, 1]
        if freq <= normalized_cutoff:
            freq_response[i] = 1

    # Convolve the input signal with the normalized impulse response
    filtered_signal = np.convolve(signal, freq_response, mode='same')

    return filtered_signal


def ideal_bandpass_filter(signal, low_cutoff, high_cutoff, fs, filter_length=101):
    
    nyquist = fs / 2
    normalized_low = low_cutoff / nyquist
    normalized_high = high_cutoff / nyquist

    # Create frequency response for a band-pass filter
    freq_response = np.zeros(filter_length)
    half_length = filter_length // 2

    for i in range(filter_length):
        freq = abs(i - half_length) / half_length  # Normalize frequency [-1, 1]
        if normalized_low <= freq <= normalized_high:
            freq_response[i] = 1

    # Inverse FFT to find impulse response
    filtered_signal = np.convolve(signal, freq_response, mode='same')

    return filtered_signal
