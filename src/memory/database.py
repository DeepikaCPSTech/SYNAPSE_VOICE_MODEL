
from pathlib import Path
import sqlite3


# Project directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Database storage directory
DATA_DIR = BASE_DIR / "data" / "memory"

# SQLite database file
DATABASE_PATH = DATA_DIR / "synapse_memory.db"


def get_connection():

    # Create the database directory if it doesn't exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    # Enable foreign key support
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # Store conversation sessions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Store individual conversation messages
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (conversation_id)
                REFERENCES conversations(id)
                ON DELETE CASCADE
            )
        """)

                # Store long-term personal facts
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fact_key TEXT NOT NULL UNIQUE,
                fact_value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()

        print("SYNAPSE memory database initialized successfully!")

    finally:

        connection.close()


if __name__ == "__main__":
    initialize_database()
