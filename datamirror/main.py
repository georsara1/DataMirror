import os
import sys
from openai import OpenAI
import pandas as pd
import json

# Set your OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")  # Or replace with your API key directly

def read_file(file_path):
    """
    Summarize a dataset to provide input for the LLM.
    Includes dataset name, size, columns, and a sample.
    """
    try:
        # Load the dataset
        data = pd.read_csv(file_path)
        
        json_df = data.to_json()
        return json_df
        
    except Exception as e:
        return f"Error preparing dataset summary for {file_path}: {e}"

def query_llm():
    """
    Query the LLM with the provided prompt and return the response.
    Uses the updated openai.Completion API with 'messages' for Chat-style interaction.
    """
    try:
        # Use the Completion.create method with chat-style input
        client = OpenAI()
        
        my_file1 = client.files.create(
                file=open("/Users/georsara11/Desktop/python/DataMirror/data/data1.csv", "rb"),
                purpose='assistants'
                )
        my_file2 = client.files.create(
                file=open("/Users/georsara11/Desktop/python/DataMirror/data/data2.csv", "rb"),
                purpose='assistants'
                )
        # print(f"This is the file object: {my_file} \n")

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
        
        # Step 6: Periodically retrieve the Run to check on its status to see if it has moved to completed
        while my_run.status in ["queued", "in_progress"]:
            keep_retrieving_run = client.beta.threads.runs.retrieve(
                thread_id=my_thread.id,
                run_id=my_run.id
            )
            print(f"Run status: {keep_retrieving_run.status}")

            if keep_retrieving_run.status == "completed":
                print("\n")

                # Step 7: Retrieve the Messages added by the Assistant to the Thread
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

        # completion = client.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": "You are a data scientist whose role is to analyze data"},
        #         {
        #             "role": "user",
        #             "content": {prompt}
        #         }
        #     ]
        # )

        # print(completion.choices[0].message)
    except Exception as e:
        return f"An error occurred with the OpenAI API: {e}"

if __name__ == "__main__":
    # # Ensure correct arguments
    # if len(sys.argv) != 3:
    #     print("Usage: python main.py <file1.csv> <file2.csv>")
    #     sys.exit(1)
    
    # file1, file2 = sys.argv[1], sys.argv[2]

    # # Ensure both files exist
    # if not os.path.exists(file1) or not os.path.exists(file2):
    #     print("One or both of the specified files do not exist.")
    #     sys.exit(1)

    # Prepare dataset summaries
    # data1 = read_file(file1)
    # data2 = read_file(file2)

    # Combine summaries and create a prompt for the LLM
    prompt = """
    The two uploaded datasets represent two snapshots of the same data in different points in time. Can you please tell me how the data has changed?

    For example, provide insights on:
    - Any differences in columns (names, types)
    - Differences in numerical columns (e.g. distribution shifts)
    - Differences in categorical variables after performing a value count

    I dont want extensive analysis, only the major differences.
    """
    
    # Query the LLM
    result = query_llm()

    # Display the result
    print("\n### Analysis Result ###")
    print(result)
