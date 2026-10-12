# Claude Cookbooks

一组用于基于 Claude API 构建应用的 Jupyter 笔记本和 Python 示例。

## 快速开始

```bash
# Install dependencies
uv sync --all-extras

# Install pre-commit hooks
uv run pre-commit install

# Set up the cookbook-only Qwen gateway (does not alter Claude Desktop/Code configuration)
cp .cookbook.env.example .cookbook.env
# Edit .cookbook.env and add your personal gateway key
uv run --env-file .cookbook.env python -m jupyterlab

# For Claude-only API examples, configure a separate Anthropic API key and use
# the Anthropic endpoint instead.
```

## 开发命令

```bash
make format        # Format code with ruff
make lint          # Run linting
make check         # Run format-check + lint
make fix           # Auto-fix issues + format
make test          # Run pytest
```

也可以直接用 uv 执行：

```bash
uv run ruff format .           # Format
uv run ruff check .            # Lint
uv run ruff check --fix .      # Auto-fix
uv run pre-commit run --all-files
```

## 代码风格

- **行长度：** 100 个字符
- **引号：** 双引号
- **格式化工具：** Ruff

笔记本对文件中部导入（E402）、重复定义（F811）以及变量命名（N803、N806）采用宽松规则。

## Git 工作流

**分支命名：** `<username>/<feature-description>`

**提交格式（约定式提交）：**
```
feat(scope): add new feature
fix(scope): fix bug
docs(scope): update documentation
style: lint/format
```

## 关键规则

1. **API 密钥：** 绝不提交 `.env` 文件。先使用 `dotenv.load_dotenv()`，再通过 `os.environ` 或 `os.getenv()` 访问密钥

2. **依赖：** 使用 `uv add <package>` 或 `uv add --dev <package>`。绝不直接编辑 pyproject.toml。

3. **模型：** 使用当前的 Claude 模型。最新版本请查看 docs.anthropic.com。
   - Sonnet：`claude-sonnet-5`
   - Haiku：`claude-haiku-4-5`
   - Opus：`claude-opus-4-8`
   - **绝不使用带日期的模型 ID**（例如 `claude-sonnet-4-6-20250514`）。始终使用不带日期的别名。
   - **Bedrock 模型 ID** 采用不同格式。使用文档中的基础 Bedrock 模型 ID：
     - Opus 4.8：`anthropic.claude-opus-4-8`
     - Sonnet 5：`anthropic.claude-sonnet-5`
     - Haiku 4.5：`anthropic.claude-haiku-4-5-20251001-v1:0`
     - 全局端点（推荐）需在前面加上 `global.`：`global.anthropic.claude-opus-4-8`
     - 说明：较旧的 Bedrock 模型使用带日期的 `-YYYYMMDD-v1:0` 后缀（例如上面的 Haiku 4.5）；较新的模型使用不带后缀的 `anthropic.claude-<model>` 格式。

4. **笔记本：**
   - 在笔记本中保留输出（出于演示目的有意为之）
   - 每个笔记本只讲一个概念
   - 测试笔记本能够自上而下无错误运行

5. **质量检查：** 提交前运行 `make check`。Pre-commit 钩子会校验格式和笔记本结构。

## 斜杠命令

以下命令在 Claude Code 和 CI 中可用：

- `/notebook-review` - 审查笔记本质量
- `/model-check` - 校验 Claude 模型引用
- `/link-review` - 检查变更文件中的链接

## 项目结构

```
capabilities/      # Core Claude capabilities (RAG, classification, etc.)
evals/             # Model evaluation patterns and benchmarks
skills/            # Advanced skill-based notebooks
tool_use/          # Tool use and integration patterns
multimodal/        # Vision and image processing
misc/              # Batch processing, caching, utilities
third_party/       # Pinecone, Voyage, Wikipedia integrations
extended_thinking/ # Extended reasoning patterns
scripts/           # Validation scripts
.claude/           # Claude Code commands and skills
```

## 新增 Cookbook

1. 在合适的目录中创建笔记本
2. 在 `registry.yaml` 中添加条目，包含标题、描述、路径、作者和分类
3. 如果是新贡献者，在 `authors.yaml` 中添加作者信息
4. 运行质量检查并提交 PR
