from plotting import plot_time_domain, plot_magnitude_spectrum
from filtering import apply_lpf, apply_bandpass
from processing import read_audio_file, ssb_modulate, combine_signals, ssb_demodulate, save_signal_to_file
from constants import SAMPLE_RATE, F_INPUT_MAX, \
    CARRIER_FREQ_1,CARRIER_FREQ_2, CARRIER_FREQ_3

def process_audio(filename, carrier_freq, show_plots=False, save_plots=False):
    audio, fs = read_audio_file(filename)
    filtered = apply_lpf(audio, SAMPLE_RATE, F_INPUT_MAX)
    modulated = ssb_modulate(filtered, carrier_freq, SAMPLE_RATE)
    
    if show_plots:
        filename = filename.split('.')[0]
        plot_time_domain(audio, fs, chart_title=f"{filename} in Time Domain", save=save_plots)
        plot_magnitude_spectrum(audio, fs, chart_title=f"{filename} Magnitude Spectrum", save=save_plots)
        plot_magnitude_spectrum(filtered, fs, f'Filtered {filename} Magnitude Spectrum', save=save_plots)
        plot_magnitude_spectrum(modulated, fs, f'Modulated {filename} Magnitude Spectrum', save=save_plots)
        
    return modulated

def reconstruct_signal(modulated_signal, carrier_freq, fs, signal_name="",show_plots=False, save_plots=False):
    # Apply bandpass filter to isolate the desired signal
    lowcut = carrier_freq - F_INPUT_MAX / 2
    highcut = carrier_freq + F_INPUT_MAX / 2
    bandpassed_signal = apply_bandpass(modulated_signal, fs, lowcut, highcut)
    demodulated = ssb_demodulate(bandpassed_signal, carrier_freq, fs)
    # Apply low-pass filter after demodulation
    recovered_signal = apply_lpf(demodulated, fs, F_INPUT_MAX)
    
    if show_plots:
        signal_name = signal_name.split('.')[0]
        plot_magnitude_spectrum(bandpassed_signal, fs, f'{signal_name.split('.')[0]} Bandpassed Signal at {carrier_freq} Hz', save=save_plots)
        plot_magnitude_spectrum(demodulated, fs, f'{signal_name} Demodulated Signal from {carrier_freq} Hz', save=save_plots)
        plot_magnitude_spectrum(recovered_signal, fs, f' {signal_name} Recovered Signal from {carrier_freq} Hz', save=save_plots)
    
    return recovered_signal

def  main():
    # Load the recorded audio signals
    input_files = ['input1.wav', 'input2.wav', 'input3.wav']
    carrier_frequencies = [CARRIER_FREQ_1, CARRIER_FREQ_2, CARRIER_FREQ_3] 
    modulated_signals = []
    
    for i, (file, carrier) in enumerate(zip(input_files, carrier_frequencies)):
        modulated_signals.append(process_audio(file, carrier, show_plots=True, save_plots=(i==0)))
        # i will only save the first plot (i==0)
    
    # Combine modulated signals for FDM
    fdm_signal = combine_signals(modulated_signals)
    plot_magnitude_spectrum(fdm_signal, SAMPLE_RATE, 'FDM Signal', save=True)

    # Perform SSB Demodulation
    output_files = ['output1.wav', 'output2.wav', 'output3.wav']
    demodulated_signals = []
    
    for i, (file, carrier) in enumerate(zip(output_files, carrier_frequencies)):
        demodulated_signals.append(reconstruct_signal(fdm_signal, carrier, SAMPLE_RATE, input_files[i], show_plots=True, save_plots=(i==0)))
        # i will only save the first plot (i==0)
        save_signal_to_file(demodulated_signals[i], SAMPLE_RATE, file)

if __name__ == "__main__":
    main()