# Sentry × Claude Managed Agents 已迁移

该示例现在位于 Claude Quickstarts 仓库中：

**[claude-quickstarts/managed-agents/sentry](https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/sentry)**

它是一个可运行的应用，而不是笔记本，可运行的应用应放在 [claude-quickstarts](https://github.com/anthropics/claude-quickstarts) 中。本仓库只保留笔记本演示，包括 [`sre_incident_responder.ipynb`](../sre_incident_responder.ipynb)。

## 如果你配置过旧版本

定时分诊的运行方式完全相同。迁移过程中有两点变化：

- 密钥库、环境和智能体在 `agents/sentry-triage/*.yaml` 中定义，并通过 `./agents/setup.sh` 和 [`ant` CLI](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/quickstart) 创建。`setup_agent.py`、`update_agent.py` 和 `agent_config.py` 已取消。要修改智能体，请编辑 YAML 并重新运行 `./agents/setup.sh`，该脚本也会把部署重新固定到新版本。
- `COOKBOOK_MODEL` 覆盖项已取消。请在 `agents/sentry-triage/agent.yaml` 中设置 `model`。

曾位于此处的代码的最后一个版本在 [`a97b9a2`](https://github.com/anthropics/claude-cookbooks/tree/a97b9a2dc300635f0c26b5e05d0b54bbe0279ee5/managed_agents/sentry)。
