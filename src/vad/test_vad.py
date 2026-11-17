
from pathlib import Path
import soundfile as sf

from vad import create_vad


BASE_DIR = Path(__file__).resolve().parents[2]
AUDIO_FILE = BASE_DIR / "data" / "cache" / "microphone_test.wav"

SAMPLE_RATE = 16000
WINDOW_SIZE = 512


def test_vad():

    print("Reading audio...")

    if not AUDIO_FILE.is_file():
        raise FileNotFoundError(
            f"Audio file not found: {AUDIO_FILE}"
        )

    audio, sample_rate = sf.read(
        str(AUDIO_FILE),
        dtype="float32"
    )

    if sample_rate != SAMPLE_RATE:
        raise ValueError(
            f"Expected 16000 Hz, but got {sample_rate} Hz"
        )

    # Convert stereo audio to mono if necessary
    if audio.ndim > 1:
        audio = audio.mean(axis=1)

    print(f"Audio duration: {len(audio) / SAMPLE_RATE:.2f} seconds")

    print("\nLoading Silero VAD...")
    vad = create_vad()

    print("\nTesting speech detection...\n")

    speech_detected = False

    for i in range(0, len(audio), WINDOW_SIZE):

        chunk = audio[i:i + WINDOW_SIZE]

        if len(chunk) < WINDOW_SIZE:
            continue

        vad.accept_waveform(chunk)

        if vad.is_speech_detected() and not speech_detected:
            print("Speech detected!")
            speech_detected = True

    # Finish processing the recorded audio
    vad.flush()

    print("\n--- VAD Results ---")
    print("Speech detected:", speech_detected)
    print("VAD queue empty:", vad.empty())

    if not vad.empty():

        segment = vad.front

        print("\nCompleted speech segment found!")
        print("Number of samples:", len(segment.samples))
        print("Segment start:", segment.start)

        vad.pop()

    else:
        print("\nNo completed speech segment found.")

    print("\nVAD test completed!")


if __name__ == "__main__":
    test_vad()
