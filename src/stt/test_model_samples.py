from pathlib import Path
import numpy as np
import soundfile as sf

from recognizer import create_recognizer

BASE_DIR = Path(__file__).resolve().parents[2]

SAMPLE_DIR = (
    BASE_DIR
    / "models"
    / "stt"
    / "sherpa-onnx-streaming-zipformer-en-2023-06-26"
    / "test_wavs"
)

SAMPLE_RATE = 16000

recognizer = create_recognizer()

for filename in ["0.wav", "1.wav"]:

    audio_file = SAMPLE_DIR / filename

    audio, sample_rate = sf.read(
        str(audio_file),
        dtype="float32"
    )

    print(f"\nTesting {filename}...")

    if sample_rate != SAMPLE_RATE:
        print("Incorrect sample rate. Skipping.")
        continue

    stream = recognizer.create_stream()

    stream.accept_waveform(SAMPLE_RATE, audio)

    silence = np.zeros(8000, dtype=np.float32)
    stream.accept_waveform(SAMPLE_RATE, silence)

    stream.input_finished()

    while recognizer.is_ready(stream):
        recognizer.decode_stream(stream)

    result = recognizer.get_result(stream)

    print("Recognized text:")
    print(result)