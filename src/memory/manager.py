
from src.memory.database import get_connection


def create_conversation(title="New Conversation"):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO conversations (title) VALUES (?)",
            (title,)
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()


def save_message(conversation_id, role, content):

    if role not in ("user", "assistant", "system"):
        raise ValueError("Invalid message role")

    if not content or not content.strip():
        raise ValueError("Message content cannot be empty")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO messages
            (conversation_id, role, content)
            VALUES (?, ?, ?)
            """,
            (conversation_id, role, content)
        )

        connection.commit()

    finally:
        connection.close()


def get_conversation_history(conversation_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT role, content, created_at
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id ASC
            """,
            (conversation_id,)
        )

        return cursor.fetchall()

    finally:
        connection.close()


def get_recent_conversations(limit=10):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, title, created_at
            FROM conversations
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        return cursor.fetchall()

    finally:
        connection.close()


def get_recent_messages(conversation_id, limit=10):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT role, content
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (conversation_id, limit)
        )

        messages = cursor.fetchall()

        # Reverse to restore chronological order
        return list(reversed(messages))

    finally:
        connection.close()


def get_chat_context(conversation_id, limit=10):

    messages = get_recent_messages(conversation_id, limit)

    chat_context = []

    for role, content in messages:

        chat_context.append({
            "role": role,
            "content": content
        })

    return chat_context



def save_fact(fact_key, fact_value):
    """Save or update a long-term memory fact."""

    if not fact_key or not fact_key.strip():
        raise ValueError("Fact key cannot be empty")

    if not fact_value or not fact_value.strip():
        raise ValueError("Fact value cannot be empty")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO user_facts (fact_key, fact_value)
            VALUES (?, ?)
            ON CONFLICT(fact_key)
            DO UPDATE SET
                fact_value = excluded.fact_value,
                updated_at = CURRENT_TIMESTAMP
            """,
            (fact_key.strip(), fact_value.strip())
        )

        connection.commit()

    finally:
        connection.close()


def get_all_facts():
    """Retrieve all long-term memory facts."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT fact_key, fact_value
            FROM user_facts
            ORDER BY fact_key
            """
        )

        return cursor.fetchall()

    finally:
        connection.close()


def get_fact(fact_key):
    """Retrieve one specific fact."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT fact_value
            FROM user_facts
            WHERE fact_key = ?
            """,
            (fact_key,)
        )

        result = cursor.fetchone()

        return result[0] if result else None

    finally:
        connection.close()

