
from pathlib import Path
import subprocess
import sys

import soundfile as sf
import sounddevice as sd


# Locate the SYNAPSE project folder
BASE_DIR = Path(__file__).resolve().parents[2]

# Piper voice model
MODEL_PATH = BASE_DIR / "models" / "tts" / "en_US-lessac-medium.onnx"

# Generated audio file
OUTPUT_PATH = BASE_DIR / "data" / "cache" / "synapse_speech.wav"


def speak(text):

    if not text.strip():
        print("No text provided for speech.")
        return

    if not MODEL_PATH.is_file():
        raise FileNotFoundError(f"Piper model not found: {MODEL_PATH}")

    print("SYNAPSE is generating speech...")

    # Run Piper locally
    subprocess.run(
        [
            sys.executable,
            "-m",
            "piper",
            "-m",
            str(MODEL_PATH),
            "-f",
            str(OUTPUT_PATH)
        ],
        input=text,
        text=True,
        check=True
    )

    # Read generated audio
    audio, sample_rate = sf.read(
        str(OUTPUT_PATH),
        dtype="float32"
    )

    # Play through the speaker
    print("SYNAPSE is speaking...")

    sd.play(audio, sample_rate)
    sd.wait()


if __name__ == "__main__":

    speak("Hello! I am SYNAPSE, your offline voice assistant.")
