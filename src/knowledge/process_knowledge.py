
import json
from pathlib import Path

from src.knowledge.chunker import chunk_documents


BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    BASE_DIR / "data" / "knowledge" / "processed" / "documents.json"
)

OUTPUT_FILE = (
    BASE_DIR / "data" / "knowledge" / "processed" / "knowledge_chunks.json"
)


def process_knowledge():

    print("Loading extracted documents...")

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        documents = json.load(file)

    print(f"Documents loaded: {len(documents)}")

    print("\nCreating knowledge chunks...")

    chunks = chunk_documents(documents)

    print(f"Total chunks created: {len(chunks)}")

    print("\nSaving knowledge chunks...")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(chunks, file, ensure_ascii=False)

    print("\nSYNAPSE knowledge processing completed!")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    process_knowledge()
