# Claude Skills Cookbook 🚀

使用 Claude 的 Skills（技能）功能进行文档生成、数据分析与业务自动化的完整指南。本 Cookbook 演示如何利用 Claude 内置的 Excel、PowerPoint 与 PDF 创建技能，以及如何为专门的工作流构建自定义技能。

> **🎯 看技能实际运行：** 看看 **[Claude Creates Files](https://www.anthropic.com/news/create-files)**，了解这些技能如何支撑 Claude 在 Claude.ai 和桌面应用中直接创建与编辑文档！

## 什么是技能（Skills）？

技能是组织好的指令、可执行代码与资源的包，为 Claude 提供面向特定任务的专业能力。可以把它们看作“专业知识包”，Claude 可以动态地发现并加载它们，用来：

- 创建专业文档（Excel、PowerPoint、PDF、Word）
- 执行复杂的数据分析与可视化
- 应用公司专属的工作流与品牌风格
- 以领域专业知识自动化业务流程

📖 阅读我们的工程博客文章 [用 Skills 为智能体装备真实世界的能力](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

## 关键特性

- ✨ **渐进式披露架构** —— 技能只在需要时加载，优化词元用量
- 📊 **金融聚焦** —— 面向金融与业务分析的真实案例
- 🔧 **自定义技能开发** —— 学会构建并部署你自己的技能
- 🎯 **可用于生产的示例** —— 你可以直接改造并立即使用的代码

## Cookbook 结构

### 📚 [笔记本 1：技能入门](notebooks/01_skills_introduction.ipynb)

通过快速上手示例学习 Claude 的 Skills 功能的基础。

- 理解技能的架构
- 使用 beta 请求头配置 API
- 创建你的第一个 Excel 电子表格
- 生成 PowerPoint 演示文稿
- 导出为 PDF 格式

### 💼 [笔记本 2：金融应用](notebooks/02_skills_financial_applications.ipynb)

用真实金融数据探索强大的业务用例。

- 用图表和数据透视表构建金融仪表盘
- 投资组合分析与投资报告
- 跨格式工作流：CSV → Excel → PowerPoint → PDF
- 词元优化策略

### 🔧 [笔记本 3：自定义技能开发](notebooks/03_skills_custom_development.ipynb)

掌握创建你自己的专用技能的技巧。

- 构建一个财务比率计算器
- 创建公司品牌规范技能
- 进阶：金融建模套件
- [最佳实践](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)与安全考量

## 快速上手

### 前置条件

- Python 3.8 或更高版本
- Anthropic API 密钥（[在此获取](https://console.anthropic.com/)）
- Jupyter Notebook 或 JupyterLab

### 安装

1. **克隆仓库**

```bash
git clone https://github.com/anthropics/claude-cookbooks.git
cd claude-cookbooks/skills
```

2. **创建虚拟环境**（推荐）

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **安装依赖**

```bash
pip install -r requirements.txt
```

4. **配置 API 密钥**

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

5. **启动 Jupyter**

```bash
jupyter notebook
```

6. **从笔记本 1 开始**
   打开 `notebooks/01_skills_introduction.ipynb` 并跟着做！

## 示例数据

本 cookbook 在 `sample_data/` 中包含了逼真的金融数据集：

- 📊 **financial_statements.csv** —— 季度的损益表、资产负债表与现金流数据
- 💰 **portfolio_holdings.json** —— 带有绩效指标的投资组合
- 📋 **budget_template.csv** —— 带有差异分析的部门预算
- 📈 **quarterly_metrics.json** —— KPI 与运营指标

## 项目结构

```
skills/
├── notebooks/                    # Jupyter notebooks
│   ├── 01_skills_introduction.ipynb
│   ├── 02_skills_financial_applications.ipynb
│   └── 03_skills_custom_development.ipynb
├── sample_data/                  # Financial datasets
│   ├── financial_statements.csv
│   ├── portfolio_holdings.json
│   ├── budget_template.csv
│   └── quarterly_metrics.json
├── custom_skills/                # Your custom skills
│   ├── financial_analyzer/
│   ├── brand_guidelines/
│   └── report_generator/
├── outputs/                      # Generated files
├── docs/                         # Documentation
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
└── README.md                    # This file
```

## API 配置

技能需要特定的 beta 请求头。笔记本会自动处理这件事，但幕后发生的事情如下：

```python
from anthropic import Anthropic

client = Anthropic(
    api_key="your-api-key",
    default_headers={
        "anthropic-beta": "code-execution-2025-08-25,files-api-2025-04-14,skills-2025-10-02"
    }
)
```

**必需的 Beta 请求头：**

- `code-execution-2025-08-25` —— 为技能启用代码执行
- `files-api-2025-04-14` —— 下载生成的文件时必需
- `skills-2025-10-02` —— 启用 Skills（技能）功能

## 处理生成的文件

当技能创建文档（Excel、PowerPoint、PDF 等）时，它们会在响应中返回 `file_id` 属性。你必须使用 **Files API** 下载这些文件。

### 工作机制

1. **技能在代码执行过程中创建文件**
2. **响应中包含**每个所创建文件的 **file_ids**
3. **使用 Files API** 下载真正的文件内容
4. **保存到本地**或按需处理

### 示例：创建并下载一个 Excel 文件

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

# Step 1: Use a skill to create a file
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    container={
        "skills": [
            {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
        ]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[{
        "role": "user",
        "content": "Create an Excel file with a simple budget spreadsheet"
    }]
)

# Step 2: Extract file_id from the response
file_id = None
for block in response.content:
    if block.type == "tool_result" and hasattr(block, 'output'):
        # Look for file_id in the tool output
        if 'file_id' in str(block.output):
            file_id = extract_file_id(block.output)  # Parse the file_id
            break

# Step 3: Download the file using Files API
if file_id:
    file_content = client.beta.files.download(file_id=file_id)

    # Step 4: Save to disk
    with open("outputs/budget.xlsx", "wb") as f:
        f.write(file_content.read())

    print(f"✅ File downloaded: budget.xlsx")
```

### Files API 方法

```python
# Download file content (binary)
content = client.beta.files.download(file_id="file_abc123...")
with open("output.xlsx", "wb") as f:
    f.write(content.read())  # Use .read() not .content

# Get file metadata
info = client.beta.files.retrieve_metadata(file_id="file_abc123...")
print(f"Filename: {info.filename}, Size: {info.size_bytes} bytes")  # Use size_bytes not size

# List all files
files = client.beta.files.list()
for file in files.data:
    print(f"{file.filename} - {file.created_at}")

# Delete a file
client.beta.files.delete(file_id="file_abc123...")
```

**重要说明：**

- 文件临时存储在 Anthropic 的服务器上
- 下载的文件应当保存到你本地的 `outputs/` 目录
- Files API 使用与 Messages API 相同的 API 密钥
- 所有笔记本都包含了用于文件下载的辅助函数
- **文件默认会被覆盖** —— 重跑单元格会替换已有文件（你会在输出中看到 `[overwritten]`）

完整细节见 [Files API 文档](https://docs.claude.com/en/api/files-content)。

## 内置技能参考

Claude 自带以下预构建的技能：

| 技能 | ID | 说明 |
| ---------- | ------ | --------------------------------------------------------------------------- |
| Excel | `xlsx` | 创建并操作带公式、图表与格式的 Excel 工作簿 |
| PowerPoint | `pptx` | 生成带幻灯片、图表与切换效果的专业演示文稿 |
| PDF | `pdf` | 创建含文本、表格与图像的格式化 PDF 文档 |
| Word | `docx` | 生成带丰富格式与结构的 Word 文档 |

## 创建自定义技能

自定义技能遵循以下结构：

```
my_skill/
├── SKILL.md           # Required: Instructions for Claude
├── scripts/           # Optional: Python/JS code
│   └── processor.py
└── resources/         # Optional: Templates, data
    └── template.xlsx
```

更多内容见[笔记本 3](notebooks/03_skills_custom_development.ipynb)。

## 常见用例

### 财务报告

- 自动化的季度报告
- 预算差异分析
- 投资绩效仪表盘

### 数据分析

- 基于 Excel 的、含复杂公式的分析
- 数据透视表生成
- 统计分析与可视化

### 文档自动化

- 带品牌风格的演示文稿生成
- 从多个来源汇编报告
- 跨格式的文档转换

## 性能建议

1. **利用渐进式披露**：技能分阶段加载，以尽量减少词元用量
2. **批量操作**：在一次会话中处理多个文件
3. **技能组合**：组合多个技能以应对复杂工作流
4. **缓存复用**：使用容器 ID 复用已加载的技能

## 故障排查

### 常见问题

**未找到 API 密钥**

```
ValueError: ANTHROPIC_API_KEY not found
```

→ 确认你已把 `.env.example` 复制为 `.env` 并填入了你的密钥

**缺少 Skills Beta 请求头**

```
Error: Skills feature requires beta header
```

→ 确认你使用了笔记本中所示的正确 beta 请求头

**超出词元上限**

```
Error: Request exceeds token limit
```

→ 把大操作拆成更小的块，或使用渐进式披露

## 资源

### 文档

- 📖 [Claude API 文档](https://docs.anthropic.com/en/api/messages)
- 🔧 [Skills 文档](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)

### 支持文章

- 📚 [用 Skills 教会 Claude 你的工作方式](https://support.claude.com/en/articles/12580051-teach-claude-your-way-of-working-using-skills) —— 使用 Skills 的用户指南
- 🛠️ [如何通过对话与 Claude 一起创建技能](https://support.claude.com/en/articles/12599426-how-to-create-a-skill-with-claude-through-conversation) —— 交互式技能创建指南

### 社区与支持

- 💬 [Claude 支持](https://support.claude.com)
- 🐙 [GitHub Issues](https://github.com/anthropics/claude-cookbooks/issues)

## 贡献

我们欢迎贡献！请参阅 [CONTRIBUTING.md](../CONTRIBUTING.md) 了解指引。

## 许可证

本 cookbook 以 MIT 许可证提供。细节见 [LICENSE](../LICENSE)。

## 致谢

特别感谢 Anthropic 团队开发了 Skills 功能并提供了 SDK。

---

**有疑问？** 查看 [FAQ](docs/FAQ.md) 或开一个 issue。

**准备开始了吗？** 打开[笔记本 1](notebooks/01_skills_introduction.ipynb)，我们一起造点了不起的东西！🎉
