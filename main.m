function main()
    
    % this will be three audios, but let's just test with only one for now

    sampling_freq = 44100;
    duration = 10;


    audio_signal = recordAudio("input1.wav", duration, sampling_freq);
    
    computeFFT(audio_signal, sampling_freq, 'Original Signal Spectrum');

    % next steps are roughly
    % get fourier transform of each speech signal
    % low pass filter
    % modulate
    % demodulte
end

function audio_signal = recordAudio(filename, seconds, sampling_freq)
    % this records audio for the given seconds and sampling frequency
    % then saves the recording at the given file path
    recorder = audiorecorder(sampling_freq, 16, 1);
    fprintf('Recording voice signal (%d seconds)...\n', seconds);
    recordblocking(recorder, seconds);
    audio_signal = getaudiodata(recorder);
    audiowrite(filename, audio_signal, sampling_freq);
    fprintf("Recording was saved at %s\n", filename)
end

function computeFFT(signal, sampling_freq, title_text)
    % fft is short for fast fourier transform
    N = length(signal);
    fft_signal = fft(signal);
    mag_spectrum = abs(fft_signal(1:N/2)); % Positive frequencies
    f = (0:N/2-1)*(sampling_freq/N);
    
    % now display our 
    figure;
    plot(f, mag_spectrum);
    title(title_text);
    xlabel('Frequency (Hz)');
    ylabel('Magnitude');
    grid on;
end