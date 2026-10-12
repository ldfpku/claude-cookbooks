# Linear × Claude Managed Agents 已迁移

该示例现在位于 Claude Quickstarts 仓库中：

**[claude-quickstarts/managed-agents/linear](https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/linear)**

它是一个可运行的应用，而不是笔记本，可运行的应用应放在 [claude-quickstarts](https://github.com/anthropics/claude-quickstarts) 中。本仓库只保留笔记本演示。

## 如果你配置过旧版本

桥接的工作方式完全相同。迁移过程中有四点变化：

- 智能体和环境在 `agents/linear-assistant/*.yaml` 中定义，并通过 `./agents/setup.sh` 和 [﷐2﷑ CLI](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/quickstart) 创建。`bun run setup` 已取消。
- Anthropic 的 Webhook 路由是 `/managed-agents/webhook`，不再是 `/cma-webhook`。请在 Claude Console → Manage → Webhooks 中更新端点 URL。
- 配置从 `.env` 读取，而不是 `.env.local`。
- 第一个安装该智能体的 Linear 工作区拥有这个桥接。除非你在 `LINEAR_ALLOWED_ORG_IDS` 中列出其他工作区，来自任何其它工作区的安装都会被拒绝。旧版本允许任何能访问服务器的工作区安装它。

曾位于此处的代码的最后一个版本在 [﷐0﷑](https://github.com/anthropics/claude-cookbooks/tree/a97b9a2dc300635f0c26b5e05d0b54bbe0279ee5/managed_agents/linear)。
