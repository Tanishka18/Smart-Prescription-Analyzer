import pandas as pd
import json

# Load the JSON file
file_path = r'drug-labels/drug-label-0001-of-0013.json'

with open(file_path, 'r') as f:
    data = json.load(f)

# Extract the list of drug records
records = data['results']

# Flatten nested fields if necessary
df = pd.read_json(file_path)
df=pd.json_normalize(records)
# Save to CSV
df.to_csv('output1.csv', index=False)

