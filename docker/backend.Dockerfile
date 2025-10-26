# AI Certificate Verifier - Simple Backend
FROM python:3.11-slim

# Install minimal system dependencies for Pillow and basic operations
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    libpng-dev \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY backend/requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY backend/ .

# Create uploads directory
RUN mkdir -p /data/uploads

# Expose port
EXPOSE 5000

# Set Python path and run the Flask app
ENV PYTHONPATH=/app
CMD ["python", "-m", "app.main"]
