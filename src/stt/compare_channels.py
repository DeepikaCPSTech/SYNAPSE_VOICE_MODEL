from pathlib import Path
import numpy as np
import soundfile as sf

from recognizer import create_recognizer

BASE_DIR = Path(__file__).resolve().parents[2]
AUDIO_DIR = BASE_DIR / "data" / "cache"

recognizer = create_recognizer()

for channel in [1, 2]:

    audio_file = AUDIO_DIR / f"mic_channel_{channel}.wav"

    audio, sample_rate = sf.read(
        str(audio_file),
        dtype="float32"
    )

    stream = recognizer.create_stream()

    stream.accept_waveform(sample_rate, audio)

    silence = np.zeros(8000, dtype=np.float32)
    stream.accept_waveform(sample_rate, silence)

    stream.input_finished()

    while recognizer.is_ready(stream):
        recognizer.decode_stream(stream)

    result = recognizer.get_result(stream)

    print(f"\nChannel {channel} result:")
    print(result)