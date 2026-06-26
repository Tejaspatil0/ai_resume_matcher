import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "AI Resume Matcher"
APP_VERSION = "1.0.0"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
MODELS_DIR = os.path.join(BASE_DIR, "models")

MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = ["pdf", "txt"]
LANGUAGE = "english"
MIN_WORD_LENGTH = 3

SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"
TFIDF_MAX_FEATURES = 5000
TFIDF_NGRAM_RANGE = (1, 2)

SCORE_EXCELLENT = 80
SCORE_GOOD = 60
SCORE_AVERAGE = 40

TECH_SKILLS = [
    "python", "java", "javascript", "typescript", "c++", "c#",
    "html", "css", "react", "angular", "vue", "nodejs", "django",
    "flask", "fastapi", "machine learning", "deep learning", "nlp",
    "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy",
    "sql", "mysql", "postgresql", "mongodb", "aws", "azure", "gcp",
    "docker", "kubernetes", "git", "github", "tableau", "power bi",
    "communication", "leadership", "teamwork", "agile", "scrum",
]

PAGE_TITLE = "AI Resume Matcher"
PAGE_ICON = "🎯"
PAGE_LAYOUT = "wide"

COLOR_EXCELLENT = "#00C851"
COLOR_GOOD = "#FFD700"
COLOR_AVERAGE = "#FF8800"
COLOR_POOR = "#FF4444"
COLOR_PRIMARY = "#4A90D9"