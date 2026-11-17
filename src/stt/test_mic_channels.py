from pathlib import Path
import sounddevice as sd
import soundfile as sf
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = BASE_DIR / "data" / "cache"

SAMPLE_RATE = 16000
DEVICE = 5
DURATION = 5

print("Recording from all 4 microphone channels...")
print("Speak a clear sentence.")

audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=4,
    dtype="float32",
    device=DEVICE
)

sd.wait()

for channel in range(4):
    channel_audio = audio[:, channel]

    output_file = OUTPUT_DIR / f"mic_channel_{channel + 1}.wav"

    sf.write(str(output_file), channel_audio, SAMPLE_RATE)

    rms = np.sqrt(np.mean(channel_audio ** 2))

    print(
        f"Channel {channel + 1}: "
        f"RMS = {rms:.5f}"
    )

print("\nAll 4 channel recordings saved.")