
import sounddevice as sd
import numpy as np
import wave
from pathlib import Path
from queue import Queue, Empty

# Audio configuration
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_DURATION = 0.1

# Temporary silence detection settings
SILENCE_THRESHOLD = 0.01
SILENCE_DURATION = 1.0

audio_queue = Queue()


def audio_callback(indata, frames, time, status):

    if status:
        print("Audio status:", status)

    audio_queue.put(indata.copy())


def record_audio():

    recorded_chunks = []

    speech_started = False
    silence_chunks = 0

    required_silence_chunks = int(
        SILENCE_DURATION / CHUNK_DURATION
    )

    print("\nMicrophone is listening...")
    print("Speak whenever you are ready.")
    print("Press Ctrl+C to stop the program.\n")

    try:

        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="float32",
            blocksize=int(SAMPLE_RATE * CHUNK_DURATION),
            callback=audio_callback
        ):

            while True:

                try:
                    audio_chunk = audio_queue.get(timeout=1)

                except Empty:
                    continue

                # Calculate audio energy
                volume = np.sqrt(
                    np.mean(audio_chunk ** 2)
                )

                # Detect speech
                if volume > SILENCE_THRESHOLD:

                    if not speech_started:
                        print("Speech detected!")

                    speech_started = True
                    silence_chunks = 0

                elif speech_started:

                    silence_chunks += 1

                # Preserve all audio after speech begins
                if speech_started:
                    recorded_chunks.append(audio_chunk)

                # Detect the end of speech
                if silence_chunks >= required_silence_chunks:

                    print("\nSpeech ended!")
                    break

    except KeyboardInterrupt:
        print("\nRecording interrupted.")

    if not recorded_chunks:
        print("No speech detected.")
        return None

    return np.concatenate(recorded_chunks, axis=0)


def save_audio(audio):

    if audio is None:
        return

    output_folder = Path("data/cache")
    output_folder.mkdir(parents=True, exist_ok=True)

    output_file = output_folder / "microphone_test.wav"

    audio_int16 = (
        np.clip(audio, -1.0, 1.0) * 32767
    ).astype(np.int16)

    with wave.open(str(output_file), "wb") as wav_file:

        wav_file.setnchannels(CHANNELS)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)

        wav_file.writeframes(audio_int16.tobytes())

    print("Audio saved:", output_file)


if __name__ == "__main__":

    audio_data = record_audio()

    save_audio(audio_data)
