# 层级 3 — Kubernetes（每会话一个 pod）

> 本文是 [Agent SDK 托管 cookbook](../../07_Hosting_the_agent.ipynb) 的一部分。
> 如果你还没有选定托管层级，请从那里开始——它讲解了何时更
> 适合选用托管方案，以及何时确实需要本方案。

在 Kubernetes 集群上运行智能体，每个会话都获得自己隔离的 pod，并通过网络层控制确保智能体 pod 只能访问 Anthropic API。

```
                     ┌──────────────────────────────────────────────────┐
                     │                  Kubernetes                      │
                     │                                                  │
  curl / SDK ──────► Gateway (FastAPI)                                  │
                     │  ├─ creates/deletes agent pods via K8s API       │
                     │  ├─ routes /sessions/{id}/messages to right pod  │
                     │  └─ session → pod mapping stored in Redis        │
                     │                                                  │
              ┌──────┴──────┐                                           │
              │             │                                           │
          Agent Pod    Agent Pod ──► Egress Proxy ──► api.anthropic.com │
          (session A)  (session B)      ▲                               │
              │             │            │                               │
              │     NetworkPolicy: pods can ONLY reach egress-proxy     │
              │                                                         │
            Redis (session → pod-IP mapping)                            │
                     │                                                  │
                     └──────────────────────────────────────────────────┘
```

智能体镜像与层级 1 从 [﷐0﷑](../Dockerfile) 构建的**完全相同**。镜像相同，机制不同：不再是单个容器或 Modal 沙箱，而是由网关为每个会话分配一个专属 pod，并由集群强制限制该 pod 能够访问的范围。

> **自建托管之前：**如果你只想要一个托管的智能体而不想自己运维
> 基础设施，请使用 Anthropic 的托管方案——参见
> [托管总览](../README.md)。本指南面向需要把
> 智能体部署在自己 Kubernetes 集群上的团队（受监管环境、已有
> 平台、自定义网络）。


## 每个组件存在的原因

**网关** — 每个用户会话都有自己的智能体 pod。必须有组件按需创建这些 pod、把流量路由到正确的 pod，并在会话空闲时将其清理，这个组件就是网关。它通过 Kubernetes API 管理 pod 生命周期，并用 Redis 记住哪个会话对应哪个 pod IP。

**出口代理 + NetworkPolicy** — 智能体会运行任意代码。这一组合确保智能体 pod 只能访问 `api.anthropic.com`，*其他一切都不行*。NetworkPolicy 阻断所有出站流量，只放行到出口代理（443 端口）和 DNS（53 端口）的流量。出口代理终止来自智能体的 TLS，再把请求重新加密后发往 Anthropic 的 API。任何访问互联网、其他服务或其他命名空间的尝试都会在网络层被丢弃。

**Redis** — 网关需要记住哪个 pod 在处理哪个会话。请求到达时，它在 Redis 中查找会话 ID 以找到 pod IP，并把流量路由过去。Redis 会持久化到磁盘，因此映射关系在网关重启后依然存在。

**待机池** — pod 启动需要 10–30 秒（拉取镜像 + 容器启动）。网关会预先启动可配置数量的待机 pod，让新会话可以立即认领一个而不必等待。pod 被认领后，池会在后台补充。

## 前置条件

| 工具 | 用途 |
|------|---------------|
| [kind](https://kind.sigs.k8s.io/) | 在 Docker 中运行本地 Kubernetes 集群 |
| [kubectl](https://kubernetes.io/docs/tasks/tools/) | 应用清单、检查集群 |
| [docker](https://docs.docker.com/get-docker/) | 构建容器镜像 |
| `openssl` | 生成出口代理的 TLS 证书 |
| `ANTHROPIC_API_KEY` | 设置为环境变量 |

## 快速开始（本地，使用 kind）

```bash
cd hosting/kubernetes
export ANTHROPIC_API_KEY=sk-ant-...
./kind-quickstart.sh
```

这会构建三个镜像，把它们加载进本地 `kind` 集群，应用全部清单，并把网关端口转发到 `localhost:8080`。它还会为两个演示租户（`alice` 和 `bob`）生成 bearer 令牌并在最后打印出来——导出你要使用的那个：

```bash
export ALICE_TOKEN=...   # printed by kind-quickstart.sh
export BOB_TOKEN=...
```

## 与之对话

路径和请求形态与层级 1/2 相同——基础 URL 变了，并且网关现在要求一个标识调用租户的 bearer 令牌：

```bash
curl -N -X POST http://localhost:8080/sessions/demo/messages \
  -H "Authorization: Bearer $ALICE_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "What tools do you have?"}'
```

在新 `session_id` 上的第一个请求会认领一个待机 pod（池为空则生成一个）。使用相同 `session_id` 的后续请求会路由到同一个 pod，因此智能体看到的是一段连续的对话。

该会话现在归属于 `alice` — 网关在 Redis 中记录创建会话的租户，并在每个后续请求上校验。用 `$BOB_TOKEN` 发起相同调用会返回 `403 {"detail":"session belongs to another tenant"}`，完全不带令牌则返回 `401`。租户映射是 `gateway-tenants` secret 中一个静态的 `token:tenant,token:tenant` 字符串；把 [﷐6﷑](./gateway/main.py) 中的 `authenticate()` 桩函数替换为你的 IdP，从真实凭据推导租户。

观察这套机制运转：

```bash
kubectl -n claude-agent get pods -w
# you'll see agent-standby-* pods appear, then one flip to active when you curl
```

要结束会话，请经由网关操作，以便清理 Redis 映射（仅限所有者，与其他所有会话操作一致）：

```bash
curl -X DELETE http://localhost:8080/sessions/demo \
  -H "Authorization: Bearer $ALICE_TOKEN"
```

（`kubectl delete pod` 也可以，但会在 Redis 中留下一条过期的 `session → pod-IP` 条目，直到该会话的下一次请求返回 502。）

## 验证出口封锁

智能体会运行模型决定要运行的代码。出口代理 + NetworkPolicy 意味着即使智能体遭到提示注入，也无法访问任意主机。来证明这一点：

> `kind-quickstart.sh` 会安装 Calico，因为 kind 默认的 CNI（kindnet）
> 不强制实施 NetworkPolicy。在 GKE/EKS/AKS 或任何 Calico/Cilium 集群上，
> 强制实施默认开启，本节无需改动即可工作。

```bash
AGENT_POD=$(kubectl -n claude-agent get pods -l role=agent \
  -o jsonpath='{.items[0].metadata.name}')

# This should FAIL — Calico drops the route to anything except egress-proxy.
# (The agent image is slim and has no curl, so we use Python's socket.)
kubectl -n claude-agent exec "$AGENT_POD" -- python3 -c \
  "import socket; socket.setdefaulttimeout(5); socket.create_connection(('example.com',443)); print('REACHED — policy NOT enforcing')"
```

预期结果：`OSError: [Errno 101] Network is unreachable`（或超时）且退出码非零。正向对照——出口代理通路*确实是*开放的——已经由上面的 curl 返回模型输出来证明。

## 待机池

`STANDBY_POOL_SIZE`（位于 `agent-config` ConfigMap 中）控制网关保持就绪的热 pod 数量。查看当前状态（任意有效租户令牌均可）：

```bash
curl http://localhost:8080/api/pool -H "Authorization: Bearer $ALICE_TOKEN"
```

## 持久化

`server.py` 把会话记录（以及它的调用者 ID → SDK ID 映射）持久化到 `CLAUDE_CONFIG_DIR=/data`。在这一层级中那是 pod 的临时文件系统，所以：

- **在 pod 存活期间**（空闲超时窗口内），后续
  消息会像层级 1 和层级 2 那样精确恢复对话。
- **在 pod 被回收之后**，`/data` 就消失了。该
  `session_id` 的下一条消息会得到一个没有任何历史记录的新 pod。

对于 cookbook 演示来说这没问题——会话比 curl 活得久，但不比集群活得久。在生产环境你需要能在 pod 回收后存活的持久存储。有两个选择：

1. **挂载一个 PersistentVolumeClaim** 到 `/data`，替代 pod 的本地
   磁盘，并让网关在会话返回时重新挂接同一个 PVC。`server.py` 无需改动即可工作，但会把每个会话耦合到某个可用区中的一个卷。
2. **用 SDK 的 [﷐0﷑](https://code.claude.com/docs/en/agent-sdk/session-storage)
   把 `/data` 镜像到外部存储**：本地磁盘写入仍然先发生；该存储是一份镜像，且 `mirror_error` 不致命。这正是笔记本中 *Making it production-ready* 一节描述的方案——它需要在 `server.py` 中加一个小钩子，cookbook 还没有写这个。

## 部署到你自己的集群

`kind` 验证了拓扑结构；清单与云厂商无关。要在 EKS、AKS、GKE、OpenShift 或裸机上运行，只需更换镜像仓库和入口：

```bash
REG=your.registry.example.com/claude-agent     # ECR, ACR, GHCR, Artifact Registry, ...

# 1. Build and push the three images
docker build -t $REG/agent:latest -f ../Dockerfile ..
docker build -t $REG/gateway:latest ./gateway
docker build -t $REG/egress-proxy:latest ./egress-proxy
docker push $REG/agent:latest $REG/gateway:latest $REG/egress-proxy:latest

# 2. TLS certs for the egress proxy
./generate-certs.sh

# 3. Namespace + secrets + config
kubectl apply -f manifests/namespace.yaml
kubectl -n claude-agent create secret generic anthropic-api-key \
    --from-literal=ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY"
kubectl -n claude-agent create secret generic gateway-tenants \
    --from-literal=GATEWAY_TENANTS="$(openssl rand -hex 16):tenant-a,$(openssl rand -hex 16):tenant-b"
kubectl -n claude-agent create secret generic egress-proxy-tls \
    --from-file=ca.crt=certs/ca.crt \
    --from-file=proxy.crt=certs/proxy.crt \
    --from-file=proxy.key=certs/proxy.key
kubectl -n claude-agent create configmap agent-config \
    --from-literal=AGENT_IMAGE=$REG/agent:latest \
    --from-literal=STANDBY_POOL_SIZE=2

# 4. Apply manifests with your registry substituted
for f in manifests/*.yaml; do
  sed "s|REGISTRY_URL|$REG|g" "$f" | kubectl apply -f -
done
```

> 如果之后你修改了 `$REG`，请同时重建 `agent-config` ConfigMap —
> 网关在生成智能体 pod 时从中读取 `AGENT_IMAGE`，所以只重跑
> 针对清单的 `sed` 并不会重新指向它们。

然后通过你的集群使用的任何入口方式暴露 `gateway` Service——云 LoadBalancer、Ingress 控制器或服务网格网关。有三件事因环境而异：

- **仓库认证** — 你的节点需要 `$REG` 的拉取凭据
（`imagePullSecrets`、IRSA/Workload Identity，或使用公开仓库）。
- **NetworkPolicy 强制实施** — 出口封锁只有当你的 CNI
  强制实施 `NetworkPolicy` 时才有效（Cilium、Calico、GKE Dataplane V2、带 VPC CNI 策略附加组件的 EKS）。在不理会它的 CNI 上，智能体 pod 可以访问互联网。
- **网关前的 TLS + 认证** — 静态的 `GATEWAY_TENANTS` 令牌
  映射只是真实凭据的替身。在公开暴露之前，把你的 IdP / API 网关放在前面。

## 本方案不能给你什么

- 真正的身份提供者。网关*确实*会按租户强制会话
  所有权 — `GATEWAY_TENANTS` 中的每个 bearer 令牌都映射到一个租户，创建会话的租户拥有该会话，其他租户会收到 403 — 但令牌本身是一个静态映射，没有签发、轮换、吊销，也没有按租户的 RBAC。把 `authenticate()` 换成你的 IdP；所有权检查不变。
- 持久的会话存储（见 [持久化](#persistence)）
- 网关自动扩缩或多区域路由
- DNS 层面的出口控制 — 53 端口对任意解析器保持开放，以便节点本地
  DNS 缓存继续工作，这使 DNS 隧道成为一个残余的数据外泄通道。[﷐0﷑](./manifests/network-policy.yaml) 中的说明展示了在集群直接与 kube-dns/CoreDNS 通信时如何收紧它。
- 加固过的支撑服务 — 网关、Redis 和 nginx 以其
  官方镜像的默认（root）用户运行。加固的投入放在了智能体 pod 上，因为只有它们在运行模型驱动的代码；在生产之前，其余部分请按你组织的基线加固。
- 超出
  [﷐0﷑](https://code.claude.com/docs/en/agent-sdk/observability) 免费提供的可观测性

## 拆除

```bash
./teardown.sh        # kind delete cluster + remove certs/
```

## 目录结构

```
kubernetes/
├── README.md
├── kind-quickstart.sh         # local end-to-end on kind
├── teardown.sh
├── generate-certs.sh          # self-signed CA + proxy cert for egress-proxy
├── gateway/
│   ├── main.py                # FastAPI: route + reap
│   ├── k8s.py                 # pod lifecycle + standby pool
│   ├── proxy.py               # SSE relay
│   ├── requirements.txt
│   └── Dockerfile
├── egress-proxy/
│   ├── nginx.conf
│   └── Dockerfile
└── manifests/
    ├── namespace.yaml
    ├── redis.yaml
    ├── egress-proxy.yaml
    ├── gateway.yaml           # SA + RBAC + Deployment + Service
    └── network-policy.yaml
```
