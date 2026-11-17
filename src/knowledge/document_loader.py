
import json
from pathlib import Path
from pypdf import PdfReader

# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]

DOCUMENTS_DIR = BASE_DIR / "data" / "knowledge" / "documents"
PROCESSED_DIR = BASE_DIR / "data" / "knowledge" / "processed"

# Exclude potentially sensitive student records
EXCLUDED_KEYWORDS = [
    "student data",
    "student details",
    "niat student",
    "niat students",
    "fresh",
    "renewal",
    "placement"
]


def is_excluded_file(file_path):
    filename = file_path.stem.lower()

    return any(
        keyword in filename
        for keyword in EXCLUDED_KEYWORDS
    )


def extract_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8-sig") as file:
            data = json.load(file)

        # Preserve page structure when JSON contains pages
        if isinstance(data, dict) and isinstance(data.get("pages"), list):

            extracted_pages = []

            for page in data["pages"]:
                page_number = page.get("page_number")
                content = page.get("full_text", "")

                if not content and page.get("lines"):
                    content = "\n".join(page["lines"])

                if content.strip():
                    extracted_pages.append({
                        "page_number": page_number,
                        "content": content.strip()
                    })

            return extracted_pages

        # Handle ordinary JSON files
        return json.dumps(data, ensure_ascii=False, indent=2)

    except Exception as error:
        print(f"JSON error: {file_path.name}: {error}")
        return None


def extract_pdf(file_path):
    try:
        reader = PdfReader(str(file_path))

        pages = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()

            if text and text.strip():
                pages.append({
                    "page_number": page_number,
                    "content": text.strip()
                })

        return pages

    except Exception as error:
        print(f"PDF error: {file_path.name}: {error}")
        return None


def load_documents():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    documents = []

    for file_path in DOCUMENTS_DIR.rglob("*"):

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in [".json", ".pdf"]:
            continue

        if is_excluded_file(file_path):
            print(f"SKIPPED: {file_path.name}")
            continue

        if file_path.suffix.lower() == ".json":
            content = extract_json(file_path)
        else:
            content = extract_pdf(file_path)

        if not content:
            print(f"EMPTY: {file_path.name}")
            continue

        documents.append({
            "source": str(file_path.relative_to(DOCUMENTS_DIR)),
            "content": content
        })

        print(f"LOADED: {file_path.name}")

    return documents


def save_processed_documents(documents):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    output_file = PROCESSED_DIR / "documents.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(documents, file, ensure_ascii=False, indent=2)

    print(f"\nSaved {len(documents)} documents.")
    print(f"Output: {output_file}")


if __name__ == "__main__":
    print("SYNAPSE Document Loader")
    print("-----------------------")

    documents = load_documents()
    save_processed_documents(documents)
