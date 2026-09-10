# Mine Subsidence AI Platform — Dockerfile (Optimized for Cloud Free Tiers)
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

# Environment variables
ENV PORT=8050
ENV TF_CPP_MIN_LOG_LEVEL=3
ENV TF_ENABLE_ONEDNN_OPTS=0
ENV OMP_NUM_THREADS=1
ENV TF_NUM_INTRAOP_THREADS=1
ENV TF_NUM_INTEROP_THREADS=1

# Expose port
EXPOSE 8050

# Run single worker Uvicorn server bound to $PORT for memory efficiency (<250MB RAM)
CMD sh -c "uvicorn web_app.server:app --host 0.0.0.0 --port ${PORT:-8050} --workers 1"
