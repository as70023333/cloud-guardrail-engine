# Multi-stage Dockerfile for Zero-Trust Quarantine Engine
# Optimized for security and minimal attack surface

# Stage 1: Build stage
FROM python:3.11-slim as builder

WORKDIR /build

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies to a prefix directory
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Production stage
FROM python:3.11-slim

# Metadata
LABEL maintainer="security-team@company.com"
LABEL description="Zero-Trust Identity Quarantine Engine"
LABEL version="1.0.0"

# Create non-root user for security (UID 10001)
RUN groupadd -r -g 10001 appgroup && \
    useradd -r -u 10001 -g appgroup -d /app -s /sbin/nologin appuser

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy application code
COPY --chown=appuser:appgroup main.py config.py ./
COPY --chown=appuser:appgroup providers/ ./providers/

# Create necessary directories with proper permissions
RUN mkdir -p /app/logs && \
    chown -R appuser:appgroup /app && \
    chmod -R 550 /app && \
    chmod 750 /app/logs

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Health check configuration
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/healthz')" || exit 1

# Environment variables with defaults
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    API_HOST=0.0.0.0 \
    API_PORT=8080 \
    LOG_LEVEL=INFO

# Run the application with uvicorn
# Using 4 workers for production load handling
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4", "--access-log", "--log-level", "info"]
