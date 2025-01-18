from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from enum import Enum
import sounddevice as sd
from kokoro_onnx import Kokoro
import io
import wave
import numpy as np
import asyncio
from pydub import AudioSegment
import logging
from datetime import datetime
import sys
import os
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing TTS service...")
    try:
        # 记录模型加载
        logger.info("Loading Kokoro model...")
        logger.debug(f"Current working directory: {os.getcwd()}")
        logger.debug(f"Directory contents: {os.listdir('.')}")
        global kokoro
        kokoro = Kokoro("kokoro-v0_19.onnx", "voices.json")
        logger.info("Kokoro model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to initialize service: {str(e)}")
        logger.exception("Detailed error:")
        raise e
    yield

app = FastAPI(lifespan=lifespan)
logger = logging.getLogger(__name__)

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

@app.middleware("http")
async def log_request(request, call_next):
    if request.url.path == "/text-to-speech":
        body = await request.body()
        logger.info(f"Raw request body: {body.decode()}")
    response = await call_next(request)
    return response

class AudioFormat(str, Enum):
    WAV = "wav"
    MP3 = "mp3"
    OGG = "ogg"
    BASE64 = "base64"

class AudioFormatHandler:
    @staticmethod
    def get_media_type(format: AudioFormat) -> str:
        media_types = {
            AudioFormat.WAV: "audio/wav",
            AudioFormat.MP3: "audio/mpeg",
            AudioFormat.OGG: "audio/ogg",
            AudioFormat.BASE64: "application/json"
        }
        return media_types[format]
    
    @staticmethod
    def get_export_settings(format: AudioFormat) -> dict:
        settings = {
            AudioFormat.MP3: {
                'format': 'mp3',
                'bitrate': '64k',
                'codec': 'libmp3lame',
                'parameters': ['-q:a', '5']
            },
            AudioFormat.OGG: {
                'format': 'ogg',
                'codec': 'libvorbis',
                'parameters': ['-q:a', '4']
            },
            AudioFormat.BASE64: {
                'format': 'mp3',
                'bitrate': '64k',
                'codec': 'libmp3lame',
                'parameters': ['-q:a', '5']
            }
        }
        return settings.get(format, {})

class TTSRequest(BaseModel):
    text: str
    voice: str = "af"
    speed: float = 1.0
    stream: bool = True
    format: AudioFormat = AudioFormat.MP3

async def audio_generator(text: str, voice: str, speed: float, format: AudioFormat):
    try:
        stream = kokoro.create_stream(
            text,
            voice=voice,
            speed=speed,
            lang="en-us",
        )

        async for samples, sample_rate in stream:
            samples = (samples * 32767).astype(np.int16)
            
            wav_buffer = io.BytesIO()
            with wave.open(wav_buffer, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(samples.tobytes())
            
            if format == AudioFormat.WAV:
                wav_buffer.seek(0)
                yield wav_buffer.read()
            else:
                wav_buffer.seek(0)
                audio_segment = AudioSegment.from_wav(wav_buffer)
                output_buffer = io.BytesIO()
                
                export_settings = AudioFormatHandler.get_export_settings(format)
                audio_segment.export(output_buffer, **export_settings)
                
                output_buffer.seek(0)
                yield output_buffer.read()
            
    except Exception as e:
        logger.error(f"Error in audio generation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/text-to-speech")
async def text_to_speech(request: TTSRequest):
    logger.info(f"Received TTS request: {request.dict()}")
    try:
        generator = audio_generator(
            request.text, 
            request.voice, 
            request.speed,
            request.format
        )
        
        media_type = AudioFormatHandler.get_media_type(request.format)
        
        if request.format == AudioFormat.BASE64:
            # BASE64
            audio_chunks = []
            async for chunk in generator:
                audio_chunks.append(chunk)
            
            import base64
            audio_data = b''.join(audio_chunks)
            base64_data = base64.b64encode(audio_data).decode('utf-8')
            return {"audio_data": base64_data, "format": "mp3"}
            
        if request.stream:
            return StreamingResponse(
                generator,
                media_type=media_type
            )
        else:
            audio_chunks = []
            async for chunk in generator:
                audio_chunks.append(chunk)
            
            return Response(
                content=b''.join(audio_chunks),
                media_type=media_type
            )
                
    except Exception as e:
        logger.error(f"Error in text_to_speech endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)