function main()
    % Sampling frequency
    fs = 44100;  

    % Filter length for the ideal low-pass filter
    filter_length = 101;  % You can change this value as needed

    % Step 1: Read audio files
    [audio1, ~] = audioread('input1.wav');
    [audio2, ~] = audioread('input2.wav');
    [audio3, ~] = audioread('input3.wav');

    % Plot the spectrum of the original signals
    computeFFT(audio1, fs, ' Signal 1 Spectrum');
    computeFFT(audio2, fs, ' Signal 2 Spectrum');
    computeFFT(audio3, fs, ' Signal 3 Spectrum');

    % Step 2: Apply Low-Pass Filter (LPF)
    cutoff = 4000;  % LPF cutoff frequency
    filtered1 = low_pass_filter(audio1, cutoff, fs,6);
    filtered2 = low_pass_filter(audio2, cutoff, fs,6);
    filtered3 = low_pass_filter(audio3, cutoff, fs,6);

    % Plot the spectrum of the filtered signals
    computeFFT(filtered1, fs, 'Filtered Signal 1 Spectrum');
    computeFFT(filtered1, fs, 'Filtered Signal 2 Spectrum');
    computeFFT(filtered1, fs, 'Filtered Signal 3 Spectrum');

    % Save the filtered audio files
    audiowrite('output1.wav', filtered1, fs);
    audiowrite('output2.wav', filtered2, fs);
    audiowrite('output3.wav', filtered3, fs);
end


% Butterworth Low-Pass Filter
function filtered_signal = low_pass_filter(signal, cutoff, fs, order)
    nyquist = 0.5 * fs;
    normal_cutoff = cutoff / nyquist;
    [b, a] = butter(order, normal_cutoff, 'low');
    filtered_signal = filtfilt(b, a, signal);
end

% Butterworth Band-Pass Filter
function filtered_signal  = band_pass_filter(signal,lowcut, highcut, fs, order)
    nyquist = 0.5 * fs;
    low = lowcut / nyquist;
    high = highcut / nyquist;
    [b, a] = butter(order, [low high], 'bandpass');
    filtered_signal = filtfilt(b, a, signal);
end

% Custom Band-Pass Filter using sinc
function filtered_signal = band_pass_filter_Custom(signal, lowcut, highcut, fs, filter_length)
    nyquist = 0.5 * fs;
    low = lowcut / nyquist;
    high = highcut / nyquist;

    % Generate filter coefficients
    n = (0:filter_length-1) - (filter_length - 1) / 2;
    h_low = sinc(2 * high * n) .* hamming(filter_length)';
    h_high = sinc(2 * low * n) .* hamming(filter_length)';

    % Band-pass kernel = high-pass - low-pass
    h_band = h_high - h_low;
    h_band = h_band / sum(h_band);

    % Convolution
    filtered_signal = conv(signal, h_band, 'same');
end

% Custom Low-Pass Filter using sinc
function filtered_signal = low_pass_filter_custom(signal, cutoff, fs, filter_length)
    nyquist = 0.5 * fs;
    normalized_cutoff = cutoff / nyquist;

    % Generate filter coefficients
    n = (0:filter_length-1) - (filter_length - 1) / 2;
    h = sinc(2 * normalized_cutoff * n);

    % Apply Hamming window
    window = hamming(filter_length)';
    h = h .* window;

    % Normalize filter
    h = h / sum(h);

    % Convolution
    filtered_signal = conv(signal, h, 'same');
end

% Ideal Low-Pass Filter
function filtered_signal = ideal_lowpass_filter(signal, cutoff, fs, filter_length)
    nyquist = fs / 2;
    normalized_cutoff = cutoff / nyquist;

    freq_response = zeros(1, filter_length);
    half_length = floor(filter_length / 2);

    % Frequency response
    for i = 1:filter_length
        freq = abs(i - half_length) / half_length;
        if freq <= normalized_cutoff
            freq_response(i) = 1;
        end
    end

    % Convolution
    filtered_signal = conv(signal, freq_response, 'same');
end

% Ideal Band-Pass Filter
function filtered_signal = ideal_bandpass_filter(signal, low_cutoff, high_cutoff, fs, filter_length)
    nyquist = fs / 2;
    normalized_low = low_cutoff / nyquist;
    normalized_high = high_cutoff / nyquist;

    freq_response = zeros(1, filter_length);
    half_length = floor(filter_length / 2);

    % Frequency response
    for i = 1:filter_length
        freq = abs(i - half_length) / half_length;
        if normalized_low <= freq && freq <= normalized_high
            freq_response(i) = 1;
        end
    end

    % Convolution
    filtered_signal = conv(signal, freq_response, 'same');
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

function [modulated_signal] = custom_modulation(message_signal, carrier_freq, fs)
  

    t = (0:length(message_signal)-1) / fs;  % Time vector based on sampling frequency
    carrier = cos(2 * pi * carrier_freq * t);  % Carrier signal with frequency w_c

    % Modulated signal = m(t) * cos(w_c * t)
    modulated_signal = message_signal .* carrier;

end


function [modulated_signal] = custom_modulation(message_signal, carrier_freq, fs)
    % Check if inputs are valid
    if isempty(message_signal)
        error('Message signal is empty.');
    end
    if carrier_freq <= 0
        error('Carrier frequency must be positive.');
    end
    if fs <= 0
        error('Sampling frequency must be positive.');
    end

    % Initialize modulated signal
    modulated_signal = zeros(size(message_signal));
    
    % Define chunk size
    chunk_size = 1e6;  % Adjust this value based on available memory
    
    % Process signal in chunks
    num_chunks = ceil(length(message_signal) / chunk_size);
    for k = 1:num_chunks
        % Define chunk indices
        start_idx = (k-1) * chunk_size + 1;
        end_idx = min(k * chunk_size, length(message_signal));
        
        % Extract chunk
        chunk = message_signal(start_idx:end_idx);
        
        % Time vector for the chunk
        t = (start_idx-1:end_idx-1) / fs;
        
        % Carrier signal for the chunk
        carrier = cos(2 * pi * carrier_freq * t);
        
        % Modulate the chunk
        modulated_signal(start_idx:end_idx) = chunk .* carrier;
    end
end