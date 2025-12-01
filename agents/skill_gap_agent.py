"""Skill Gap Agent - Pure ADK"""
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from tools.scoring_tools import (
    calculate_tfidf_similarity,
    calculate_keyword_match,
    calculate_final_score
)
from tools.skill_tools import identify_missing_skills
from config import Config
from typing import Dict

config = Config()


# @agent(name="skill_gap_agent")
async def skill_gap_agent_v1(resume_data: dict,
                          job_data: dict,
                          resume_text: str,
                          job_desc: str)-> dict:


    """
    ADK Agent: Analyze skill gaps and calculate match scores.

    Uses multiple scoring tools:
    1. TF-IDF similarity
    2. Keyword matching
    3. Skill gap identification

    Args:
        resume_data: Parsed resume
        job_data: Analyzed job
        resume_text: Raw resume text
        job_desc: Raw job description

    Returns:
        Comprehensive gap analysis
    """

    # Extract skills
    resume_skills = resume_data.get("skills", [])
    job_skills = job_data.get("required_technical_skills", [])

    # Calculate TF-IDF score
    tfidf_score = calculate_tfidf_similarity(resume_text, job_desc)

    # Calculate keyword match
    keyword_result = calculate_keyword_match(resume_skills, job_skills)
    keyword_score = keyword_result["score"]

    # Calculate final score
    final_score = calculate_final_score(
        tfidf_score,
        keyword_score,
        config.TFIDF_WEIGHT,
        config.KEYWORD_WEIGHT
    )

    # Identify missing skills
    missing_skills = identify_missing_skills(resume_skills, job_skills)

    # Identify matched skills
    matched_skills = [s for s in resume_skills
                      if s.lower() in [j.lower() for j in job_skills]]

    return {
        "scores": {
            "final_score": final_score,
            "tfidf_score": tfidf_score,
            "keyword_score": keyword_score
        },
        "skills_analysis": {
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "match_count": len(matched_skills),
            "total_required": len(job_skills)
        },
        "status": "gap_analysis_complete"
    }


def create_skill_gap_agent() -> Agent:
    """
    Create Skill Gap Agent.

    This agent:
    1. Calculates TF-IDF similarity
    2. Calculates keyword match score
    3. Identifies skill gaps
    4. Generates match analysis

    Returns:
        Agent object for gap analysis
    """

    # Create tools
    tfidf_tool = FunctionTool(calculate_tfidf_similarity)
    keyword_tool = FunctionTool(calculate_keyword_match)
    final_score_tool = FunctionTool(calculate_final_score)
    gap_tool = FunctionTool(identify_missing_skills)

    # Create Agent
    agent = Agent(
        model=Config.GEMINI_MODEL,
        name="skill_gap_agent",
        description="Analyzes skill gaps and calculates match scores",
        instruction="""You are a skill gap analysis agent. Your job is to:
            1. Calculate TF-IDF similarity between resume and job description
            2. Calculate keyword match score for skills
            3. Identify missing and matched skills
            4. Calculate final weighted match score
            5. Provide actionable recommendations
            
            Use the available tools to perform comprehensive analysis.
            Present results with clear metrics and insights.""",
        tools=[tfidf_tool, keyword_tool, final_score_tool, gap_tool]
    )

    return agent