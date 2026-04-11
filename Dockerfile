# Stage 1: Microsoft Playwright image containing all necessary system dependencies
FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install required Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download only Chromium for Playwright
RUN playwright install chromium

COPY . .

CMD ["python", "src/main.py"]