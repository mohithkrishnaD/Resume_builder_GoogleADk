"""Resume Parser Agent - Pure ADK"""
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from tools.pdf_tools import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_resume_sections,
    extract_contact_info,
)
from tools.skill_tools import extract_skills
from google.genai import types
# from tools.pdf_tools import parse_pdf_tool, parse_docx_tool, extract_sections_tool
from tools.skill_tools import extract_skills_tool
from config import Config

config = Config()


def create_resume_parser_agent() -> Agent:
    """
    Create Resume Parser Agent.

    This agent parses resume text and extracts:
    1. Resume sections
    2. Contact information
    3. Skills

    Note: Text is parsed locally before being passed to this agent to avoid upload issues.

    Returns:
        Agent object for parsing resumes
    """

    # Create tools (no file parsing tools since we parse locally)
    section_extractor_tool = FunctionTool(extract_resume_sections)
    contact_extractor_tool = FunctionTool(extract_contact_info)

    # Get skill database for the skill extraction tool
    def extract_skills_with_db(text: str):
        return extract_skills(text, Config.SKILL_DATABASE)

    skill_extractor_tool = FunctionTool(extract_skills_with_db)
    extract_text_from_pdf_tool = FunctionTool(extract_text_from_pdf)
    extract_text_from_docx_tool = FunctionTool(extract_text_from_docx)

    # Create Agent with all tools
    agent = Agent(
        model=Config.GEMINI_MODEL,
        name="resume_parser_agent",
        description="Parses resume text and extracts structured data",
        instruction="""You are a resume parsing agent. Your job is to:
            1. Identify and extract resume sections (experience, education, skills)
            2. Extract contact information (emails, phones)
            3. Identify technical and soft skills

            When a user provides resume text, extract sections, contact info, and skills.

            Provide a comprehensive summary of the resume contents.""",
        tools=[
            section_extractor_tool,
            contact_extractor_tool,
            skill_extractor_tool,
            extract_text_from_pdf_tool,
            extract_text_from_docx_tool
        ]
    )

    return agent

# @agent(name="resume_parser_agent")
# async def resume_parser_agent_v1(file_path: str, file_type: str) -> dict:
#     """
#     ADK Agent: Parse resume and extract structured data.
#     This agent uses multiple tools to:
#     1. Extract text from PDF/DOCX
#     2. Parse resume sections
#     3. Extract skills
#     Args:
#     file_path: Path to resume file
#     file_type: 'pdf' or 'docx'
#     Returns:
#     Structured resume data
#     """
#     # Step 1: Parse file based on type
#     if file_type == "pdf":
#         parse_result = parse_pdf_tool(file_path)
#     elif file_type == "docx":
#         parse_result = parse_docx_tool(file_path)
#     else:
#         return {"error": "Unsupported file type"}
#
#     if not parse_result["success"]:
#         return {"error": parse_result.get("error", "Parsing failed")}
#
#     raw_text = parse_result["text"]
#
#     # Step 2: Extract sections
#     sections = extract_sections_tool(raw_text)
#
#     # Step 3: Extract skills
#     skills = extract_skills_tool(raw_text, config.SKILL_DATABASE)
#
#     return {
#         "raw_text": raw_text,
#         "sections": sections,
#         "skills": skills,
#         "word_count": len(raw_text.split()),
#         "file_type": file_type,
#         "status": "parsed_successfully"
#     }