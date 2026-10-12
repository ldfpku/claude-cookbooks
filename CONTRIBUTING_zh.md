# 为 Claude Cookbooks 做贡献

感谢你有意为 Claude Cookbooks 做出贡献！本指南将帮助你开始开发，并确保你的贡献符合我们的质量标准。

## 开发环境设置

### 前置条件

- Python 3.11 或更高版本
- [uv](https://docs.astral.sh/uv/) 包管理器（推荐）或 pip

### 快速开始

1. **安装 uv**（推荐的包管理器）：
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   
   或者使用 Homebrew：
   ```bash
   brew install uv
   ```

2. **克隆代码仓库**：
   ```bash
   git clone https://github.com/anthropics/claude-cookbooks.git
   cd claude-cookbooks
   ```

3. **搭建开发环境**：
   ```bash
   # Create virtual environment and install dependencies
   uv sync --all-extras
   
   # Or with pip:
   pip install -e ".[dev]"
   ```

4. **安装 pre-commit 钩子**：
   ```bash
   uv run pre-commit install
   # Or: pre-commit install
   ```

5. **配置 cookbook 网关**（用于 Anthropic Messages API 示例）：
   ```bash
   cp .cookbook.env.example .cookbook.env
   # Edit .cookbook.env and add your personal Qwen gateway key
   uv run --env-file .cookbook.env python -m jupyterlab
   ```

这只会把网关设置传递给 Jupyter 及其内核。它不会修改系统或用户的 环境变量，也不会修改 Claude Desktop/Claude Code 的配置。请对 `.cookbook.env` 严格保密。需要 Claude 专属 API 或服务的示例，必须使用单独的 Anthropic API 凭证和 Anthropic 端点；不要为这些示例使用网关密钥。请在不含 网关环境的独立进程中运行它们（例如，使用已有的 Anthropic `.env` 执行 `uv run --env-file .env python -m jupyterlab`；不要覆盖已有的 `.env`）。

## 质量标准

本仓库使用自动化工具来维护代码质量：

### 笔记本校验体系

- **[nbconvert](https://nbconvert.readthedocs.io/)**：用于测试的笔记本执行
- **[ruff](https://docs.astral.sh/ruff/)**：快速 Python 代码检查器与格式化工具，原生支持 Jupyter
- **Claude AI 审查**：使用 Claude 进行智能代码审查

**说明**：本仓库有意保留笔记本输出，因为它们向用户展示了预期结果。

### Claude Code 斜杠命令

本仓库包含的斜杠命令既可在 Claude Code（本地开发）中使用，也可在 GitHub Actions CI 中使用。当你在这个仓库中用 Claude Code 工作时，这些命令会自动可用。

**可用命令**：
- `/link-review` - 校验 Markdown 和笔记本中的链接
- `/model-check` - 核实 Claude 模型的使用是否为当前模型
- `/notebook-review` - 全面的笔记本质量检查

**在 Claude Code 中的用法**：
```bash
# Run the same validations that CI will run
/notebook-review skills/my-notebook.ipynb
/model-check
/link-review README.md
```

这些命令使用的校验逻辑与我们的 CI 流水线完全一致，帮助你在推送之前就发现问题。命令定义保存在 `.claude/commands/` 中，本地和 CI 共用。

### 提交之前

1. **运行质量检查**：
   ```bash
   uv run ruff check skills/ --fix
   uv run ruff format skills/
   
   uv run python scripts/validate_notebooks.py
   ```

2. **测试笔记本执行**（可选，需要 API 密钥）：
   ```bash
   uv run jupyter nbconvert --to notebook \
     --execute skills/classification/guide.ipynb \
     --ExecutePreprocessor.kernel_name=python3 \
     --output test_output.ipynb
   ```

### pre-commit 钩子

每次提交之前会自动运行 pre-commit 钩子，以确保代码质量：

- 使用 ruff 格式化代码
- 校验笔记本结构

如果某个钩子失败，请修复问题后再次提交。

## 贡献指南

### 笔记本最佳实践

1. **为 API 密钥使用环境变量**：
   ```python
   import os
   api_key = os.environ.get("ANTHROPIC_API_KEY")
   ```

2. **使用当前的 Claude 模型**：
   - 可用时优先使用模型别名，以提升可维护性
   - 最新的 Haiku 模型：`claude-haiku-4-5`（Haiku 4.5）
   - 在以下地址查看当前模型：https://docs.claude.com/en/docs/about-claude/models/overview
   - Claude 会在 PR 审查中自动校验模型的使用

3. **保持笔记本主题集中**：
   - 每个笔记本只讲一个概念
   - 说明和注释要清晰
   - 以 Markdown 单元格的形式包含预期输出

4. **测试你的笔记本**：
   - 确保它们能从首行到末行无错误地运行
   - 示例 API 调用应尽量少消耗词元
   - 包含错误处理

5. **为 Managed Agents 打上 cookbook 名称标签**：
   ```python
   agent = client.beta.agents.create(
       name="cookbook-data-analyst",
       metadata={"anthropic_cookbook": "claude-cookbooks/data-analyst-agent"},
       ...
   )
   ```
   - 在每次 `agents.create` 调用时都传入该标签，这样我们就能看到人们运行了哪些 cookbook
   - 取值为 `claude-cookbooks/` 加上笔记本文件名（kebab-case 形式，`data_analyst_agent.ipynb` 变为 `data-analyst-agent`）
   - 只能使用小写字母、数字和连字符。任何其他形式的取值都会被归因统计忽略，而且不会报错提醒你
   - 会话会从所属智能体继承该标签，因此 `sessions.create` 无需再做任何处理

### Git 工作流

1. **创建功能分支**：
   ```bash
   git checkout -b <your-name>/<feature-description>
   # Example: git checkout -b alice/add-rag-example
   ```

2. **使用约定式提交**：
   ```bash
   # Format: <type>(<scope>): <subject>
   
   # Types:
   feat     # New feature
   fix      # Bug fix
   docs     # Documentation
   style    # Formatting
   refactor # Code restructuring
   test     # Tests
   chore    # Maintenance
   ci       # CI/CD changes
   
   # Examples:
   git commit -m "feat(skills): add text-to-sql notebook"
   git commit -m "fix(api): use environment variable for API key"
   git commit -m "docs(readme): update installation instructions"
   ```

3. **保持提交原子化**：
   - 每次提交只做一处逻辑变更
   - 编写清晰、具有描述性的提交信息
   - 适用时引用相关 issue 编号

4. **推送并创建 PR**：
   ```bash
   git push -u origin your-branch-name
   gh pr create  # Or use GitHub web interface
   ```

### Pull Request 指南

1. **PR 标题**：使用约定式提交格式
2. **描述**：应包含：
   - 你做了哪些改动
   - 你为什么做这些改动
   - 如何测试这些改动
   - 相关的 issue 编号
3. **保持 PR 集中**：每个 PR 只做一项功能或修复
4. **回应反馈**：及时处理审查意见

## 测试

### 本地测试

运行校验套件：

```bash
# Check all notebooks
uv run python scripts/validate_notebooks.py

# Run pre-commit on all files
uv run pre-commit run --all-files
```

### CI/CD

我们的 GitHub Actions 工作流会自动：

- 校验笔记本结构
- 使用 ruff 检查代码
- 测试笔记本执行（面向维护者）
- 检查链接
- 由 Claude 审查代码和模型使用

为节省资源，外部贡献者的 API 测试额度有限。

## 获取帮助

- **Issues**：[GitHub Issues](https://github.com/anthropics/claude-cookbooks/issues)
- **Discord**：[Anthropic Discord](https://www.anthropic.com/discord)

## 安全

- 切勿提交 API 密钥或机密信息
- 敏感数据请使用环境变量
- 安全问题请私下报告至 security@anthropic.com

## 许可证

提交贡献即表示你同意你的贡献将按与项目相同的许可证（MIT 许可证）授权。