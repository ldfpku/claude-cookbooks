# Claude 示例手册（Cookbooks）

Claude 示例手册提供代码与指南，帮助开发者基于 Claude 构建应用，其中包含可直接复制的代码片段，便于集成到你自己的项目中。

## 前提条件

大多数使用 Anthropic Messages API 的示例都可以针对兼容 Anthropic 的
[Qwen 网关](https://qwen.smjtools.com) 运行。依赖 Claude 专属 API 或服务的示例
仍然需要 Anthropic API 密钥。

### 在 cookbook 示例中使用 Qwen 网关

该网关提供 Qwen3.8-Flash-Next 模型，并接受 Anthropic Messages API 请求。创建一个
cookbook 专用的环境文件，并填入你的个人网关密钥：

```bash
cp .cookbook.env.example .cookbook.env
# Edit .cookbook.env and replace YOUR_QWEN_GATEWAY_KEY with your personal gateway key.
```

如果 `.cookbook.env` 已经存在，请编辑它，不要用模板覆盖它。

对于本地 Python 3.15 环境，更新依赖并固定解释器版本：

```powershell
uv python pin 3.15
uv sync --python 3.15 --all-extras --upgrade
uv run python -m ipykernel install --sys-prefix --name cookbook-venv --display-name "Python 3.15 (cookbook .venv)"
```

项目仍将 Python 3.11 作为最低版本；本地的 `.python-version` 固定版本不会
提交。VoyageAI 目前声明 Python `<3.15`，只在这些版本上安装。请在另一个兼容的环境中运行
VoyageAI 示例。
在 Windows 上，从源码构建 `pywinpty` 需要 NuGet。源码构建出的 wheel 可能
缺少 `conpty.dll` 和 `OpenConsole.exe`；在启动 Jupyter 之前验证 `import winpty`，
如有需要，把匹配的、经 Microsoft 签名的 ConPTY 运行时安装到环境的
`Lib\site-packages\winpty` 目录。重建环境时需要
再次检查这些原生运行时文件。

使用该文件启动 Jupyter，使其内核继承网关设置：

```bash
uv run --env-file .cookbook.env python -m jupyterlab
```

这样是以 Python 模块方式运行 JupyterLab，可避免 Windows 控制台启动器的错误，例如
`uv trampoline failed to canonicalize script path`。

对于 Python 示例，使用同样的项目级设置：

```bash
uv run --env-file .cookbook.env python path/to/example.py
```

这些命令只把设置传给被启动的进程及其子进程；它们不会
更改系统或用户的环境变量，也不会更改 Claude Desktop 或 Claude Code 的配置。
请对 `.cookbook.env` 保密。现有的 `.env` 和 `.env.example` 保持独立，不会被
此设置覆盖。

该网关文档说明的是 `POST /v1/messages` 兼容性，而不是完整的 Claude API 对等支持。Claude Agent
SDK 示例以及需要其他 Anthropic 端点（例如 Batch、Files 或 Admin API）的示例
必须使用 Anthropic API 凭证和 Anthropic 端点。超出文档所述兼容性范围的 Messages 层功能
应核对网关当前的支持情况。耗时较长的请求
应使用流式输出，因为网关可能使耗时过长的非流式请求超时；
图片请求需要有一个可用的支持视觉的节点。

### 使用 Anthropic API

对于需要 Claude 专属 API 或服务的示例，请从
[Anthropic Console](https://console.anthropic.com/settings/keys) 获取 Anthropic API 密钥，并单独配置。
不要在这些示例中使用你的网关密钥。仓库的 `.env.example` 仍然是
Anthropic 密钥模板；如果你需要本地的 `.env`，仅在它不存在时创建。
请在不含 cookbook 网关环境的单独进程中运行这些示例，例如：

```bash
uv run --env-file .env python -m jupyterlab
```

代码示例主要以 Python 编写，但这些概念可以改造为任何能够与 Claude API 交互的编程语言。

如果你刚开始使用 Claude API，建议从 [Claude API 基础课程](https://github.com/anthropics/courses/tree/master/anthropic_api_fundamentals) 开始，打下扎实的基础。

## 进一步探索

想寻找更多资源来提升你使用 Claude 和 AI 助手的体验？请查看以下链接：

- [Anthropic 开发者文档](https://docs.claude.com/claude/docs/guide-to-anthropics-prompt-engineering-resources)
- [Anthropic 支持文档](https://support.anthropic.com)
- [Anthropic Discord 社区](https://www.anthropic.com/discord)

## 贡献

Claude 示例手册离不开开发者社区的贡献。无论是提交想法、修正错别字、新增指南，还是改进现有内容，我们都很重视你的意见。通过贡献，你让这一资源对所有人更有价值。

为避免重复劳动，请在贡献之前先查看现有的 issue 和 pull request。

如果你有关于新示例或新指南的想法，请在 [issues 页面](https://github.com/anthropics/anthropic-cookbook/issues) 上分享。

## 示例目录

### 核心能力
- [分类](https://github.com/anthropics/anthropic-cookbook/tree/main/capabilities/classification)：探索使用 Claude 进行文本与数据分类的技术。
- [检索增强生成](https://github.com/anthropics/anthropic-cookbook/tree/main/capabilities/retrieval_augmented_generation)：了解如何用外部知识增强 Claude 的回答。
- [摘要](https://github.com/anthropics/anthropic-cookbook/tree/main/capabilities/summarization)：发现使用 Claude 进行有效文本摘要的技术。

### 工具使用与集成
- [工具使用](https://github.com/anthropics/anthropic-cookbook/tree/main/tool_use)：了解如何将 Claude 与外部工具和函数集成，以扩展它的能力。
  - [客服智能体](https://github.com/anthropics/anthropic-cookbook/blob/main/tool_use/customer_service_agent.ipynb)
  - [计算器集成](https://github.com/anthropics/anthropic-cookbook/blob/main/tool_use/calculator_tool.ipynb)
  - [SQL 查询](https://github.com/anthropics/anthropic-cookbook/blob/main/misc/how_to_make_sql_queries.ipynb)

### 第三方集成
- [检索增强生成](https://github.com/anthropics/anthropic-cookbook/tree/main/third_party)：用外部数据源补充 Claude 的知识。
  - [向量数据库（Pinecone）](https://github.com/anthropics/anthropic-cookbook/blob/main/third_party/Pinecone/rag_using_pinecone.ipynb)
  - [维基百科](https://github.com/anthropics/anthropic-cookbook/blob/main/third_party/Wikipedia/wikipedia-search-cookbook.ipynb/)
  - [网页](https://github.com/anthropics/anthropic-cookbook/blob/main/misc/read_web_pages_with_haiku.ipynb)
- [使用 Voyage AI 创建嵌入](https://github.com/anthropics/anthropic-cookbook/blob/main/third_party/VoyageAI/how_to_create_embeddings.md)

### 多模态能力
- [使用 Claude 处理视觉](https://github.com/anthropics/anthropic-cookbook/tree/main/multimodal)：
  - [图像入门](https://github.com/anthropics/anthropic-cookbook/blob/main/multimodal/getting_started_with_vision.ipynb)
  - [视觉最佳实践](https://github.com/anthropics/anthropic-cookbook/blob/main/multimodal/best_practices_for_vision.ipynb)
  - [解读图表与图形](https://github.com/anthropics/anthropic-cookbook/blob/main/multimodal/reading_charts_graphs_powerpoints.ipynb)
  - [从表单中提取内容](https://github.com/anthropics/anthropic-cookbook/blob/main/multimodal/how_to_transcribe_text.ipynb)
- [用 Claude 生成图像](https://github.com/anthropics/anthropic-cookbook/blob/main/misc/illustrated_responses.ipynb)：将 Claude 与 Stable Diffusion 结合用于图像生成。

### 高级技术
- [子智能体](https://github.com/anthropics/anthropic-cookbook/blob/main/multimodal/using_sub_agents.ipynb)：了解如何把 Haiku 作为子智能体与 Opus 配合使用。
- [向 Claude 上传 PDF](https://github.com/anthropics/anthropic-cookbook/blob/main/misc/pdf_upload_summarization.ipynb)：解析 PDF 并以文本形式传给 Claude。
- [自动化评估](https://github.com/anthropics/anthropic-cookbook/blob/main/misc/building_evals.ipynb)：使用 Claude 自动完成提示词评估。
- [启用 JSON 模式](https://github.com/anthropics/anthropic-cookbook/blob/main/misc/how_to_enable_json_mode.ipynb)：确保 Claude 输出一致的 JSON。
- [创建内容审核过滤器](https://github.com/anthropics/anthropic-cookbook/blob/main/misc/building_moderation_filter.ipynb)：使用 Claude 为你的应用创建内容审核过滤器。
- [提示词缓存](https://github.com/anthropics/anthropic-cookbook/blob/main/misc/prompt_caching.ipynb)：学习使用 Claude 进行高效提示词缓存的技术。
- [成本优化](https://github.com/anthropics/anthropic-cookbook/blob/main/cost_optimization/cost_optimization.ipynb)：针对一个智能体逐项完成成本优化清单，测量通过率和每项任务的成本，以找到帕累托最优配置。

## 其他资源

- [AWS 上的 Anthropic](https://github.com/aws-samples/anthropic-on-aws)：探索在 AWS 基础设施上使用 Claude 的示例与解决方案。
- [AWS Samples](https://github.com/aws-samples/)：AWS 提供的代码示例合集，可改造后用于 Claude。注意其中部分示例可能需要修改才能在 Claude 上达到最佳效果。
