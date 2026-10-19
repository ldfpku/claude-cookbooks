# 自托管沙箱已迁移

这些示例现在位于 Claude Quickstarts 仓库中：

**[claude-quickstarts/managed-agents/self-hosted-sandboxes](https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/self-hosted-sandboxes)**

它们是可直接运行的应用，而不是笔记本，而可直接运行的应用应放在 [claude-quickstarts](https://github.com/anthropics/claude-quickstarts) 中。本仓库只保留笔记本演示。

## 如果你配置过旧版本

整体形态没有变：自托管环境就是一个工作队列，由你自己的计算资源从中领取会话。迁移中有六处变化：

- 两个目录被重命名。`cf/` 改为 `cloudflare-containers/`，`cf-worker/` 改为 `cloudflare-worker/`。`daytona/`、`modal/` 和 `vercel/` 保留了原名。Quickstart 新增了 `docker-memory/` 和 `archil/`。
- 智能体和环境现在以文件定义，用 [`ant apply`](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/apply) 创建。五个由 webhook 启动的提供方共用一对文件，位于 `webhook-demo/`。你不再需要在 Console 中手动创建环境，但仍需在那里签发它的环境密钥。
- `docs/usage-guide.md` 和 `docs/upgrade-guide.md` 已删除。每个提供方的 README 就是它自己的操作手册：设置、部署、注册 webhook、测试。
- 在 Daytona、Modal 和 Vercel 上，沙箱不再持有环境密钥。每个沙箱会获得一个会话级密钥，未携带密钥到达的工作项会被拒绝。`cloudflare-containers/` 仍必须把密钥传入容器，因此在设置 `ALLOW_ENVIRONMENT_KEY_IN_SANDBOX` 之前它会拒绝所有工作。其 README 说明了这种取舍何时可以接受。
- `@anthropic-ai/sdk` 和 `anthropic` 的 SDK 最低版本从 0.97 提升到 0.124，因为会话级密钥是从该版本开始提供的。
- 此处 `docker/` 镜像曾为 MongoDB Atlas cookbook 打包了 `pymongo`。该镜像留在了本仓库，并移动到 [`mongodb_on_cma/self_hosted_sandbox/`](../mongodb_on_cma/self_hosted_sandbox/)，与该笔记本其余支持代码放在一起。Quickstart 中的 `docker/` 是不含它的通用版本。

曾位于此处的代码的最后一个版本在 [`a4b0d89`](https://github.com/anthropics/claude-cookbooks/tree/a4b0d89061bc65769fea7947c080b3b11d938515/managed_agents/self_hosted_sandboxes)。
