"""Skill Extraction Tools - Pure ADK"""
# from google.adk.tools import tool
from typing import List, Dict


# @tool
def extract_skills_tool(text: str, skill_database: List[str]) -> List[str]:
    """
    ADK Tool: Extract skills from text.

    Args:
        text: Resume or job description text
        skill_database: List of known skills

    Returns:
        List of found skills
    """
    text_lower = text.lower()
    found_skills = []
    for skill in skill_database:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return list(dict.fromkeys(found_skills))


# @tool
def identify_missing_skills_tool(resume_skills: List[str],
                                 job_skills: List[str]) -> List[str]:
    """
    ADK Tool: Identify skills gap.
    
    Args:
        resume_skills: Skills in resume
        job_skills: Skills required by job
    
    Returns:
        List of missing skills
    """
    resume_set = {s.lower() for s in resume_skills}
    job_set = {s.lower() for s in job_skills}
    
    missing = job_set - resume_set
    
    return [s for s in job_skills if s.lower() in missing]


def extract_skills(text: str, skill_database: List[str]) -> Dict:
    """
    Extract skills from text.

    Args:
        text: Resume or job description text
        skill_database: List of known skills

    Returns:
        Dictionary with found skills
    """
    text_lower = text.lower()
    found_skills = []

    for skill in skill_database:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    # Remove duplicates while preserving order
    unique_skills = list(dict.fromkeys(found_skills))

    return {
        "skills": unique_skills,
        "count": len(unique_skills)
    }


def identify_missing_skills(resume_skills: List[str],
                            job_skills: List[str]) -> Dict:
    """
    Identify skills gap between resume and job.

    Args:
        resume_skills: Skills from resume
        job_skills: Skills required by job

    Returns:
        Dictionary with missing skills analysis
    """
    resume_set = {s.lower() for s in resume_skills}
    job_set = {s.lower() for s in job_skills}

    missing = job_set - resume_set
    matched = resume_set & job_set

    # Return with original casing from job_skills
    missing_skills = [s for s in job_skills if s.lower() in missing]
    matched_skills = [s for s in resume_skills if s.lower() in matched]

    return {
        "missing_skills": missing_skills,
        "matched_skills": matched_skills,
        "missing_count": len(missing_skills),
        "matched_count": len(matched_skills),
        "total_required": len(job_skills),
        "gap_percentage": round((len(missing) / len(job_set) * 100) if job_set else 0, 2)
    }