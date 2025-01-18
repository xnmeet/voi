# Bob Kokoro TTS Plugin

Bob 的文本转语音插件，使用 Kokoro 本地部署模型作为语音合成服务。

## 功能特点

- 支持多种声音选项
- 可自定义服务器接口地址
- 支持 Base64 格式的音频输出
- 与 Bob 无缝集成

## 安装要求

- Bob 版本 ≥ 1.6.0
- 需要有运行中的 Kokoro TTS 服务器

## 插件配置

### 必需配置

- **服务器地址**: 设置 Kokoro TTS 服务器的完整地址（例如：`http://localhost:8000/synthesize`）

### 可选配置

- **声音选择**: 可选择不同的声音模型
  - af: 默认声音
  - af_bella: Bella 声音
  - af_nicole: Nicole 声音
  - af_sarah: Sarah 声音
  - af_sky: Sky 声音
  - am_adam: Adam 声音
  - am_michael: Michael 声音
  - bf_emma: Emma 声音
  - bf_isabella: Isabella 声音
  - bm_george: George 声音
  - bm_lewis: Lewis 声音

## 使用方法

1. 在 Bob 中选择文本
2. 选择 Kokoro TTS 作为语音合成服务
3. 点击播放按钮即可听到合成的语音

## 开发说明

本插件使用 GitHub Actions 进行自动化发布。当插件代码有更新时，会自动：

1. 创建新的版本号
2. 生成插件包
3. 更新 `appcast.json`
4. 发布新版本
