
from pathlib import Path
import sys
import time
import sounddevice as sd

BASE_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = BASE_DIR / "src"

sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(SRC_DIR))

from stt.recognizer import create_recognizer
from vad.vad import create_vad
from llm.response import generate_response
from tts.speak import speak

from src.memory.database import initialize_database
from src.memory.manager import (
    create_conversation,
    save_message,
    get_chat_context
)
from src.memory.fact_extractor import extract_and_save_facts



SAMPLE_RATE = 16000
WINDOW_SIZE = 512
MICROPHONE_DEVICE = 1
MAX_LISTEN_SECONDS = 30


def listen_for_question(recognizer, vad):

    # Reset VAD state for the new question
    vad.reset()

    stream = recognizer.create_stream()

    previous_text = ""
    previous_speech_active = False

    start_time = time.time()
    speech_started = False

    print("\nSpeak your question...")

    try:

        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            blocksize=WINDOW_SIZE,
            device=MICROPHONE_DEVICE
        ) as microphone:

            while True:

                audio, overflowed = microphone.read(WINDOW_SIZE)

                if overflowed:
                    print("\nMicrophone overflow warning.")

                audio = audio.flatten()

                # VAD processing
                vad.accept_waveform(audio)

                speech_active = vad.is_speech_detected()

                if speech_active and not previous_speech_active:
                    print("\n[VAD] LIVE SPEECH DETECTED")

                previous_speech_active = speech_active

                if speech_active:
                    speech_started = True

                # Zipformer processing
                stream.accept_waveform(
                    SAMPLE_RATE,
                    audio
                )

                while recognizer.is_ready(stream):
                    recognizer.decode_stream(stream)

                # Partial transcription
                text = recognizer.get_result(stream)

                if text and text.strip() != previous_text:

                    print(
                        "\r" + " " * 120,
                        end=""
                    )

                    print(
                        "\rYou:",
                        text,
                        end="",
                        flush=True
                    )

                    previous_text = text.strip()

                # End of speech
                if speech_started and not vad.empty():

                    segment = vad.front

                    print("\n\n[VAD] Speech completed.")

                    print(
                        "[VAD] Segment samples:",
                        len(segment.samples)
                    )

                    vad.pop()

                    print("[VAD] Stopping microphone...")
                    break

                # Listening timeout
                if time.time() - start_time >= MAX_LISTEN_SECONDS:

                    print("\n[INFO] Maximum listening time reached.")
                    break

        # Finalize Zipformer
        stream.input_finished()

        while recognizer.is_ready(stream):
            recognizer.decode_stream(stream)

        recognized_text = recognizer.get_result(stream).strip()

        print("\n\nRecognized question:", recognized_text)

        return recognized_text

    except KeyboardInterrupt:
        raise


def start_voice_chat():

    print("Initializing SYNAPSE memory...")
    initialize_database()

    conversation_id = create_conversation(
        "SYNAPSE Voice Conversation"
    )

    print("Memory conversation created!")
    print("Conversation ID:", conversation_id)

    print("\nLoading Zipformer STT...")
    recognizer = create_recognizer()

    print("\nLoading Silero VAD...")
    vad = create_vad()

    print("\nLoading completed!")

    print("\nSYNAPSE is ready!")
    print("Continuous voice chat activated.")
    print("Press Ctrl + C to stop.\n")

    try:

        while True:

            # Listen to the next question
            recognized_text = listen_for_question(
                recognizer,
                vad
            )

            if not recognized_text:
                print("\nNo speech recognized. Listening again...")
                continue

            # Retrieve previous conversation
            print("\nRetrieving previous conversation...")

            chat_history = get_chat_context(conversation_id)

            # Save current user message
            save_message(
                conversation_id,
                "user",
                recognized_text
            )

            memory_response = extract_and_save_facts(recognized_text            )

            if memory_response:
                print("SYNAPSE MEMORY:", memory_response)

            # Generate response
            print("\nSYNAPSE is thinking...")

            answer = generate_response(
                recognized_text,
                chat_history=chat_history
            )

            print("\nSYNAPSE:", answer)

            # Save assistant response
            save_message(
                conversation_id,
                "assistant",
                answer
            )

            print("\n[MEMORY] Conversation saved successfully!")

            # Speak response
            speak(answer)

            print("\n[READY] Waiting for your next question...")

    except KeyboardInterrupt:

        print("\n\nSYNAPSE voice chat stopped.")
        print("Conversation saved in SQLite.")


if __name__ == "__main__":
    start_voice_chat()
