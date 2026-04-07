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
EXPOSE 8000

# Default command for validation
CMD ["python", "inference.py"]

# Alternative commands for different use cases:
# For OpenEnv validation: docker run policymind-ai python -c "import environment.env; print('Validation passed')"
# For interactive mode: docker run -it policymind-ai python
# For web service: docker run -p 8000:8000 policymind-ai python app.py
