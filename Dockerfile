FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system deps (optional but safe)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list first (for caching)
COPY requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 5015

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5015"]
