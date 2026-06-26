from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from config import (TFIDF_MAX_FEATURES, TFIDF_NGRAM_RANGE,
                    SCORE_EXCELLENT, SCORE_GOOD, SCORE_AVERAGE,
                    TECH_SKILLS, COLOR_EXCELLENT, COLOR_GOOD,
                    COLOR_AVERAGE, COLOR_POOR)


def calculate_tfidf_similarity(resume_text, job_text):
    vectorizer = TfidfVectorizer(
        max_features=TFIDF_MAX_FEATURES,
        ngram_range=TFIDF_NGRAM_RANGE,
        stop_words='english',
        lowercase=True
    )
    try:
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])
        similarity_score = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:2]
        )[0][0]
        match_percentage = round(float(similarity_score) * 100, 2)
        feature_names = vectorizer.get_feature_names_out()
        resume_vector = tfidf_matrix[0].toarray()[0]
        job_vector = tfidf_matrix[1].toarray()[0]
        resume_top_indices = np.argsort(resume_vector)[::-1][:20]
        job_top_indices = np.argsort(job_vector)[::-1][:20]
        resume_keywords = [feature_names[i] for i in resume_top_indices
                          if resume_vector[i] > 0]
        job_keywords = [feature_names[i] for i in job_top_indices
                       if job_vector[i] > 0]
        return {
            "success": True,
            "match_percentage": match_percentage,
            "similarity_score": float(similarity_score),
            "resume_keywords": resume_keywords,
            "job_keywords": job_keywords,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "match_percentage": 0,
            "similarity_score": 0,
            "resume_keywords": [],
            "job_keywords": [],
            "error": str(e)
        }


def extract_skills_from_text(text):
    text_lower = text.lower()
    found_skills = []
    for skill in TECH_SKILLS:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    return found_skills


def get_matching_and_missing_skills(resume_text, job_text):
    resume_skills = set(extract_skills_from_text(resume_text))
    job_skills = set(extract_skills_from_text(job_text))
    matching_skills = list(resume_skills.intersection(job_skills))
    missing_skills = list(job_skills - resume_skills)
    extra_skills = list(resume_skills - job_skills)
    skill_match_percentage = 0
    if len(job_skills) > 0:
        skill_match_percentage = round(
            (len(matching_skills) / len(job_skills)) * 100, 2
        )
    return {
        "resume_skills": list(resume_skills),
        "job_skills": list(job_skills),
        "matching_skills": sorted(matching_skills),
        "missing_skills": sorted(missing_skills),
        "extra_skills": sorted(extra_skills),
        "skill_match_percentage": skill_match_percentage,
        "total_job_skills": len(job_skills),
        "total_matching": len(matching_skills),
        "total_missing": len(missing_skills)
    }


def get_score_category(score):
    if score >= SCORE_EXCELLENT:
        return {
            "category": "Excellent Match",
            "emoji": "🟢",
            "color": COLOR_EXCELLENT,
            "message": "Outstanding! Your resume is a great match!",
            "advice": "You are highly qualified. Apply with confidence!"
        }
    elif score >= SCORE_GOOD:
        return {
            "category": "Good Match",
            "emoji": "🟡",
            "color": COLOR_GOOD,
            "message": "Good match! A few improvements can make it stronger.",
            "advice": "Add the missing skills to your resume if you have them."
        }
    elif score >= SCORE_AVERAGE:
        return {
            "category": "Average Match",
            "emoji": "🟠",
            "color": COLOR_AVERAGE,
            "message": "Average match. Consider upskilling in missing areas.",
            "advice": "Work on the missing skills before applying."
        }
    else:
        return {
            "category": "Poor Match",
            "emoji": "🔴",
            "color": COLOR_POOR,
            "message": "Low match. This role needs significant skill upgrades.",
            "advice": "This role may not be the right fit right now."
        }


def calculate_final_score(tfidf_score, skill_score):
    final_score = (tfidf_score * 0.6) + (skill_score * 0.4)
    return round(final_score, 2)


def match_resume_to_job(resume_text, job_text):
    if not resume_text or not job_text:
        return {
            "success": False,
            "error": "Resume or job description text is empty!"
        }
    try:
        tfidf_result = calculate_tfidf_similarity(resume_text, job_text)
        if not tfidf_result["success"]:
            return {"success": False, "error": tfidf_result["error"]}
        skills_result = get_matching_and_missing_skills(
            resume_text, job_text
        )
        final_score = calculate_final_score(
            tfidf_result["match_percentage"],
            skills_result["skill_match_percentage"]
        )
        score_info = get_score_category(final_score)
        return {
            "success": True,
            "final_score": final_score,
            "tfidf_score": tfidf_result["match_percentage"],
            "skill_score": skills_result["skill_match_percentage"],
            "score_category": score_info["category"],
            "score_emoji": score_info["emoji"],
            "score_color": score_info["color"],
            "score_message": score_info["message"],
            "score_advice": score_info["advice"],
            "matching_skills": skills_result["matching_skills"],
            "missing_skills": skills_result["missing_skills"],
            "extra_skills": skills_result["extra_skills"],
            "resume_keywords": tfidf_result["resume_keywords"],
            "job_keywords": tfidf_result["job_keywords"],
            "total_job_skills": skills_result["total_job_skills"],
            "total_matching": skills_result["total_matching"],
            "total_missing": skills_result["total_missing"],
            "error": None
        }
    except Exception as e:
        return {"success": False, "error": str(e)}