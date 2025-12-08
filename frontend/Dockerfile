FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements (assuming we reuse the one from backend or create a new one?)
# The user didn't specify a separate requirements.txt for frontend, but frontend/app.py uses requests, pandas, plotly, streamlit.
# I will assume there is no separate requirements.txt for frontend yet, but usually it's best practice.
# For now, I will manually install the known frontend deps or copy the backend one if it has everything.
# Backend requirements.txt HAS streamlit, pandas, plotly, requests. So I can reuse it or create a minimal one.
# To be safe and since I don't want to assume complex paths, I will create a requirements.txt on the fly or simply install packages.
# The user instruction was "Crie frontend/Dockerfile... instale dependências".
# Let's create a requirements.txt for frontend to be clean.

# Copy application code
COPY . .

# Install dependencies directly to ensure it works even if we don't have a specific file yet
RUN pip install --no-cache-dir streamlit pandas requests plotly

# Expose port
EXPOSE 8501

# Run command
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
