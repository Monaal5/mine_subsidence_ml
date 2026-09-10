# Mine Subsidence AI Platform — Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose FastAPI port
EXPOSE 8050

# Environment variables
ENV PORT=8050
ENV TF_CPP_MIN_LOG_LEVEL=2

# Run Uvicorn production server
CMD ["uvicorn", "web_app.server:app", "--host", "0.0.0.0", "--port", "8050", "--workers", "2"]
