"""
This script demonstrates how to create a stateful chatbot using the Assistants OpenAI API
(currently in beta version). The chatbot will remember the conversation history and generate
responses based on it.
""" 

# Importing required packages
import streamlit as st
import time
from openai import OpenAI

# load files for assistant api
def _load_file(client, file_path):
    my_file = client.files.create(
        file=open(file_path, "rb"),
        purpose='assistants'
        )
    return my_file

# Set openAi client , assistant ai and assistant ai thread
def load_openai_client_and_assistant(file1_path, file2_path):
    client          = OpenAI()

    my_file1 = _load_file(client, file1_path)
    my_file2 = _load_file(client, file2_path)

    my_assistant    = client.beta.assistants.create(
                        model="gpt-4o",
                        instructions="You are a data scientist whose role is to analyze data.",
                        name="Data John",
                        tools=[{"type": "code_interpreter"}],
                        tool_resources={ "code_interpreter": {"file_ids": [my_file1.id, my_file2.id]}}
                    )
    thread          = client.beta.threads.create()

    return client , my_assistant, thread


# check in loop  if assistant ai parse our request
def wait_on_run(my_run, my_thread):
    while my_run.status in ["queued", "in_progress"]:
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=my_thread.id,
            run_id=my_run.id
        )
        print(f"Run status: {keep_retrieving_run.status}")
        time.sleep(2)

        if keep_retrieving_run.status == "completed":
            print("\n")

            # Retrieve the Messages added by the Assistant to the Thread
            all_messages = client.beta.threads.messages.list(
                thread_id=my_thread.id
            )

            print("------------------------------------------------------------ \n")

            # print(f"User: {my_thread_message.content[0].text.value}")
            # print(f"Assistant: {all_messages.data[0].content[0].text.value}")

            break
        elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
            pass
        else:
            print(f"Run status: {keep_retrieving_run.status}")
            break
    return my_run

# initiate assistant ai response
def get_assistant_response(user_input=""):

    message = client.beta.threads.messages.create(
        thread_id=assistant_thread.id,
        role="user",
        content=user_input,
    )
    
    run = client.beta.threads.runs.create(
        thread_id=assistant_thread.id,
        assistant_id=my_assistant.id,
    )

    run = wait_on_run(run, assistant_thread)

    # Retrieve all the messages added after our last user message
    messages = client.beta.threads.messages.list(
        thread_id=assistant_thread.id, order="asc", after=message.id
    )
    print(messages.data[0].content[0].text.value)
    return messages.data[0].content[0].text.value

# Run the Assistant
file1_path = "/Users/georsara11/Desktop/python/DataMirror/data/data1.csv"
file2_path = "/Users/georsara11/Desktop/python/DataMirror/data/data2.csv"

client, my_assistant, assistant_thread = load_openai_client_and_assistant(file1_path, file2_path)

if 'user_input' not in st.session_state:
    st.session_state.user_input = ''

def submit():
    st.session_state.user_input = st.session_state.query
    st.session_state.query = ''



st.title("Data John is here to help you!")

st.text_input("Play with me:", key='query', on_change=submit)

user_input = st.session_state.user_input

st.write("You entered: ", user_input)

if user_input:
    result = get_assistant_response(user_input)
    st.header('Assistant:')
    st.text(result)