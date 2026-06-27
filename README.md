# 🎯 AI Resume Matcher

> An AI-powered tool that compares resumes with job descriptions
> and calculates a match score using NLP and Machine Learning.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)
![NLP](https://img.shields.io/badge/NLP-NLTK-green)
![ML](https://img.shields.io/badge/ML-scikit--learn-orange)
![License](https://img.shields.io/badge/License-MIT-brightgreen)
![Status](https://img.shields.io/badge/Status-Live-success)

---

## 🚀 Live Demo

👉 **[Try it here](https://airesumematcher-j2acwdstgtvqcjtrcp6xcf.streamlit.app/)**

> Upload your resume and a job description to get your match score instantly!

---

## 📌 Problem Statement

Recruiters spend an average of **6 seconds** reading a resume.
With hundreds of applications, manually matching each one to job
requirements is impossible. This tool automates that process
using AI and NLP — giving instant match scores and skill gap analysis.

---

## ✨ Features

- 📄 Upload PDF Resume and Job Description
- 🧠 NLP Preprocessing Pipeline using NLTK
- 📊 TF-IDF Vectorization + Cosine Similarity Matching
- 🎯 Match Score with Color-coded Results
- ✅ Matching Skills Detection
- ❌ Missing Skills Gap Analysis
- ⭐ Bonus Skills Display
- 📥 Downloadable PDF Report

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| Frontend | Streamlit |
| NLP | NLTK |
| Machine Learning | scikit-learn |
| PDF Processing | PyPDF2, pdfplumber |
| Report Generation | fpdf2 |
| Data Processing | pandas, numpy |
| Visualization | plotly, matplotlib |
| Language | Python 3.11 |

---

## 🧠 How It Works
Resume PDF + Job Description PDF

↓

Text Extraction (PyPDF2 + pdfplumber)

↓

NLP Preprocessing

(Tokenization → Stopword Removal → Lemmatization)

↓

TF-IDF Vectorization + Cosine Similarity

↓

Skills Extraction + Gap Analysis

↓

Match Score + Downloadable PDF Report

---

## 📁 Project Structure
ai-resume-matcher/

├── app/

│   ├── core/

│   │   ├── extractor.py        # PDF text extraction

│   │   ├── preprocessor.py     # NLP preprocessing

│   │   └── matcher.py          # TF-IDF matching engine

│   └── utils/

│       ├── file_handler.py     # File validation

│       └── report_generator.py # PDF report generation

├── data/                       # Sample files

├── assets/                     # Screenshots

├── streamlit_app.py            # Main entry point

├── config.py                   # Configuration

└── requirements.txt            # Dependencies

---

## ⚙️ Installation

```bash
# 1. Clone the repository
git clone https://github.com/Tejaspatil0/ai_resume_matcher.git
cd ai_resume_matcher

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

# 5. Run the app
streamlit run streamlit_app.py
```

---

## 📊 Sample Results
Resume:          John Doe — Python Developer

Job Description: Python Developer — AI & ML Role
🎯 Final Match Score:  56.14%

📊 TF-IDF Score:       35.24%

🛠️ Skill Match Score:  87.50%
✅ Matching Skills (21): aws, django, docker, flask,

git, github, python, sql...

❌ Missing Skills  (3):  agile, communication, deep learning

---

## 🗺️ Roadmap

- [x] Phase 1: Project Setup & Architecture
- [x] Phase 2: PDF Text Extraction
- [x] Phase 3: NLP Preprocessing Pipeline
- [x] Phase 4: TF-IDF Matching & Skills Analysis
- [x] Phase 5: PDF Report Generation
- [x] Phase 6: Streamlit Deployment
- [ ] Phase 7: BERT Semantic AI Matching
- [ ] Phase 8: Multi-Resume Ranking System
- [ ] Phase 9: Recruiter Dashboard

---

## 🎓 What I Learned

- Building end-to-end NLP pipelines
- TF-IDF vectorization and Cosine Similarity
- PDF text extraction techniques
- Streamlit web app development
- Git & GitHub version control
- Cloud deployment

---

## 👤 Author

**Tejas Patil** — Computer Science Engineering Student

[![GitHub](https://img.shields.io/badge/GitHub-Tejaspatil0-black?logo=github)](https://github.com/Tejaspatil0)

---

## 📄 License

MIT License — feel free to use this project!

---

⭐ **If you found this useful, please star the repository!**