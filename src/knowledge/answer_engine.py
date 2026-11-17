import re
from src.knowledge.search_engine import KnowledgeSearch
from src.llm.response import generate_response


class KnowledgeAnswerEngine:

    def __init__(self):

        print("Initializing SYNAPSE Knowledge Answer Engine...")

        self.search_engine = KnowledgeSearch()

        print("SYNAPSE Knowledge Answer Engine is ready!")

    def answer(self, user_question):

        # Step 1: Select retrieval count
        timing_keywords = [
            "timing",
            "timings",
            "opening time",
            "closing time",
            "library hours"
        ]

        if any(word in user_question.lower() for word in timing_keywords):
            top_k = 1
        else:
            top_k = 10

        # Step 2: Retrieve knowledge
        results = self.search_engine.search(
            user_question,
            top_k=top_k
        )

        # Step 3: Remove exact duplicate chunks
        seen_content = set()
        unique_results = []

        for result in results:

            content = result["content"].strip()

            normalized_content = " ".join(
                content.lower().split()
            )

            if normalized_content in seen_content:
                continue

            seen_content.add(normalized_content)
            unique_results.append(result)

        print(f"Retrieved chunks: {len(results)}")
        print(f"Unique chunks: {len(unique_results)}")

        print("\n--- RETRIEVED KNOWLEDGE CHUNKS ---")

        for index, result in enumerate(unique_results, start=1):
            print(f"\nCHUNK {index}")
            print("Source:", result["source"])
            print("Page:", result["page_number"])
            print("Content:", result["content"])
        # Step 4: Prepare knowledge context
        knowledge_context = ""

        MAX_CONTEXT_CHARS = 5500
        seen_sentences = set()

        for index, result in enumerate(unique_results, start=1):

            content = result["content"]

            # Split content into sentences
            sentences = re.split(r'(?<=[.!?])\s+', content)

            unique_sentences = []

            for sentence in sentences:
                sentence = sentence.strip()

                if not sentence:
                    continue

                normalized = " ".join(sentence.lower().split())

                if normalized not in seen_sentences:
                    seen_sentences.add(normalized)
                    unique_sentences.append(sentence)

            cleaned_content = " ".join(unique_sentences)

            document_text = (
                f"\nDocument {index}\n"
                f"Source File: {result['source']}\n"
                f"Page Number: {result['page_number']}\n"
                f"Content: {cleaned_content}\n"
            )

            remaining_chars = MAX_CONTEXT_CHARS - len(knowledge_context)

            if remaining_chars <= 0:
                break

            knowledge_context += document_text[:remaining_chars]

        # Step 5: Generate answer
        response = generate_response(
            user_text=user_question,
            knowledge_context=knowledge_context
        )

        # Step 6: Collect source references
        sources = []

        for result in unique_results:

            source_info = (
                f"{result['source']} "
                f"(Page {result['page_number']})"
            )

            if source_info not in sources:
                sources.append(source_info)

        # Step 7: Attach sources
        if sources:

            response += "\n\nSources:\n"

            for source in sources:
                response += f"- {source}\n"

        return response


if __name__ == "__main__":

    engine = KnowledgeAnswerEngine()

    while True:

        question = input("\nAsk SYNAPSE (type exit to stop): ")

        if question.lower().strip() == "exit":
            break

        print("\nSYNAPSE is thinking...")

        answer = engine.answer(question)

        print("\nSYNAPSE:", answer)
