
import sounddevice as sd
import numpy as np

print("Testing InputStream with device 1 (MME)...")
print("Speak continuously for 5 seconds.\n")

with sd.InputStream(
    samplerate=16000,
    channels=1,
    dtype="float32",
    device=1
) as microphone:

    for i in range(10):
        audio, overflowed = microphone.read(1600)

        rms = np.sqrt(np.mean(audio ** 2))

        print(
            f"Test {i + 1}: RMS = {rms:.6f}"
            f" | Overflow = {overflowed}",
            flush=True
        )

print("\nTest completed!")
