
from pathlib import Path
import sys

import numpy as np
import sounddevice as sd

# Add the src folder to Python's import path
BASE_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = BASE_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from vad.vad import create_vad
from stt.recognizer import create_recognizer


SAMPLE_RATE = 16000
WINDOW_SIZE = 512


def finish_transcription(recognizer, stream):
    """Finish decoding and return the final recognized text."""

    stream.input_finished()

    while recognizer.is_ready(stream):
        recognizer.decode_stream(stream)

    return recognizer.get_result(stream)


def start_listening():

    print("Loading Silero VAD...")
    vad = create_vad()

    print("Loading Zipformer STT...")
    recognizer = create_recognizer()

    # Create one streaming recognition session
    stream = recognizer.create_stream()

    print("\nSYNAPSE is ready!")
    print("Start speaking.")
    print("It will stop after 1.5 seconds of silence.\n")

    previous_text = ""
    speech_finished = False

    try:

        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            blocksize=WINDOW_SIZE
        ) as microphone:

            print("SYNAPSE is listening...\n")

            while True:

                # Read live microphone audio
                audio, overflowed = microphone.read(WINDOW_SIZE)

                if overflowed:
                    print("Warning: Microphone audio overflowed.")

                audio = audio.flatten().astype(np.float32)

                # Send the same audio to both models
                stream.accept_waveform(SAMPLE_RATE, audio)
                vad.accept_waveform(audio)

                # Decode available streaming audio
                while recognizer.is_ready(stream):
                    recognizer.decode_stream(stream)

                # Display changing partial transcription
                current_text = recognizer.get_result(stream)

                if current_text and current_text != previous_text:
                    print("Live text:", current_text, flush=True)
                    previous_text = current_text

                # VAD creates a completed segment after silence
                if not vad.empty():
                    speech_finished = True
                    break

        # Microphone is now closed
        print("\nSilence detected. Microphone stopped.")

        # Finalize the streaming transcription
        final_text = finish_transcription(recognizer, stream)

        print("\nFinal recognized text:")
        print(final_text if final_text else "No speech recognized.")

    except KeyboardInterrupt:

        print("\nManual stop requested.")

        final_text = finish_transcription(recognizer, stream)

        print("\nFinal recognized text:")
        print(final_text if final_text else "No speech recognized.")

    finally:
        print("\nSYNAPSE stopped.")


if __name__ == "__main__":
    start_listening()
