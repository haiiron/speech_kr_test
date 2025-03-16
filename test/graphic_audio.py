import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from six.moves import queue

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
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
        """Continuously collect data from the audio stream, into the buffer."""
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


def plot_audio(audio_gen):
    full_frame = []
    plt.ion()

    for i, x in enumerate(audio_gen):
        full_frame.append(x)
        str_frame = b''.join(full_frame)

        # FIXME: Deprecation Warning 수정: fromstring -> frombuffer
        wav = np.frombuffer(str_frame, np.int16)

        plt.cla()
        plt.axis([0, CHUNK * 10, -5000, 5000])
        try:
            plt.plot(wav[-CHUNK * 10:])
        except Exception:
            plt.plot(wav)

        plt.pause(0.01)


def main():
    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        plot_audio(audio_generator)

    print("Audio Stream Ended.")

if __name__ == '__main__':
    main()
    print("End of Program")
