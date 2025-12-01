"""Simple launch script for ADK Web"""

import subprocess
import os
import sys


def main():
    """Launch ADK web interface"""

    # Check if GEMINI_API_KEY is set
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY environment variable not set!")
        print("\nSet it with:")
        print("  export GEMINI_API_KEY='your-key-here'")
        sys.exit(1)

    print("🚀 Starting ADK Resume Optimizer...")
    print("=" * 60)

    try:
        # Launch ADK web
        subprocess.run(["adk", "web", "."], check=True)

    except FileNotFoundError:
        print("❌ Error: ADK CLI not found!")
        print("\nInstall with: pip install google-adk")
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")


if __name__ == "__main__":
    main()