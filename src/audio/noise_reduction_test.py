
import numpy as np
import soundfile as sf
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data" / "cache" / "complete_sentence.wav"
OUTPUT_FILE = BASE_DIR / "data" / "cache" / "complete_sentence_cleaned.wav"

# Load original audio
audio, sample_rate = sf.read(INPUT_FILE, dtype="float32")

# Convert stereo to mono if needed
if audio.ndim == 2:
    audio = np.mean(audio, axis=1)

# Check sample rate
if sample_rate != 16000:
    raise ValueError(f"Expected 16000 Hz audio, received {sample_rate} Hz")

# Estimate background noise from the first 0.5 seconds
noise_duration = 0.5
noise_samples = int(noise_duration * sample_rate)
noise_audio = audio[:noise_samples]

if len(noise_audio) < 512:
    raise ValueError("Not enough audio to estimate background noise.")

# Calculate noise spectrum
frame_size = 512
noise_frames = []

for start in range(0, len(noise_audio) - frame_size + 1, frame_size):
    frame = noise_audio[start:start + frame_size]
    noise_frames.append(np.abs(np.fft.rfft(frame)))

if not noise_frames:
    raise ValueError("Could not calculate background noise.")

noise_profile = np.mean(noise_frames, axis=0)

# Process audio in overlapping frames
hop_size = 256
window = np.hanning(frame_size).astype(np.float32)

padded = np.pad(audio, (frame_size // 2, frame_size // 2))
output = np.zeros(len(padded), dtype=np.float32)
weight = np.zeros(len(padded), dtype=np.float32)

for start in range(0, len(padded) - frame_size + 1, hop_size):
    frame = padded[start:start + frame_size]

    spectrum = np.fft.rfft(frame * window)
    magnitude = np.abs(spectrum)
    phase = np.angle(spectrum)

    # Reduce estimated background noise
    cleaned_magnitude = np.maximum(
        magnitude - (1.5 * noise_profile),
        magnitude * 0.10
    )

    cleaned_spectrum = cleaned_magnitude * np.exp(1j * phase)
    cleaned_frame = np.fft.irfft(cleaned_spectrum, n=frame_size)

    output[start:start + frame_size] += cleaned_frame * window
    weight[start:start + frame_size] += window ** 2

# Normalize overlapping frames
valid = weight > 1e-8
output[valid] /= weight[valid]

# Remove padding
cleaned_audio = output[frame_size // 2:frame_size // 2 + len(audio)]

# Save cleaned recording
sf.write(OUTPUT_FILE, cleaned_audio, sample_rate)

print("Noise reduction test completed!")
print("Original:", INPUT_FILE)
print("Cleaned:", OUTPUT_FILE)
print("Sample rate:", sample_rate)
print("Duration:", len(cleaned_audio) / sample_rate)

print("\n--- Audio Quality Comparison ---")

print(
    "Original RMS:",
    np.sqrt(np.mean(audio ** 2))
)

print(
    "Cleaned RMS:",
    np.sqrt(np.mean(cleaned_audio ** 2))
)

print(
    "Original Peak:",
    np.max(np.abs(audio))
)

print(
    "Cleaned Peak:",
    np.max(np.abs(cleaned_audio))
)