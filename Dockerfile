# Hugging Face Spaces Dockerfile
# Serves the FastAPI backend on port 7860 (HF default)

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy backend code
COPY backend/ .

# HF Spaces runs on port 7860
EXPOSE 7860

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
