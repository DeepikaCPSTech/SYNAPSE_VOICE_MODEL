
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parents[2]

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.memory.manager import get_all_facts
from src.llm.model import load_llm


# Load local SmolLM2
llm = load_llm()


# SYNAPSE system instructions
SYSTEM_PROMPT = (
    "You are SYNAPSE, a helpful offline university assistant. "
    "Answer the user's exact question using the retrieved knowledge context. "
    "Read all provided context before answering. "
    "For broad questions, summarize all relevant topics, "
    "not just the first document or paragraph. "
    "Identify different topics and combine related information. "
    "For admission guideline questions, organize information under "
    "General Rules, Application Procedure, Eligibility, "
    "Entrance Examination, Reservation, Fee Refund, "
    "and Foreign Nationals whenever the information is available. "
    "Include important numbers, percentages, durations, and conditions. "
    "Do not omit relevant information from later documents. "
    "Do not repeat the same fact or sentence. "
    "Do not generate duplicate bullet points. "
    "For specific questions, provide only relevant details. "
    "Use simple English and clear bullet points. "
    "Never invent missing information. "
    "If information is incomplete, clearly mention it. "
    "Give natural answers suitable for speech."
)


def generate_response(
    user_text,
    chat_history=None,
    knowledge_context=None
):

    if not user_text or not user_text.strip():
        return "I didn't hear anything. Please try again."

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # Load saved personal memory
    facts = get_all_facts()

    if facts:

        memory_text = "\n".join(
            f"{key}: {value}"
            for key, value in facts
        )

        messages.append({
            "role": "system",
            "content": (
                "Saved information about the user:\n"
                + memory_text
            )
        })

    # Add retrieved knowledge
    if knowledge_context:

        messages.append({
            "role": "system",
            "content": (
                "Retrieved information from the SYNAPSE "
                "university knowledge database follows. "
                "Use all relevant sections when answering. "
                "Treat this information as the source of truth:\n\n"
                + knowledge_context
            )
        })

    # Add conversation history
    if chat_history:

        for message in chat_history:

            messages.append({
                "role": message["role"],
                "content": message["content"]
            })

    # Add current question
    messages.append({
        "role": "user",
        "content": user_text
    })

    # Generate response using local SmolLM2
    response = llm.create_chat_completion(
        messages=messages,
        max_tokens=450,
        temperature=0.3
    )

    answer = response["choices"][0]["message"]["content"]

    return answer.strip()
