# 1. Import the function that creates agents
from .coordinator_agent import create_coordinator_agent

# 2. Create ONE instance at module level
root_agent = create_coordinator_agent()

# Now ADK Web can find it and use it!
