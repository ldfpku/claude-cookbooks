# 托管研究智能体

该目录通过三个层级部署来自 [`00_The_one_liner_research_agent.ipynb`](../00_The_one_liner_research_agent.ipynb) 的研究智能体：本地 Docker、Modal 和 Kubernetes。智能体、容器镜像和 HTTP 接口在三个层级中 **相同**——只有容器周围的运行机制发生变化。

请阅读 [`07_Hosting_the_agent.ipynb`](../07_Hosting_the_agent.ipynb) 了解完整叙述。

## 接口约定

三个层级都遵循这一约定。Kubernetes 网关依据它进行路由。

```
The agent image exposes:

  GET  /health
       → 200 {"status": "ok"}
       Liveness check for orchestration.

  POST /sessions/{session_id}/messages
       Body: {"prompt": "<user message>"}
       → 200 text/event-stream
         event: message  — data is a serialized SDK message
                           (SystemMessage | AssistantMessage | ResultMessage)
         event: done     — turn complete
         event: error    — data is {"message": "..."}
       Resumes the session if it exists, creates if not.
       Stream contains ONLY the new turn's events, not history.

  session_id MUST match ^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$. Invalid → 400.

  Port: 8000
  Required env: ANTHROPIC_API_KEY
  Optional env: MODEL (default: claude-sonnet-4-6),
                CLAUDE_CONFIG_DIR (default: /data — mount this for persistence),
                AGENT_AUTH_TOKEN (when set, /sessions/* requires
                                  Authorization: Bearer <token>; /health stays open)

  ⚠️  SECURITY: This server has no authentication by default. It MUST sit
      behind a gateway/proxy that (1) authenticates callers and (2) only
      forwards session_ids that belong to the authenticated caller. Do not
      expose port 8000 to the internet directly.

      If there is no gateway (tier 2: Modal hands out a public tunnel), set
      AGENT_AUTH_TOKEN. It is the minimal stand-in, not a replacement — it
      does not scope session_ids to callers.

  LIFECYCLE: The server does not self-terminate. The orchestrator is
      responsible for killing idle containers.
```

## 目录结构

```
hosting/
  README.md            ← you are here
  Dockerfile           ← shared agent image (build context = claude_agent_sdk/)
  Dockerfile.dockerignore
  server.py            ← FastAPI + SSE server (the hybrid path)
  run_once.py          ← ephemeral path: one prompt, print result, exit
  entrypoint.sh        ← dispatches: ephemeral run vs. start server
  requirements.txt
  .env.example         ← ANTHROPIC_API_KEY, MODEL
  docker/              ← Tier 1: local Docker / docker-compose
  modal/               ← Tier 2: Modal Sandbox
  kubernetes/          ← Tier 3: pod-per-session on your own k8s cluster
```

## 构建

Docker 构建上下文是**父**目录（`claude_agent_sdk/`），而不是 `hosting/`，因为镜像需要在 `hosting/` 之外包含 `research_agent/` 和 `utils/`：

```bash
cd claude_agent_sdk/
docker build -f hosting/Dockerfile -t research-agent .
```

> 构建使用同级的 `Dockerfile.dockerignore`（注意带前缀的名称），
> 这需要 BuildKit——Docker 23.0+ 和 Docker Desktop 的默认构建器。
> 在较旧引擎上，请用 `DOCKER_BUILDKIT=1` 执行构建。
