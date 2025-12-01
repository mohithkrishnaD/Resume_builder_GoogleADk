"""Resume Optimizer - Google ADK Implementation"""

__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "AI-powered resume optimizer using Google ADK"

from config import Config
from agents import (
    create_resume_parser_agent,
    create_job_analyzer_agent,
    create_skill_gap_agent,
    create_recommendation_agent,
    create_coordinator_agent
)

__all__ = [
    'Config',
    'create_resume_parser_agent',
    'create_job_analyzer_agent',
    'create_skill_gap_agent',
    'create_recommendation_agent',
    'create_coordinator_agent'
]
