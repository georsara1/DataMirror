# Use the Completion.create method with chat-style input
from openai import OpenAI

def _load_file(client, file_path):
    my_file = client.files.create(
        file=open(file_path, "rb"),
        purpose='assistants'
        )
    return my_file

def ask_gpt(file1_path, file2_path, prompt):        
    client = OpenAI()

    my_file1 = _load_file(client, file1_path)
    my_file2 = _load_file(client, file2_path)

    # my_file1 = client.files.create(
    #         file=open(file1_path, "rb"),
    #         purpose='assistants'
    #         )
    # my_file2 = client.files.create(
    #         file=open(file2_path, "rb"),
    #         purpose='assistants'
    #         )

    my_assistant = client.beta.assistants.create(
                    model="gpt-4o",
                    instructions="You are a data scientist whose role is to analyze data.",
                    name="Data John",
                    tools=[{"type": "code_interpreter"}],
                    tool_resources={ "code_interpreter": {"file_ids": [my_file1.id, my_file2.id]}}
                )
    
    my_thread = client.beta.threads.create()
    my_thread_message = client.beta.threads.messages.create(
                        thread_id=my_thread.id,
                        role="user",
                        content=(prompt)
                        )
    
    my_run = client.beta.threads.runs.create(
                thread_id=my_thread.id,
                assistant_id=my_assistant.id,
                )
    
    # Periodically retrieve the Run to check on its status to see if it has moved to completed
    while my_run.status in ["queued", "in_progress"]:
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=my_thread.id,
            run_id=my_run.id
        )
        print(f"Run status: {keep_retrieving_run.status}")

        if keep_retrieving_run.status == "completed":
            print("\n")

            # Retrieve the Messages added by the Assistant to the Thread
            all_messages = client.beta.threads.messages.list(
                thread_id=my_thread.id
            )

            print("------------------------------------------------------------ \n")

            print(f"User: {my_thread_message.content[0].text.value}")
            print(f"Assistant: {all_messages.data[0].content[0].text.value}")

            break
        elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
            pass
        else:
            print(f"Run status: {keep_retrieving_run.status}")
            break