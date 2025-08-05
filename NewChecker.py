import pytesseract
from PIL import Image
import re
import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

def load_all_drug_names(csv_path):
    """Load and clean all drug names from a CSV file."""
    df = pd.read_csv(csv_path)
    if 'Drug Name' not in df.columns:
        raise ValueError("CSV must contain a column named 'Drug Name'")

    drug_names = (df['Drug Name']
                  .dropna()
                  .str.replace('.', '', regex=False) 
                  .str.strip()                       
                  .str.title()                       
                  .unique()                          
                  .tolist())

    drug_names = [name for name in drug_names if name]
    return drug_names

def load_ddi_pairs(csv_path):
    """Load and clean drug-drug interaction pairs from a CSV file."""
    df = pd.read_csv(csv_path)
    df['Drug 1'] = df['Drug 1'].str.replace('.', '', regex=False).str.strip().str.title()
    df['Drug 2'] = df['Drug 2'].str.replace('.', '', regex=False).str.strip().str.title()
    return list(zip(df['Drug 1'], df['Drug 2']))

def extract_text_from_image(image_path):
    """Extract text from an image using Tesseract OCR."""
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return ""

def extract_drug_names(text, drug_list):
    """Find all drug names from the master list within the OCR text."""
    found = set() 
    for drug in drug_list:
        if re.search(rf"\b{re.escape(drug)}\b", text, re.IGNORECASE):
            found.add(drug)
    return sorted(list(found)) 

def check_ddi(drugs_found, ddi_database):
    """Check for known dangerous interactions between the found drugs."""
    risky_pairs = []
    ddi_set = {frozenset(pair) for pair in ddi_database}
    
    for i in range(len(drugs_found)):
        for j in range(i + 1, len(drugs_found)):
            pair_to_check = frozenset([drugs_found[i], drugs_found[j]])
            if pair_to_check in ddi_set:
                risky_pairs.append((drugs_found[i], drugs_found[j]))
    return risky_pairs

root = tk.Tk()
root.withdraw() 
file_path = filedialog.askopenfilename(
    title="Select Prescription Image",
    filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
)

if file_path:
    drugs_csv = "C:/Users/aadya/Desktop/ocr/drugs.csv"
    ddi_csv = "C:/Users/aadya/Desktop/ocr/ddi_pairs/db_drug_interactions.csv"
    
    try:
        drug_list = load_all_drug_names(drugs_csv)
        ddi_database = load_ddi_pairs(ddi_csv)

        ocr_text = extract_text_from_image(file_path)
        drugs_found = extract_drug_names(ocr_text, drug_list)
        risky_pairs = check_ddi(drugs_found, ddi_database)

        print("="*40)
        print("📄 OCR Text Extracted from Image:")
        print("="*40)
        print(ocr_text)
        print("\n" + "="*40)
        print("💊 Detected Drugs:")
        print("="*40)
        print(drugs_found if drugs_found else "None detected.")
        print("\n" + "="*40)
        print("⚠️ Potentially Dangerous Interactions (DDIs):")
        print("="*40)
        print(risky_pairs if risky_pairs else "None found ✅")
        print("="*40)

    except FileNotFoundError as e:
        print(f"❌ ERROR: A data file could not be found. Please check the path.\n{e}")
    except ValueError as e:
        print(f"❌ ERROR: A problem occurred with a CSV file.\n{e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

else:
    print("❌ No file selected. Program terminated.")
