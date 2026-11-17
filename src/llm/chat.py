from model import load_llm


def start_chat():

    llm = load_llm()

    messages = [
        {
            "role": "system",
            "content": "You are SYNAPSE, a helpful offline voice assistant. Give simple, clear and short answers."
        }
    ]

    print("\nSYNAPSE Chat Started!")
    print("Type 'exit' to stop.\n")

    while True:

        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("SYNAPSE: Goodbye!")
            break

        if not user_input:
            continue

        messages.append({
            "role": "user",
            "content": user_input
        })

        response = llm.create_chat_completion(
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )

        answer = response["choices"][0]["message"]["content"]

        print("\nSYNAPSE:", answer, "\n")

        messages.append({
            "role": "assistant",
            "content": answer
        })


if __name__ == "__main__":
    start_chat()