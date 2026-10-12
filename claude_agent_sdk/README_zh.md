# 使用 Claude Agent SDK 构建强大的智能体

使用 [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python) 构建智能体的配方，从 SDK 核心基础到多智能体编排与生产部署。

## 开始使用

#### 1. 安装 uv、[node](https://nodejs.org/en/download/) 和 Claude Code CLI（如果尚未安装）

```curl -LsSf https://astral.sh/uv/install.sh | sh```

```npm install -g @anthropic-ai/claude-code```

`npm` 步骤是可选的，除非某个笔记本在它自己的前置条件中单独列出了 CLI 安装：`claude-agent-sdk` 包已内置该 CLI。

#### 2. 克隆并配置项目

```git clone https://github.com/anthropics/claude-cookbooks.git```

```cd claude-cookbooks/claude_agent_sdk```

```uv sync```

uv 环境为每个笔记本提供统一内核。首个单元格自行安装依赖的笔记本在任何其他内核上也能运行。

#### 3. 将 venv 注册为 Jupyter 内核，以便在笔记本中使用它

```uv run python -m ipykernel install --user --name="cc-sdk-tutorial" --display-name "Python (cc-sdk-tutorial)"```

#### 4. Claude API 密钥
1. 访问 [platform.claude.com](https://platform.claude.com/dashboard)
2. 注册或登录你的账户
3. 点击“Get API keys”
4. 复制密钥，并以 ```ANTHROPIC_API_KEY=``` 的形式粘贴到你的 `.env` 文件中

#### 5. 配方 02 所需的 GitHub 词元
如果你打算学习配方 02「可观测性智能体」：
1. 在[这里](https://github.com/settings/personal-access-tokens/new)获取 GitHub 个人访问词元
2. 选择使用默认选项的“Fine-grained”词元（公开仓库，无账户权限）
3. 以 `GITHUB_TOKEN="<token>"` 的形式添加到你的 `.env` 文件中
4. 确认你的机器上已运行 [Docker](https://www.docker.com/products/docker-desktop/)

#### 6. 可选：导入配套的智能体模块
要在笔记本之外使用基础配方的配套代码，请从 `claude_agent_sdk/` 目录运行 Python，这样配套包才能作为导入被解析。

## 你将学到什么

通过基础系列，你将接触到：
- **SDK 核心基础**：Python SDK 中的 `query()` 以及 `ClaudeSDKClient` 与 `ClaudeAgentOptions` 接口
- **工具使用模式**：从基础的 WebSearch 到复杂的 MCP 服务器集成
- **多智能体编排**：使用专业化子智能体并进行协调
- **企业级特性**：利用钩子实现合规跟踪与审计留痕
- **外部系统集成**：通过模型上下文协议（MCP）

说明：这些配方假定你对 Claude Code 已有一定程度的熟悉。理想情况下，如果你一直在用 Claude Code 提升编码任务的效率，并希望把它原始的智能体能力用于软件工程之外的任务，这些配方会帮助你入门。

## 基础系列

基础系列带你走过一段旅程，从基础的智能体实现，到能够应对真实世界复杂性的复杂多智能体系统。每个配方都建立在前一个之上，引入新的概念与能力，同时保持实用、可用于生产的实现。

### [00：单行研究智能体](00_The_one_liner_research_agent.ipynb)

用一个仅由几行代码构建的简单而强大的研究智能体开始你的旅程。这个笔记本介绍 SDK 的核心概念，并演示 Claude Agent SDK 如何实现自主的信息收集与综合。

**核心概念：**
- 用 `query()` 与异步迭代实现的基础智能体循环
- 用于自主研究的 WebSearch 工具
- 借助 Read 工具实现的多模态能力
- 用 `ClaudeSDKClient` 管理对话上下文
- 用于智能体专业化的系统提示词

**配套代码：** [﷐0﷑](research_agent/)

### [01：幕僚长智能体](01_The_chief_of_staff_agent.ipynb)

为初创公司 CEO 构建一个全面的 AI 幕僚长，展示面向生产环境的进阶 SDK 特性。这个笔记本演示如何创建具备治理、合规与专业能力的复杂智能体架构。

**所探索的关键特性：**
- **记忆与上下文：** 用 CLAUDE.md 文件保存持久指令
- **输出风格：** 为不同受众定制表达方式
- **规划模式：** 对复杂任务做战略规划而不执行
- **自定义斜杠命令：** 为常见操作提供易用的快捷方式
- **钩子：** 自动化的合规跟踪与审计留痕
- **子智能体编排：** 协调专业化智能体以提供领域专长
- **Bash 工具集成：** 执行 Python 脚本以获得过程性知识和完成复杂计算

**配套代码：** [﷐0﷑](chief_of_staff_agent/)

### [02：可观测性智能体](02_The_observability_agent.ipynb)

通过模型上下文协议把智能体连接到外部系统，从而超越本地能力。把你的智能体从被动的观察者转变为 DevOps 工作流中的主动参与者。

**进阶能力：**
- **Git MCP 服务器：** 13 个以上用于仓库分析与版本控制的工具
- **GitHub MCP 服务器：** 100 个以上用于完整集成 GitHub 平台的工具
- **实时监控：** CI/CD 流水线分析与故障检测
- **智能事件响应：** 自动化的根因分析
- **生产工作流自动化：** 从监控到可执行的洞察

**配套代码：** [﷐0﷑](observability_agent/)

### [03：站点可靠性智能体](03_The_site_reliability_agent.ipynb)

从只读观察走向读写修复。构建一个 SRE 事件响应智能体，它可以调查生产事故、诊断根因、应用修复并记录结果——全部自主完成。

**关键能力：**
- **MCP 工具服务器：** 通过 JSON-RPC 子进程提供 12 个以上用于指标、基础设施、诊断与文档的工具
- **Prometheus 集成：** 用 PromQL 查询监控错误率、时延与数据库连接
- **读写式修复：** 编辑配置文件、重启 Docker 服务并验证修复效果
- **安全钩子：** 校验写操作的 PreToolUse 钩子（连接池大小范围、配置合理性检查）
- **端到端事件生命周期：** 从检测到修复再到事后复盘文档
- **生产扩展：** 通过条件式 MCP 工具注册，可选集成 PagerDuty 与 Confluence

**配套代码：** [﷐0﷑](site_reliability_agent/)

### [04：从 OpenAI Agents SDK 迁移](04_migrating_from_openai_agents_sdk.ipynb)

把一个已有的 OpenAI Agents SDK 应用移植到 Claude Agent SDK，在一个费用审批智能体示例中逐一映射两边的基本构件，同时让两个 SDK 都在实际运行。

**核心概念：**
- **基本构件映射：** 把 `@function_tool`、护栏和 `Runner.run` 对应到 Claude 侧的等价物
- **单智能体移植：** 自定义工具、输入/输出护栏、多轮会话与可持久恢复
- **客户端与 `query()`：** 何时使用有状态的 `ClaudeSDKClient`，何时使用无状态的 `query()`
- **可观测性：** 把 SDK 的 OpenTelemetry 导出接入已有的技术栈

### [05：构建会话浏览器](05_Building_a_session_browser.ipynb)

构建用户在智能体产品中期待的对话历史侧边栏，直接读取 SDK 存储在磁盘上的会话记录，而不必自己写解析器。

**核心概念：**
- **列出会话：** 带分支、标题和最后修改时间元数据的分页会话列表
- **读取记录：** 重放某个已存储会话的消息，无需启动智能体
- **组织历史：** 重命名、打标签并筛选会话
- **分叉：** 在任意位置为会话建立分支，并把分叉作为一次实时 `query()` 调用继续运行

**配套代码：** [﷐0﷑](session_browser_demo/)

### [06：漏洞检测智能体](06_The_vulnerability_detection_agent.ipynb)

构建一个漏洞发现智能体：对 C 语言目标进行威胁建模，用内置文件工具搜寻内存安全缺陷，并把发现分诊整理成审阅者可以采取行动的报告。

**核心概念：**
- **威胁建模：** 先自举再访谈的 `ClaudeSDKClient` 会话，产出 `THREAT_MODEL.md`
- **智能体式发现循环：** 使用内置的 `Read`/`Grep`/`Glob` 工具，而不是自行实现文件访问
- **串联阶段：** 分别执行发现、分诊与报告的 `query()` 调用，输出符合模式的 JSON

**配套代码：** [﷐0﷑](vulnerability_detection_agent/)

### [07：托管你的智能体](07_Hosting_the_agent.ipynb)

把配方 00 的研究智能体部署到三个运营成熟度层级，每个层级都使用相同的容器镜像和 HTTP 接口。

**核心概念：**
- **Docker：** 面向开发循环和内部工具的本地与单虚拟机托管
- **Modal：** 带 URL、可缩容到零的托管无服务器服务
- **Kubernetes：** 在你自己的集群中进行多租户部署
- **可移植接口：** 三个层级使用完全相同的智能体代码、镜像和 HTTP 接口

**配套代码：** [﷐0﷑](hosting/)

### [08：用动态工作流大规模编排子智能体](08_Dynamic_workflows.ipynb)

突破单个上下文窗口所能协调的范围。从 Agent SDK 触发动态工作流：Claude 为你的任务编写一个 JavaScript 编排脚本，运行时在后台跨一组并行子智能体执行它。

**核心概念：**
- **子智能体与工作流：** 计划由谁持有：模型的上下文，还是确定性脚本
- **从 SDK 触发工作流：** `Workflow` 工具、`allowed_tools` 以及流式输出运行进度
- **扇出 + 对抗性验证：** 每条论断并行分配一个验证者，其结论生效前先由质疑者智能体挑战
- **阅读生成的脚本：** `agent()`、`parallel()`、`pipeline()`、阶段以及结构化输出模式

## 独立配方

独立的、以任务为形状的配方。每个配方都有自己的目录，其中包含笔记本及所有支持文件。

### [构建定时仓库评审器](scheduled_repository_reviewer/scheduled_repository_reviewer.ipynb)

把重复性的评审苦活变成由你掌控的无人值守任务。构建一个只读评审智能体，按计划评审仓库，并在各次运行之间恢复其会话，使一次完整的基线评审之后跟着简短的跟进评审；并通过符合模式校验的字段（回显上次评审的 id 与发现项）证明这种连续性。笔记本手动运行前两个周期，最后用配套脚本 [﷐0﷑](scheduled_repository_reviewer/scheduled_review.py) 把评审器设为定时任务。

**核心概念：**
- **只读智能体：** `tools` 决定存在哪些内置工具，`allowed_tools` 决定哪些工具无需询问即可运行；把两者都限制为 `Read`、`Glob` 和 `Grep`，智能体就没有任何写工具
- **无人值守权限模式：** `permission_mode="dontAsk"` 配合预先批准的工具，再用 `max_turns` 和 `max_budget_usd` 限制单次运行可消耗的轮次与花费
- **可恢复会话带来的连续性：** 从 `ResultMessage` 捕获 `session_id`，在各次调用之间持久保存，并在下次运行时传入 `resume`
- **符合模式校验的连续性：** 跟进评审的 `output_format` 模式要求回复回显上次评审的 id 与发现项 id，于是恢复链接成为可以断言的字段
- **类型化的失败路径与可检索的输出：** `VERDICT:` 行取自结构化回复自身的字段，完成行只在经过验证的成功之后打印，而对 `ResultError` 的窄范围捕获让超限运行以 `REVIEW-RUN-INCOMPLETE` 非零退出

## 背景
### Claude Agent SDK 的演进

Claude Code 已成为 Anthropic 最成功的产品之一，但这不仅是因为它 SOTA 的编码能力。它真正的突破在于更根本的一点：**Claude 极其擅长智能体式工作**。

让 Claude Code 出众的不只是代码理解能力，而是以下能力：
- 自主把复杂任务拆解为可管理的步骤
- 有效地使用工具，并就使用哪个工具、何时使用做出明智决策
- 在长时间运行的任务中保持上下文与记忆
- 从错误中优雅恢复，并在需要时调整方法
- 知道何时该请求澄清，何时该基于合理假设继续推进

这些能力使 Claude Code 成为最接近 Claude 原始智能体能力“裸金属”运行框架的东西：一个极简但完整且精巧的接口，让模型的能力以最少的开销充分展现。

### 超越编码：智能体构建者的工具箱

它最初是 Anthropic 工程师为加速开发工作流而构建的内部工具，而 SDK 的公开发布揭示了意想不到的潜力。在 Claude Agent SDK 及其 GitHub 集成发布之后，开发者开始把它用于远超编码范畴的任务：

- **研究智能体**：跨多个来源收集并综合信息
- **数据分析智能体**：探索数据集并生成洞察
- **工作流自动化智能体**：处理重复性的业务流程
- **监控与可观测性智能体**：监视系统并响应问题
- **内容生成智能体**：创建并打磨各种类型的内容

规律很清楚：SDK 无意间已成为一个高效的智能体构建框架。它为处理软件开发复杂性而设计的架构，被证明非常适合通用智能体的创建。

本配方系列演示如何利用 Claude Agent SDK 为任何领域或用例构建高效的智能体，从简单自动化到复杂企业系统。

## 贡献

发现了问题或有建议？请提交 issue 或发起 pull request！
