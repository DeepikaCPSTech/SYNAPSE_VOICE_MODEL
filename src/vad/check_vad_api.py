import sherpa_onnx

print("Sherpa-ONNX VAD API check")

print(
    "VoiceActivityDetector:",
    hasattr(sherpa_onnx, "VoiceActivityDetector")
)

print(
    "VadModelConfig:",
    hasattr(sherpa_onnx, "VadModelConfig")
)

print(
    "SileroVadModelConfig:",
    hasattr(sherpa_onnx, "SileroVadModelConfig")
)

print("\nAvailable VAD-related names:")

for name in dir(sherpa_onnx):
    if "vad" in name.lower():
        print(name)