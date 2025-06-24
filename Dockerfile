# Use a lightweight Python Alpine image
FROM python:3.13-alpine

# Set working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apk update && apk add --no-cache \
    build-base \
    libffi-dev \
    musl-dev \
    gcc \
    python3-dev
RUN pip install --upgrade pip

# Install pip requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .

# Expose FastAPI default port
EXPOSE 8000

# Run the app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
