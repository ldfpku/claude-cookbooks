# Claude Managed Agents cookbooks

Claude Managed Agents 是 Anthropic 的托管运行时，用于有状态、可使用工具的智能体。你一次性定义好智能体和沙箱环境，然后在会话中运行它们，文件、工具状态和对话都跨轮次持久化。这些教程完整演示了整个过程。

## Managed Agents 上的 MongoDB

想让智能体接上一个真正的数据库——用于检索、图遍历，并作为它的记录系统？**[﷐0﷑](CMA_with_mongodb_atlas.ipynb)** 是整合后的 cookbook：把 MongoDB 接入 CMA 智能体的三种方式（以及每条通路上凭证存放在哪里），四种检索模式（向量 / 全文 / 混合 / 图）作为可提取的构件，以及一个端到端的人工介入欺诈审核智能体，由 Atlas 充当记录系统与审计中枢。

## 应用类 cookbook

- **[data_analyst_agent.ipynb](data_analyst_agent.ipynb)** 构建一个
  分析师智能体，用 pandas 和 plotly 把 CSV 变成叙述性的 HTML 报告。你会配置环境和智能体、挂载数据集、流式读取运行过程，并取回生成的产物。
- **[slack_data_bot.ipynb](slack_data_bot.ipynb)** 把那个智能体包装成
  一个 Slack 机器人。提及它并附上 CSV，就能在帖子线程内拿到报告；回复会继续同一个会话。
- **[sre_incident_responder.ipynb](sre_incident_responder.ipynb)** 把
  Managed Agents 放到值班响应链路上：一次寻呼告警开启一个会话，智能体进行调查并开一个 PR，然后在合并前暂停等待人工批准。你会接好告警 webhook、挂载一个 Skill 和自定义工具，并在 Console 中查看整次运行。

## 教程系列

端到端的教程，通过真实工作流讲解 Managed Agents 的 API 面。没有严格的阅读顺序，但 `CMA_iterate_fix_failing_tests.ipynb` 是个好的入口，它介绍其余各篇所依赖的每一种 API 形态。

| 笔记本 | 它教什么 |
| --- | --- |
| [﷐0﷑](CMA_iterate_fix_failing_tests.ipynb) | 在一个失败的测试套件上做“执行 → 观察 → 修复”循环。入口笔记本：以让一个有缺陷的包转绿为线索，介绍智能体 / 环境 / 会话、文件挂载和流式事件循环。|
| [﷐0﷑](CMA_orchestrate_issue_to_pr.ipynb) | 通过一个模拟的 `gh` CLI 走完 issue → 修复 → PR → CI → 评审 → 合并。多轮引导、从 CI 失败和评审意见中在链条中途恢复。侧栏演示如何把文件挂载换成针对真实仓库的 `github_repository` 资源。|
| [﷐0﷑](CMA_explore_unfamiliar_codebase.ipynb) | 在不熟悉的代码库中扎根，并埋有一个过时文档的陷阱。侧栏演示如何通过 `sessions.resources.add` 给运行中的会话添加资源。|
| [﷐0﷑](CMA_gate_human_in_the_loop.ipynb) | 通过自定义工具 `decide()` / `escalate()` 实现人工介入的费用审批。涵盖自定义工具往返模式、`requires_action` 空闲弹回，以及并行工具使用的去重。|
| [﷐0﷑](CMA_with_mongodb_atlas.ipynb) | **MongoDB Atlas** 端到端：三条连接通路（宿主侧自定义工具、自托管沙箱、自托管 MCP），四种检索模式（向量 / 全文 / 倒数排名融合混合 / `$graphLookup`），以及一个人工介入的欺诈审核智能体，把裁决和只追加的审计轨迹记录在同一个集群里。通过 `requires_action` 门控在高风险案例上暂停；展示了面向 CI 的自动解除门控和面向生产环境的 webhook 交接。|
| [﷐0﷑](CMA_prompt_versioning_and_rollback.ipynb) | 服务端提示词版本管理：创建 v1，对照带标签的测试集评估，发布 v2，检测回归，并通过把会话固定到版本 1 实现回滚。涵盖 `agents.update`、`sessions.create` 上的版本固定，以及当提示词不是代码时评审门控该移到何处。|
| [﷐0﷑](CMA_operate_in_production.ipynb) | 生产环境配置：MCP 工具集、用于存放每个终端用户凭证的密钥库、面向人工介入和成本监督的 `session.status_idled` 与 `session.budget_reached` webhook 模式（无需长连接），用于数据驻留的 `inference_geo` 固定，以及资源生命周期的 CRUD 动词。|
| [﷐0﷑](CMA_remember_user_preferences.ipynb) | 记忆存储：一个购物智能体在一次会话中学到客户偏好，并在下一次会话中回忆起来。涵盖 `memory_stores.create`、带逐附件 `instructions` 的 `resources` 附件、从你自己的应用查看和预置记忆，以及把每客户读写存储与品牌级只读存储结合使用。|
| [﷐0﷑](CMA_coordinate_specialist_team.ipynb) | 用 `multiagent` 协调器配置组建异构团队：一个协调器运行三个专家（网络搜索研究员、读文件的图书馆员、基于规则的定价员），用限定范围的工具集拼出一份销售提案。涵盖 `multiagent` 字段、`thread_created` / `thread_message_received` 事件类型、为什么按角色限定工具范围很重要，以及协调器在写作前咨询的 `advisor` 名册条目。|
| [﷐0﷑](CMA_watch_subagents_live.ipynb) | 一个可以实时观看的课程规划团队。涵盖按线程的 `event_deltas`（让子智能体文本实时流式输出）、会话创建时的 `initial_events`、按智能体设置的模型 `effort` 作为成本抓手，以及无版本的 `agents.update`。建立在 coordinate-specialist-team 的这些形态之上。|
| [﷐0﷑](CMA_plan_big_execute_small.ipynb) | 协调器模式的经济学：前沿协调器把耗词元大量的网络阅读交给廉价的并行工作者，并与一个严谨度相当的前沿模型单干对照组比较，用按线程的 `usage.list_cost` 计量和会话 `budget` 作为扇出护栏。|
| [﷐0﷑](CMA_verify_with_outcome_grader.ipynb) | 用成果构建一个评分与修改循环：写作者起草一份带引用的研究简报，一个无状态评分器抓取每个 URL 并对照评分细则核查每条引文，反馈推动修改直到简报通过。涵盖 `user.define_outcome`、`span.outcome_evaluation_*` 事件，以及如何写一份评分器可据此执行的评分细则。|
| [﷐0﷑](CMA_consult_an_advisor.ipynb) | 一个中档工作智能体，通过 `advisor` 名册条目在轮次中途咨询一个更强的模型。涵盖 `multiagent.agents` 中的 `{"type": "advisor"}` 条目、主流程上的 `anthropic.advisor` 线程生命周期、来自 advisor 线程 `usage` 的每次咨询成本，以及脱敏的交付分支。|
| [﷐0﷑](CMA_cap_session_spend.ipynb) | 对单个会话施加支出上限。涵盖 `sessions.create` 上的 `budget` 字段、`session.usage` 快照事件和 `usage.list_cost`、`budget_reached` 暂停，以及用 `sessions.update` 提高、降低和取消上限。|
| [﷐0﷑](CMA_use_skills_from_a_repo.ipynb) | 会话开始时从挂载仓库根目录的 `.claude/skills/` 发现 Skill，智能体上不需要 `skills` 字段。涵盖扫描器期望的目录布局、先读再遵循的协议，以及生命周期规则（Skill 上限、单次扫描、嵌套的惰性发现）。|
| [﷐0﷑](CMA_pin_inference_geo.ipynb) | 在智能体定义上实现数据驻留：`model.inference_geo` 固定、该固定在何处生效、它与工作区 `allowed_inference_geos` 策略的相互作用，以及用 `agent_with_overrides` 做单次会话的地域覆盖。|

流式事件循环在 iterate 笔记本中逐行讲解，然后抽取为 `utilities.stream_until_end_turn`，这样其余笔记本可以直接导入它，而不必重复那段 `match ev.type:` 代码块。门控笔记本和 MongoDB cookbook 是例外：它们把循环保留在内联位置，因为使用自定义工具的智能体除了 `requires_action` 空闲弹回之外还要处理 `end_turn`，而那个辅助函数没有覆盖。

## 开始使用

在环境中设置 `ANTHROPIC_API_KEY`，然后在 Jupyter 中打开 `data_analyst_agent.ipynb`，自上而下运行各单元格。每个笔记本都会安装自己的依赖，并提示输入所需的凭证。`CMA_orchestrate_issue_to_pr.ipynb` 中从 issue 到 PR 的编排侧栏、`CMA_operate_in_production.ipynb` 中基于密钥库的 MCP 示例，以及 `CMA_use_skills_from_a_repo.ipynb` 还需要设置 `GITHUB_TOKEN`（具有公共仓库读取权限的细粒度 PAT 就够了）。`CMA_with_mongodb_atlas.ipynb` 中的 MongoDB cookbook 还需要把 `MONGO_URI` 设置为 Atlas SRV 连接字符串（M0 免费集群即可）；提供商密钥 —— `MDB_ATLAS_API_KEY` 或 `VOYAGE_API_KEY` —— 是可选的，只用于启用实时嵌入和重排序通路。

所有 cookbook 的示例数据 —— 应用类 cookbook 的输入 CSV 和配套资源，以及教程系列读取的埋设陷阱数据 —— 都位于 `example_data/` 下。目录地图见 [﷐1﷑](example_data/OVERVIEW.md)。

## 可运行的应用

本目录存放笔记本。基于 Managed Agents 构建的完整应用，例如 Slack 和 Linear 机器人、Sentry 分诊智能体、公路旅行规划器、MCP 服务器，以及曾经位于此处的自托管沙箱变体，都在 [claude-quickstarts/managed-agents](https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents) 中。
