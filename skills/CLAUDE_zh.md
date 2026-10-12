# Skills Cookbook - Claude Code 指南

## 项目概览

这是一份完整的 Jupyter 笔记本 Cookbook，演示 Claude 的 Skills 功能用于文档生成（Excel、PowerPoint、PDF）。它面向学习把 Skills 集成进自己应用的开发者。

## 快速开始命令

### 环境准备
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (MUST use local whl for Skills support)
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 运行笔记本
```bash
# Launch Jupyter
jupyter notebook

# Or use VSCode with Jupyter extension
# Make sure to select the venv kernel in VSCode: Cmd+Shift+P → "Python: Select Interpreter"
```

### 测试与验证
```bash
# Verify environment and SDK version
python -c "import anthropic; print(f'SDK Version: {anthropic.__version__}')"

# Check outputs directory for generated files
ls -lh outputs/
```

## 架构概览

### 目录结构
```
skills/
├── notebooks/              # 3 progressive Jupyter notebooks
│   ├── 01_skills_introduction.ipynb
│   ├── 02_skills_financial_applications.ipynb  # WIP
│   └── 03_skills_custom_development.ipynb      # WIP
├── sample_data/           # Financial datasets for examples
├── custom_skills/         # Custom skill development area
├── outputs/               # Generated files (xlsx, pptx, pdf)
├── file_utils.py          # Files API helper functions
└── docs/                  # Implementation tracking
```

### 关键技术细节

**Beta API 要求：**
- 所有 Skills 功能都使用 `client.beta.*` 命名空间
- 必需的 beta 请求头：`code-execution-2025-08-25`、`files-api-2025-04-14`、`skills-2025-10-02`
- 必须使用带 `container` 参数的 `client.beta.messages.create()`
- 代码执行工具（`code_execution_20250825`）是必需的
- 通过引用 `skill_id` 使用预置的 Agent 技能，或通过 Skills API 创建并上传你自己的技能

**Files API 集成：**
- Skills 生成文件并返回 `file_id` 属性
- 必须使用 `client.beta.files.download()` 下载文件
- 必须使用 `client.beta.files.retrieve_metadata()` 获取文件信息
- `file_utils.py` 中的辅助函数负责提取和下载

**内置 Skills：**
- `xlsx` - 带公式和图表的 Excel 工作簿
- `pptx` - PowerPoint 演示文稿
- `pdf` - PDF 文档
- `docx` - Word 文档

## 开发中的坑

### 1. SDK 版本
**重要**：确认你使用的是支持 Skills 的 Anthropic SDK 0.71.0 或更高版本
```bash
pip install anthropic>=0.71.0
# Restart Jupyter kernel after installation if upgrading!
```

### 2. 必须使用 Beta 命名空间
**问题**：`container` 参数不被识别，files API 失败 **解决办法**：使用 `client.beta.messages.create()` 和 `client.beta.files.*`
```python
# ❌ Wrong
response = client.messages.create(container={...})
content = client.files.content(file_id)

# ✅ Correct
response = client.beta.messages.create(container={...})
content = client.beta.files.content(file_id)
```

### 3. Beta 请求头的位置
**问题**：在 default_headers 中设置 Skills beta 会让所有请求都必须带 code_execution **解决办法**：改为按请求使用 `betas` 参数
```python
# ❌ Wrong (affects all requests)
client = Anthropic(default_headers={"anthropic-beta": "skills-2025-10-02"})

# ✅ Correct (per-request)
response = client.beta.messages.create(
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"],
    ...
)
```

### 4. 文件 ID 提取
**问题**：响应结构与标准 Messages API 不同 **解决办法**：文件 ID 位于 `bash_code_execution_tool_result.content.content[0].file_id`
```python
# Use file_utils.extract_file_ids() - handles beta response structure
from file_utils import extract_file_ids, download_all_files
file_ids = extract_file_ids(response)
```

### 5. Files API 响应对象
**问题**：`'BinaryAPIResponse' object has no attribute 'content'`、`'FileMetadata' object has no attribute 'size'` **解决办法**：文件内容用 `.read()`，文件大小用 `.size_bytes`
```python
# ❌ Wrong
file_content = client.beta.files.download(file_id)
with open(path, 'wb') as f:
    f.write(file_content.content)  # No .content attribute!

# ✅ Correct
file_content = client.beta.files.download(file_id)
with open(path, 'wb') as f:
    f.write(file_content.read())  # Use .read()

# FileMetadata fields: id, filename, size_bytes (not size), mime_type, created_at, type, downloadable
metadata = client.beta.files.retrieve_metadata(file_id)
print(f"Size: {metadata.size_bytes} bytes")  # Use size_bytes, not size
```

### 6. Jupyter 内核选择
**问题**：错误的 Python 解释器 = 错误的依赖 **解决办法**：在 VSCode/Jupyter 中始终选择 venv 内核
- VSCode：Cmd+Shift+P → "Python: Select Interpreter" → 选择 venv
- Jupyter：Kernel → Change Kernel → 选择 venv

### 7. 需要重载模块
**问题**：对 `file_utils.py` 的改动不会反映到正在运行的笔记本中 **解决办法**：重启内核或重载模块
```python
import importlib
importlib.reload(file_utils)
```

### 8. 文档生成耗时
**问题**：创建文件比典型 API 调用耗时更长，用户可能以为单元格卡住了 **实际观察到的耗时：**
- Excel：约 2 分钟
- PowerPoint：约 1-2 分钟（简单的 2-3 页演示文稿）
- PDF：约 1-2 分钟

**解决办法**：在创建文件的单元格之前给出清晰的耗时预期
```markdown
**⏱️ Note**: Excel generation typically takes 1-2 minutes.
Be patient - the cell will show [*] while running!
```
**重要**：保持示例简单而聚焦。对于范围界定良好的示例，生成耗时稳定在 1-2 分钟。

## 常见任务

### 添加新的笔记本章节
1. 遵循 `01_skills_introduction.ipynb` 中的既有结构
2. 包含带导入和 beta 请求头的准备单元格
3. 展示 API 调用、响应处理、文件下载
4. 添加错误处理示例
5. 更新 `docs/skills_cookbook_plan.md` 的检查清单

### 创建示例数据
1. 在 `sample_data/` 中添加真实的财务数据
2. 表格数据用 CSV，结构化数据用 JSON
3. 包含表头并做好格式
4. 在笔记本中用 pandas 引用
5. 保持文件大小合理（<100KB）

### 测试文件下载
1. 运行笔记本单元格生成文件
2. 检查响应中的 file_id
3. 使用 `download_all_files()` 辅助函数
4. 在 `outputs/` 目录中确认文件
5. 用原生应用打开文件以验证

**说明**：文件默认会被覆盖。当文件已存在时，你会在下载摘要中看到 `[overwritten]`。设置 `overwrite=False` 可防止这种情况。

### 调试 API 错误
1. 检查 SDK 版本：`anthropic.__version__` 应为 `0.69.0`
2. 确认 beta 请求头是按请求传入的
3. 确保包含了 code_execution 工具
4. 用 `print(response)` 查看响应结构
5. 在 `response.stop_reason` 中查找错误详情

## 测试检查清单

在提交笔记本改动之前：
- [ ] 重启内核并运行所有单元格
- [ ] 确认所有文件下载都能工作
- [ ] 检查 outputs/ 中的生成文件
- [ ] 用原生应用打开文件确认能正确打开
- [ ] 更新 skills_cookbook_plan.md 检查清单
- [ ] 在全新的虚拟环境中测试

## 资源

- **API 参考**：https://docs.claude.com/en/api/messages
- **Files API**：https://docs.claude.com/en/api/files-content
- **Skills 文档**：https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview

## 项目专属说明

- **聚焦领域**：金融与分析，配合实际的商业应用
- **目标读者**：中级开发者和业务分析师
- **笔记本 1**：已完成并通过测试（文件下载可用）
- **笔记本 2**：金融应用 - 下一个优先项
- **笔记本 3**：自定义 Skills 开发 - 在笔记本 2 之后

## 环境变量

`.env` 中必需：
```bash
ANTHROPIC_API_KEY=your-api-key-here
```

可选（用于进阶示例）：
```bash
ANTHROPIC_BASE_URL=https://api.anthropic.com  # If using proxy
```
