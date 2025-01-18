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
# 下载 ONNX 模型文件
wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/kokoro-v0_19.onnx
# 下载声音配置文件
wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/voices.json
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
