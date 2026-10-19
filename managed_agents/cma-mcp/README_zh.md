# Managed Agents MCP 服务器已迁移

该示例现在位于 Claude Quickstarts 仓库中：

**[claude-quickstarts/managed-agents/mcp-server-typescript](https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/mcp-server-typescript)**

它是一个可运行的应用，而不是笔记本，可运行的应用应放在 [claude-quickstarts](https://github.com/anthropics/claude-quickstarts) 中。本仓库只保留笔记本演示。

## 如果你配置过旧版本

九个工具和两种传输方式的工作方式完全相同。迁移过程中有五点变化：

- 目录是 `mcp-server-typescript`，不再是 `cma-mcp`。如果你曾用绝对路径注册 stdio 服务器，请在新位置重新注册。
- 承载令牌变量是 `MANAGED_AGENTS_MCP_TOKEN`，不再是 `CMA_MCP_TOKEN`。它必须至少 32 个字符，否则 HTTP 服务器拒绝启动。
- HTTP 服务器默认绑定 `127.0.0.1`。旧版本监听所有网络接口。要从其他地址提供服务，请设置 `HOST`，并在 `ALLOWED_HOSTS` 中列出公开主机名。带有其他 `Host` 请求头的请求会被拒绝。
- `ALLOWED_AGENT_IDS` 是新引入的。未设置时，令牌可以访问工作区中的每个智能体，与之前相同。将其设置为逗号分隔的列表，即可把服务器限制在这些智能体内。
- 环境在 `environment.yaml` 中定义，并使用 [`ant` CLI](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/quickstart) 创建。内联的 `--config` 命令已取消。

曾位于此处的代码的最后一个版本在 [`6b671ef`](https://github.com/anthropics/claude-cookbooks/tree/6b671ef60ada2a8d3b0c07cadb424172da5135f5/managed_agents/cma-mcp)。
