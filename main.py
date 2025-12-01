"""Main Application - Using Correct ADK Pattern"""

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.genai import types
from agents.coordinator_agent import create_coordinator_agent
from config import Config
from tools.pdf_tools import extract_text_from_pdf, extract_text_from_docx
import asyncio
import os


def parse_resume_locally(file_path: str) -> str:
    """
    Parse resume file locally to extract text.

    Args:
        file_path: Path to resume file (PDF or DOCX)

    Returns:
        Extracted text content
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Resume file not found: {file_path}")

    file_extension = file_path.lower().split('.')[-1]

    if file_extension == 'pdf':
        result = extract_text_from_pdf(file_path)
    elif file_extension in ['docx', 'doc']:
        result = extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}. Supported: pdf, docx, doc")

    if not result.get('success', False):
        raise Exception(f"Failed to parse resume: {result.get('error', 'Unknown error')}")

    return result['text']


async def main():
    """Main application entry point"""

    print("=" * 60)
    print("🚀 AI Resume Optimizer - Google ADK")
    print("=" * 60)

    # Create coordinator agent
    print("\n✓ Creating coordinator agent...")
    coordinator_agent = create_coordinator_agent()

    # Create ADK Runner
    print("✓ Initializing ADK Runner...")
    runner = Runner(
        agent=coordinator_agent,
        app_name=Config.APP_NAME,
        session_service=InMemorySessionService(),
        memory_service=InMemoryMemoryService()
    )

    # Example query
    print("\n" + "=" * 60)
    print("Example: Resume-Job Analysis")
    print("=" * 60)

    query = """
    Please analyze my resume and compare it with this job description.

    Resume: /path/to/resume.pdf (type: pdf)

    Job Description:
    We're looking for a Senior Python Developer with experience in:
    - Python (5+ years)
    - AWS and cloud infrastructure
    - Docker and Kubernetes
    - Machine Learning (TensorFlow/PyTorch)
    - Team leadership

    Analyze the match and provide recommendations.
    """

    print(f"\nQuery: {query[:200]}...")

    # Create content
    content = types.Content.from_parts(types.Part.from_text(query))

    # Run the agent
    print("\n" + "-" * 60)
    print("🤖 Agent is processing your request...")
    print("-" * 60)

    try:
        # Note: Actual implementation depends on ADK Runner API
        # This is a conceptual example

        result = await runner.run(
            user_id=Config.USER_ID,
            session_id=Config.SESSION_ID,
            content=content
        )

        print("\n✓ Analysis Complete!")
        print("\nResult:")
        print(result)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nNote: Make sure you have:")
        print("1. Set GEMINI_API_KEY environment variable")
        print("2. Provided valid resume file path")
        print("3. Proper ADK session setup")


def run_interactive_mode():
    """Run in interactive CLI mode"""
    print("\n" + "=" * 60)
    print("📝 Interactive Mode")
    print("=" * 60)

    # Create coordinator
    coordinator_agent = create_coordinator_agent()

    # Create runner
    runner = Runner(
        agent=coordinator_agent,
        app_name=Config.APP_NAME,
        session_service=InMemorySessionService()
    )

    print("\nAvailable commands:")
    print("1. parse <file_path>              - Parse resume locally")
    print("2. analyze <job_description>      - Analyze job")
    print("3. compare <resume_path> <job>    - Full analysis")
    print("4. exit                           - Quit")

    while True:
        try:
            user_input = input("\n> ").strip()

            if user_input.lower() == "exit":
                print("Goodbye! 👋")
                break

            if user_input.startswith("parse"):
                parts = user_input.split(" ", 1)
                if len(parts) < 2:
                    print("Usage: parse <file_path>")
                    continue

                file_path = parts[1].strip()
                try:
                    resume_text = parse_resume_locally(file_path)
                    print(f"✓ Resume parsed successfully ({len(resume_text)} characters)")
                    print(f"Preview: {resume_text[:200]}...")
                except Exception as e:
                    print(f"❌ Failed to parse resume: {e}")

            elif user_input.startswith("analyze"):
                print("Job analysis initiated...")
                # Implementation would follow

            elif user_input.startswith("compare"):
                parts = user_input.split(" ", 2)
                if len(parts) < 3:
                    print("Usage: compare <resume_path> <job_description>")
                    continue

                resume_path = parts[1].strip()
                job_desc = parts[2].strip()

                try:
                    resume_text = parse_resume_locally(resume_path)
                    print("✓ Resume parsed locally, starting analysis...")
                    # Here you would pass resume_text and job_desc to the agent
                    print("Analysis would proceed with parsed text...")
                except Exception as e:
                    print(f"❌ Failed to parse resume: {e}")

            else:
                print("Unknown command. Try: parse, analyze, compare, or exit")

        except KeyboardInterrupt:
            print("\nInterrupted. Goodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        run_interactive_mode()
    else:
        # Run async main
        asyncio.run(main())