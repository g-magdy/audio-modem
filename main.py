from plotting import plot_time_domain, plot_magnitude_spectrum
from filtering import low_pass_filter, band_pass_filter
from processing import read_audio_file, modulate, demodulate, save_signal_to_file
from constants import F_INPUT_MAX, CARRIER_FREQ_1

def main():
    fs, audio = read_audio_file("./recordings/input/input1.wav")
    
    plot_time_domain(audio, fs, chart_title="Initial Input Audio Signal in Time Domain", save=True)
    plot_magnitude_spectrum(audio, fs, chart_title="Initial Input Audio Spectrum", save=True)
    
    # to limit the max frequency of the audio signal
    # human voice is usually below 4kHz
    filtered_audio = low_pass_filter(audio, F_INPUT_MAX, fs)
    
    plot_magnitude_spectrum(filtered_audio, fs, chart_title=f"Magnitude Spectrum with max f = {F_INPUT_MAX} Hz", save=True)
    
    modulated_signal = modulate(filtered_audio, CARRIER_FREQ_1, fs)
    
    plot_magnitude_spectrum(modulated_signal, fs, chart_title="Modulated Signal Magnitude Spectrum", save=True)
    
    # now let's get one sideband of the modulated signal
    # this is a crucial step in demodulation to achieve a single sidedband signal
    # make it closer to ideal filter
    filtered_modulated_signal = band_pass_filter(modulated_signal,CARRIER_FREQ_1,CARRIER_FREQ_1 + F_INPUT_MAX, fs, order=25)
    
    plot_magnitude_spectrum(filtered_modulated_signal, fs, chart_title="USB of Modulated Signal Spectrum", save=True)
    
    # Now the signal is ready to be sent to the channel
    # taking only BW = F_INPUT_MAX
    
    # now demodulate the signal
    demodulated_signal = demodulate(filtered_modulated_signal, CARRIER_FREQ_1, fs)
    
    plot_magnitude_spectrum(demodulated_signal, fs, chart_title="Demodulated Signal Spectrum before LPF", save=True)
    
    low_pass_filtered_signal = low_pass_filter(demodulated_signal, F_INPUT_MAX, fs)
    
    # save the demodulated signal
    save_signal_to_file(low_pass_filtered_signal, fs, "./recordings/output/output1.wav")
    
    plot_magnitude_spectrum(low_pass_filtered_signal, fs, chart_title="Demodulated Signal Spectrum after LPF", save=True)
    plot_time_domain(low_pass_filtered_signal, fs, chart_title="Reconstucted Signal in Time Domain", save=True)
    
    
    print("Done.")


if __name__ == "__main__":
    main()