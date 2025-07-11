# Base image with Python and Git
FROM python:3.10-slim

# Install Git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the agent script
COPY code_diff_agent.py .

# Install GitPython (required by the agent)
RUN pip install --no-cache-dir GitPython

# Entrypoint to run the diff agent
ENTRYPOINT ["python", "code_diff_agent.py"]
