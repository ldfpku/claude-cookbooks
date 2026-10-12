# ElevenLabs 与 Claude Cookbooks

[ElevenLabs](https://elevenlabs.io/) 提供由 AI 驱动的语音转文字与文字转语音 API，可用于构建听起来自然的语音应用，并支持语音克隆、流式合成等高级功能。

这份 Cookbook 演示如何把 ElevenLabs 的语音处理与 Claude 的智能回复结合起来，构建一个低时延语音助手，并针对实时性能逐步优化。

## 内含内容

* **[低时延语音助手 Notebook](./low_latency_stt_claude_tts.ipynb)** - 一个交互式教程，带你一步步构建语音助手，演示如何通过流式处理把时延降到最低的多种优化技术。

* **[WebSocket 流式脚本](./stream_voice_assistant_websocket.py)** - 一个可用于生产的对话式语音助手，支持持续麦克风输入、无缝音频播放，并使用 WebSocket 流式处理实现尽可能低的时延。

## 如何使用这份 Cookbook

建议按以下顺序进行，以便从这份 Cookbook 中获得最多收获：

### 第 1 步：准备环境

1. **创建虚拟环境：**
   ```bash
   # Navigate to the ElevenLabs directory
   cd /path/to/claude-cookbooks/third_party/ElevenLabs

   # Create virtual environment
   python -m venv venv

   # Activate it
   source venv/bin/activate  # On macOS/Linux
   # OR
   venv\Scripts\activate     # On Windows
   ```

2. **获取你的 API 密钥：**
   - **ElevenLabs API 密钥：** [elevenlabs.io/app/developers/api-keys](https://elevenlabs.io/app/developers/api-keys)

     创建 API 密钥时，请确保它具备以下最低权限：
     - 文字转语音
     - 语音转文字
     - 对语音（voices）的读取权限
     - 对模型（models）的读取权限

   - **Anthropic API 密钥：** [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)

3. **配置你的环境：**
   ```bash
   cp .env.example .env
   ```

   编辑 `.env` 并填入你的 API 密钥：
   ```
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   ANTHROPIC_API_KEY=sk-ant-api03-...
   ```

4. **安装依赖：**
   ```bash
   # With venv activated
   pip install -r requirements.txt
   ```

### 第 2 步：完成 Notebook 学习

从 **[低时延语音助手 Notebook](./low_latency_stt_claude_tts.ipynb)** 开始。这份交互式指南会教你：

- 如何使用 ElevenLabs 进行语音转文字转录
- 如何生成 Claude 的回复并测量时延
- 流式处理如何缩短首个词元时间
- 如何对流式文字转语音，让音频播放更快
- 不同流式方案之间的取舍
- 为什么 WebSocket 流式在时延与质量之间提供了最佳平衡

Notebook 在每一步都包含性能指标与对比，帮助你理解每项优化的效果。

### 第 3 步：试用生产脚本

在理解 Notebook 中的概念之后，运行 **[WebSocket 流式脚本](./stream_voice_assistant_websocket.py)**，体验一个功能完整的语音助手：

```bash
python stream_voice_assistant_websocket.py
```

**工作原理：**
1. 按 Enter 开始录音
2. 对着麦克风说出你的问题
3. 按 Enter 停止录音
4. 助手会用自然的语音回答
5. 重复上述步骤，或按 Ctrl+C 退出

该脚本演示了以下可用于生产的实现：
- 用 sounddevice 进行实时麦克风录音
- 保留上下文的连续对话
- 基于 WebSocket 的流式处理，把时延降到最低
- 用于无缝播放的自定义音频队列

## 故障排查

### 音频爆音或杂音

**现象：** 播放过程中你可能偶尔听到短暂的爆音、咔哒声或音频中断。

**原因说明：**

这是因为脚本使用 MP3 格式音频，而 ElevenLabs 免费套餐必须使用 MP3。实时分块流式传输 MP3 数据时，FFmpeg 偶尔会收到无法解码的不完整帧。这通常发生在：
- 流式传输开始时（第一个块可能过小）
- 出现短暂网络时延期间
- 音频生成结束时（最后一个块可能不完整）

脚本会自动处理这些解码失败的块，方式是跳过它们（在音频解码逻辑中使用 try-except 模式），这可以防止控制台出现报错，但可能造成短暂的音频间隙，表现为爆音或咔哒声。

**影响：**
- 音频播放正常继续
- 短暂的爆音或咔哒声通常难以察觉或影响很小
- WebSocket 连接保持稳定
- 不会损失任何功能

**解决办法：**

在免费套餐使用 MP3 格式时，这是预期行为。如果你想彻底消除音频爆音：
1. 升级到 ElevenLabs 付费套餐
2. 修改脚本，改用 `pcm_44100` 格式而不是 MP3
3. PCM 格式可以更干净地流式传输，没有解码问题

### API 密钥问题

**现象：** `AssertionError: ELEVENLABS_API_KEY is not set` 或 `AssertionError: ANTHROPIC_API_KEY is not set`

**解决办法：**
1. 确认你已把 `.env.example` 复制为 `.env`：`cp .env.example .env`
2. 编辑 `.env`，确保两个 API 密钥都正确设置
3. 检查 API 密钥中是否有拼写错误或多余空格
4. 确认你的 ElevenLabs 密钥具备所需权限（见第 1 步）

### 依赖问题

**现象：** 出现 `ImportError: PortAudio library not found` 之类的错误或音频播放失败

**解决办法：**

**macOS：**
```bash
brew install portaudio ffmpeg
```

**Ubuntu/Debian：**
```bash
sudo apt-get install portaudio19-dev ffmpeg
```

**Windows：**
- 从 [ffmpeg.org](https://ffmpeg.org/download.html) 安装 FFmpeg
- 把 FFmpeg 加入系统 PATH
- 在 Windows 上，PortAudio 通常会随 sounddevice 自动安装

然后重新安装 Python 依赖：
```bash
pip install -r requirements.txt
```

### 麦克风权限

**现象：** `OSError: [Errno -9999] Unanticipated host error`，或无法访问麦克风

**解决办法：**
- **macOS：** 进入系统偏好设置 → 安全性与隐私 → 隐私 → 麦克风，为终端（或你的 Python IDE）启用权限
- **Windows：** 进入设置 → 隐私 → 麦克风，为 Python/终端启用麦克风访问
- **Linux：** 确认你的用户在 `audio` 组中：`sudo usermod -a -G audio $USER`（然后注销并重新登录）

测试你的麦克风设置：
```bash
python -c "import sounddevice as sd; print(sd.query_devices())"
```

### WebSocket 连接失败

**现象：** 连接错误、超时或流中断

**解决办法：**
1. 检查你的网络连接是否稳定
2. 确认防火墙没有阻止 WebSocket 连接（端口 443）
3. 尝试临时关闭 VPN 或代理
4. 确认你没有超出 API 速率限制（用量可在 ElevenLabs 控制台查看）

如果问题仍然存在，请查看 [ElevenLabs 状态页](https://status.elevenlabs.io/) 了解服务动态。

## 项目点子

当你熟悉这个语音助手之后，可以尝试构建以下这些富有启发性的项目：

- **会议记录助手** - 实时录制并转录会议，然后用 Claude 从对话中生成摘要、待办事项和关键结论。

- **语言学习导师** - 用任意语言练习对话并获得实时反馈。Claude 可以纠正发音、建议更地道的表达，并根据你的水平调整难度。

- **互动故事讲述者** - 创建“选择你自己的冒险”游戏：Claude 讲述故事并回应你口述的选择，为每个角色使用不同的语音。

- **免动手编程助手** - 手放在键盘上，用口述描述代码改动、缺陷或功能。非常适合“橡皮鸭调试法”或单人结对编程。

- **语音控制智能家居** - 为控制家中设备构建自然的对话界面。可以问“冷到该开暖气了吗？”这类复杂问题，而不是简单的开关指令。

- **个人语音日记** - 用口述记录每日想法，形成日记。Claude 可以按主题整理条目、追踪你的情绪变化，并在你需要时调出相关的过往条目。

## 关于 ElevenLabs 的更多信息

以下是一些有助于深入理解的资源：

- [ElevenLabs 平台](https://elevenlabs.io/) - 官方网站
- [API 文档](https://elevenlabs.io/docs/overview) - 完整的 API 参考
- [语音库](https://elevenlabs.io/voice-library) - 浏览可用的语音
- [API 试验场](https://elevenlabs.io/app/speech-synthesis/text-to-speech) - 交互式试听语音
- [Python SDK](https://github.com/elevenlabs/elevenlabs-python) - 官方 Python SDK