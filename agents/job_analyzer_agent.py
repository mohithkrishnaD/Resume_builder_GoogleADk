"""Job Analyzer Agent - Pure ADK"""
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
import google.generativeai as genai
from tools.skill_tools import extract_skills

from config import Config
import json

config = Config()
genai.configure(api_key=config.GEMINI_API_KEY)
model = genai.GenerativeModel(config.GEMINI_MODEL)


# @agent(name="job_analyzer_agent")
async def job_analyzer_agent_v1(job_description: str)-> dict:
    """
    ADK Agent: Analyze job description using Gemini.

    Extracts:
    1. Required technical skills
    2. Soft skills
    3. Experience level
    4. Key responsibilities

    Args:
        job_description: Raw job description text

    Returns:
        Structured job requirements
    """

    prompt = f"""
    
       Job Description:
       {job_description[:2500]}
    
       Return ONLY a JSON object with these keys:
       {{
           "required_technical_skills": [],
           "required_soft_skills": [],
           "experience_level": "",
           "key_responsibilities": []
       }}
       """

    try:
        response = model.generate_content(prompt)
        result = _parse_json(response.text)

        # Also extract skills using keyword tool
        extracted_skills = extract_skills(
            job_description,
            config.SKILL_DATABASE
        )

        # Combine
        all_skills = list(set(
            result.get("required_technical_skills", []) + extracted_skills
        ))
        result["required_technical_skills"] = all_skills
        result["status"] = "analyzed_successfully"

        return result

    except Exception as e:
        return {
            "required_technical_skills": [],
            "required_soft_skills": [],
            "experience_level": "Not specified",
            "key_responsibilities": [],
            "error": str(e),
            "status": "analysis_failed"
        }


def _parse_json(text: str)-> dict:
    """Parse JSON from response"""

    try:
        if "```json" in text:
            json_str = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            json_str = text.split("```")[1].split("```")[0]
        else:
            json_str = text
        return json.loads(json_str.strip())
    except:
        return {}


def analyze_job_with_gemini(job_description: str) -> dict:
    """
    Use Gemini to analyze job description.

    Args:
        job_description: Raw job description text

    Returns:
        Structured job requirements
    """
    genai.configure(api_key=Config.GEMINI_API_KEY)
    model = genai.GenerativeModel(Config.GEMINI_MODEL)

    prompt = f"""
    Analyze this job description and extract key information.

    Job Description:
    {job_description[:2500]}

    Return ONLY a JSON object with these exact keys:
    {{
        "required_technical_skills": [],
        "required_soft_skills": [],
        "experience_level": "",
        "key_responsibilities": [],
        "salary_range": ""
    }}

    Be specific and extract actual skills mentioned in the job description.
    """

    try:
        response = model.generate_content(prompt)
        result = _parse_json_response(response.text)

        # Also extract skills using keyword tool
        extracted_skills = extract_skills(job_description, Config.SKILL_DATABASE)

        # Combine
        all_technical = list(set(
            result.get("required_technical_skills", []) +
            extracted_skills.get("skills", [])
        ))
        result["required_technical_skills"] = all_technical

        return result

    except Exception as e:
        return {
            "required_technical_skills": [],
            "required_soft_skills": [],
            "experience_level": "Not specified",
            "key_responsibilities": [],
            "salary_range": "",
            "error": str(e)
        }

def _parse_json_response(text: str) -> dict:
    """Parse JSON from Gemini response"""
    try:
        if "```json" in text:
            json_str = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            json_str = text.split("```")[1].split("```")[0]
        else:
            json_str = text

        return json.loads(json_str.strip())
    except:
        return {}

def create_job_analyzer_agent() -> Agent:
    """
    Create Job Analyzer Agent.

    This agent analyzes job descriptions using Gemini to extract:
    1. Required technical skills
    2. Required soft skills
    3. Experience level
    4. Key responsibilities

    Returns:
        Agent object for analyzing jobs
    """

    # Create tool
    job_analyzer_tool = FunctionTool(analyze_job_with_gemini)

    # Create Agent
    agent = Agent(
        model=Config.GEMINI_MODEL,
        name="job_analyzer_agent",
        description="Analyzes job descriptions to extract requirements",
        instruction="""You are a job analysis agent. Your job is to:
            1. Use the job analyzer tool to extract structured data from job descriptions
            2. Identify required technical and soft skills
            3. Determine experience level needed
            4. Extract key responsibilities
            
            When given a job description, use the analyzer tool to extract all relevant information.
            Present the findings in a clear, organized manner.""",
        tools=[job_analyzer_tool]
    )

    return agent
