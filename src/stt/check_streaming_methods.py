from recognizer import create_recognizer

print("Loading Zipformer...")
recognizer = create_recognizer()

print("\nChecking streaming methods:\n")

for name in dir(recognizer):
    if not name.startswith("_"):
        print(name)

print("\nChecking streaming methods completed!")