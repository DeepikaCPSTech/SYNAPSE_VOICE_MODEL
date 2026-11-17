
import re

from src.memory.manager import save_fact


def extract_and_save_facts(user_text):
    """
    Detect and save basic personal facts.
    """

    text = user_text.strip()
    saved_facts = []

    patterns = {
        "name": [
            r"\bmy name is\s+([A-Za-z][A-Za-z ]{0,40})",
            r"\bcall me\s+([A-Za-z][A-Za-z ]{0,40})"
        ],
        "college": [
            r"\bi study at\s+(.+)",
            r"\bmy college is\s+(.+)"
        ],

        "education": [
            r"\bi am studying\s+(.+)",
            r"\bi study (?!at\b)(.+)",
            r"\bmy branch is\s+(.+)",
            r"\bmy course is\s+(.+)"
        ],

        "skills": [
            r"\bmy skills are\s+(.+)",
            r"\bi know\s+(.+)"
        ],
        "interests": [
            r"\bi am interested in\s+(.+)",
            r"\bi like\s+(.+)"
        ]
    }

    for fact_key, fact_patterns in patterns.items():

        for pattern in fact_patterns:

            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                value = match.group(1).strip()
                value = re.sub(r"[.!?,;]+$", "", value).strip()

                if value:
                    save_fact(fact_key, value)
                    saved_facts.append((fact_key, value))
                    break

    if saved_facts:
        return saved_facts

    return None
