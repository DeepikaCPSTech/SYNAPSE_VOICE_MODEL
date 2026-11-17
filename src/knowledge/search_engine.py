
import json
import re
from pathlib import Path

from rank_bm25 import BM25Okapi


# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]

CHUNKS_FILE = (
    BASE_DIR
    / "data"
    / "knowledge"
    / "processed"
    / "knowledge_chunks.json"
)


def tokenize(text):
    """Convert text into lowercase searchable words."""
    return re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())


class KnowledgeSearch:

    def __init__(self):

        print("Loading SYNAPSE knowledge base...")

        with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
            self.documents = json.load(file)

        print(f"Loaded {len(self.documents)} knowledge chunks.")
        print("SYNAPSE knowledge search is ready!")

    def select_documents(self, query):
        """Select relevant documents based on the question."""

        query_lower = query.lower()

        # CSE AIML course and syllabus questions
        aiml_keywords = [
            "aiml",
            "ai&ml",
            "ai ml",
            "artificial intelligence",
            "machine learning"
        ]

        course_keywords = [
            "syllabus",
            "course",
            "subject",
            "curriculum",
            "semester",
            "credits",
            "subjects"
        ]

        is_aiml_query = any(
            word in query_lower for word in aiml_keywords
        )

        is_course_query = any(
            word in query_lower for word in course_keywords
        )

        if is_aiml_query and is_course_query:

            selected = [
                doc for doc in self.documents
                if (
                    "btech cse (ai&ml) full syllabus.json"
                    in doc["source"].lower()
                )
            ]

            if selected:
                print("Document filter: CSE AIML course")
                return selected

        # General syllabus questions
        if "syllabus" in query_lower:

            selected = [
                doc for doc in self.documents
                if (
                    "syllabus" in doc["source"].lower()
                    and doc["source"].lower().endswith(".json")
                )
            ]

            if selected:
                print("Document filter: Syllabus JSON documents")
                return selected

        # Library questions
        if "library" in query_lower:

            selected = [
                doc for doc in self.documents
                if (
                    "library" in doc["source"].lower()
                    and doc["source"].lower().endswith(".json")
                )
            ]

            if selected:
                print("Document filter: Library JSON document")
                return selected

        # Admission questions
        if "admission" in query_lower:

            selected = [
                doc for doc in self.documents
                if (
                    "admission" in doc["source"].lower()
                    and doc["source"].lower().endswith(".json")
                )
            ]

            if selected:
                print("Document filter: Admission JSON documents")
                return selected

        # Default: search all documents
        return self.documents

    def rank_documents(self, query, documents):

        query_tokens = tokenize(query)

        if not query_tokens or not documents:
            return []

        tokenized_documents = [
            tokenize(document["content"])
            for document in documents
        ]

        bm25 = BM25Okapi(tokenized_documents)
        scores = bm25.get_scores(query_tokens)

        ranked = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True
        )

        return [
            (documents[index], float(scores[index]))
            for index in ranked
            if scores[index] > 0
        ]

    def search_admission_overview(self, query, documents, top_k):

        print("Admission search mode: Topic-based retrieval")

        topics = {

            "General admission rules": [
                "general instructions",
                "admissions to undergraduate programmes",
                "order of merit"
            ],

            "Application procedure": [
                "application procedure",
                "offline application form",
                "online application form"
            ],

           "Entrance examinations": [
            "chaitanya entrance test",
            "entrance test conducted by the university",
            "details of the entrance test",
            "entrance test is of 90 minutes duration",
            "total questions: 100",
            "declaration of cet result",
            "examination pattern for mba"
            ],

            "Eligibility": [
                "minimum qualification",
                "minimum eligibility criteria",
                "qualifying examination",
                "aggregate of 55%",
                "aggregate of 50%"
            ],

            "Reservation": [
                "15% of seats",
                "27% of the seats",
                "10% reservation in admissions",
            ],

            "Fee refund and cancellation": [
                "refund of fees/cancellation of admission",
                "refund will be made as per the norms of ugc",
                "ugc fee refund policy"
            ],

            "Foreign nationals": [
                "admission of foreign nationals",
                "foreign nationals will be admitted",
                "overseas citizen of india",
                "foreign country"
            ]
        }

        selected_results = []
        used_chunks = set()

        for topic, keywords in topics.items():

            matching = []

            # Search every selected admission chunk
            for document in documents:

                content = " ".join(
                    document["content"].lower().split()
                )

                matched_keywords = [
                    keyword
                    for keyword in keywords
                    if keyword in content
                ]

                if matched_keywords:

                    matching.append((
                        document,
                        len(matched_keywords)
                    ))

            # Prioritize chunks with more matching phrases
            matching.sort(
                key=lambda item: item[1],
                reverse=True
            )

            # Allow two chunks for entrance examinations
            if topic == "Entrance examinations":
                limit = 2
            elif topic == "Reservation":
                limit = 3
            else:
                limit = 1
            added = 0

            for document, keyword_count in matching:

                chunk_key = (
                    document["source"],
                    document.get("page_number"),
                    document["chunk_id"]
                )

                if chunk_key in used_chunks:
                    continue

                selected_results.append({
                    "source": document["source"],
                    "page_number": document.get("page_number"),
                    "chunk_id": document["chunk_id"],
                    "content": document["content"],
                    "score": float(keyword_count),
                    "topic": topic
                })

                used_chunks.add(chunk_key)
                added += 1

                if added >= limit:
                    break

            if added:
                print(
                    f"Selected topic: {topic} "
                    f"({added} chunk(s))"
                )

        return selected_results[:top_k]

    def search(self, query, top_k=5):

        query = query.strip().lower()

        # Ignore ordinary greetings
        greetings = {
            "hi",
            "hello",
            "hey",
            "hi synapse",
            "hello synapse",
            "good morning",
            "good afternoon",
            "good evening",
            "how are you"
        }

        if query in greetings:
            print("Normal conversation detected.")
            return []

        query_tokens = tokenize(query)

        if not query_tokens:
            return []

        # Select relevant documents
        candidate_documents = self.select_documents(query)

        if not candidate_documents:
            return []

        # Broad admission questions use topic-based retrieval
        broad_admission_terms = [
            "guideline",
            "guidelines",
            "rules",
            "regulations",
            "overview",
            "process",
            "procedure"
        ]

        is_broad_admission = (
            "admission" in query
            and any(
                term in query
                for term in broad_admission_terms
            )
        )

        if is_broad_admission:
            return self.search_admission_overview(
                query,
                candidate_documents,
                top_k
            )

        # Normal BM25 search
        ranked = self.rank_documents(
            query,
            candidate_documents
        )

        results = []

        for document, score in ranked[:top_k]:

            results.append({
                "source": document["source"],
                "page_number": document.get("page_number"),
                "chunk_id": document["chunk_id"],
                "content": document["content"],
                "score": score
            })

        return results


if __name__ == "__main__":

    search_engine = KnowledgeSearch()

    while True:

        query = input("\nAsk SYNAPSE (type exit to stop): ")

        if query.lower().strip() == "exit":
            break

        results = search_engine.search(query, top_k=8)

        if not results:
            print("\nNo relevant information found.")
            continue

        for index, result in enumerate(results, start=1):

            print(f"\nResult {index}")
            print(f"Source: {result['source']}")
            print(f"Page: {result['page_number']}")
            print(f"Chunk ID: {result['chunk_id']}")
            print(f"Score: {result['score']:.3f}")

            if "topic" in result:
                print(f"Topic: {result['topic']}")

            print(result["content"][:500])
