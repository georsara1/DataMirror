from api.openai_client import ask_gpt

if __name__ == "__main__":
    try:
        file1_path = "/Users/georsara11/Desktop/python/DataMirror/data/data1.csv"
        file2_path = "/Users/georsara11/Desktop/python/DataMirror/data/data2.csv"
        response = ask_gpt(file1_path, file2_path)
    except Exception as e:
        print(f"An error occurred with the OpenAI API: {e}")
