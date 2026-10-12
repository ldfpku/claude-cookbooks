# 构建高效智能体 Cookbook

这是 Erik Schluntz 与 Barry Zhang 所著 [Building Effective Agents](https://anthropic.com/research/building-effective-agents) 的参考实现。

本仓库包含博文中讨论的常见智能体工作流的最小化示例实现：

- 基本构件
  - 提示词链（Prompt Chaining）
  - 路由（Routing）
  - 多 LLM 并行化
- 高级工作流
  - 编排器-子智能体（Orchestrator-Subagents）
  - 评估器-优化器（Evaluator-Optimizer）

## 开始使用
有关详细示例，请查看 Jupyter 笔记本：

- [基本工作流](basic_workflows.ipynb)
- [评估器-优化器工作流](evaluator_optimizer.ipynb)
- [编排器-工作者工作流](orchestrator_workers.ipynb)
- [异步多智能体编排](async_multi_agent_orchestration.ipynb)
- [时延压力与预算约束下的多智能体团队](latency_multi_agent.ipynb)
