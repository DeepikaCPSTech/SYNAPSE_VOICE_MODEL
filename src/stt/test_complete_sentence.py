import sounddevice as sd
import soundfile as sf
from pathlib import Path
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[2]

OUTPUT_FILE = BASE_DIR / "data" / "cache" / "complete_sentence_stereo.wav"

print("Speak this sentence naturally:")
print("Hello SYNAPSE, I am testing my offline voice assistant.")

audio = sd.rec(
    int(7 * 16000),
    samplerate=16000,
    channels=2,
    dtype="float32",
    device=5
)

sd.wait()

sf.write(str(OUTPUT_FILE), audio, 16000)

# Combine channels 1 and 2
combined = np.mean(audio, axis=1)

sf.write(
    str(BASE_DIR / "data" / "cache" / "complete_sentence_combined.wav"),
    combined,
    16000
)

print("Stereo and combined recordings saved successfully!")