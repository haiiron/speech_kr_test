import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from six.moves import queue
from scipy.signal import spectrogram, butter, filtfilt

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


class MicrophoneStream(object):
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break
            yield b''.join(data)


def plot_audio_with_stft_and_fft(audio_gen):
    plt.ion()
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))

    while True:
        audio_data = next(audio_gen, None)
        if audio_data is None:
            break

        wav = np.frombuffer(audio_data, np.int16)
        filtered_wav = apply_bandpass_filter(wav)

        ax1.cla()
        ax1.set_title("Time Domain")
        ax1.set_xlabel("Samples")
        ax1.set_ylabel("Amplitude")
        ax1.plot(filtered_wav)
        ax1.set_xlim(0, len(filtered_wav))
        ax1.set_ylim(-5000, 5000)

        # FFT
        fft_data = np.fft.fft(filtered_wav)
        freqs = np.fft.fftfreq(len(fft_data), 1 / RATE)
        mask = (freqs > 0) & (freqs < RATE / 2)

        ax2.cla()
        ax2.set_title("Frequency Spectrum (FFT)")
        ax2.set_xlabel("Frequency (Hz)")
        ax2.set_ylabel("Magnitude")
        ax2.plot(freqs[mask], np.abs(fft_data[mask]))

        # 가장 강한 주파수 찾기
        peak_freq = freqs[mask][np.argmax(np.abs(fft_data[mask]))]
        print(f"Highest Frequency Component: {peak_freq:.2f} Hz")

        # STFT (Spectrogram)
        f, t, Sxx = spectrogram(filtered_wav, fs=RATE, nperseg=512)

        ax3.cla()
        ax3.set_title("Spectrogram (STFT)")
        ax3.set_xlabel("Time (s)")
        ax3.set_ylabel("Frequency (Hz)")
        ax3.imshow(10 * np.log10(Sxx + 1e-10), aspect='auto', origin='lower',
                   extent=[t.min(), t.max(), f.min(), f.max()], cmap='inferno')

        plt.pause(0.01)


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def apply_bandpass_filter(data, lowcut=100, highcut=7500, fs=RATE, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    return filtfilt(b, a, data)


def main():
    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        plot_audio_with_stft_and_fft(audio_generator)
    print("Audio Stream Ended.")


if __name__ == '__main__':
    main()
    print("End of Program")