# Slack × Claude Managed Agents 已迁移

该示例现在位于 Claude Quickstarts 仓库中：

**[claude-quickstarts/managed-agents/slack](https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/slack)**

它是一个可运行的应用而非笔记本，而可运行应用属于 [claude-quickstarts](https://github.com/anthropics/claude-quickstarts)。本仓库保留笔记本演示，包括 [`slack_data_bot.ipynb`](../slack_data_bot.ipynb)。

## 如果你配置过旧版本

应用行为相同。迁移中有三处变化：

- 智能体与环境在 `agents/slack-assistant/*.yaml` 中定义，并用 `./agents/setup.sh` 和 [`ant` CLI](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/quickstart) 创建。`bun run setup` 已移除。
- Anthropic webhook 路由是 `/managed-agents/webhook`，不再是 `/cma-webhook`。请在 Claude Console → Manage → Webhooks 中更新端点 URL。
- 配置从 `.env` 读取，不再是 `.env.local`。

在此存放的最后一版代码位于 [`a97b9a2`](https://github.com/anthropics/claude-cookbooks/tree/a97b9a2dc300635f0c26b5e05d0b54bbe0279ee5/managed_agents/slack)。
