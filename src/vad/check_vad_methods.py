import sherpa_onnx

print("Checking Sherpa-ONNX VAD methods...\n")

for name in dir(sherpa_onnx.VoiceActivityDetector):
    if not name.startswith("_"):
        print(name)