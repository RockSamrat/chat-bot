from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import sys
import time

template = """
Answer the question below.
Here is the conversation history: {context}
Question: {question}
Answer:
"""

model = OllamaLLM(model="llama3.2", streaming=True)
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


def conversation():
    context = ""
    print("\nWelcome to AI Chatbot! Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("You: ")
        except KeyboardInterrupt:
            # handles Ctrl+C gracefully instead of crashing
            print("\nGoodbye!")
            break

        if user_input.strip() == "":
            print("Bot: Please type something!\n")
            continue

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        try:
            print("Bot: ", end="", flush=True)

            full_response = ""
            start_time = time.time()  # start the timer before bot replies

            for chunk in chain.stream({"context": context, "question": user_input}):
                sys.stdout.write(chunk)
                sys.stdout.flush()
                full_response += chunk

            end_time = time.time()  # stop the timer after full reply
            elapsed = end_time - start_time

            print()  # newline after response ends
            print(f"  (responded in {elapsed:.2f}s)\n")  # show time taken

            context += f"\nUser: {user_input}\nAI: {full_response}"

        except ConnectionError:
            print("\nError: Could not connect to Ollama. Is it running?\n")

        except Exception as e:
            print(f"\nSomething went wrong: {e}\n")


if __name__ == "__main__":
    conversation()