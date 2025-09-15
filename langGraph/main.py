# main.py
from chatbot import ask_chatbot

while True:
    user_input = input("\n🧑 Ask a question (or type 'exit'): ")
    if user_input.lower() in ["exit", "quit"]:
        break

    response = ask_chatbot(user_input)
    print("\n📄 Result:\n", response)
    