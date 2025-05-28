#!/bin/bash
set -e

echo "Current working directory: $(pwd)"
echo "Listing directory contents:"
ls -la

echo "Checking for required files..."
test -f kokoro-v1.0.onnx || (echo "Error: kokoro-v1.0.onnx not found" && exit 1)
test -f voices-v1.0.bin || (echo "Error: voices-v1.0.bin not found" && exit 1)

echo "Checking Python environment..."
python --version
pip list

echo "Starting TTS service..."
exec uvicorn server:app --host 0.0.0.0 --port 8000 --workers 1 --log-level debug
