
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def split_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """
    Divide text into smaller overlapping chunks.
    """

    if not text:
        return []

    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk size")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:

        end = min(start + chunk_size, text_length)

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == text_length:
            break

        start = end - overlap

    return chunks


def chunk_documents(documents):
    """
    Convert extracted documents into searchable chunks.
    Supports both normal text and page-based documents.
    """

    all_chunks = []

    for document in documents:

        source = document["source"]
        content = document["content"]

        # Handle page-based documents
        if isinstance(content, list):

            for page in content:

                page_number = page["page_number"]
                page_content = page["content"]

                text_chunks = split_text(page_content)

                for index, chunk in enumerate(text_chunks):

                    all_chunks.append({
                        "source": source,
                        "page_number": page_number,
                        "chunk_id": index,
                        "content": chunk
                    })

        # Handle ordinary text documents
        elif isinstance(content, str):

            text_chunks = split_text(content)

            for index, chunk in enumerate(text_chunks):

                all_chunks.append({
                    "source": source,
                    "page_number": None,
                    "chunk_id": index,
                    "content": chunk
                })

    return all_chunks
