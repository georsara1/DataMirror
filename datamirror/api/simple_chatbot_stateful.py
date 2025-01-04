"""
This script demonstrates how to create a stateful chatbot using the OpenAI API.
The chatbot will remember the conversation history and generate responses based on it.
"""
from openai import OpenAI
client = OpenAI()

# Initialize an empty message history
message_history = [
    {
        "role": "system", 
        "content": "You are a helpful assistant."}
]

def chatbot(user_input):
    message_history.append({"role": "user", "content": user_input})

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=message_history
    )
        # Extract and save the assistant's reply
    assistant_reply = completion.choices[0].message.content
    message_history.append({"role": "assistant", "content": assistant_reply})

    # print(completion.choices[0].message)
    return assistant_reply

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    reply = chatbot(user_input)
    print("Bot:", reply)