# Starlink Monitor CLI - Docker Image
# Build: docker build -t starlink-monitor .
# Run: docker run -it --rm starlink-monitor status

FROM python:3.11-slim

LABEL maintainer="Daniel Azevedo Novais"
LABEL description="Starlink Connectivity Monitor CLI Tool"
LABEL version="0.1.0"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY src/ ./src/
COPY cli/ ./cli/
COPY pyproject.toml ./
COPY README.md ./
COPY LICENSE ./

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Create config directory
RUN mkdir -p /root/.config/starlink_monitor

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create non-root user (optional, commented out for now)
# RUN useradd -m -u 1000 starlink && chown -R starlink:starlink /app
# USER starlink

# Default command
ENTRYPOINT ["python3", "cli/starlink_cli.py"]
CMD ["--help"]
