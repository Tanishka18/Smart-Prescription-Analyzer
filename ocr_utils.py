import pytesseract
from PIL import Image
import re
import os
import pandas as pd
import platform

# Detect platform and set tesseract path only for Windows
if platform.system() == 'Windows':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    tesseract_path = os.path.join(base_dir, "tesseract", "tesseract.exe")
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

def load_all_drug_names(csv_path):
    df = pd.read_csv(csv_path)
    if 'Drug Name' not in df.columns:
        raise ValueError("CSV must contain a column named 'Drug Name'")
    drug_names = df['Drug Name'].dropna().str.strip().str.title().unique().tolist()
    return drug_names

def load_ddi_pairs(csv_path):
    df = pd.read_csv(csv_path)
    df['Drug 1'] = df['Drug 1'].str.strip().str.title()
    df['Drug 2'] = df['Drug 2'].str.strip().str.title()
    return list(zip(df['Drug 1'], df['Drug 2']))

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    return pytesseract.image_to_string(img)

def extract_drug_names(text, drug_list):
    found = []
    for drug in drug_list:
        if re.search(rf"\b{re.escape(drug)}\b", text, re.IGNORECASE):
            found.append(drug)
    return found

def check_ddi(drugs_found, ddi_database):
    risky_pairs = []
    for i in range(len(drugs_found)):
        for j in range(i + 1, len(drugs_found)):
            pair = (drugs_found[i], drugs_found[j])
            reverse_pair = (drugs_found[j], drugs_found[i])
            if pair in ddi_database or reverse_pair in ddi_database:
                risky_pairs.append(pair)
    return risky_pairs
