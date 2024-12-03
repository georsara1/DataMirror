# **DataMirror**

---

## **DataMirror**: An Intelligent Dataset Comparison Tool

![DataMirror Logo](web_app/static/datamirror_logo.webp)

DataMirror is a Python-based application designed to leverage Large Language Models (LLMs) like OpenAI’s GPT to analyze and compare datasets. The application empowers users to gain insights into the differences between two datasets without requiring manual analysis or complex data wrangling. 

---

## **Key Features**

1. **Multiple Interaction Methods**:
   - **Command-Line Interface (CLI)**: Compare two datasets programmatically via scripts.
   - **Jupyter Notebook Integration**: Perform and save analysis interactively with rich visualizations and outputs.
   - **Web Interface**: An easy-to-use Flask-powered web application to upload datasets and view insights in a browser.

2. **Automatic Analysis with LLMs**:
   - Provides insights into dataset structure, size, column differences, and summary statistics.
   - Customizable prompts for deep comparative analysis.
   - Eliminates the need for explicit coding of comparison functions.

3. **Flexible Data Formats**:
   - Accepts `.csv` files for dataset inputs.
   - Processes datasets into structured summaries for efficient analysis by LLMs.

4. **Reproducible Randomized Datasets**:
   - A utility script to generate sample datasets for testing and demonstration purposes.

---

## **Project Structure**

```plaintext
DataMirror/
│
├── app/                         # Core application code
│   ├── main.py                  # Entry point for CLI-based dataset comparison
│   ├── utils/                   # Utility scripts
│       ├── data_generation.py   # Generate sample datasets
│       ├── llm_helpers.py       # Interact with the LLM
│
├── data/                        # Default folder for storing datasets
│   ├── sample_file1.csv
│   ├── sample_file2.csv
│
├── notebooks/                   # Jupyter notebooks for interactive analysis
│   ├── dataset_comparison.ipynb
│
├── web/                         # Web application code
│   ├── app.py                   # Flask app for web-based interface
│   ├── templates/               # HTML templates for the Flask app
│   ├── static/                  # Static assets (CSS, JS, images)
│
├── tests/                       # Unit and integration tests
│
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
├── LICENSE                      # Project license
└── venv/                        # Virtual environment (if local)
```
---

## **Getting Started**

### Prerequisites
- Python 3.12 or later
- OpenAI API key (for LLM functionality)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/DataMirror.git
   cd DataMirror
   ```
2. Set up the virtual environment:
   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
   ```
3. Add your OPENAI API key:
    - Create an environment variable OPENAI_API_KEY or update the application configuration.

---

## Usage
### Command-Line interface
Run the application:
   ```bash
   python main.py
   ```
### Jupyter notebook
  - Open notebooks/dataset_comparison.ipynb in Jupyter Lab.
  - Follow the instructions to upload datasets and view results interactively.

### Web Interface
[to be defined]

---

## Example outcomes
### 1. Command-line

Assistant: 
### Observations:

#### Numerical Columns (`Value1` and `Value2`):
- **`Value1`:**
  - The mean has decreased slightly from the first to the second dataset.
  - The standard deviation has slightly increased, indicating a marginally wider spread of values in the second dataset.
  - The minimum remains quite close, but the maximum remains the same.
  
- **`Value2`:**
  - There is a decrease in the mean from the first to the second dataset.
  - The standard deviation has increased, suggesting a wider spread in the second dataset.
  - The minimum is slightly lower, and the maximum has significantly increased in the second dataset, showing a potential outlier or high-value record was added.

#### Categorical Columns (`Category1`, `Category2`, `Category3`):

- **Category1:**
  - A new category "E" appears in the second dataset with a small count. This category was not present in the first dataset.
  - Other categories (A, B, C, D) remain, though their counts have changed slightly.

- **`Category2`:**
  - There are no new or disappearing categories in the second dataset compared to the first. The distribution of counts among the categories has changed slightly, but the categories themselves remain the same (A, B, C, D).

- **`Category3`:**
  - Similar to `Category2`, there are no new or disappearing categories. The existing categories (A, B, C, D) have changed slightly in their distribution of counts.

Overall, the second dataset contains one new category in `Category1`, a shift in the distributions of numerical columns, particularly in `Value2`, suggesting possible changes in data collection or processing between the two periods.

### 2. Jupyter notebook
[tbd]

### 3. Web interface
[tbd]

---

## License
This project is licenced under the Apache 2.0 license
