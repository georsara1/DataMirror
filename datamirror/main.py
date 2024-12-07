import argparse
from api.openai_client import ask_gpt

if __name__ == "__main__":
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

    # Add a document parser for custom user prompts
    parser = argparse.ArgumentParser(description="Dataset Comparison")
    parser.add_argument("--prompt", default=prompt, help = "user-defined prompt for data analysis")

    # Parse arguments
    args = parser.parse_args()

    # Use custom prompt or fallback to default one
    prompt = args.prompt
    
    try:
        file1_path = "/Users/georsara11/Desktop/python/DataMirror/data/data1.csv"
        file2_path = "/Users/georsara11/Desktop/python/DataMirror/data/data2.csv"
        response = ask_gpt(file1_path, file2_path, prompt)
    except Exception as e:
        print(f"An error occurred with the OpenAI API: {e}")
