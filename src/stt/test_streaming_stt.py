from pathlib import Path
import soundfile as sf
import numpy as np

from recognizer import create_recognizer

BASE_DIR = Path(__file__).resolve().parents[2]

AUDIO_FILE = BASE_DIR / "data" / "cache" / "microphone_test.wav"

SAMPLE_RATE = 16000
CHUNK_SIZE = 512


def test_streaming_stt():

    print("Reading audio...")

    audio, sample_rate = sf.read(
        str(AUDIO_FILE),
        dtype="float32"
    )

    if audio.ndim > 1:
        audio = audio.mean(axis=1)

    if sample_rate != SAMPLE_RATE:
        raise ValueError("Audio must be 16000 Hz")

    print("Loading Zipformer...")
    recognizer = create_recognizer()

    stream = recognizer.create_stream()

    print("\nStreaming audio in chunks...\n")

    previous_text = ""

    for i in range(0, len(audio), CHUNK_SIZE):

        chunk = audio[i:i + CHUNK_SIZE]

        stream.accept_waveform(SAMPLE_RATE, chunk)

        while recognizer.is_ready(stream):
            recognizer.decode_stream(stream)

        current_text = recognizer.get_result(stream)

        if current_text != previous_text:
            print("Live text:", current_text)
            previous_text = current_text

    print("\nFinishing transcription...")

    stream.input_finished()

    while recognizer.is_ready(stream):
        recognizer.decode_stream(stream)

    print("\nFinal text:")
    print(recognizer.get_result(stream))


if __name__ == "__main__":
    test_streaming_stt()