FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ .
COPY database/ /database/
COPY frontend/ /frontend/

# Create directories for runtime data
RUN mkdir -p /tmp/certificates && chmod 777 /tmp/certificates

# Expose port
EXPOSE 10000

# Start the application
# Use PORT environment variable from Render
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-10000} --workers 2 --timeout 60 --access-logfile - --error-logfile - app:app"]
