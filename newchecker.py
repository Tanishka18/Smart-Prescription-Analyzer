import pytesseract
from PIL import Image
import re
import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

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
    text = pytesseract.image_to_string(img)
    return text

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

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(
    title="Select Prescription Image",
    filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
)

if file_path:
    drugs_csv = "C:/Users/aadya/Desktop/ocr/drugs.csv"
    ddi_csv = "C:/Users/aadya/Desktop/ocr/ddi_pairs/db_drug_interactions.csv"

    drug_list = load_all_drug_names(drugs_csv)
    ddi_database = load_ddi_pairs(ddi_csv)

    ocr_text = extract_text_from_image(file_path)
    drugs_found = extract_drug_names(ocr_text, drug_list)
    risky_pairs = check_ddi(drugs_found, ddi_database)

    print("OCR Output:\n", ocr_text)
    print("Detected Drugs:", drugs_found)
    print("Risky Drug Pairs (DDIs):", risky_pairs if risky_pairs else "None found")
else:
    print("No file selected.")
