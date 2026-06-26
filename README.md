# 🎯 AI Resume Matcher

> An AI-powered tool that compares resumes with job descriptions
> and calculates a match score using NLP and Machine Learning.

## 🚀 Live Demo
Try it here - link coming after deployment!

## 📌 Problem Statement
Recruiters spend an average of 6 seconds reading a resume.
With hundreds of applications, manually matching each one to
job requirements is impossible. This tool automates that
process using AI and NLP.

## ✨ Features
- Upload PDF Resume and Job Description
- NLP Preprocessing Pipeline using NLTK and spaCy
- TF-IDF and Cosine Similarity Matching
- Match Score with Color-coded Results
- Matching Skills Detection
- Missing Skills Gap Analysis
- Downloadable PDF Report

## 🛠️ Tech Stack
- Frontend: Streamlit
- NLP: NLTK, spaCy
- Machine Learning: scikit-learn
- PDF Processing: PyPDF2, pdfplumber
- Report Generation: fpdf2
- Language: Python 3.13

## 🧠 How It Works
1. Upload Resume PDF and Job Description PDF
2. Text is extracted from both files
3. NLP cleans and processes the text
4. TF-IDF vectors are created and compared
5. Skills are extracted and matched
6. Match Score and PDF Report generated

## ⚙️ Installation
1. Clone the repository
   git clone https://github.com/YourUsername/ai-resume-matcher.git

2. Create virtual environment
   python -m venv venv
   venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

4. Download NLP data
   python -m spacy download en_core_web_sm

5. Run the app
   streamlit run streamlit_app.py

## 🗺️ Roadmap
- Phase 1: Project Setup - Done
- Phase 2: PDF Text Extraction - Done
- Phase 3: NLP Preprocessing - Done
- Phase 4: TF-IDF Matching - Done
- Phase 5: PDF Report Generation - Done
- Phase 6: BERT Semantic AI - Planned

## 👤 Author
Tejas - Computer Science Engineering Student

## 📄 License
MIT License