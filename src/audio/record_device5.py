import sounddevice as sd
import soundfile as sf
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

OUTPUT_FILE = BASE_DIR / "data" / "cache" / "device5_recording.wav"

print("Recording using Device 5...")
print("Say clearly:")
print("Hello SYNAPSE, I am testing my offline voice assistant.")

audio = sd.rec(
    int(7 * 16000),
    samplerate=16000,
    channels=1,
    dtype="float32",
    device=5
)

sd.wait()

sf.write(str(OUTPUT_FILE), audio, 16000)

print("\nRecording completed!")
print("Saved at:", OUTPUT_FILE)
print("RMS:", np.sqrt(np.mean(audio ** 2)))