
from pathlib import Path
import numpy as np
import soundfile as sf

BASE_DIR = Path(__file__).resolve().parents[2]
AUDIO_FILE = BASE_DIR / "data" / "cache" / "complete_sentence.wav"

audio, sr = sf.read(str(AUDIO_FILE), dtype="float32")

print("--- Volume by Second ---")

for second in range(int(len(audio) / sr)):
    start = second * sr
    end = start + sr
    segment = audio[start:end]

    rms = np.sqrt(np.mean(segment ** 2))
    peak = np.max(np.abs(segment))

    print(
        f"Second {second + 1}: "
        f"RMS={rms:.5f}, Peak={peak:.5f}"
    )
