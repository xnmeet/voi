# Kokoro TTS Server

<p align="center">
  基于 Kokoro 模型的本地部署 TTS 服务器。
</p>

## 🔗 开源项目依赖

本项目基于以下开源项目：

- 🚀 [kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx) - Kokoro TTS 的 ONNX 运行时实现
- 🧠 [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) - Kokoro TTS 模型

感谢这些优秀的开源项目的贡献！

## 💻 系统要求

- Python 3.8+
- ONNX Runtime
- 2GB+ 内存（用于加载模型）
- Docker（可选，如果使用 Docker 部署）

## 📥 准备工作

在启动服务器之前，需要下载模型文件和声音配置文件：

```bash
# 下载 ONNX 模型文件
wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/kokoro-v0_19.onnx

# 下载声音配置文件
wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/voices.json
```

将这两个文件放在 `server` 目录下。这些文件由于体积较大（模型文件约 310MB），不包含在代码仓库中。

## 🚀 快速开始

### 方式一：直接运行

1. 安装依赖：

```bash
pip install -r requirements.txt
```

2. 启动服务器：

```bash
python server.py
```

### 方式二：使用 Docker

1. 使用标准 Docker：

```bash
docker build -t kokoro-tts .
docker run -p 8000:8000 kokoro-tts
```

2. 使用 Conda 环境（推荐）：

```bash
docker build -f Dockerfile.conda -t kokoro-tts-conda .
docker run -p 8000:8000 kokoro-tts-conda
```

## ⚙️ 服务器配置

默认配置：

- 🌐 监听地址：`0.0.0.0:8000`
- 🛣️ API 端点：`/text-to-speech`
- 🎵 支持的音频格式：WAV, MP3
- 📤 支持多种响应格式：流式、二进制、Base64

## 📡 API 接口

### 语音合成接口

- **端点**：`/text-to-speech`
- **方法**：POST
- **请求体**：

```json
{
  "text": "要转换的文本",
  "voice": "声音选项",
  "speed": 1.0,
  "format": "wav|mp3|ogg|base64"
}
```

- **响应格式**：

1. 🌊 流式响应：

   - Content-Type: audio/wav 或 audio/mpeg
   - 直接返回音频流

2. 📦 二进制响应：

   - Content-Type: audio/wav 或 audio/mpeg
   - 返回完整的音频文件

3. 📝 JSON 响应 (`format=base64`)：

```json
{
  "audio_data": "base64编码的音频数据"
}
```

### 🎙️ 可用声音列表

```
🎤 基础声音
├── af: 默认声音
├── af_bella: Bella 声音
├── af_nicole: Nicole 声音
├── af_sarah: Sarah 声音
└── af_sky: Sky 声音

👨 男声
├── am_adam: Adam 声音
├── am_michael: Michael 声音
├── bm_george: George 声音
└── bm_lewis: Lewis 声音

👩 女声
├── bf_emma: Emma 声音
└── bf_isabella: Isabella 声音
```
