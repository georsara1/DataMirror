"""
This is a simple chatbot that uses OpenAI's GPT-4 model to generate responses.
The connection is stateless, meaning that the chatbot does not remember the conversation history.
"""
from openai import OpenAI
client = OpenAI()

def chatbot(prompt):
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system", 
                "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    reply = chatbot(user_input)
    print("Bot:", reply)