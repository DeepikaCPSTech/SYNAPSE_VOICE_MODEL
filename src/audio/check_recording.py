
import soundfile as sf
import numpy as np

file_path = "data/cache/device5_recording.wav"

audio, sample_rate = sf.read(file_path)

print("Recording diagnostics")
print("---------------------")
print("Sample rate:", sample_rate)
print("Shape:", audio.shape)
print("Data type:", audio.dtype)
print("Duration:", len(audio) / sample_rate)
print("Minimum:", np.min(audio))
print("Maximum:", np.max(audio))
print("RMS:", np.sqrt(np.mean(audio ** 2)))

print("\nRMS per second:")

for i in range(int(len(audio) / sample_rate)):
    segment = audio[
        i * sample_rate:(i + 1) * sample_rate
    ]

    rms = np.sqrt(np.mean(segment ** 2))
    print(f"Second {i + 1}: {rms:.6f}")
