# 第 1 档 — 本地 Docker

在本地运行共享镜像。有两条路径：

## 临时式（无服务器）

一个提示词、一个进程，然后退出。适合任务型工作（批处理、一次性分析），即没有需要恢复的会话的场景。

```bash
cd claude_agent_sdk/
docker build -f hosting/Dockerfile -t research-agent .
docker run --rm \
  -e ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
  -e PROMPT="What is the Claude Agent SDK?" \
  research-agent
```

## 混合式（带服务器）

启动 FastAPI 服务器，并把 `./sessions` 挂载到 `/data`，这样会话可以在容器重启后保留。

```bash
cd claude_agent_sdk/hosting/docker/
docker compose up --build
```

然后，在另一个 shell 中：

```bash
curl -N -X POST http://localhost:8000/sessions/demo-1/messages \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"What are the latest AI agent trends?"}'

# Follow-up — the agent remembers the first turn:
curl -N -X POST http://localhost:8000/sessions/demo-1/messages \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"Tell me more about the second one."}'

curl http://localhost:8000/health
```

停止容器，再次执行 `docker compose up`，再发送一条追问——智能体仍保有上下文，因为 `./sessions` 持久化了 `/data`。
