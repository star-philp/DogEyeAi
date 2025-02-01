# dataset_download.py

import requests
from zipfile import ZipFile
from pathlib import Path

# Define the URL and local file paths
url = 'https://github.com/kairess/toy-datasets/raw/master/dog-inflammation.zip'
local_filename = 'dog-inflammation.zip'
extracted_folder = '/Users/rainstar/Project/Python/DogAI/dog_inflammation'
#/Users/rainstar/Project/Python/DogAI/dog_inflammation/dog-inflammation/negative
# Download the dataset
print("Downloading dataset...")
response = requests.get(url)
with open(local_filename, 'wb') as file:
    file.write(response.content)
print("Download complete.")

# Extract the dataset
print("Extracting dataset...")
with ZipFile(local_filename, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder)
print("Extraction complete.")
