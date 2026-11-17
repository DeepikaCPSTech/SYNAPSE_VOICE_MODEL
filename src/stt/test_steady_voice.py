import soundfile as sf
import numpy as np
from recognizer import create_recognizer

audio, sample_rate = sf.read(
    "data/cache/steady_voice_test.wav",
    dtype="float32"
)

if audio.ndim > 1:
    audio = audio.mean(axis=1)

print("Loading Zipformer...")
recognizer = create_recognizer()

stream = recognizer.create_stream()

stream.accept_waveform(sample_rate, audio)

silence = np.zeros(int(0.5 * sample_rate), dtype=np.float32)
stream.accept_waveform(sample_rate, silence)

stream.input_finished()

while recognizer.is_ready(stream):
    recognizer.decode_stream(stream)

print("\nExpected: THE WEATHER IS PLEASANT TODAY")
print("Recognized:", recognizer.get_result(stream))