import requests
import json
import pandas as pd
import pickle
import os

def download_notebook_from_url(url, local_path):
    """Download a notebook from a URL (GitHub, Google Colab, etc.)"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        with open(local_path, 'w') as f:
            f.write(response.text)
        
        return True
    except Exception as e:
        print(f"Error downloading notebook: {e}")
        return False

def extract_code_from_notebook(notebook_path):
    """Extract Python code from a Jupyter notebook"""
    with open(notebook_path, 'r') as f:
        notebook = json.load(f)
    
    code_cells = []
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            code_cells.append(''.join(cell['source']))
    
    return code_cells

def load_notebook_outputs(notebook_path):
    """Extract outputs from notebook cells"""
    with open(notebook_path, 'r') as f:
        notebook = json.load(f)
    
    outputs = []
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code' and 'outputs' in cell:
            outputs.append(cell['outputs'])
    
    return outputs

# Example usage functions
def download_colab_notebook(colab_url, local_path):
    """Download from Google Colab"""
    # Convert Colab URL to raw format
    if 'colab.research.google.com' in colab_url:
        # Extract file ID and convert to raw download URL
        file_id = colab_url.split('/')[-1].split('#')[0]
        raw_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        return download_notebook_from_url(raw_url, local_path)
    
    return download_notebook_from_url(colab_url, local_path)

def download_github_notebook(github_url, local_path):
    """Download from GitHub"""
    # Convert GitHub URL to raw format
    if 'github.com' in github_url:
        raw_url = github_url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
        return download_notebook_from_url(raw_url, local_path)
    
    return download_notebook_from_url(github_url, local_path)

def save_processed_data(data, filename):
    """Save processed data from notebook"""
    if isinstance(data, pd.DataFrame):
        data.to_csv(f"data_processed/{filename}.csv", index=False)
    else:
        with open(f"data_processed/{filename}.pkl", 'wb') as f:
            pickle.dump(data, f)

def load_processed_data(filename, data_type='csv'):
    """Load processed data"""
    if data_type == 'csv':
        return pd.read_csv(f"data_processed/{filename}.csv")
    else:
        with open(f"data_processed/{filename}.pkl", 'rb') as f:
            return pickle.load(f)