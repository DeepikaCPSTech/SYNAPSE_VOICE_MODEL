from pathlib import Path
import sherpa_onnx

BASE_DIR = Path(__file__).resolve().parents[2]
VAD_MODEL = BASE_DIR / "models" / "vad" / "silero_vad.onnx"


def create_vad():

    if not VAD_MODEL.is_file():
        raise FileNotFoundError(
            f"VAD model not found: {VAD_MODEL}"
        )

    config = sherpa_onnx.VadModelConfig()

    config.silero_vad.model = str(VAD_MODEL)
    config.silero_vad.threshold = 0.5
    config.silero_vad.min_silence_duration = 3.0
    config.silero_vad.min_speech_duration = 0.25
    config.silero_vad.max_speech_duration = 10.0

    config.sample_rate = 16000
    config.num_threads = 1
    config.provider = "cpu"

    vad = sherpa_onnx.VoiceActivityDetector(
        config,
        buffer_size_in_seconds=30
    )

    return vad


if __name__ == "__main__":

    print("Loading Silero VAD...")

    vad = create_vad()

    print("Silero VAD loaded successfully!")
    print("SYNAPSE Voice Activity Detection is ready!")