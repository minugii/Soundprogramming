import math
import wave
from pathlib import Path

import numpy as np
from IPython.display import Audio


class ToneGenerator:
    """간단한 소리 생성기.

    다른 노트북에서 import 해서 사용하면 됩니다.
    예:
        from sound_generator import ToneGenerator
        synth = ToneGenerator(sample_rate=44100)
        tone = synth.sine(440, duration=1.0)
    """

    def __init__(self, sample_rate=44100, amplitude=0.5):
        self.sample_rate = sample_rate
        self.amplitude = amplitude

    def _time_array(self, duration_seconds):
        return np.linspace(
            0,
            duration_seconds,
            int(self.sample_rate * duration_seconds),
            endpoint=False,
        )

    def sine(self, frequency_hz, duration_seconds=1.0, amplitude=None, phase=0.0):
        amp = self.amplitude if amplitude is None else amplitude
        t = self._time_array(duration_seconds)
        return amp * np.sin(2 * np.pi * frequency_hz * t + phase)

    def square(self, frequency_hz, duration_seconds=1.0, amplitude=None, phase=0.0):
        amp = self.amplitude if amplitude is None else amplitude
        t = self._time_array(duration_seconds)
        wave = np.sin(2 * np.pi * frequency_hz * t + phase)
        return amp * np.sign(wave)

    def triangle(self, frequency_hz, duration_seconds=1.0, amplitude=None, phase=0.0):
        amp = self.amplitude if amplitude is None else amplitude
        t = self._time_array(duration_seconds)
        angle = 2 * np.pi * frequency_hz * t + phase
        wave = 2 / math.pi * np.arcsin(np.sin(angle))
        return amp * wave

    def render(self, frequency_hz, duration_seconds=1.0, waveform="sine", amplitude=None, phase=0.0):
        if waveform == "sine":
            return self.sine(frequency_hz, duration_seconds, amplitude, phase)
        if waveform == "square":
            return self.square(frequency_hz, duration_seconds, amplitude, phase)
        if waveform == "triangle":
            return self.triangle(frequency_hz, duration_seconds, amplitude, phase)
        raise ValueError("지원하지 않는 waveform: {}".format(waveform))

    def play(self, wave_data):
        return Audio(wave_data, rate=self.sample_rate)

    def save_wav(self, filename, wave_data, normalized=True):
        path = Path(filename)
        if normalized:
            data = np.clip(wave_data, -1.0, 1.0)
            pcm = (data * 32767).astype(np.int16)
        else:
            pcm = np.asarray(wave_data, dtype=np.int16)

        with wave.open(str(path), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(pcm.tobytes())

        return path


class SineTone:
    """단일 톤을 쉽게 만들기 위한 간단한 별칭 클래스."""

    def __init__(self, frequency_hz, sample_rate=44100, amplitude=0.5):
        self.frequency_hz = frequency_hz
        self.sample_rate = sample_rate
        self.amplitude = amplitude

    def waveform(self, duration_seconds=1.0, phase=0.0):
        synth = ToneGenerator(sample_rate=self.sample_rate, amplitude=self.amplitude)
        return synth.sine(self.frequency_hz, duration_seconds, phase=phase)

    def play(self, duration_seconds=1.0):
        synth = ToneGenerator(sample_rate=self.sample_rate, amplitude=self.amplitude)
        return synth.play(self.waveform(duration_seconds))

    def save(self, filename, duration_seconds=1.0):
        synth = ToneGenerator(sample_rate=self.sample_rate, amplitude=self.amplitude)
        wave_data = self.waveform(duration_seconds)
        return synth.save_wav(filename, wave_data)
