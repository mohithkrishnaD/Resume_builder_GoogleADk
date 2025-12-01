"""Recommendation Agent - Correct ADK Pattern"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
import google.generativeai as genai
from config import Config
from typing import List


def generate_tailored_section(original_section: str,
                              job_description: str,
                              missing_skills: List[str]) -> dict:
    """Generate tailored resume section using Gemini"""
    genai.configure(api_key=Config.GEMINI_API_KEY)
    model = genai.GenerativeModel(Config.GEMINI_MODEL)

    prompt = f"""
    Rewrite this resume section to better match the job requirements.
    Use action verbs, quantify achievements, and make it ATS-friendly.

    Original Section:
    {original_section[:800]}

    Target Job Description:
    {job_description[:1000]}

    Skills to emphasize: {', '.join(missing_skills[:5])}

    Guidelines:
    - Use strong action verbs
    - Quantify results with numbers/percentages
    - Match job keywords
    - Keep concise
    - Maintain truthfulness

    Return ONLY the rewritten section.
    """

    try:
        response = model.generate_content(prompt)
        return {
            "success": True,
            "tailored_section": response.text.strip()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def generate_cover_letter(resume_text: str,
                          job_description: str,
                          company_name: str = "") -> dict:
    """Generate personalized cover letter"""
    genai.configure(api_key=Config.GEMINI_API_KEY)
    model = genai.GenerativeModel(Config.GEMINI_MODEL)

    prompt = f"""
    Write a professional cover letter (3 paragraphs).

    Resume Content:
    {resume_text[:1000]}

    Job Description:
    {job_description[:1000]}

    Company: {company_name or '[Company Name]'}

    Guidelines:
    - Be enthusiastic and personable
    - Show specific fit with the role
    - Reference 2-3 matching skills
    - Professional but warm tone

    Return the complete cover letter.
    """

    try:
        response = model.generate_content(prompt)
        return {
            "success": True,
            "cover_letter": response.text.strip()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def suggest_learning_resources(missing_skills: List[str]) -> dict:
    """Suggest learning resources for skill gaps"""
    genai.configure(api_key=Config.GEMINI_API_KEY)
    model = genai.GenerativeModel(Config.GEMINI_MODEL)

    if not missing_skills:
        return {
            "success": True,
            "resources": "No skill gaps identified!"
        }

    skills_str = ', '.join(missing_skills[:5])

    prompt = f"""
    For each of these skills: {skills_str}

    Suggest:
    1. Free online courses (Coursera, edX, Udemy, YouTube)
    2. Practice projects
    3. Estimated learning time
    4. Industry certifications (if applicable)

    Be specific with course names and links where possible.
    Format as a practical learning roadmap.
    """

    try:
        response = model.generate_content(prompt)
        return {
            "success": True,
            "resources": response.text.strip()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def create_recommendation_agent() -> Agent:
    """
    Create Recommendation Agent.

    This agent generates:
    1. Tailored resume sections
    2. Cover letters
    3. Learning resources
    4. Action plans

    Returns:
        Agent object for recommendations
    """

    # Create tools
    tailor_tool = FunctionTool(generate_tailored_section)
    letter_tool = FunctionTool(generate_cover_letter)
    resources_tool = FunctionTool(suggest_learning_resources)

    # Create Agent
    agent = Agent(
        model=Config.GEMINI_MODEL,
        name="recommendation_agent",
        description="Generates personalized recommendations and content",
        instruction="""You are a career recommendation agent. Your job is to:
            1. Generate tailored resume sections optimized for specific jobs
            2. Create personalized cover letters
            3. Suggest learning resources for skill gaps
            4. Provide actionable next steps
            
            Use the available tools to help users improve their job applications.
            Provide practical, specific recommendations.""",
        tools=[tailor_tool, letter_tool, resources_tool]
    )

    return agent