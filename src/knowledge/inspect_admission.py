
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

CHUNKS_FILE = (
    BASE_DIR
    / "data"
    / "knowledge"
    / "processed"
    / "knowledge_chunks.json"
)

with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
    documents = json.load(file)

keywords = [
    "entrance",
    "chaitanya entrance",
    "foreign national",
    "overseas citizen",
    "refund of fees",
    "application procedure"
]

for document in documents:

    source = document["source"].lower()

    if "admissions guidelines" not in source:
        continue

    content = document["content"].lower()

    matched = [
        keyword for keyword in keywords
        if keyword in content
    ]

    if matched:
        print("\n" + "=" * 70)
        print("Page:", document.get("page_number"))
        print("Chunk ID:", document["chunk_id"])
        print("Matched keywords:", matched)
        print(document["content"][:1200])
