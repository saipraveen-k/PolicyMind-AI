# PolicyMind AI Dockerfile
# Optimized for OpenEnv validation and Hugging Face Spaces deployment

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs

# Set permissions
RUN chmod +x inference.py

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import environment.env; print('Environment import successful')" || exit 1

# Expose port for web service (if needed)
EXPOSE 7860

# Default command for FastAPI backend
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]

# Alternative commands for different use cases:
# For OpenEnv validation: docker run policymind-ai python -c "import environment.env; print('Validation passed')"
# For inference: docker run policymind-ai python inference.py
# For web service: docker run -p 7860:7860 policymind-ai
