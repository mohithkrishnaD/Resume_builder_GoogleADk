"""Coordinator Agent - Pure ADK Root Agent"""
from google.adk.agents import Agent
from agents.resume_parser_agent import create_resume_parser_agent
from agents.job_analyzer_agent import create_job_analyzer_agent
from agents.skill_gap_agent import create_skill_gap_agent
from agents.recommendation_agent import create_recommendation_agent
from config import Config


config = Config()
# genai.configure(api_key=config.GEMINI_API_KEY)
# model = genai.GenerativeModel(config.GEMINI_MODEL)


def create_coordinator_agent() -> Agent:
    """
    Create Coordinator Agent.

    This is the root agent that orchestrates all sub-agents.

    Sub-agents:
    1. Resume Parser Agent
    2. Job Analyzer Agent
    3. Skill Gap Agent
    4. Recommendation Agent

    Returns:
        Root coordinator agent
    """

    # Create all sub-agents
    parser_agent = create_resume_parser_agent()
    analyzer_agent = create_job_analyzer_agent()
    gap_agent = create_skill_gap_agent()
    recommendation_agent = create_recommendation_agent()

    # Create Coordinator Agent with sub-agents
    coordinator = Agent(
        model=Config.GEMINI_MODEL,
        name="coordinator_agent",
        description="Coordinates all resume analysis agents",
        instruction="""You are the coordinator agent for the Resume Optimizer system.
            Your role is to orchestrate the work of specialized agents:
            1. Resume Parser Agent - Parses and extracts resume data
            2. Job Analyzer Agent - Analyzes job requirements
            3. Skill Gap Agent - Identifies gaps and calculates match scores
            4. Recommendation Agent - Generates personalized recommendations
            
            Workflow:
            1. When given a resume and job description, route to parser and analyzer
            2. Use skill gap agent to compare and identify gaps
            3. Use recommendation agent to generate tailored content
            
            Provide users with comprehensive analysis and actionable next steps.""",
        sub_agents=[
            parser_agent,
            analyzer_agent,
            gap_agent,
            recommendation_agent
        ]
    )

    return coordinator