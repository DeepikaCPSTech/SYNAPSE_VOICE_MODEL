
from pathlib import Path
import sherpa_onnx


# Find the main SYNAPSE project folder
BASE_DIR = Path(__file__).resolve().parents[2]

# Location of our downloaded Zipformer model
MODEL_DIR = (
    BASE_DIR
    / "models"
    / "stt"
    / "sherpa-onnx-streaming-zipformer-en-2023-06-26"
)

# Required model files
TOKENS = MODEL_DIR / "tokens.txt"

ENCODER = (
    MODEL_DIR
    / "encoder-epoch-99-avg-1-chunk-16-left-128.int8.onnx"
)

DECODER = (
    MODEL_DIR
    / "decoder-epoch-99-avg-1-chunk-16-left-128.onnx"
)

JOINER = (
    MODEL_DIR
    / "joiner-epoch-99-avg-1-chunk-16-left-128.int8.onnx"
)


def create_recognizer():

    # Check whether all model files exist
    model_files = [TOKENS, ENCODER, DECODER, JOINER]

    for file in model_files:
        if not file.is_file():
            raise FileNotFoundError(
                f"Model file not found: {file}"
            )

    print("Loading Zipformer STT model...")

    # Create the offline speech recognition engine
    recognizer = sherpa_onnx.OnlineRecognizer.from_transducer(
        tokens=str(TOKENS),
        encoder=str(ENCODER),
        decoder=str(DECODER),
        joiner=str(JOINER),
        num_threads=2,
        sample_rate=16000,
        feature_dim=80,
        decoding_method="greedy_search",
        provider="cpu",
    )

    print("Zipformer STT model loaded successfully!")

    return recognizer


if __name__ == "__main__":

    recognizer = create_recognizer()

    print("SYNAPSE STT is ready!")
