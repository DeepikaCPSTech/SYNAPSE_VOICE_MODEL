import sounddevice as sd

print("Default input device:")
print(sd.default.device[0])

print("\nAvailable input devices:\n")

for index, device in enumerate(sd.query_devices()):
    if device["max_input_channels"] > 0:
        print(
            f"Device {index}: {device['name']}"
        )

print("\nDefault device details:")
print(sd.query_devices(sd.default.device[0]))