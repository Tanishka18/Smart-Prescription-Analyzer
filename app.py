from flask import Flask, request, render_template, redirect, url_for
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from ocr_utils import extract_text_from_image, load_all_drug_names, load_ddi_pairs, extract_drug_names, check_ddi
from datetime import datetime



app = Flask(__name__)
CORS(app)  # Allow frontend JS to access Flask API

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load data once
drug_list = load_all_drug_names('drugs.csv')
ddi_database = load_ddi_pairs('db_drug_interactions.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/results')
def results():
    return render_template('result.html')

@app.route('/analyze', methods=['POST'])
def analyze_prescription():
    print(">>> Analyze route hit")

    if 'prescription' not in request.files:
        print(">>> No 'prescription' in request.files")
        return render_template('result.html', error='No prescription uploaded.')

    file = request.files['prescription']
    filename = secure_filename(file.filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(image_path)
    print(f">>> File saved to: {image_path}")

    try:
        text = extract_text_from_image(image_path)
        print(">>> OCR Text:", text)

        found_drugs = extract_drug_names(text, drug_list)
        print(">>> Extracted drugs:", found_drugs)

        risky_pairs = check_ddi(found_drugs, ddi_database)
        print(">>> Risky pairs:", risky_pairs)

        return render_template('result.html',
                               success=True,
                               text=text,
                               extracted_medicines=found_drugs,
                               warnings=[f"{a} and {b}" for a, b in risky_pairs],
                               current_date=datetime.now().strftime('%B %d, %Y'),
                                image_filename=filename)
    
    except Exception as e:
        print(">>> Exception occurred:", str(e))
        return render_template('result.html', error=str(e))


if __name__ == '__main__':
    app.run(debug=True)
