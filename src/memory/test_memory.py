
from src.memory.database import initialize_database
from src.memory.manager import (
    create_conversation,
    save_message,
    get_conversation_history,
    get_recent_conversations,
    get_recent_messages
)


print("Initializing database...")
initialize_database()

print("\nCreating conversation...")
conversation_id = create_conversation("First SYNAPSE Conversation")

print("Conversation ID:", conversation_id)

print("\nSaving messages...")

save_message(conversation_id, "user", "Hello SYNAPSE!")

save_message(
    conversation_id,
    "assistant",
    "Hello! How can I help you?"
)

print("Messages saved successfully!")

print("\nRetrieving conversation history...")

history = get_conversation_history(conversation_id)

for role, content, timestamp in history:
    print(f"{role}: {content}")

print("\nRecent conversations:")

for conversation in get_recent_conversations():
    print(conversation)

print("\nMemory test completed!")


print("\nLatest conversation messages:")

recent_messages = get_recent_messages(conversation_id, limit=5)

for role, content in recent_messages:
    print(f"{role}: {content}")

