FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .

RUN pip install --no-cache-dir \
    fastapi==0.111.0 \
    "uvicorn[standard]==0.30.1" \
    sqlalchemy==2.0.30 \
    pydantic==2.7.4 \
    python-multipart==0.0.9 \
    yt-dlp==2024.5.27 \
    opencv-python-headless==4.10.0.84 \
    pytest==8.2.2 \
    requests==2.32.3

RUN pip install --no-cache-dir --no-build-isolation openai-whisper==20231117

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]