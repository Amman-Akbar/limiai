# ==============================================================================
# Stage 1: Builder — install Python dependencies
# ==============================================================================
FROM python:3.13-slim AS builder

WORKDIR /build

# Build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ && \
    rm -rf /var/lib/apt/lists/*

# Install via pip with prefix for easy copying
COPY pyproject.toml ./
RUN pip install --no-cache-dir --prefix=/install .

# ==============================================================================
# Stage 2: Runtime — lean production image
# ==============================================================================
FROM python:3.13-slim

WORKDIR /app

# System dependencies for OpenCV and ML libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 && \
    rm -rf /var/lib/apt/lists/*

# Copy pre-installed packages
COPY --from=builder /install /usr/local

# Copy application source
COPY app/ ./app/

# Copy model assets into the centralized models/ directory
COPY models/ ./models/

# Environment configuration
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Pre-download Transformer models for faster startup & offline consistency
RUN python -c "\
from transformers import pipeline; \
pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english'); \
pipeline('zero-shot-classification', model='typeform/distilbert-base-uncased-mnli'); \
pipeline('ner', aggregation_strategy='simple')"

EXPOSE 9000

# Health-check hit the monitoring endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:9000/health')" || exit 1

# Launch using v1 router entry point in app.main
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]
