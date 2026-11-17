from pathlib import Path
import numpy as np
import soundfile as sf

from recognizer import create_recognizer

BASE_DIR = Path(__file__).resolve().parents[2]
AUDIO_FILE = BASE_DIR / "data" / "cache" / "complete_sentence_combined.wav"

SAMPLE_RATE = 16000

audio, sample_rate = sf.read(
    str(AUDIO_FILE),
    dtype="float32"
)

if audio.ndim > 1:
    audio = audio.mean(axis=1)

print("Loading Zipformer...")
recognizer = create_recognizer()

stream = recognizer.create_stream()

print("Processing recorded audio...")

stream.accept_waveform(sample_rate, audio)

# Add a short silence at the end
silence = np.zeros(int(0.5 * SAMPLE_RATE), dtype=np.float32)
stream.accept_waveform(SAMPLE_RATE, silence)

stream.input_finished()

while recognizer.is_ready(stream):
    recognizer.decode_stream(stream)

print("\nRecognized result:")
print(recognizer.get_result(stream))