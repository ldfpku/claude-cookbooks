# 第 2 层 — Modal

通过 `modal.Sandbox` 在 [Modal](https://modal.com) 上运行**同一个** `hosting/Dockerfile` 镜像。你可以获得公开的 HTTPS URL、缩容到零，并且无需管理基础设施。

## 前置条件

```bash
pip install modal
modal setup            # opens a browser to authenticate
modal secret create anthropic ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY"
```

## 部署

```bash
cd claude_agent_sdk/
python hosting/modal/modal_app.py
```

这会在 Modal 上远程构建 Dockerfile（构建上下文 = `claude_agent_sdk/`，与本地相同），启动一个运行 `serve` 的沙箱，并打印一个隧道 URL。

## 与它对话

部署脚本会打印一行 `url:` 和一行 `token:`。隧道 URL 是公开的，因此服务器在消息端点上要求提供承载令牌（只有 `/health` 是开放的）：

```bash
curl -N -X POST "$MODAL_URL/sessions/demo-1/messages" \
  -H "Authorization: Bearer $MODAL_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"What are the latest AI agent trends?"}'
```

## 持久化

默认情况下，`modal_app.py` 会在 `/data` 挂载一个 `modal.Volume` —— 与第 1 层使用 `CLAUDE_CONFIG_DIR` 的技法相同。会话记录在沙箱重启后依然存在。

> **说明：** `modal.Volume` 有显式的提交语义。如果你的工作负载有多个
> 沙箱并发写入大量会话并出现写入丢失，
> 请改用由 Modal `Dict` 或外部存储支撑的 [﷐1﷑](https://code.claude.com/docs/en/agent-sdk/session-storage)
> —— 第 3 层也使用这种方式。

## 存活检测

Modal 会让沙箱一直运行，直到传给 `Sandbox.create` 的 `timeout=` 到期；它不会探测 `GET /health`。如果沙箱内的服务器死亡，沙箱仍保持运行，请求会失败，直到超时把它回收。对于比演示更长期的场景，请把你自己的监控指向 `/health`，并在它停止响应时重建沙箱。

## 拆除

```bash
python hosting/modal/teardown.py
```

停止沙箱并删除卷，以免为闲置资源付费。
