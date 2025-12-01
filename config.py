"""Configuration for Pure ADK Resume Optimizer"""
import os
from typing import List
class Config:
    """Application configuration"""
    # Gemini API
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = "gemini-2.0-flash-lite"
    # ADK Settings
    APP_NAME = "resume_optimizer"
    SESSION_ID = "resume_session_123"
    USER_ID = "user_123"
    # Skill Database
    SKILL_DATABASE: List[str] = [
        # Programming Languages
        "Python", "Java", "JavaScript", "TypeScript", "C++", "Go", "Rust",
        "Ruby", "PHP", "Swift", "Kotlin",

        # Web Technologies
        "React", "Angular", "Vue.js", "Node.js", "Django", "Flask",
        "FastAPI", "Spring Boot", "Express.js", "Next.js",

        # Cloud & DevOps
        "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes",
        "Terraform", "Jenkins", "CI/CD", "GitHub Actions",

        # Databases
        "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis",
        "DynamoDB", "Cassandra", "Elasticsearch",

        # Data Science & ML
        "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
        "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy",

        # Soft Skills
        "Leadership", "Project Management", "Agile", "Scrum",
        "Communication", "Problem Solving", "Team Collaboration"

    ]
    # Scoring Weights
    TFIDF_WEIGHT = 0.6
    KEYWORD_WEIGHT = 0.4

