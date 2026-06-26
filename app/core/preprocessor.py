import re
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from config import LANGUAGE, MIN_WORD_LENGTH


def download_nltk_data():
    packages = ['punkt', 'stopwords', 'wordnet',
                'averaged_perceptron_tagger', 'punkt_tab']
    for package in packages:
        try:
            nltk.download(package, quiet=True)
        except:
            pass


download_nltk_data()


def lowercase_text(text):
    return text.lower()


def remove_punctuation(text):
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def tokenize(text):
    try:
        tokens = word_tokenize(text)
    except:
        tokens = text.split()
    return tokens


def remove_stopwords(tokens):
    stop_words = set(stopwords.words(LANGUAGE))
    custom_stopwords = {
        'experience', 'work', 'working', 'years',
        'year', 'etc', 'also', 'using', 'used',
        'use', 'good', 'well', 'able', 'must'
    }
    stop_words.update(custom_stopwords)
    filtered = [
        word for word in tokens
        if word not in stop_words and len(word) >= MIN_WORD_LENGTH
    ]
    return filtered


def lemmatize(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(word) for word in tokens]
    return lemmatized


def preprocess_text(text):
    if not text or len(text.strip()) == 0:
        return {
            "success": False,
            "original_text": text,
            "cleaned_text": "",
            "tokens": [],
            "token_count": 0,
            "error": "Empty text provided"
        }
    try:
        step1 = lowercase_text(text)
        step2 = remove_punctuation(step1)
        step3 = tokenize(step2)
        step4 = remove_stopwords(step3)
        step5 = lemmatize(step4)
        cleaned_text = " ".join(step5)
        return {
            "success": True,
            "original_text": text,
            "cleaned_text": cleaned_text,
            "tokens": step5,
            "token_count": len(step5),
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "original_text": text,
            "cleaned_text": "",
            "tokens": [],
            "token_count": 0,
            "error": str(e)
        }


def get_unique_words(tokens):
    return list(set(tokens))


def get_word_frequency(tokens):
    frequency = {}
    for word in tokens:
        frequency[word] = frequency.get(word, 0) + 1
    sorted_freq = dict(
        sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    )
    return sorted_freq


def preprocess_for_matching(text):
    result = preprocess_text(text)
    if not result["success"]:
        return result
    tokens = result["tokens"]
    unique_words = get_unique_words(tokens)
    word_freq = get_word_frequency(tokens)
    top_keywords = list(word_freq.keys())[:20]
    result.update({
        "unique_words": unique_words,
        "unique_word_count": len(unique_words),
        "word_frequency": word_freq,
        "top_keywords": top_keywords
    })
    return result