FROM python:3.11-slim


WORKDIR /app


RUN apt-get update && apt-get install -y \
    build-essential \
    libsndfile1 \
    ffmpeg \
    portaudio19-dev \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*


ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONUNBUFFERED=1


COPY requirements.txt .
COPY server.py .
COPY kokoro-v0_19.onnx .
COPY voices.json .
COPY start.sh .


RUN chmod +x start.sh


RUN chown -R nobody:nogroup /app && \
    chmod -R 755 /app



RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir onnxruntime>=1.20.1 && \
    pip install --no-cache-dir -r requirements.txt


EXPOSE 8000


HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1


CMD ["./start.sh"] 