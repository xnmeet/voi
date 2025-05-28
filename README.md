# Bob Kokoro TTS Plugin

<div align="center">
  <img src="bob-plugin/src/icon.png" width="200" height="200" alt="Plugin Icon">
</div>

<p align="center">
  一个基于 <a href="https://bobtranslate.com/">Bob</a> 的文本转语音插件，使用 Kokoro 本地部署模型作为语音合成服务。
</p>

<p align="center">
  <a href="https://github.com/xnmeet/voi/releases/latest">
    <img src="https://img.shields.io/github/v/release/xnmeet/voi?include_prereleases&style=flat-square" alt="Version">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/github/license/xnmeet/voi?style=flat-square" alt="MIT License">
  </a>
</p>

## 📦 项目结构

本项目包含两个主要部分：

1. **Bob 插件** (`bob-plugin/`): Bob 的文本转语音插件
2. **TTS 服务器** (`server/`): Kokoro TTS 本地服务器

## 🚀 快速开始

### 1️⃣ 部署 TTS 服务器

首先下载必需的模型文件：

```bash
cd server
# 下载 ONNX 模型文件 (v1.0)
wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
# 下载声音配置文件 (v1.0)
wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```

然后选择以下任一方式部署服务器：

```bash
# 方式一：直接运行
pip install -r requirements.txt
python server.py

# 方式二：Docker（推荐）
docker build -f Dockerfile.conda -t kokoro-tts-conda .
docker run -p 8000:8000 kokoro-tts-conda
```

详细说明请参考 [服务器文档](server/README.md)

### 2️⃣ 安装 Bob 插件

1. 下载最新版本的插件（[Releases](https://github.com/xnmeet/voi/releases/latest)）
2. 安装 `.bobplugin` 文件到 Bob 中
3. 在 Bob 的偏好设置中配置服务器地址（例如：`http://localhost:8000/text-to-speech`）

详细说明请参考 [插件文档](bob-plugin/README.md)

## 📡 API 调用示例

### 基本调用

TTS 服务器提供了简单易用的 REST API，以下是各种调用方式的示例：

#### 配置在 Bob 插件

自定义接口完整地址：http://localhost:55000/text-to-speech

> 前面的域名和端口替换为你实际起的服务对应域名和端口

#### curl 命令行调用

```bash
# 基本调用（使用默认声音）
curl -X POST http://localhost:8000/text-to-speech \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, this is a test message"}' \
  --output audio.mp3

# 指定声音和语速
curl -X POST http://localhost:8000/text-to-speech \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, this is a test with custom voice",
    "voice": "af_bella",
    "speed": 1.2,
    "format": "wav"
  }' \
  --output audio.wav

# 获取 Base64 编码的音频数据
curl -X POST http://localhost:8000/text-to-speech \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello world",
    "voice": "af_heart",
    "format": "base64"
  }' | jq -r '.audio_data' | base64 -d > audio.mp3
```

#### Python 调用示例

```python
import requests
import base64

# 基本调用
def text_to_speech_basic():
    url = "http://localhost:8000/text-to-speech"
    data = {
        "text": "你好，这是一个测试消息",
        "voice": "af_heart",
        "speed": 1.0,
        "format": "mp3"
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        with open("output.mp3", "wb") as f:
            f.write(response.content)
        print("音频文件已保存为 output.mp3")
    else:
        print(f"请求失败: {response.status_code}")

# 获取 Base64 编码的音频
def text_to_speech_base64():
    url = "http://localhost:8000/text-to-speech"
    data = {
        "text": "这是 Base64 编码示例",
        "voice": "af_bella",
        "format": "base64"
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        result = response.json()
        audio_data = base64.b64decode(result["audio_data"])

        with open("output_base64.mp3", "wb") as f:
            f.write(audio_data)
        print("Base64 音频文件已保存")
    else:
        print(f"请求失败: {response.status_code}")

# 调用函数
text_to_speech_basic()
text_to_speech_base64()
```

#### JavaScript 调用示例

```javascript
// 基本调用
async function textToSpeech() {
  const response = await fetch('http://localhost:8000/text-to-speech', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      text: 'Hello from JavaScript!',
      voice: 'af_heart',
      speed: 1.0,
      format: 'mp3'
    })
  });

  if (response.ok) {
    const audioBlob = await response.blob();
    const audioUrl = URL.createObjectURL(audioBlob);

    // 创建音频元素并播放
    const audio = new Audio(audioUrl);
    audio.play();
  } else {
    console.error('TTS 请求失败:', response.status);
  }
}

// Base64 格式调用
async function textToSpeechBase64() {
  const response = await fetch('http://localhost:8000/text-to-speech', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      text: 'Base64 格式示例',
      voice: 'af_bella',
      format: 'base64'
    })
  });

  if (response.ok) {
    const result = await response.json();
    const audioData = 'data:audio/mp3;base64,' + result.audio_data;

    // 创建音频元素并播放
    const audio = new Audio(audioData);
    audio.play();
  }
}
```

### 可用参数说明

| 参数     | 类型    | 默认值     | 说明                         |
| -------- | ------- | ---------- | ---------------------------- |
| `text`   | string  | -          | 要转换的文本内容（必需）     |
| `voice`  | string  | "af_heart" | 声音选择，详见服务器文档     |
| `speed`  | float   | 1.0        | 语速调节（0.5-2.0）          |
| `format` | string  | "mp3"      | 音频格式：wav/mp3/ogg/base64 |
| `stream` | boolean | true       | 是否使用流式响应             |

### 健康检查

```bash
# 检查服务器状态
curl http://localhost:8000/health

# 返回结果
{"status": "healthy"}
```

## 🙏 致谢

本项目使用了以下开源项目：

- [kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx) - Kokoro TTS 的 ONNX 运行时实现
- [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) - Kokoro TTS 模型

## ❓ 问题反馈

如果您在使用过程中遇到任何问题，请通过以下方式反馈：

1. 在 GitHub 上提交 Issue
2. 发送邮件至 xxnmeet@gmail.com

## 📄 许可证

[MIT License](LICENSE)
