"""Scoring Tools - Pure ADK"""
# from google.adk.tools import tool
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List


# @tool
def calculate_tfidf_tool(resume_text: str, job_desc: str) -> float:
    """
    ADK Tool: Calculate TF-IDF similarity.

    Args:
        resume_text: Resume text
        job_desc: Job description text

    Returns:
        Similarity score (0-100)
    """
    try:
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        vectors = vectorizer.fit_transform([resume_text, job_desc])
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        return round(similarity * 100, 2)
    except:
        return 0.0


# @tool
def calculate_keyword_match_tool(resume_skills: list,
                                 job_skills: list) -> Dict:
    """
    ADK Tool: Calculate keyword match score.

    Args:
        resume_skills: Skills from resume
        job_skills: Skills from job

    Returns:
        Match statistics
    """
    if not job_skills:
        return {"score": 0.0, "matched": 0, "total": 0}

    resume_set = {s.lower() for s in resume_skills}
    job_set = {s.lower() for s in job_skills}

    matches = resume_set & job_set
    score = (len(matches) / len(job_set)) * 100

    return {
        "score": round(score, 2),
        "matched": len(matches),
        "total": len(job_set)
    }

# @tool
def calculate_final_score_tool(tfidf_score: float,
                               keyword_score: float,
                               tfidf_weight: float = 0.6,
                               keyword_weight: float = 0.4) -> float:
    
    
    """
    ADK Tool: Calculate weighted final score.
    
    Args:
        tfidf_score: TF-IDF score
        keyword_score: Keyword match score
        tfidf_weight: Weight for TF-IDF
        keyword_weight: Weight for keywords
    
    Returns:
        Final weighted score
    """
    final = (tfidf_weight * tfidf_score) + (keyword_weight * keyword_score)
    return round(final, 2)


def calculate_tfidf_similarity(resume_text: str, job_desc: str) -> Dict:
    """
    Calculate TF-IDF cosine similarity.

    Args:
        resume_text: Resume text
        job_desc: Job description text

    Returns:
        Dictionary with TF-IDF score
    """
    try:
        vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=1000
        )

        vectors = vectorizer.fit_transform([resume_text, job_desc])
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

        return {
            "success": True,
            "tfidf_score": round(similarity * 100, 2),
            "method": "TF-IDF"
        }
    except Exception as e:
        return {
            "success": False,
            "tfidf_score": 0.0,
            "error": str(e)
        }


def calculate_keyword_match(resume_skills: List[str],
                            job_skills: List[str]) -> Dict:
    """
    Calculate keyword match percentage.

    Args:
        resume_skills: Skills from resume
        job_skills: Skills from job

    Returns:
        Dictionary with match statistics
    """
    if not job_skills:
        return {
            "success": True,
            "keyword_score": 0.0,
            "matched_count": 0,
            "total_required": 0
        }

    resume_set = {s.lower() for s in resume_skills}
    job_set = {s.lower() for s in job_skills}

    matches = resume_set & job_set
    match_percentage = (len(matches) / len(job_set)) * 100

    return {
        "success": True,
        "keyword_score": round(match_percentage, 2),
        "matched_count": len(matches),
        "total_required": len(job_set),
        "matched_skills": [s for s in job_skills if s.lower() in matches]
    }


def calculate_final_score(tfidf_score: float,
                          keyword_score: float,
                          tfidf_weight: float = 0.6,
                          keyword_weight: float = 0.4) -> Dict:
    """
    Calculate weighted final match score.

    Args:
        tfidf_score: TF-IDF similarity (0-100)
        keyword_score: Keyword match (0-100)
        tfidf_weight: Weight for TF-IDF
        keyword_weight: Weight for keywords

    Returns:
        Dictionary with final score
    """
    final_score = (tfidf_weight * tfidf_score) + (keyword_weight * keyword_score)

    return {
        "final_score": round(final_score, 2),
        "tfidf_score": tfidf_score,
        "keyword_score": keyword_score,
        "weights": {
            "tfidf": tfidf_weight,
            "keyword": keyword_weight
        }
    }
