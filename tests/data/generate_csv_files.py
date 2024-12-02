import pandas as pd
import random
import os

# Set a seed for reproducibility
SEED = 42
random.seed(SEED)

# Function to generate a dataset
def generate_dataset(num_rows, columns, file_name):
    """
    Generate a dataset with specified columns and save it to a CSV file.
    """
    data = {}
    for column_name, column_type in columns.items():
        if column_type == 'categorical':
            data[column_name] = [random.choice(['A', 'B', 'C', 'D']) for _ in range(num_rows)]
        elif column_type == 'numerical':
            data[column_name] = [random.uniform(1, 100) for _ in range(num_rows)]
    
    # Create a DataFrame and save it as CSV
    df = pd.DataFrame(data)
    df.to_csv(file_name, index=False)
    print(f"Generated {file_name} with {num_rows} rows and {len(columns)} columns.")

# Define columns for the two datasets
columns_file1 = {
    'Category1': 'categorical',
    'Category2': 'categorical',
    'Category3': 'categorical',
    'Value1': 'numerical',
    'Value2': 'numerical'
}

columns_file2 = {
    'Category1': 'categorical',  # Same as in file1
    'Category2': 'categorical',  # Same as in file1
    'Group': 'categorical',      # Different from file1
    'Value1': 'numerical',       # Same as in file1
    'Score': 'numerical'         # Different from file1
}

# Generate the datasets
generate_dataset(500, columns_file1, 'data1.csv')
generate_dataset(600, columns_file2, 'data2.csv')
