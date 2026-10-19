# 面向 MongoDB cookbook 的自托管沙箱

这就是 [MongoDB Atlas cookbook](../../CMA_with_mongodb_atlas.ipynb) 中 **路径 B** 背后的镜像：一个自托管沙箱，内置 `pymongo`，因此智能体能用它的 `bash` 工具查询 MongoDB。它放在这里，是因为那个笔记本依赖它。通用的自托管沙箱示例（使用 Docker 和五家云服务商）位于 [claude-quickstarts](https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/self-hosted-sandboxes)。

宿主机直接运行 `ant beta:worker poll`；对每个领取到的工作项，它的 `--on-work` 脚本（`on-work.sh`）用 `docker run` 启动一个按会话划分的容器，该容器的入口命令是 `ant beta:worker run`。每个容器都有一个 `/workspace`（智能体的工作树；技能下载到此处），并由按会话划分的 Docker 卷支撑，因此工作树和技能在同一个会话的多个容器之间得以保留。

它就是运行在你自己掌控的宿主机上的普通 Docker，使用与 [`docker/` 快速上手示例](https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/self-hosted-sandboxes/docker) 相同的 CLI 和相同的环境变量约定。

- **`Dockerfile`** —— 按会话使用的镜像：固定版本的 `ant` CLI、`WORKDIR
  /workspace`、`ENTRYPOINT ["ant"，"beta:worker"，"run"，…]`。CLI 负责心跳、待办工作对齐、SSE、`bash`/`read`/`write`/`edit`/`glob`/`grep` 工具集，以及退出时对工作项的强制停止。
- **`on-work.sh`** —— 由轮询程序针对每个工作项调用。它读取轮询程序设置的
  `ANTHROPIC_{WORK_ID,ENVIRONMENT_ID,SESSION_ID,ENVIRONMENT_KEY}`，从标准输入读完工作 JSON，并在**前台** `exec` 一个带 `--rm` 的按会话容器（幂等：对仍在运行的会话收到重复工作项时什么也不做）。它会阻塞到容器退出为止——必须如此，因为 `ant beta:worker poll` 会在 `--on-work` 脚本返回的那一刻对工作项发出停止（CLI 没有关闭这一行为的选项）。如果用后台的 `docker run -d`，轮询程序会在容器来得及领取该工作之前就把它停止，于是 `bash` 工具使用永远不会执行。
- **`start.sh`** —— 构建镜像，并带着
  `--on-work on-work.sh` 执行宿主机轮询程序。

空闲策略采用 SDK 默认值：每个容器在 `session.status_idle` 且 `stop_reason: end_turn` 之后 60 秒退出；任何其他事件都会重置这个计时。随后 `--rm` 把它移除；按会话的卷会保留，供该会话的下一条消息使用。

任何地方都没有组织 API 密钥：唯一的凭据是**环境密钥**。轮询程序用它领取工作；它作为 `ANTHROPIC_ENVIRONMENT_KEY` 传入每个容器（用于按会话的调用——事件流、租约心跳、强制停止），**并且**作为 `ANTHROPIC_AUTH_TOKEN` 传入（CLI 的技能下载客户端只解析 `ANTHROPIC_API_KEY` / `ANTHROPIC_AUTH_TOKEN`，不解析 `ANTHROPIC_ENVIRONMENT_KEY`——缺少它时技能会静默下载失败）。

## 从沙箱中查询 MongoDB

该镜像内置 `python3` + `pymongo`，并且 `on-work.sh` 会把可选的 `MONGO_URI` 转发进每个按会话的容器，因此智能体能直接用它的 `bash` 工具查询 MongoDB：

```sh
python3 -c 'import os; from pymongo import MongoClient; \
c = MongoClient(os.environ["MONGO_URI"]); \
print(list(c["mydb"]["mycoll"].find({}, {"_id": 0}).limit(5)))'
```

在运行 `./start.sh` 之前于宿主机侧设置它（它按 轮询程序 → `on-work.sh` → 容器 的路径传递）：

```sh
export MONGO_URI="mongodb+srv://<user>:<password>@<cluster>/"
```

`MONGO_URI` 是**你的**机密，不是 Anthropic 的。因为这是你自己构建并运行的容器，它只是一个普通环境变量，永远不会进入控制平面或会话事件历史——这正是自托管的优势。（*云*沙箱没有用于数据库机密的环境变量或保管库通道，所以在那里要把该凭据留在宿主机侧，通过自定义工具封装。见 [MongoDB-on-CMA 入口页](../README.md) 和 [cookbook](../../CMA_with_mongodb_atlas.ipynb)，其第 1 节讲解了全部三条连接路径。）

智能体的 `bash` 在这个容器内运行，所以它能读取 `MONGO_URI`——当你信任所执行的任务时这没问题。为了最小权限，把内置工具集换成你自己的工人工具，让它只暴露一个范围狭窄的 `mongo_query(...)`，而不是原始 URI。更偏好 MongoDB shell？在镜像中加入 `mongosh`（MongoDB 的 apt 仓库），然后调用 `mongosh "$MONGO_URI" --eval '…'`。

## 前置条件

- Docker
- 宿主机 PATH 上有 `ant`，且是 `Dockerfile` 中固定的**同一构建版本**
（`ARG ANT_VERSION`）。安装它：

  ```sh
  VERSION=1.10.0   # must match ANT_VERSION in Dockerfile
  OS=$(uname -s | tr '[:upper:]' '[:lower:]')
  ARCH=$(uname -m | sed -e 's/x86_64/amd64/' -e 's/aarch64/arm64/')
  curl -fsSL "https://github.com/anthropics/anthropic-cli/releases/download/v${VERSION}/ant_${VERSION}_${OS}_${ARCH}.tar.gz" \
    | sudo tar -xz -C /usr/local/bin ant
  ant --version
  ```

## 运行

```sh
export ANTHROPIC_ENVIRONMENT_ID=env_...
export ANTHROPIC_ENVIRONMENT_KEY=sk-ant-oat...
./start.sh
```

然后创建一个指向该 `ANTHROPIC_ENVIRONMENT_ID` 的会话并向它发送一条消息。你应当按顺序看到：

```
[start] polling env=env_... base=https://api.anthropic.com
[on-work] session=sesn_... work=work_... container=... (started)
```

容器日志（`docker logs cma-sesn_...`）会显示 `ant beta:worker run` 的 JSON：`downloaded skill …`、`executing tool …` 等。容器在空闲超时后自行移除；`cma-ws-<session_id>` 卷会保留，供该会话的下一条消息使用（用 `docker volume rm` 丢弃）。

与 claude-quickstarts 中那些[由 webhook 启动的服务商](https://github.com/anthropics/claude-quickstarts/tree/main/managed-agents/self-hosted-sandboxes)不同，这里没有 webhook——`ant beta:worker poll` 直接对环境长轮询，因此没有任何东西需要暴露到互联网上。
