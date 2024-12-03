# Use the Completion.create method with chat-style input
from openai import OpenAI

def ask_gpt(file1_path, file2_path):        
    client = OpenAI()
        
    my_file1 = client.files.create(
            file=open(file1_path, "rb"),
            purpose='assistants'
            )
    my_file2 = client.files.create(
            file=open(file2_path, "rb"),
            purpose='assistants'
            )

    prompt = """
        The two uploaded datasets represent two snapshots of the same data in different points in time. Can you please tell me how the data has changed?

        For example, provide insights on:
        - Any differences in columns (names, types). Only comment if a difference is actually found.
        - Differences in numerical columns (e.g. distribution shifts between the first and second dataset).
        - Differences in categorical variables after performing a value count. Do not give me the actual value counts, give me a comment on what is more
        or less the same and what has changed (e.g. some categories disappear or new categories appear - and if so, which ones specifically). 
        The order of appearence of the categories does not qualify as a change.

        Please do not return any graphs, figures, images or any kind of visuallization.
    """

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
                        content=prompt
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