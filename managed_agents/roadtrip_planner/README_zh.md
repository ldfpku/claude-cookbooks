# 公路旅行规划器已迁移

该示例现在位于 Claude Quickstarts 仓库中：

**[claude-quickstarts/managed-agents/roadtrip-planner](https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/roadtrip-planner)**

它是一个可运行的应用，而不是笔记本，可运行的应用应放在 [claude-quickstarts](https://github.com/anthropics/claude-quickstarts) 中。本仓库保留笔记本演示，包括 [﷐0﷑](../CMA_coordinate_specialist_team.ipynb) 和 [﷐1﷑](../CMA_watch_subagents_live.ipynb)，它们以笔记本形式覆盖了同样的 `multiagent` 和 `event_deltas` 功能。

## 如果你配置过旧版本

该应用演示同样的四项功能。迁移过程中有三点变化：

- 两个智能体、环境和密钥库在 `agents/` 目录下的 YAML 中定义，并通过 `./agents/setup.sh` 和 [﷐2﷑ CLI](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/quickstart) 创建。`npm run setup` 和 `npm run teardown` 已取消。拆除命令是 `./agents/teardown.sh`。
- 配置从 `.env` 读取，而不是 `.env.local`，并且资源 ID 命名为 `CLAUDE_*`（`CLAUDE_VAULT_ID`、`CLAUDE_AGENT_ID`），不再是 `ROADTRIP_PLANNER_*`。
- 目录是 `roadtrip-planner`，带连字符。

曾位于此处的代码的最后一个版本在 [﷐0﷑](https://github.com/anthropics/claude-cookbooks/tree/a97b9a2dc300635f0c26b5e05d0b54bbe0279ee5/managed_agents/roadtrip_planner)。
