from pathlib import Path
import soundfile as sf
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[2]
AUDIO_FILE = BASE_DIR / "data" / "cache" / "microphone_test.wav"

audio, sample_rate = sf.read(AUDIO_FILE)

print("Sample rate:", sample_rate)
print("Audio shape:", audio.shape)
print("Duration:", len(audio) / sample_rate, "seconds")
print("Minimum value:", np.min(audio))
print("Maximum value:", np.max(audio))
print("Average volume:", np.sqrt(np.mean(audio ** 2)))