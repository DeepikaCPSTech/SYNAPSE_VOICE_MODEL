from src.memory.database import initialize_database
from src.memory.manager import (
    create_conversation,
    save_message,
    get_chat_context
)

from src.llm.response import generate_response


print("Initializing SYNAPSE memory...")
initialize_database()


print("\nCreating test conversation...")

conversation_id = create_conversation("LLM Memory Test")


print("\nSaving conversation...")

save_message(
    conversation_id,
    "user",
    "My name is Alex."
)

save_message(
    conversation_id,
    "assistant",
    "Hello Alex! Nice to meet you."
)


print("\nRetrieving conversation from SQLite...")

history = get_chat_context(conversation_id)

print("Retrieved memory:", history)


print("\nAsking SmolLM2 using retrieved memory...")

answer = generate_response(
    "What is my name?",
    chat_history=history
)

print("\nSYNAPSE:", answer)

print("\nSQLite + LLM memory test completed!")