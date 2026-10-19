# Claude Cookbooks 顺序学习计划

这份计划按知识依赖排序，不按仓库目录或发布时间排序。
默认先用 Qwen 网关练习通用模式，再按需学习 Claude 专有功能。
目标是独立完成一个可测试的“资料问答 + 工具调用”应用。

## 1. 如何记录学习状态

在 VS Code 中编辑本文件并保存，即可持久化学习进度。
Markdown 预览用于阅读；勾选时将源码中的 `[ ]` 改为 `[x]`。

- 每课有三个检查项：阅读、实践、验收。
- **未开始**：三个检查项都未勾选。
- **学习中**：已开始阅读或实践，但尚未通过验收。
- **已完成**：三个检查项全部勾选。
- **受阻**：在下方日志写明原因；不要为运行失败勾选验收。
- **暂缓**：写明理由；选修课可以暂缓，不阻塞主线。

当前学习位置：`阶段 0 / 第 00 课`

进度：`已验收 ____ / 主线 22 课（00–21）；选修另计`

完成一课时留下：修改后的练习、测试输入、实际输出、一个失败案例。
不要将密钥、内部资料或私人对话写入本文件或提交到 Git。

## 2. 运行边界与课前检查

先阅读 [项目说明](./README.md) 和 [示例索引](./registry.yaml)。
索引用于查找专题，不是学习顺序。

用 cookbook 专属配置启动：

```powershell
uv sync --python 3.15 --all-extras --locked
uv run --env-file .cookbook.env python -m jupyterlab
```

- 本地项目已固定到 Python 3.15；依赖版本由 `uv.lock` 记录。
- VoyageAI 包当前要求 Python <3.15，本环境跳过安装；相关示例需单独使用兼容环境。
- Windows 下 `pywinpty` 源码构建可能遗漏 ConPTY 运行库；重建环境后按 README 检查。
- 使用项目 `.venv` 对应的内核；先跑一个短文本请求。
- 不改 Claude Desktop、Claude Code、用户或系统环境变量。
- 不覆盖已有 `.env`；网关个人密钥只放在 `.cookbook.env`。
- 不把 Anthropic 密钥用于 Qwen 网关。
- Notebook 里的 Claude 模型名不代表实际执行的模型。
- 先确认网关接受的模型 ID；不要假设它支持所有 Claude 别名。
- `/v1/messages` 兼容不等于工具、beta 功能和响应细节全部兼容。
- `load_dotenv(override=True)` 或显式端点/密钥可能覆盖启动设置。
- 运行前检查这些覆盖项；不要打印密钥来排查。
- 网关长请求优先使用流式；图片请求需要在线视觉节点。
- Voyage、Pinecone、MongoDB、搜索、语音等服务需要独立配置。
- 未安装的依赖按该示例的安装说明处理，不必预装全部第三方组件。
- Notebook 的已有输出只是历史演示，不是本次执行成功的证据。

本计划中的“网关候选”表示适合先验证通用 Messages 调用，
不是对整本 Notebook 可直接运行的认证。
需要专有能力的章节可先读原理，不必购买服务来完成主线。

### 2.1 创建一个独立的入门 Notebook

你已经用 cookbook 配置启动了 JupyterLab，无须再次启动。
如果服务在升级 SDK 前启动过，先停止旧服务，再用上面的命令启动。

1. 在 JupyterLab 左侧选择项目根目录。
2. 点击左上角 `+`，打开 Launcher（启动器）。
3. 在 Notebook 区点击 `Python 3 (ipykernel)`。
4. 将新文件重命名为 `gateway_smoke_test.ipynb`。
5. 每次粘贴代码到一个新代码单元格。
6. 按 `Shift+Enter` 执行当前单元格。

新 Notebook 初始有一个代码单元格。
按 `Shift+Enter` 执行后，可继续在下一个单元格输入。
右上角显示当前内核，但内核名称不是环境验证结果。

### 2.2 第一个单元格：验证项目 Python

复制并执行：

```python
import sys
from pathlib import Path
from importlib.metadata import version

expected_python = Path(r"D:\tutorial\claude-cookbooks\.venv\Scripts\python.exe")
actual_python = Path(sys.executable)
print("当前 Python：", actual_python)
print("Python 版本：", sys.version.split()[0])
print("anthropic 版本：", version("anthropic"))
print("ipykernel 版本：", version("ipykernel"))

if actual_python.resolve() != expected_python.resolve():
    raise RuntimeError("内核不是 cookbook 项目 Python，请按下一节切换内核。")

print("项目内核检查通过")
```

期望 Python 路径是 `D:\tutorial\claude-cookbooks\.venv\Scripts\python.exe`。
本次环境核对得到 `Python 3.15.0`、`anthropic 1.13.0`、`ipykernel 7.4.0`。
以后版本更新可能不同；路径一致才是本步骤的核心标准。

如果路径不一致，在项目 PowerShell 中执行：

```powershell
Set-Location D:\tutorial\claude-cookbooks
uv run python -m ipykernel install --sys-prefix --name cookbook-venv --display-name "Python 3.15 (cookbook .venv)"
```

这个命令将内核定义安装到项目虚拟环境。
它不使用 `--user`，不修改其他应用的 Python 配置。

回到 JupyterLab：

1. 刷新页面，保存当前 Notebook。
2. 选择 `Kernel → Change Kernel…`。
3. 选择 `Python 3.15 (cookbook .venv)`。
4. 重新执行第一个单元格。

若新内核未出现在列表中，重启 cookbook 的 Jupyter 服务。
仍须通过 Python 路径检查，不只检查显示名称。

### 2.3 第二个单元格：验证网关配置

这一步不发网络请求，也不打印密钥。
不调用 `load_dotenv()`，避免误加载原有 Anthropic `.env`。

```python
import os

gateway_url = os.environ.get("ANTHROPIC_BASE_URL", "").rstrip("/")
gateway_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()

print("目标端点：", gateway_url)
print("密钥已配置：", bool(gateway_key))

if gateway_url != "https://qwen.smjtools.com":
    raise RuntimeError("端点不是 cookbook 网关，请检查 Jupyter 的启动命令。")
if not gateway_key or gateway_key == "YOUR_QWEN_GATEWAY_KEY":
    raise RuntimeError("请在 .cookbook.env 中填写你的个人网关密钥。")
if gateway_key.startswith("sk-ant-"):
    raise RuntimeError("检测到 Anthropic 密钥，请不要将它发送到 Qwen 网关。")
if os.environ.get("ANTHROPIC_AUTH_TOKEN"):
    raise RuntimeError("存在额外的 Anthropic auth token，请使用无此变量的独立启动环境。")

print("网关配置检查通过")
```

期望显示目标端点、`密钥已配置： True` 和检查通过。
密钥前缀检查只防止明显误配，不验证网关密钥是否有效。
如果修改了配置文件，必须重启 Jupyter 服务和内核。
仅重新执行单元格不会让旧进程重新读取配置文件。
不要截取或发送配置文件内容来排查。

### 2.4 第三个单元格：发送短文本请求

前两个单元格通过后，再运行下面的代码。
它向你的网关发送固定的公开测试提示。

这里使用 `strata`，与网关仓库的 Messages 测试保持一致。
使用流式接口，以兼容网关等待队列的保活机制。
关闭自动重试，避免排查时重复发送请求。

```python
from anthropic import Anthropic

with Anthropic(
    api_key=gateway_key,
    base_url=gateway_url,
    timeout=180.0,
    max_retries=0,
) as client:
    with client.messages.stream(
        model="strata",
        max_tokens=128,
        messages=[{"role": "user", "content": "Reply with exactly: pong"}],
    ) as stream:
        print("模型回复：", end="", flush=True)
        for text in stream.text_stream:
            print(text, end="", flush=True)
        result = stream.get_final_message()

print()
print("返回模型：", result.model)
print("停止原因：", result.stop_reason)
print("用量：", result.usage)

if not any(block.type == "text" and block.text.strip() for block in result.content):
    raise RuntimeError("请求结束但没有文本，请检查停止原因和输出 token 上限。")
```

运行时，单元格左侧 `[*]` 表示正在等待或生成。
不要因为短时间无输出就反复点击执行。
网关有队列，短请求也可能等待其他任务完成。

**连接验收**：没有异常，且返回非空文本与完成信息。
**提示遵循验收**：文本应为 `pong`；若不同，记录实际结果。
连通成功与严格遵循提示是两项不同的检查。
`max_tokens` 耗尽可能导致截断，并不证明模型不支持请求。

### 2.5 常见问题与学习状态

| 现象 | 先检查什么 | 处理方式 |
|---|---|---|
| `ModuleNotFoundError: anthropic` | 第一个单元格的 Python 路径 | 先切换项目内核，不在错误环境盲目安装 |
| 端点为空或不是网关 | Jupyter 服务如何启动 | 停止旧服务，使用 cookbook 专用命令重启 |
| 密钥未配置或仍是占位符 | 本地 `.cookbook.env` | 填写个人网关密钥，再重启服务；不要公开密钥 |
| 401 / 403 | 网关鉴权与访问规则 | 确认个人密钥有效；403 也可能来自边缘访问限制 |
| 模型不存在 / 请求参数错误 | 网关部署版本及错误信息 | 本例用 `strata`；不要直接换成 Claude 别名 |
| 超时 / 5xx / 服务不可用 | 网关节点、队列及返回错误 | 查看网关监控；不要切换到 Anthropic 自动兜底 |
| 有输出但不是 `pong` | 实际文本和停止原因 | 记录为提示遵循差异，不当作连接失败 |

完成后按 `Ctrl+S` 保存 Notebook。
再用 `Kernel → Restart Kernel…` 重启内核。
按顺序重新执行三个单元格，确认不依赖旧变量。

只有你实际执行成功后，才勾选第 00 课的实践和验收。
本指南已核对项目 Python、SDK 接口和网关测试的模型 ID。
编写指南时未读取你的密钥，也未代你发送真实网关请求。

## 3. 主线：按顺序完成

### 阶段 0：环境与最小调用

#### 00. 建立可重复的运行环境

材料：[项目说明](./README.md)、[开发说明](./CONTRIBUTING.md)。

练习：从项目目录启动 Jupyter，确认内核和网关端点。
用一条不含敏感数据的短提示测试连接。
验收：重启内核后仍可复现；能区分启动错误、鉴权错误和模型错误。

- [X] 阅读
- [X] 实践
- [X] 验收

#### 01. 理解 Messages 的输入与输出

材料：[JSON 提示示例](./misc/how_to_enable_json_mode.ipynb) 的初始化与普通文本调用部分。

练习：先只发送普通文本，再加 system 指令和两轮对话。
观察 content 块、stop_reason、usage，不只读取第一个块。
验收：能解释 model、messages、max_tokens 的作用，并处理非文本内容块。
运行：网关候选；先核对模型 ID 和响应格式。

- [X] 阅读
- [X] 实践
- [X] 验收

### 阶段 1：提示词与可验证输出

#### 02. 从文本提示到 JSON 输出

材料：[JSON 提示示例](./misc/how_to_enable_json_mode.ipynb)。

练习：把一段订单描述转换为 JSON，用解析器验证结果。
验收：至少测试正常、缺字段、格式错误三类输入；不能只凭肉眼判断。
运行：网关候选；提示词 JSON 不等于服务端约束解码。

- [X] 阅读
- [X] 实践
- [X] 验收

#### 03. 改进提示模板

材料：[元提示词](./misc/metaprompt.ipynb)。

练习：为一个固定任务保存初版、改版提示词及同一组测试输入。
验收：能指出改版解决的具体问题，而不是只说“更详细”。
运行：网关候选。

- [X] 阅读
- [X] 实践
- [X] 验收

#### 04. 使用明确的分类规则

材料：[内容审核过滤器](./misc/building_moderation_filter.ipynb)。

练习：改为自己的非敏感文本分类任务，定义类别和边界案例。
验收：相同输入可重复评估；记录错分样本和不确定的情况。
运行：网关候选；后续再读 [完整内容审核流程](./capabilities/content_moderation/guide.ipynb)。

- [ ] 阅读
- [ ] 实践
- [ ] 验收

### 阶段 2：工具调用与应用控制

#### 05. 完成一个工具调用循环

材料：[计算器工具](./tool_use/calculator_tool.ipynb)。

练习：看懂工具 schema、tool_use、执行函数、tool_result、继续对话。
验收：执行成功和执行失败都能返回明确结果；不直接执行模型任意代码。
运行：需验证网关工具调用能力。

- [ ] 阅读
- [ ] 实践
- [ ] 验收

#### 06. 控制工具选择

材料：[工具选择](./tool_use/tool_choice.ipynb)。

练习：对比允许自动选择与要求指定工具的行为。
验收：检查实际返回的工具块；不把参数设置视为执行成功。
运行：需验证网关 tool_choice 支持范围。

- [ ] 阅读
- [ ] 实践
- [ ] 验收

#### 07. 用工具 schema 提取结构化数据

材料：[结构化 JSON 提取](./tool_use/extracting_structured_json.ipynb)。

练习：从本地文本提取实体；先去掉网页抓取依赖，专注提取本身。
验收：校验必填字段、字段类型及未知字段；记录不符合 schema 的输出。
运行：需验证网关工具调用能力；网页部分另需网络及依赖。

- [ ] 阅读
- [ ] 实践
- [ ] 验收

#### 08. 加入类型与参数校验

材料：[Pydantic 工具使用](./tool_use/tool_use_with_pydantic.ipynb)。

练习：为第 05 课工具加入输入校验和明确错误返回。
验收：无效参数不会进入工具执行函数。
运行：需核对 Notebook 使用的 SDK helper 和网关支持。

- [ ] 阅读
- [ ] 实践
- [ ] 验收

#### 09. 整合为一个小型服务助手

材料：[客户服务代理](./tool_use/customer_service_agent.ipynb)。

练习：用虚构订单数据实现查询助手，不接真实业务写操作。
验收：能处理无需工具、一次工具调用、工具失败及连续工具调用。
设置最大工具循环次数，避免无限重试。
运行：需验证网关工具调用能力。

- [ ] 阅读
- [ ] 实践
- [ ] 验收

### 阶段 3：多步骤工作流

#### 10. 先学确定性的工作流

材料：[基础多模型工作流](./patterns/agents/basic_workflows.ipynb)。

练习：分别实现提示链、路由和并行处理。
验收：能画出调用顺序，并说明每一步由程序还是模型决定。
运行：网关候选；同一 Qwen 模型不能证明多模型分工收益。

- [ ] 阅读
- [ ] 实践
- [ ] 验收

#### 11. 将任务拆给工作节点

材料：[编排器与工作节点](./patterns/agents/orchestrator_workers.ipynb)。

练习：把报告任务拆成子任务，再聚合结果。
验收：一个子任务失败时，主流程能明确报告失败，不返回虚假完整结果。
运行：网关候选；本地服务可能排队，并行不一定更快。

- [ ] 阅读
- [ ] 实践
- [ ] 验收

#### 12. 建立评价与改写循环

材料：[评价器与优化器](./patterns/agents/evaluator_optimizer.ipynb)。

练习：让评价器依据固定规则检查输出，设置改写次数上限。
验收：保存原稿、评分和改稿；停止条件不能只依赖模型说“满意”。
运行：网关候选；用程序校验补充模型评价。

- [ ] 阅读
- [ ] 实践
- [ ] 验收

### 阶段 4：知识处理与 RAG

#### 13. 先理解长文摘要

材料：[摘要指南](./capabilities/summarization/guide.ipynb)。

练习：用一份短公开文档对比整段摘要与分段摘要。
验收：检查关键事实遗漏和无来源补充；不要一开始运行全部长文实验。
运行：网关候选；长上下文、文件输入等部分需单独核对。

- [ ] 阅读
- [ ] 实践
- [ ] 验收

#### 14. 实现最小 RAG

材料：[RAG 指南](./capabilities/retrieval_augmented_generation/guide.ipynb) 的 Level 1。

练习：用少量公开资料完成切分、检索、拼上下文和回答。
验收：每条回答可定位到原始材料；无相关材料时说明无法回答。
运行：生成部分为网关候选；原示例还需要 Voyage 等独立依赖。

- [ ] 阅读
- [ ] 实践
- [ ] 验收

#### 15. 比较检索优化策略

材料：[RAG 指南](./capabilities/retrieval_augmented_generation/guide.ipynb) 的 Level 2、Level 3。

练习：对同一测试集比较基础检索、摘要索引和重排。
验收：记录检索指标和请求成本；区分“没检索到”与“回答生成错误”。
运行：生成部分为网关候选；嵌入服务另行配置。

- [ ] 阅读
- [ ] 实践
- [ ] 验收

#### 16. 选择一个业务专题

材料：先选 [分类](./capabilities/classification/guide.ipynb)、
[Text-to-SQL](./capabilities/text_to_sql/guide.ipynb) 或
[知识图谱](./capabilities/knowledge_graph/guide.ipynb) 之一。

练习：复用检索与结构化输出知识，换成自己的公开或虚构数据。
验收：写出输入、输出、失败边界；SQL 只在只读测试库执行。
运行：先核对各自模型、嵌入服务、数据库和 SDK 功能依赖。

- [ ] 阅读
- [ ] 实践
- [ ] 验收

### 阶段 5：评估与回归

#### 17. 理解评估的组成

材料：[构建评估](./misc/building_evals.ipynb)。

练习：分别写程序评分、人工评分说明和模型评分提示。
验收：说明哪些指标可以客观计算，哪些评分依赖判断。
运行：网关候选；模型评分不等于真实答案。

- [ ] 阅读
- [ ] 实践
- [ ] 验收

#### 18. 建立固定测试集

材料：[生成测试用例](./misc/generate_test_cases.ipynb)。

练习：生成候选样本，人工核对后固定至少 10 条用例。
包含成功案例、缺信息案例和工具失败案例。
验收：测试输入与预期结果独立于正在优化的提示词。
运行：网关候选；不要直接把生成结果当作真值。

- [ ] 阅读
- [ ] 实践
- [ ] 验收

#### 19. 做一次有证据的改进

材料：[成本优化](./cost_optimization/cost_optimization.ipynb)。

练习：只改变一个变量，如提示词、检索数量或工具循环上限。
验收：对固定用例记录通过数、延迟和 token 使用；保留失败样本。
运行：读取优化思路即可；Claude 定价和不同模型比较不直接适用于 Qwen。

- [ ] 阅读
- [ ] 实践
- [ ] 验收

### 阶段 6：毕业项目

#### 20. 实现资料问答助手

材料：复用第 05–09、14–18 课，不引入新的大型框架。

练习：用公开资料做 RAG，加一个只读查询工具和结构化输出。
验收：有来源、输入校验、工具循环上限、显式错误和测试集。
至少覆盖“无资料”“工具失败”“格式错误”三种失败情况。

- [ ] 阅读
- [ ] 实践
- [ ] 验收

#### 21. 从干净内核复现

材料：[开发说明](./CONTRIBUTING.md) 和自己的练习记录。

练习：重启内核并从头运行，清理对历史变量和旧输出的依赖。
验收：另一位读者按说明能启动；不依赖你的全局环境或私人密钥。
明确列出模型、依赖、启动命令和已知限制。

- [ ] 阅读
- [ ] 实践
- [ ] 验收

## 4. 主线之后的选修顺序

完成基础评估后再选专题。以下不是 Qwen 网关兼容清单。

| 顺序 | 方向与材料 | 学习目标 | 运行条件 |
|---|---|---|---|
| A | [视觉入门](./multimodal/getting_started_with_vision.ipynb) → [裁剪工具](./multimodal/crop_tool.ipynb) | 图片输入、局部放大、视觉工具循环 | 需验证图片协议与视觉节点 |
| B | [异步编排](./patterns/agents/async_multi_agent_orchestration.ipynb) → [延迟分析](./patterns/agents/latency_multi_agent.ipynb) | 并发、等待、限流与测量 | 网关排队行为可能改变收益 |
| C | [上下文工程](./tool_use/context_engineering/context_engineering_tools.ipynb) → [记忆工具](./tool_use/memory_cookbook.ipynb) | 区分历史、记忆与上下文压缩 | 先读原理；相关 beta 能力需核对 |
| D | [提示缓存](./misc/prompt_caching.ipynb) → [上下文检索](./capabilities/contextual-embeddings/guide.ipynb) | 理解重复前缀与检索质量 | Claude 缓存语义及计费不能直接套用 |
| E | [扩展思考](./extended_thinking/extended_thinking.ipynb) → [思考与工具](./extended_thinking/extended_thinking_with_tool_use.ipynb) | 理解思考预算和工具交互 | Qwen 的推理输出不等于 Claude 思考接口 |
| F | [Agent SDK 入门](./claude_agent_sdk/00_The_one_liner_research_agent.ipynb) → [多代理](./claude_agent_sdk/01_The_chief_of_staff_agent.ipynb) → [可观测性](./claude_agent_sdk/02_The_observability_agent.ipynb) | SDK、子代理、hooks、MCP | 使用独立的正常 Claude 环境；不套用网关启动环境 |
| G | [Managed Agents 入门](./managed_agents/CMA_iterate_fix_failing_tests.ipynb) → [生产设置](./managed_agents/CMA_operate_in_production.ipynb) → [大小模型编排](./managed_agents/CMA_plan_big_execute_small.ipynb) | 服务端代理生命周期、部署、多代理分工与成本权衡 | Anthropic 专有服务，不是 Messages 网关替代品；大小模型编排示例使用新的 `multiagent_20261001` 类型 |
| H | [批处理](./misc/batch_processing.ipynb)、[Admin API](./misc/admin_api.ipynb)、[Skills](./skills/README.md) | 批量作业、管理与专有工具环境 | 需要对应 Anthropic 服务及权限 |
| I | [代理会话安全审查](./managed_agents/CMA_agent_security_review.ipynb) | 从代理会话日志中识别越权访问、凭据使用、数据外传、绕过限制和提示注入，并用证据排序风险 | 使用示例日志练习；读取真实会话需相应权限，审查不能替代网络与权限控制 |
| J | [OpenTelemetry 跟踪](./observability/opentelemetry_tracing.ipynb) | 关联 SDK、Claude API、Managed Agents 与应用自身的 spans，定位延迟和 token 消耗 | 需 Claude API、Managed Agents 和可用的观测后端；API spans 与部分属性处于 beta |

- [ ] A：阅读、实践、验收完成
- [ ] B：阅读、实践、验收完成
- [ ] C：阅读、实践、验收完成
- [ ] D：阅读、实践、验收完成
- [ ] E：阅读、实践、验收完成
- [ ] F：阅读、实践、验收完成
- [ ] G：阅读、实践、验收完成
- [ ] H：阅读、实践、验收完成
- [ ] I：阅读、实践、验收完成
- [ ] J：阅读、实践、验收完成

## 5. 学习日志与阻塞记录

每次学习复制一行。记录真实执行结果，不填写演示 Notebook 的历史结果。

| 日期 | 课号 | 状态 | 实践文件或证据 | 收获 / 阻塞原因 | 下一步 |
|---|---|---|---|---|---|
| 待填写 | 00 | 未开始 | 待填写 | 待填写 | 启动项目内核 |

## 6. 复习检查

- [ ] 能解释：提示词、工具调用、RAG、工作流各解决什么问题。
- [ ] 能区分：模型生成错误、工具执行错误和检索错误。
- [ ] 能说明：为什么已有 Notebook 输出不能证明当前代码正确。
- [ ] 能判断：网关兼容端点与 Claude 专有服务的边界。
- [ ] 能用固定测试集证明改进，而不是只看一次成功回答。
- [ ] 能在不影响 Claude Desktop / Claude Code 的前提下运行 cookbook。
