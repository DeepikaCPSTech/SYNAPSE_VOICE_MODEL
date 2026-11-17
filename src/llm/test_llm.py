from model import load_llm


def test_llm():

    llm = load_llm()

    print("\nAsking SYNAPSE a question...\n")

    response = llm.create_chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are SYNAPSE, a helpful offline voice assistant. Give simple and clear answers."
            },
            {
                "role": "user",
                "content": "Hello! Introduce yourself in two sentences."
            }
        ],
        max_tokens=100,
        temperature=0.7
    )

    answer = response["choices"][0]["message"]["content"]

    print("SYNAPSE:", answer)


if __name__ == "__main__":
    test_llm()