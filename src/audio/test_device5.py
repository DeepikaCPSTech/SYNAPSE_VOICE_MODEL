import sounddevice as sd
import soundfile as sf

print("Wait 1 second, then speak:")
print("Hello SYNAPSE, I am testing voice detection.")

audio = sd.rec(
    int(5 * 16000),
    samplerate=16000,
    channels=1,
    dtype="float32",
    device=5
)

sd.wait()

sf.write(
    "data/cache/microphone_test.wav",
    audio,
    16000
)

print("Recording saved!")