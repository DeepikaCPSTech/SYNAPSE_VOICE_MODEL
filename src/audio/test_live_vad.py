
from pathlib import Path
import sys
import sounddevice as sd
import numpy as np

# Add the src directory to Python's import path
BASE_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = BASE_DIR / "src"

sys.path.insert(0, str(SRC_DIR))

from vad.vad import create_vad


SAMPLE_RATE = 16000
WINDOW_SIZE = 512
MICROPHONE_DEVICE = 1
TEST_DURATION = 15


def test_live_vad():

    print("Loading Silero VAD...")
    vad = create_vad()

    print("\nStarting live microphone test...")
    print("Speak continuously for 5 seconds.")
    print("Then remain silent for the remaining time.\n")

    total_blocks = int(
        TEST_DURATION * SAMPLE_RATE / WINDOW_SIZE
    )

    speech_detected = False

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        blocksize=WINDOW_SIZE,
        device=MICROPHONE_DEVICE
    ) as microphone:

        for i in range(total_blocks):

            audio, overflowed = microphone.read(WINDOW_SIZE)
            audio = audio.flatten()

            vad.accept_waveform(audio)

            rms = np.sqrt(np.mean(audio ** 2))
            active = vad.is_speech_detected()

            if active:
                speech_detected = True

            if i % 31 == 0:
                print(
                    f"RMS: {rms:.5f}"
                    f" | Speech active: {active}"
                    f" | Queue empty: {vad.empty()}"
                    f" | Overflow: {overflowed}",
                    flush=True
                )

    vad.flush()

    print("\n--- FINAL RESULTS ---")
    print("Speech detected:", speech_detected)
    print("Queue empty:", vad.empty())

    if not vad.empty():

        segment = vad.front

        print(
            "Completed segment samples:",
            len(segment.samples)
        )

        vad.pop()

    print("\nLive VAD test completed!")


if __name__ == "__main__":
    test_live_vad()
