
from pathlib import Path
import numpy as np
import soundfile as sf

from recognizer import create_recognizer

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_AUDIO_DIR = (
    BASE_DIR
    / "models"
    / "stt"
    / "sherpa-onnx-streaming-zipformer-en-2023-06-26"
    / "test_wavs"
)

recognizer = create_recognizer()

files = [
    "0.wav",
    "1.wav",
    "complete_sentence.wav",
    "complete_sentence_cleaned.wav",
    "device5_recording.wav"
]

MIC_AUDIO_DIR = BASE_DIR / "data" / "cache"

files.extend([
    "complete_sentence.wav",
])

for filename in files:

    if filename in ["0.wav", "1.wav"]    :
        audio_file = MODEL_AUDIO_DIR / filename
    else:    
        audio_file = MIC_AUDIO_DIR / filename
    

    audio, sample_rate = sf.read(
        str(audio_file),
        dtype="float32"
    )

    if audio.ndim > 1:
        audio = audio.mean(axis=1)

    print("\n--- Audio Diagnostics ---")
    print("Sample rate:", sample_rate)
    print("Duration:", len(audio) / sample_rate)
    print("Audio shape:", audio.shape)
    print("Maximum volume:", np.max(np.abs(audio)))
    print("RMS volume:", np.sqrt(np.mean(audio ** 2)))

    stream = recognizer.create_stream()

    stream.accept_waveform(sample_rate, audio)

    silence = np.zeros(
        int(0.5 * sample_rate),
        dtype=np.float32
    )

    stream.accept_waveform(sample_rate, silence)

    stream.input_finished()

    while recognizer.is_ready(stream):
        recognizer.decode_stream(stream)

    result = recognizer.get_result(stream)

    expected = "HELLO SYNAPSE I AM TESTING MY OFFLINE VOICE ASSISTANT"

    print("Expected:", expected)
    print("Recognized:", result)
    print(f"\nFile: {filename}")
    print("Recognized:", result)
